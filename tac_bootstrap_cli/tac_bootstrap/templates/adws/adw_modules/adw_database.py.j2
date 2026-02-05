# /// script
# dependencies = ["aiosqlite>=0.19.0"]
# ///
"""
SQLite Database Manager for Orchestrator Persistence (TAC-14 v2)

Zero-Configuration Philosophy
-----------------------------
This module implements a zero-configuration SQLite database manager for the
TAC Bootstrap orchestrator system. No external database servers, no connection
strings, no credentials - just a single .db file that auto-initializes on first use.

Architecture
------------
- Async context manager for automatic connection lifecycle
- Single connection per instance with WAL mode for concurrent reads
- Explicit commit() after write operations for transaction control
- Auto-schema initialization from schema_orchestrator.sql
- Clean abstraction layer enabling future PostgreSQL migration

SQLite Implementation Details
----------------------------
- UUIDs stored as TEXT: "550e8400-e29b-41d4-a716-446655440000"
- Timestamps as TEXT: "2026-02-04T10:30:00.000000" (ISO 8601)
- JSON metadata as TEXT: Serialized with json.dumps(), deserialized with json.loads()
- Placeholders: Use ? (not $1, $2 like PostgreSQL)
- Last insert ID: Use cursor.lastrowid (not RETURNING id)
- WAL mode: Enabled for concurrent reads + single writer

Usage Example
-------------
```python
import asyncio
from adw_database import DatabaseManager

async def main():
    # Auto-initializes schema on first connect()
    async with DatabaseManager("orchestrator.db") as db:
        # Create orchestrator agent definition
        agent_id = await db.create_orchestrator_agent(
            name="scout-report-suggest",
            description="Scouts codebase and suggests fixes",
            agent_type="utility",
            capabilities="codebase_exploration,issue_detection",
            default_model="claude-sonnet-3.5"
        )

        # Create runtime agent instance
        runtime_id = await db.create_agent(
            orchestrator_agent_id=agent_id,
            session_id="550e8400-e29b-41d4-a716-446655440000",
            status="executing"
        )

        # Log agent activity
        await db.create_agent_log(
            agent_id=runtime_id,
            log_level="INFO",
            log_type="state_change",
            message="Agent started execution",
            details={"phase": "exploration"}
        )

        # Query agent state
        agent = await db.get_agent(runtime_id)
        print(f"Agent status: {agent['status']}")

asyncio.run(main())
```

Database Lifecycle
------------------
1. Instantiate: `db = DatabaseManager("orchestrator.db")`
2. Connect: `await db.connect()` - Opens connection, enables WAL, initializes schema
3. Operations: CRUD methods with explicit commit()
4. Close: `await db.close()` - Safely closes connection
5. Context Manager: Use `async with` for automatic lifecycle management

Future PostgreSQL Upgrade Path (v0.9.0+)
---------------------------------------
This DatabaseManager provides the same interface regardless of backend.
To add PostgreSQL support:
1. Create PostgresDatabaseManager implementing same methods
2. Use factory pattern to select backend based on config
3. Domain layer (repositories) remains unchanged
4. Pydantic models already handle serialization for both backends

Schema Reference
----------------
See: adws/schema/schema_orchestrator.sql
Tables: orchestrator_agents, agents, prompts, agent_logs, system_logs
Triggers: auto-update updated_at on orchestrator_agents
Indexes: 6 strategic indexes for common queries
"""

