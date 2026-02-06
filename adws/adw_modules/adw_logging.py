# /// script
# dependencies = ["aiosqlite>=0.19.0"]
# ///
"""
ADW Structured Logging Module - Workflow-Oriented Database Logging for Orchestrator

This module provides workflow-oriented logging functions that wrap the low-level
DatabaseManager methods from adw_database.py. It adds semantic meaning to log
entries by providing step-level tracking, agent lifecycle events, and system-wide
event logging with a consistent interface.

Architecture
------------
    Orchestrator Workflow --> adw_logging.py --> adw_database.py --> SQLite
    (step_start/end,         (this module)      (raw CRUD)         (persistence)
     agent events,
     system events)

    adw_logging.py --> adw_websockets.py (event schema alignment)
    (log schema)       (real-time broadcast)

The logging functions in this module produce entries that align with the
adw_websockets.py WebSocketEvent schema, enabling seamless bridging between
persisted logs and real-time event broadcasting.

Zero-Configuration Philosophy
-----------------------------
- Single function call to initialize logging (creates DatabaseManager + connects)
- Async context manager for automatic lifecycle management
- All functions accept a DatabaseManager instance for explicit dependency injection
- Graceful error handling on high-level event logging (never crashes workflows)

Event Types
-----------
Agent lifecycle events (used by log_agent_event):
- agent_started: Agent has been initialized and is beginning work
- agent_completed: Agent has finished successfully
- agent_failed: Agent encountered an unrecoverable error
- prompt_sent: A prompt was dispatched to the LLM
- prompt_received: A response was received from the LLM

Step tracking events (used by log_step_start / log_step_end):
- step_start: A named workflow step has begun execution
- step_end: A named workflow step has completed (with success/failure status)

System events (used by log_system_event):
- Arbitrary component-level logging at DEBUG/INFO/WARNING/ERROR/CRITICAL levels

Integration with adw_websockets.py
------------------------------------
The event schema produced by this module matches the WebSocketEvent dataclass:
- event_type maps to WebSocketEvent.event_type
- agent_id maps to WebSocketEvent.agent_id
- message maps to WebSocketEvent.message
- metadata maps to WebSocketEvent.metadata
- timestamps are ISO 8601 (same format)

Use adw_websockets.map_log_to_event() to convert database log entries into
WebSocket events for real-time broadcasting.

Usage Example
-------------
```python
import asyncio
from adw_modules.adw_logging import (
    logging_session, log_step_start, log_step_end,
    log_agent_event, log_system_event
)

async def main():
    async with logging_session("orchestrator.db") as db:
        agent_id = "550e8400-e29b-41d4-a716-446655440000"

        # Log agent lifecycle
        await log_agent_event(db, agent_id, "agent_started",
                              "Scout agent started codebase exploration",
                              metadata={"model": "claude-sonnet-3.5"})

        # Track workflow steps
        await log_step_start(db, agent_id, "code_analysis",
                             metadata={"files_queued": 42})

        # ... perform analysis ...

        await log_step_end(db, agent_id, "code_analysis", success=True,
                           metadata={"files_analyzed": 42, "issues_found": 3})

        # Log system events
        await log_system_event(db, "orchestrator", "All agents completed",
                               level="INFO", details={"total_agents": 5})

        # Log agent completion
        await log_agent_event(db, agent_id, "agent_completed",
                              "Scout agent finished successfully")

asyncio.run(main())
```

Standalone Initialization
-------------------------
```python
from adw_modules.adw_logging import init_logging, close_logging

async def standalone():
    db = await init_logging("orchestrator.db")
    try:
        await log_system_event(db, "startup", "System initialized")
        # ... workflow operations ...
    finally:
        await close_logging(db)
```
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any

from adw_database import DatabaseManager

# Configure module-level logger
logger = logging.getLogger(__name__)


# ============================================================================
# Initialization and Lifecycle
# ============================================================================

async def init_logging(db_path: str = "orchestrator.db") -> DatabaseManager:
    """
    Initialize logging by creating and connecting a DatabaseManager.

    Creates a new DatabaseManager instance pointing at the specified SQLite
    database file, opens the connection, enables WAL mode, and initializes
    the schema (idempotent). The returned DatabaseManager is ready for
    immediate use with all logging functions in this module.

    Args:
        db_path: Path to SQLite database file (default: "orchestrator.db").
                 The file is created automatically if it does not exist.

    Returns:
        Connected DatabaseManager instance ready for logging operations.

    Raises:
        aiosqlite.Error: If database connection or schema initialization fails.
        FileNotFoundError: If schema_orchestrator.sql is not found.

    Example:
        >>> db = await init_logging("my_project.db")
        >>> # db is now connected and ready for logging
        >>> await close_logging(db)
    """
    db = DatabaseManager(db_path)
    await db.connect()
    logger.debug(f"Logging initialized with database: {db_path}")
    return db


async def close_logging(db: DatabaseManager) -> None:
    """
    Close the logging database connection.

    Safely closes the DatabaseManager connection. Safe to call multiple
    times - subsequent calls are no-ops if already closed.

    Args:
        db: DatabaseManager instance to close.

    Example:
        >>> db = await init_logging()
        >>> # ... perform logging ...
        >>> await close_logging(db)
    """
    await db.close()
    logger.debug("Logging connection closed")


@asynccontextmanager
async def logging_session(db_path: str = "orchestrator.db"):
    """
    Async context manager for a complete logging session lifecycle.

    Handles DatabaseManager creation, connection, and teardown automatically.
    The yielded DatabaseManager instance is connected and ready for use with
    all logging functions in this module.

    Args:
        db_path: Path to SQLite database file (default: "orchestrator.db").

    Yields:
        Connected DatabaseManager instance.

    Raises:
        aiosqlite.Error: If database connection or schema initialization fails.
        FileNotFoundError: If schema_orchestrator.sql is not found.

    Example:
        >>> async with logging_session("orchestrator.db") as db:
        ...     await log_system_event(db, "startup", "System initialized")
        ...     # Connection is automatically closed on exit
    """
    db = await init_logging(db_path)
    try:
        yield db
    finally:
        await close_logging(db)


# ============================================================================
# Step Tracking Functions
# ============================================================================

async def log_step_start(
    db: DatabaseManager,
    agent_id: str,
    step_name: str,
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """
    Log the start of a named workflow step.

    Creates an agent_log entry with log_type="step_start" to mark the beginning
    of a discrete workflow phase. Pair with log_step_end() to track step duration
    and outcome.

    The step_name is included in both the message text and the metadata dict
    for easy querying and filtering.

    Args:
        db: Connected DatabaseManager instance.
        agent_id: UUID of the agent executing the step (FK to agents.id).
        step_name: Human-readable step identifier (e.g., "code_analysis",
                   "test_execution", "review_phase").
        metadata: Optional additional metadata dict. The step_name is
                  automatically merged into this dict under the "step" key.

    Returns:
        Integer log ID of the created log entry.

    Raises:
        aiosqlite.Error: If database write fails.

    Example:
        >>> log_id = await log_step_start(db, agent_id, "code_analysis",
        ...                                metadata={"files_queued": 42})
        >>> print(f"Step started with log_id={log_id}")
    """
    details = {"step": step_name}
    if metadata:
        details.update(metadata)

    log_id = await db.create_agent_log(
        agent_id=agent_id,
        log_level="INFO",
        log_type="step_start",
        message=f"Step started: {step_name}",
        details=details
    )

    logger.debug(f"Step started: {step_name} (agent={agent_id}, log_id={log_id})")
    return log_id


async def log_step_end(
    db: DatabaseManager,
    agent_id: str,
    step_name: str,
    success: bool,
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """
    Log the end of a named workflow step.

    Creates an agent_log entry with log_type="step_end" to mark the completion
    of a discrete workflow phase. The success/failure status is recorded in both
    the log level (INFO for success, WARNING for failure) and the metadata.

    Args:
        db: Connected DatabaseManager instance.
        agent_id: UUID of the agent that executed the step (FK to agents.id).
        step_name: Human-readable step identifier matching the corresponding
                   log_step_start() call.
        success: True if the step completed successfully, False otherwise.
        metadata: Optional additional metadata dict. The step_name and success
                  status are automatically merged into this dict.

    Returns:
        Integer log ID of the created log entry.

    Raises:
        aiosqlite.Error: If database write fails.

    Example:
        >>> log_id = await log_step_end(db, agent_id, "code_analysis",
        ...                              success=True,
        ...                              metadata={"files_analyzed": 42})
        >>> print(f"Step ended with log_id={log_id}")

        >>> # Failed step
        >>> log_id = await log_step_end(db, agent_id, "test_execution",
        ...                              success=False,
        ...                              metadata={"error": "3 tests failed"})
    """
    log_level = "INFO" if success else "WARNING"
    status_label = "completed" if success else "failed"

    details = {"step": step_name, "success": success}
    if metadata:
        details.update(metadata)

    log_id = await db.create_agent_log(
        agent_id=agent_id,
        log_level=log_level,
        log_type="step_end",
        message=f"Step {status_label}: {step_name}",
        details=details
    )

    logger.debug(
        f"Step {status_label}: {step_name} (agent={agent_id}, log_id={log_id})"
    )
    return log_id


# ============================================================================
# Agent Event Logging
# ============================================================================

async def log_agent_event(
    db: DatabaseManager,
    agent_id: str,
    event_type: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    High-level agent event logging with graceful error handling.

    Delegates to DatabaseManager.log_agent_event() which wraps create_agent_log()
    with try/except to ensure logging failures never crash orchestrator agents.
    If the database write fails, the error is logged to stderr and None is returned.

    Supported event types:
        - agent_started: Agent has been initialized and is beginning work
        - agent_completed: Agent has finished all work successfully
        - agent_failed: Agent encountered an unrecoverable error
        - prompt_sent: A prompt was dispatched to the LLM
        - prompt_received: A response was received from the LLM

    These event types align with the adw_websockets.py WebSocketEvent schema,
    enabling seamless bridging between persisted logs and real-time broadcasts.

    Args:
        db: Connected DatabaseManager instance.
        agent_id: UUID of the agent generating the event (FK to agents.id).
        event_type: One of: "agent_started", "agent_completed", "agent_failed",
                    "prompt_sent", "prompt_received".
        message: Human-readable event message describing what happened.
        metadata: Optional dict with event-specific data (e.g., model name,
                  token counts, error details).

    Returns:
        None. This function never raises exceptions - errors are logged to stderr.

    Example:
        >>> await log_agent_event(db, agent_id, "agent_started",
        ...                       "Scout agent started codebase exploration",
        ...                       metadata={"model": "claude-sonnet-3.5"})

        >>> await log_agent_event(db, agent_id, "agent_failed",
        ...                       "Agent failed due to quota exhaustion",
        ...                       metadata={"error": "quota_exceeded",
        ...                                 "retries": 15})
    """
    await db.log_agent_event(
        agent_id=agent_id,
        log_type=event_type,
        message=message,
        metadata=metadata
    )

    logger.debug(
        f"Agent event logged: {event_type} (agent={agent_id}, message={message!r})"
    )


