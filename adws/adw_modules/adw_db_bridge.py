"""Sync SQLite bridge for ADW workflow tracking.

Provides synchronous database writes to the orchestrator SQLite database
(data/orchestrator.db) using plain sqlite3. This avoids the async/sync
mismatch since ADW workflows use subprocess.run() (sync) while the web
backend uses aiosqlite (async).

SQLite WAL mode enables concurrent readers/writers, so the web backend
can read while workflows write.

All functions are wrapped in try/except - DB failures log to stderr
and never crash workflows.
"""

import os
import sqlite3
import uuid
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# Module-level connection
_conn: Optional[sqlite3.Connection] = None


def _get_default_db_path() -> str:
    """Get default database path: {project_root}/data/orchestrator.db."""
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.join(project_root, "data", "orchestrator.db")


def init_bridge(db_path: Optional[str] = None) -> None:
    """Open sqlite3 connection to orchestrator database.

    Args:
        db_path: Path to SQLite database. Defaults to data/orchestrator.db.
    """
    global _conn
    try:
        path = db_path or os.getenv("DATABASE_PATH") or _get_default_db_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _conn = sqlite3.connect(path)
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
        logger.info(f"[DB Bridge] Connected to {path}")
    except Exception as e:
        logger.warning(f"[DB Bridge] Failed to connect: {e}")
        _conn = None


def close_bridge() -> None:
    """Close the sqlite3 connection."""
    global _conn
    if _conn:
        try:
            _conn.close()
            logger.info("[DB Bridge] Connection closed")
        except Exception as e:
            logger.warning(f"[DB Bridge] Failed to close: {e}")
        finally:
            _conn = None


# ---------------------------------------------------------------------------
# Workflow lifecycle (ai_developer_workflows table)
# ---------------------------------------------------------------------------