import aiosqlite
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Async SQLite database manager for orchestrator persistence.

    Provides zero-configuration database operations with automatic schema
    initialization, WAL mode for concurrency, and explicit transaction control.

    Attributes:
        db_path: Path to SQLite database file
        conn: Active aiosqlite connection (None when not connected)
    """

    def __init__(self, db_path: str = "orchestrator.db"):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file (default: "orchestrator.db")
        """
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None
        logger.debug(f"DatabaseManager initialized with db_path={db_path}")

    async def connect(self) -> None:
        """
        Open database connection and initialize schema.

        - Opens SQLite connection
        - Sets row_factory for dict-like access
        - Enables WAL mode for concurrent reads
        - Auto-initializes schema if tables don't exist

        Raises:
            aiosqlite.Error: On connection or schema initialization failure
        """
        try:
            self.conn = await aiosqlite.connect(self.db_path)
            self.conn.row_factory = aiosqlite.Row

            # Enable WAL mode for better concurrency
            await self.conn.execute("PRAGMA journal_mode=WAL")
            await self.conn.commit()

            logger.debug(f"Connected to database: {self.db_path}")

            # Initialize schema
            await self._init_schema()

        except aiosqlite.Error as e:
            logger.error(f"Failed to connect to database {self.db_path}: {e}")
            raise

    async def close(self) -> None:
        """
        Close database connection safely.

        Gracefully closes the connection if open. Safe to call multiple times.
        """
        if self.conn:
            await self.conn.close()
            self.conn = None
            logger.debug(f"Closed database connection: {self.db_path}")

    async def __aenter__(self):
        """Async context manager entry - connect to database."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close database connection."""
        await self.close()

    async def _init_schema(self) -> None:
        """
        Initialize database schema from schema_orchestrator.sql.

        Auto-executes schema DDL if tables don't exist. Uses CREATE TABLE IF NOT EXISTS
        so safe to call multiple times (idempotent).

        Raises:
            FileNotFoundError: If schema_orchestrator.sql not found
            aiosqlite.Error: If schema execution fails
        """
        # Find schema file relative to this module
        schema_path = Path(__file__).parent.parent / "schema" / "schema_orchestrator.sql"

        if not schema_path.exists():
            error_msg = f"Schema file not found: {schema_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()

            await self.conn.executescript(schema_sql)
            await self.conn.commit()

            logger.debug("Database schema initialized successfully")

        except aiosqlite.Error as e:
            error_msg = f"Failed to initialize schema from {schema_path}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    # =========================================================================
    # CRUD Operations: orchestrator_agents table
    # =========================================================================

    async def create_orchestrator_agent(
        self,
        name: str,
        description: Optional[str],
        agent_type: str,
        capabilities: Optional[str] = None,
        default_model: Optional[str] = None
    ) -> str:
        """
        Create a new orchestrator agent definition.

        Args:
            name: Unique agent name (e.g., "scout-report-suggest")
            description: Human-readable description of capabilities
            agent_type: One of: planner, builder, reviewer, tester, orchestrator, utility
            capabilities: Comma-separated capabilities (optional)
            default_model: Default LLM model to use (optional)

        Returns:
            agent_id: UUID of created agent

        Raises:
            aiosqlite.Error: On database operation failure
        """
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        try:
            await self.conn.execute(
                """
                INSERT INTO orchestrator_agents
                (id, name, description, agent_type, capabilities, default_model, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (agent_id, name, description, agent_type, capabilities, default_model, now, now)
            )
            await self.conn.commit()

            logger.debug(f"Created orchestrator_agent: {name} (id={agent_id})")
            return agent_id

        except aiosqlite.Error as e:
            error_msg = f"Failed to create orchestrator_agent '{name}': {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def get_orchestrator_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve orchestrator agent by ID.

        Args:
            agent_id: UUID of agent to retrieve

        Returns:
            Agent data as dict, or None if not found
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM orchestrator_agents WHERE id = ?",
                (agent_id,)
            ) as cursor:
                row = await cursor.fetchone()

                if row:
                    result = dict(row)
                    logger.debug(f"Retrieved orchestrator_agent: {agent_id}")
                    return result

                return None

        except aiosqlite.Error as e:
            error_msg = f"Failed to get orchestrator_agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def list_orchestrator_agents(self) -> List[Dict[str, Any]]:
        """
        List all orchestrator agent definitions.

        Returns:
            List of agent dicts ordered by creation date (newest first)
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM orchestrator_agents ORDER BY created_at DESC"
            ) as cursor:
                rows = await cursor.fetchall()
                results = [dict(row) for row in rows]

                logger.debug(f"Listed {len(results)} orchestrator_agents")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to list orchestrator_agents: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def update_orchestrator_agent(self, agent_id: str, **kwargs) -> bool:
        """
        Update orchestrator agent fields.

        Args:
            agent_id: UUID of agent to update
            **kwargs: Fields to update (name, description, agent_type, capabilities, default_model)

        Returns:
            True if agent was updated, False if not found
        """
        if not kwargs:
            return False

        # Build dynamic UPDATE query
        allowed_fields = {'name', 'description', 'agent_type', 'capabilities', 'default_model'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        # Add updated_at timestamp
        updates['updated_at'] = datetime.utcnow().isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [agent_id]

        try:
            cursor = await self.conn.execute(
                f"UPDATE orchestrator_agents SET {set_clause} WHERE id = ?",
                values
            )
            await self.conn.commit()

            updated = cursor.rowcount > 0
            if updated:
                logger.debug(f"Updated orchestrator_agent {agent_id}: {list(updates.keys())}")

            return updated

        except aiosqlite.Error as e:
            error_msg = f"Failed to update orchestrator_agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def delete_orchestrator_agent(self, agent_id: str) -> bool:
        """
        Delete orchestrator agent definition.

        Args:
            agent_id: UUID of agent to delete

        Returns:
            True if agent was deleted, False if not found
        """
        try:
            cursor = await self.conn.execute(
                "DELETE FROM orchestrator_agents WHERE id = ?",
                (agent_id,)
            )
            await self.conn.commit()

            deleted = cursor.rowcount > 0
            if deleted:
                logger.debug(f"Deleted orchestrator_agent: {agent_id}")

            return deleted

        except aiosqlite.Error as e:
            error_msg = f"Failed to delete orchestrator_agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    # =========================================================================
    # CRUD Operations: agents table
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
        Create a runtime agent instance.

        Args:
            orchestrator_agent_id: FK to orchestrator_agents.id
            session_id: UUID identifying execution session
            parent_agent_id: FK to parent agent if this is a sub-agent (optional)
            status: One of: initializing, planning, executing, reviewing, completed, failed, cancelled
            context: JSON context data (optional)
            config: JSON config data (optional)

        Returns:
            agent_id: UUID of created agent instance
        """
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        try:
            await self.conn.execute(
                """
                INSERT INTO agents
                (id, orchestrator_agent_id, session_id, parent_agent_id, status,
                 context, config, started_at, cost_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0.0)
                """,
                (agent_id, orchestrator_agent_id, session_id, parent_agent_id,
                 status, context, config, now)
            )
            await self.conn.commit()

            logger.debug(f"Created agent instance: {agent_id} (session={session_id})")
            return agent_id

        except aiosqlite.Error as e:
            error_msg = f"Failed to create agent: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve runtime agent by ID.

        Args:
            agent_id: UUID of agent instance

        Returns:
            Agent data as dict, or None if not found
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM agents WHERE id = ?",
                (agent_id,)
            ) as cursor:
                row = await cursor.fetchone()

                if row:
                    result = dict(row)
                    logger.debug(f"Retrieved agent: {agent_id}")
                    return result

                return None

        except aiosqlite.Error as e:
            error_msg = f"Failed to get agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def list_agents(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List runtime agent instances.

        Args:
            session_id: Optional filter by session UUID

        Returns:
            List of agent dicts ordered by start time (newest first)
        """
        try:
            if session_id:
                query = "SELECT * FROM agents WHERE session_id = ? ORDER BY started_at DESC"
                params = (session_id,)
            else:
                query = "SELECT * FROM agents ORDER BY started_at DESC"
                params = ()

            async with self.conn.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                results = [dict(row) for row in rows]

                logger.debug(f"Listed {len(results)} agents (session_id={session_id})")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to list agents: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def update_agent(self, agent_id: str, **kwargs) -> bool:
        """
        Update runtime agent fields.

        Args:
            agent_id: UUID of agent to update
            **kwargs: Fields to update (status, completed_at, cost_usd, error_message, context, config)

        Returns:
            True if agent was updated, False if not found
        """
        if not kwargs:
            return False

        allowed_fields = {'status', 'completed_at', 'cost_usd', 'error_message', 'context', 'config'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [agent_id]

        try:
            cursor = await self.conn.execute(
                f"UPDATE agents SET {set_clause} WHERE id = ?",
                values
            )
            await self.conn.commit()

            updated = cursor.rowcount > 0
            if updated:
                logger.debug(f"Updated agent {agent_id}: {list(updates.keys())}")

            return updated

        except aiosqlite.Error as e:
            error_msg = f"Failed to update agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def delete_agent(self, agent_id: str) -> bool:
        """
        Delete runtime agent instance.

        Args:
            agent_id: UUID of agent to delete

        Returns:
            True if agent was deleted, False if not found
        """
        try:
            cursor = await self.conn.execute(
                "DELETE FROM agents WHERE id = ?",
                (agent_id,)
            )
            await self.conn.commit()

            deleted = cursor.rowcount > 0
            if deleted:
                logger.debug(f"Deleted agent: {agent_id}")

            return deleted

        except aiosqlite.Error as e:
            error_msg = f"Failed to delete agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    # =========================================================================
    # CRUD Operations: prompts table
    # =========================================================================

    async def create_prompt(
        self,
        agent_id: str,
        prompt_type: str,
        prompt_text: str,
        prompt_name: Optional[str] = None,
        status: str = "pending",
        model_used: Optional[str] = None
    ) -> str:
        """
        Create a prompt execution record.

        Args:
            agent_id: FK to agents.id
            prompt_type: One of: adw, command, followup, correction, tool_call
            prompt_text: The prompt content
            prompt_name: Optional human-readable name
            status: One of: pending, streaming, completed, failed, cancelled
            model_used: LLM model identifier (optional)

        Returns:
            prompt_id: UUID of created prompt
        """
        prompt_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        try:
            await self.conn.execute(
                """
                INSERT INTO prompts
                (id, agent_id, prompt_type, prompt_name, prompt_text, status,
                 model_used, tokens_input, tokens_output, cost_usd, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0.0, ?)
                """,
                (prompt_id, agent_id, prompt_type, prompt_name, prompt_text,
                 status, model_used, now)
            )
            await self.conn.commit()

            logger.debug(f"Created prompt: {prompt_id} (agent={agent_id}, type={prompt_type})")
            return prompt_id

        except aiosqlite.Error as e:
            error_msg = f"Failed to create prompt: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve prompt by ID.

        Args:
            prompt_id: UUID of prompt

        Returns:
            Prompt data as dict, or None if not found
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM prompts WHERE id = ?",
                (prompt_id,)
            ) as cursor:
                row = await cursor.fetchone()

                if row:
                    result = dict(row)
                    logger.debug(f"Retrieved prompt: {prompt_id}")
                    return result

                return None

        except aiosqlite.Error as e:
            error_msg = f"Failed to get prompt {prompt_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def list_prompts(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        List prompts for a specific agent.

        Args:
            agent_id: UUID of agent to filter by

        Returns:
            List of prompt dicts ordered by creation time (oldest first)
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM prompts WHERE agent_id = ? ORDER BY created_at ASC",
                (agent_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                results = [dict(row) for row in rows]

                logger.debug(f"Listed {len(results)} prompts for agent {agent_id}")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to list prompts for agent {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def update_prompt(self, prompt_id: str, **kwargs) -> bool:
        """
        Update prompt fields (typically response data).

        Args:
            prompt_id: UUID of prompt to update
            **kwargs: Fields to update (response_text, status, tokens_input, tokens_output,
                     cost_usd, latency_ms, completed_at, error_message)

        Returns:
            True if prompt was updated, False if not found
        """
        if not kwargs:
            return False

        allowed_fields = {
            'response_text', 'status', 'tokens_input', 'tokens_output',
            'cost_usd', 'latency_ms', 'completed_at', 'error_message'
        }
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [prompt_id]

        try:
            cursor = await self.conn.execute(
                f"UPDATE prompts SET {set_clause} WHERE id = ?",
                values
            )
            await self.conn.commit()

            updated = cursor.rowcount > 0
            if updated:
                logger.debug(f"Updated prompt {prompt_id}: {list(updates.keys())}")

            return updated

        except aiosqlite.Error as e:
            error_msg = f"Failed to update prompt {prompt_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def delete_prompt(self, prompt_id: str) -> bool:
        """
        Delete prompt record.

        Args:
            prompt_id: UUID of prompt to delete

        Returns:
            True if prompt was deleted, False if not found
        """
        try:
            cursor = await self.conn.execute(
                "DELETE FROM prompts WHERE id = ?",
                (prompt_id,)
            )
            await self.conn.commit()

            deleted = cursor.rowcount > 0
            if deleted:
                logger.debug(f"Deleted prompt: {prompt_id}")

            return deleted

        except aiosqlite.Error as e:
            error_msg = f"Failed to delete prompt {prompt_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    # =========================================================================
    # CRUD Operations: agent_logs table (append-only)
    # =========================================================================

    async def create_agent_log(
        self,
        agent_id: str,
        log_level: str,
        log_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Create an agent log entry (append-only).

        Args:
            agent_id: FK to agents.id
            log_level: One of: DEBUG, INFO, WARNING, ERROR, CRITICAL
            log_type: One of: state_change, milestone, error, performance, tool_call, cost_update
            message: Log message text
            details: Optional JSON metadata (serialized to TEXT)

        Returns:
            log_id: Integer ID of created log entry
        """
        now = datetime.utcnow().isoformat()
        details_json = json.dumps(details) if details else None

        try:
            cursor = await self.conn.execute(
                """
                INSERT INTO agent_logs
                (agent_id, log_level, log_type, message, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (agent_id, log_level, log_type, message, details_json, now)
            )
            await self.conn.commit()

            log_id = cursor.lastrowid
            logger.debug(f"Created agent_log: id={log_id} (agent={agent_id}, level={log_level})")
            return log_id

        except aiosqlite.Error as e:
            error_msg = f"Failed to create agent_log: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def get_agent_logs(
        self,
        agent_id: str,
        log_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve agent logs with optional level filter.

        Args:
            agent_id: UUID of agent to filter by
            log_level: Optional minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            List of log dicts ordered by creation time (oldest first)
        """
        try:
            if log_level:
                query = """
                    SELECT * FROM agent_logs
                    WHERE agent_id = ? AND log_level = ?
                    ORDER BY created_at ASC
                """
                params = (agent_id, log_level)
            else:
                query = "SELECT * FROM agent_logs WHERE agent_id = ? ORDER BY created_at ASC"
                params = (agent_id,)

            async with self.conn.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                results = []

                for row in rows:
                    log_dict = dict(row)
                    # Deserialize JSON details
                    if log_dict.get('details'):
                        try:
                            log_dict['details'] = json.loads(log_dict['details'])
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse details JSON for log {log_dict['id']}")
                    results.append(log_dict)

                logger.debug(f"Retrieved {len(results)} agent_logs for agent {agent_id}")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to get agent_logs for {agent_id}: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def list_recent_agent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List recent agent logs across all agents.

        Args:
            limit: Maximum number of logs to return (default: 100)

        Returns:
            List of log dicts ordered by creation time (newest first)
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM agent_logs ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                results = []

                for row in rows:
                    log_dict = dict(row)
                    # Deserialize JSON details
                    if log_dict.get('details'):
                        try:
                            log_dict['details'] = json.loads(log_dict['details'])
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse details JSON for log {log_dict['id']}")
                    results.append(log_dict)

                logger.debug(f"Listed {len(results)} recent agent_logs")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to list recent agent_logs: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    # =========================================================================
    # CRUD Operations: system_logs table (append-only)
    # =========================================================================

    async def create_system_log(
        self,
        log_level: str,
        component: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Create a system log entry (append-only).

        Args:
            log_level: One of: DEBUG, INFO, WARNING, ERROR, CRITICAL
            component: Component identifier (e.g., "orchestrator", "database", "api")
            message: Log message text
            details: Optional JSON metadata (serialized to TEXT)

        Returns:
            log_id: Integer ID of created log entry
        """
        now = datetime.utcnow().isoformat()
        details_json = json.dumps(details) if details else None

        try:
            cursor = await self.conn.execute(
                """
                INSERT INTO system_logs
                (log_level, component, message, details, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (log_level, component, message, details_json, now)
            )
            await self.conn.commit()

            log_id = cursor.lastrowid
            logger.debug(f"Created system_log: id={log_id} (component={component}, level={log_level})")
            return log_id

        except aiosqlite.Error as e:
            error_msg = f"Failed to create system_log: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def get_system_logs(
        self,
        log_level: Optional[str] = None,
        component: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve system logs with optional filters.

        Args:
            log_level: Optional log level filter (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            component: Optional component filter

        Returns:
            List of log dicts ordered by creation time (oldest first)
        """
        try:
            # Build query with optional filters
            conditions = []
            params = []

            if log_level:
                conditions.append("log_level = ?")
                params.append(log_level)

            if component:
                conditions.append("component = ?")
                params.append(component)

            where_clause = " AND ".join(conditions) if conditions else "1=1"
            query = f"SELECT * FROM system_logs WHERE {where_clause} ORDER BY created_at ASC"

            async with self.conn.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                results = []

                for row in rows:
                    log_dict = dict(row)
                    # Deserialize JSON details
                    if log_dict.get('details'):
                        try:
                            log_dict['details'] = json.loads(log_dict['details'])
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse details JSON for log {log_dict['id']}")
                    results.append(log_dict)

                logger.debug(f"Retrieved {len(results)} system_logs")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to get system_logs: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e

    async def list_recent_system_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List recent system logs.

        Args:
            limit: Maximum number of logs to return (default: 100)

        Returns:
            List of log dicts ordered by creation time (newest first)
        """
        try:
            async with self.conn.execute(
                "SELECT * FROM system_logs ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                results = []

                for row in rows:
                    log_dict = dict(row)
                    # Deserialize JSON details
                    if log_dict.get('details'):
                        try:
                            log_dict['details'] = json.loads(log_dict['details'])
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse details JSON for log {log_dict['id']}")
                    results.append(log_dict)

                logger.debug(f"Listed {len(results)} recent system_logs")
                return results

        except aiosqlite.Error as e:
            error_msg = f"Failed to list recent system_logs: {e}"
            logger.error(error_msg)
            raise aiosqlite.Error(error_msg) from e