# ============================================================================
# System Event Logging
# ============================================================================

async def log_system_event(
    db: DatabaseManager,
    component: str,
    message: str,
    level: str = "INFO",
    details: Optional[Dict[str, Any]] = None
) -> int:
    """
    Log a system-wide event to the system_logs table.

    Creates a system_log entry for infrastructure-level events that are not
    tied to a specific agent. Useful for recording orchestrator lifecycle,
    server startup/shutdown, configuration changes, and cross-cutting concerns.

    Args:
        db: Connected DatabaseManager instance.
        component: Component identifier producing the log entry. Examples:
                   "orchestrator", "database", "websocket", "api", "scheduler".
        message: Human-readable log message describing the event.
        level: Log level string. One of: "DEBUG", "INFO", "WARNING", "ERROR",
               "CRITICAL" (default: "INFO").
        details: Optional dict with event-specific metadata (serialized to
                 JSON TEXT in the database).

    Returns:
        Integer log ID of the created system_log entry.

    Raises:
        aiosqlite.Error: If database write fails.

    Example:
        >>> log_id = await log_system_event(db, "orchestrator",
        ...                                  "All agents completed successfully",
        ...                                  level="INFO",
        ...                                  details={"total_agents": 5,
        ...                                           "duration_ms": 45000})

        >>> # Error-level system event
        >>> log_id = await log_system_event(db, "database",
        ...                                  "WAL checkpoint failed",
        ...                                  level="ERROR",
        ...                                  details={"error": "disk full"})
    """
    log_id = await db.create_system_log(
        log_level=level,
        component=component,
        message=message,
        details=details
    )

    logger.debug(
        f"System event logged: [{level}] {component} - {message!r} (log_id={log_id})"
    )
    return log_id
