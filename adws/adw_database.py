# /// script
# dependencies = ["aiosqlite>=0.19.0"]
# ///
"""
DatabaseManager - SQLite Operations for Orchestrator Persistence (TAC-14 v2)

This module provides async SQLite database operations for the TAC Bootstrap orchestrator
system. It manages persistent state for orchestrator agents, runtime agent instances,
prompts, and execution logs.

Architecture:
-------------
- Infrastructure layer component (DDD Lite pattern)
- Async operations using aiosqlite for non-blocking I/O
- Single connection pattern (sufficient for orchestrator workflows)
- Zero-configuration SQLite database (no setup required)

Supported Patterns:
-------------------
1. Context Manager (Recommended):
    ```python
    async with DatabaseManager() as db:
        agent_id = await db.create_orchestrator_agent("scout-agent", "Scouts codebase")
        agent = await db.get_orchestrator_agent(agent_id)
    ```

2. Explicit Connect/Close:
    ```python
    db = DatabaseManager()
    await db.connect()
    try:
        agent_id = await db.create_orchestrator_agent("scout-agent", "Scouts codebase")
    finally:
        await db.close()
    ```

Tables Supported:
-----------------
- orchestrator_agents: Agent type definitions (7 agents in TAC-14)
- agents: Runtime agent instances (execution tracking)
- prompts: ADW execution records (deferred to Task 9)
- agent_logs: Agent lifecycle events (deferred to Task 9)
- system_logs: System-wide logging (deferred to Task 9)

Configuration:
--------------
- Database path: Default `data/orchestrator.db`
- Override via ORCHESTRATOR_DB_PATH environment variable
- Schema auto-initialized from `adws/schema/schema_orchestrator.sql`

Concurrency:
------------
SQLite limitations apply:
- Single writer (sequential writes)
- Multiple readers (concurrent reads in WAL mode)
- Recommended: One DatabaseManager instance per process

Error Handling:
---------------
- FileNotFoundError: Schema file missing (clear message)
- aiosqlite.IntegrityError: FOREIGN KEY violations, UNIQUE constraints
- aiosqlite.OperationalError: Database locked, corrupted file
All errors propagate to caller for explicit handling.

Dependencies:
-------------
- adws/schema/schema_orchestrator.sql (schema definition)
- adws/adw_modules/orch_database_models.py (Pydantic models - optional)
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import aiosqlite


class DatabaseManager:
    """
    Async SQLite database manager for orchestrator persistence.

    Provides CRUD operations for orchestrator_agents and agents tables.
    Supports both context manager and explicit connect/close patterns.

    Attributes:
        db_path (str): Path to SQLite database file
        conn (aiosqlite.Connection): Active database connection (after connect())

    Example:
        ```python
        # Context manager pattern (recommended)
        async with DatabaseManager() as db:
            agent_id = await db.create_orchestrator_agent(
                name="scout-report-suggest",
                description="Scouts codebase and suggests fixes"
            )
            agent = await db.get_orchestrator_agent(agent_id)
            print(f"Created agent: {agent['name']}")

        # Explicit pattern
        db = DatabaseManager("custom/path/db.sqlite")
        await db.connect()
        agents = await db.list_orchestrator_agents()
        await db.close()
        ```

    Notes:
        - Schema auto-initialized on first connect()
        - ORCHESTRATOR_DB_PATH env var overrides db_path
        - Foreign key constraints enabled automatically
        - WAL mode enabled for better concurrency
    """

    def __init__(self, db_path: str = "data/orchestrator.db"):
        """
        Initialize DatabaseManager with database path.

        Args:
            db_path: Path to SQLite database file (default: data/orchestrator.db)
                    Can be overridden by ORCHESTRATOR_DB_PATH environment variable.
        """
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> None:
        """
        Establish connection to SQLite database and initialize schema.

        Reads ORCHESTRATOR_DB_PATH environment variable if set, otherwise uses
        the db_path from constructor. Creates parent directory if missing.
        Automatically executes schema_orchestrator.sql to initialize tables.

        Raises:
            FileNotFoundError: If schema file (adws/schema/schema_orchestrator.sql) not found
            aiosqlite.OperationalError: If database file is corrupted or locked
        """
        # Override db_path with environment variable if set
        self.db_path = os.getenv("ORCHESTRATOR_DB_PATH", self.db_path)

        # Create parent directory if missing
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row

        # Initialize schema
        await self._init_schema()

    async def close(self) -> None:
        """
        Close database connection.

        Safe to call multiple times. Does nothing if connection already closed.
        """
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def _init_schema(self) -> None:
        """
        Initialize database schema from SQL file.

        Executes adws/schema/schema_orchestrator.sql to create tables, indexes,
        and triggers. Safe to call multiple times (uses CREATE TABLE IF NOT EXISTS).

        Raises:
            FileNotFoundError: If schema_orchestrator.sql not found with clear message
        """
        schema_path = "adws/schema/schema_orchestrator.sql"

        if not Path(schema_path).exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}\n"
                f"This file should be created in Task 6 (Database Schema).\n"
                f"Ensure you're running from project root."
            )

        with open(schema_path, "r") as f:
            schema = f.read()

        await self.conn.executescript(schema)
        await self.conn.commit()

    async def __aenter__(self):
        """
        Context manager entry - establishes connection.

        Returns:
            DatabaseManager: Self for use in async with block
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - closes connection.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)

        Returns:
            None: Propagates exceptions (does not suppress)
        """
        await self.close()
        return None

    # =========================================================================
    # orchestrator_agents CRUD Operations
    # =========================================================================

    async def create_orchestrator_agent(
        self,
        name: str,
        description: Optional[str] = None,
        agent_type: str = "utility",
        capabilities: Optional[str] = None,
        default_model: Optional[str] = None
    ) -> str:
        """
        Create a new orchestrator agent definition.

        Args:
            name: Unique agent type name (e.g., "scout-report-suggest")
            description: Human-readable description of agent capabilities
            agent_type: Agent category - 'planner', 'builder', 'reviewer', 'tester',
                       'orchestrator', or 'utility' (default: 'utility')
            capabilities: JSON string describing agent capabilities
            default_model: Default LLM model for this agent (e.g., "claude-sonnet-4")

        Returns:
            str: UUID of created agent (TEXT format in SQLite)

        Raises:
            aiosqlite.IntegrityError: If agent with same name already exists
            ValueError: If agent_type not in allowed values

        Example:
            ```python
            agent_id = await db.create_orchestrator_agent(
                name="scout-report-suggest",
                description="Scouts codebase and suggests fixes",
                agent_type="utility",
                capabilities='{"read": true, "write": false}'
            )
            ```
        """
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        sql = """
            INSERT INTO orchestrator_agents
                (id, name, description, agent_type, capabilities, default_model,
                 created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        await self.conn.execute(
            sql,
            (agent_id, name, description, agent_type, capabilities, default_model, now, now)
        )
        await self.conn.commit()

        return agent_id

    async def get_orchestrator_agent(self, agent_id: str) -> Optional[dict]:
        """
        Retrieve orchestrator agent by ID.

        Args:
            agent_id: UUID of orchestrator agent (TEXT format)

        Returns:
            dict | None: Agent data as dictionary with keys:
                - id, name, description, agent_type, capabilities, default_model,
                  created_at, updated_at
                Returns None if agent not found.

        Example:
            ```python
            agent = await db.get_orchestrator_agent("550e8400-e29b-41d4-a716-446655440000")
            if agent:
                print(f"Agent: {agent['name']} - {agent['description']}")
            ```
        """
        sql = "SELECT * FROM orchestrator_agents WHERE id = ?"

        async with self.conn.execute(sql, (agent_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def list_orchestrator_agents(self) -> List[dict]:
        """
        List all orchestrator agents, ordered by creation date (newest first).

        Returns:
            List[dict]: List of agent dictionaries. Empty list if no agents exist.

        Example:
            ```python
            agents = await db.list_orchestrator_agents()
            for agent in agents:
                print(f"{agent['name']}: {agent['description']}")
            ```
        """
        sql = "SELECT * FROM orchestrator_agents ORDER BY created_at DESC"

        async with self.conn.execute(sql) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    # =========================================================================
    # agents Table CRUD Operations
    # =========================================================================

    async def create_agent(
        self,
        orchestrator_agent_id: str,
        session_id: str,
        parent_agent_id: Optional[str] = None,
        status: str = "initializing",
        context: Optional[str] = None,
        config: Optional[str] = None
    ) -> str:
        """
        Create a new runtime agent instance.

        Args:
            orchestrator_agent_id: Foreign key to orchestrator_agents.id
            session_id: UUID identifying the execution session
            parent_agent_id: Optional parent agent ID for hierarchical orchestration
            status: Initial status (default: 'initializing')
                   Valid values: initializing, planning, executing, reviewing,
                                completed, failed, cancelled
            context: Optional JSON string with agent context
            config: Optional JSON string with agent configuration

        Returns:
            str: UUID of created agent instance

        Raises:
            aiosqlite.IntegrityError: If orchestrator_agent_id does not exist (FOREIGN KEY)

        Example:
            ```python
            agent_id = await db.create_agent(
                orchestrator_agent_id="550e8400-...",
                session_id="770e9500-...",
                status="initializing",
                context='{"project": "tac_bootstrap"}'
            )
            ```
        """
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        sql = """
            INSERT INTO agents
                (id, orchestrator_agent_id, session_id, parent_agent_id, status,
                 context, config, started_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        await self.conn.execute(
            sql,
            (agent_id, orchestrator_agent_id, session_id, parent_agent_id,
             status, context, config, now)
        )
        await self.conn.commit()

        return agent_id

    async def get_agent(self, agent_id: str) -> Optional[dict]:
        """
        Retrieve runtime agent instance by ID.

        Args:
            agent_id: UUID of agent instance

        Returns:
            dict | None: Agent data as dictionary with keys:
                - id, orchestrator_agent_id, session_id, parent_agent_id, status,
                  context, config, started_at, completed_at, cost_usd, error_message
                Returns None if agent not found.

        Example:
            ```python
            agent = await db.get_agent("770e9500-...")
            if agent:
                print(f"Status: {agent['status']}, Cost: ${agent['cost_usd']}")
            ```
        """
        sql = "SELECT * FROM agents WHERE id = ?"

        async with self.conn.execute(sql, (agent_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def list_agents_by_session(self, session_id: str) -> List[dict]:
        """
        List all agent instances for a given session, ordered by start time.

        Args:
            session_id: UUID of execution session

        Returns:
            List[dict]: List of agent dictionaries. Empty list if no agents in session.

        Example:
            ```python
            agents = await db.list_agents_by_session("770e9500-...")
            print(f"Session has {len(agents)} agents")
            for agent in agents:
                print(f"  {agent['status']}: started at {agent['started_at']}")
            ```
        """
        sql = "SELECT * FROM agents WHERE session_id = ? ORDER BY started_at"

        async with self.conn.execute(sql, (session_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def update_agent_status(
        self,
        agent_id: str,
        status: str,
        completed_at: Optional[str] = None,
        cost_usd: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Update runtime agent status and optional metadata.

        Args:
            agent_id: UUID of agent instance to update
            status: New status value
                   Valid: initializing, planning, executing, reviewing,
                         completed, failed, cancelled
            completed_at: Optional ISO 8601 timestamp of completion
            cost_usd: Optional cost in USD for this execution
            error_message: Optional error message if status is 'failed'

        Returns:
            bool: True if agent was updated, False if agent_id not found

        Example:
            ```python
            # Mark agent as completed
            success = await db.update_agent_status(
                agent_id="770e9500-...",
                status="completed",
                completed_at=datetime.utcnow().isoformat(),
                cost_usd=0.0042
            )

            # Mark agent as failed
            success = await db.update_agent_status(
                agent_id="770e9500-...",
                status="failed",
                error_message="Timeout waiting for LLM response"
            )
            ```
        """
        sql = """
            UPDATE agents
            SET status = ?, completed_at = ?, cost_usd = ?, error_message = ?
            WHERE id = ?
        """

        cursor = await self.conn.execute(
            sql,
            (status, completed_at, cost_usd, error_message, agent_id)
        )
        await self.conn.commit()

        return cursor.rowcount > 0