def track_workflow_start(
    adw_id: str,
    workflow_type: str,
    issue_number: Optional[str] = None,
    total_steps: int = 0,
) -> None:
    """Record workflow start in ai_developer_workflows table.

    Args:
        adw_id: Unique workflow identifier (used as primary key).
        workflow_type: Type of workflow (sdlc, sdlc_zte, ship, patch).
        issue_number: GitHub issue number (stored in metadata).
        total_steps: Total number of phases in the workflow.
    """
    if not _conn:
        return
    try:
        now = datetime.utcnow().isoformat()
        _conn.execute(
            """INSERT OR REPLACE INTO ai_developer_workflows
               (id, adw_name, workflow_type, status, total_steps,
                completed_steps, started_at, created_at, updated_at, metadata)
               VALUES (?, ?, ?, 'in_progress', ?, 0, ?, ?, ?, ?)""",
            (
                adw_id,
                adw_id,
                workflow_type,
                total_steps,
                now,
                now,
                now,
                f'{{"issue_number": "{issue_number}"}}' if issue_number else "{}",
            ),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Workflow started: {adw_id} ({workflow_type})")
    except Exception as e:
        logger.warning(f"[DB Bridge] track_workflow_start failed: {e}")


def track_phase_update(
    adw_id: str,
    phase_name: str,
    status: str,
    completed_steps: int,
) -> None:
    """Update workflow progress for a phase transition.

    Args:
        adw_id: Workflow identifier.
        phase_name: Name of the current phase (plan, build, test, etc).
        status: Phase status (in_progress, completed, failed, skipped).
        completed_steps: Number of phases completed so far.
    """
    if not _conn:
        return
    try:
        _conn.execute(
            """UPDATE ai_developer_workflows
               SET current_step = ?, completed_steps = ?, status = 'in_progress',
                   updated_at = datetime('now')
               WHERE id = ?""",
            (phase_name, completed_steps, adw_id),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Phase update: {adw_id} → {phase_name} ({status})")
    except Exception as e:
        logger.warning(f"[DB Bridge] track_phase_update failed: {e}")


def track_workflow_end(
    adw_id: str,
    status: str,
    error_message: Optional[str] = None,
) -> None:
    """Record workflow completion or failure.

    Args:
        adw_id: Workflow identifier.
        status: Final status (completed, failed, cancelled).
        error_message: Error details if failed.
    """
    if not _conn:
        return
    try:
        now = datetime.utcnow().isoformat()
        _conn.execute(
            """UPDATE ai_developer_workflows
               SET status = ?, completed_at = ?, error_message = ?,
                   updated_at = datetime('now'),
                   duration_seconds = CAST(
                       (julianday(?) - julianday(started_at)) * 86400 AS INTEGER
                   )
               WHERE id = ?""",
            (status, now, error_message, now, adw_id),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Workflow ended: {adw_id} → {status}")
    except Exception as e:
        logger.warning(f"[DB Bridge] track_workflow_end failed: {e}")


# ---------------------------------------------------------------------------
# Agent tracking (agents table)
# ---------------------------------------------------------------------------

def track_agent_start(
    adw_id: str,
    agent_name: str,
    model: str = "unknown",
) -> str:
    """Record agent start in agents table.

    Args:
        adw_id: Parent workflow identifier (used as session_id).
        agent_name: Name of the agent phase (e.g. adw_plan_iso).
        model: Model used by the agent.

    Returns:
        Agent ID (UUID) or empty string on failure.
    """
    if not _conn:
        return ""
    try:
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        # Use a default orchestrator_agent_id for ADW workflows
        orch_id = "adw-orchestrator"

        # Ensure the orchestrator_agent exists (idempotent)
        _conn.execute(
            """INSERT OR IGNORE INTO orchestrator_agents
               (id, name, agent_type, description, created_at, updated_at)
               VALUES (?, ?, 'orchestrator', 'ADW Workflow Orchestrator', ?, ?)""",
            (orch_id, "ADW Orchestrator", now, now),
        )

        _conn.execute(
            """INSERT INTO agents
               (id, orchestrator_agent_id, session_id, status, context, started_at)
               VALUES (?, ?, ?, 'executing', ?, ?)""",
            (agent_id, orch_id, adw_id, agent_name, now),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Agent started: {agent_name} ({agent_id[:8]})")
        return agent_id
    except Exception as e:
        logger.warning(f"[DB Bridge] track_agent_start failed: {e}")
        return ""


def track_agent_end(
    agent_id: str,
    status: str = "completed",
    cost_usd: float = 0.0,
    error_message: Optional[str] = None,
) -> None:
    """Record agent completion in agents table.

    Args:
        agent_id: Agent UUID from track_agent_start.
        status: Final status (completed, failed).
        cost_usd: Total cost in USD.
        error_message: Error details if failed.
    """
    if not _conn or not agent_id:
        return
    try:
        now = datetime.utcnow().isoformat()
        _conn.execute(
            """UPDATE agents
               SET status = ?, completed_at = ?, cost_usd = ?, error_message = ?
               WHERE id = ?""",
            (status, now, cost_usd, error_message, agent_id),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Agent ended: {agent_id[:8]} → {status}")
    except Exception as e:
        logger.warning(f"[DB Bridge] track_agent_end failed: {e}")


# ---------------------------------------------------------------------------
# System logging (system_logs table)
# ---------------------------------------------------------------------------

def log_event(
    component: str,
    message: str,
    level: str = "INFO",
    details: Optional[str] = None,
) -> None:
    """Write a system log entry.

    Args:
        component: Component name (e.g. adw_sdlc_iso, adw_plan_iso).
        message: Log message.
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        details: Additional JSON details.
    """
    if not _conn:
        return
    try:
        _conn.execute(
            """INSERT INTO system_logs (log_level, component, message, details, created_at)
               VALUES (?, ?, ?, ?, datetime('now'))""",
            (level, component, message, details),
        )
        _conn.commit()
    except Exception as e:
        logger.warning(f"[DB Bridge] log_event failed: {e}")
