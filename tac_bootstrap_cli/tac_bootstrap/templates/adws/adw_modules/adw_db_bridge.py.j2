"""Sync PostgreSQL bridge for ADW workflow tracking.

Provides synchronous database writes to the orchestrator PostgreSQL database
using psycopg2. This avoids the async/sync mismatch since ADW workflows
use subprocess.run() (sync) while the web backend uses asyncpg (async).

All functions are wrapped in try/except - DB failures log to stderr
and never crash workflows.

Requires DATABASE_URL environment variable (PostgreSQL connection string).
"""

import json
import os
import uuid
import logging
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Module-level connection
_conn = None

# Well-known orchestrator agent ID for ADW workflows
# Created by migration 10_adw_orchestrator_agent.sql
ADW_ORCHESTRATOR_ID = "00000000-0000-0000-0000-ad0000000000"

# Namespace for deterministic UUID generation from ADW ID strings
_ADW_UUID_NAMESPACE = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")


def _adw_id_to_uuid(adw_id: str) -> str:
    """Convert a string ADW ID to a deterministic UUID.

    Uses uuid5 so the same adw_id always produces the same UUID.
    """
    return str(uuid.uuid5(_ADW_UUID_NAMESPACE, adw_id))


def _map_agent_status(status: str) -> str:
    """Map bridge status values to agents table check constraint values.

    agents.status allows: idle, executing, waiting, blocked, complete
    """
    mapping = {
        "completed": "complete",
        "failed": "blocked",
        "executing": "executing",
        "idle": "idle",
    }
    return mapping.get(status, "complete")


def init_bridge(database_url: Optional[str] = None) -> None:
    """Open psycopg2 connection to orchestrator PostgreSQL database.

    Args:
        database_url: PostgreSQL connection string. Defaults to DATABASE_URL env var.
    """
    global _conn
    try:
        import psycopg2
        url = database_url or os.getenv("DATABASE_URL")
        if not url:
            logger.warning("[DB Bridge] DATABASE_URL not set, bridge disabled")
            _conn = None
            return
        _conn = psycopg2.connect(url)
        _conn.autocommit = False
        logger.info("[DB Bridge] Connected to PostgreSQL")
    except Exception as e:
        logger.warning(f"[DB Bridge] Failed to connect: {e}")
        _conn = None


def close_bridge() -> None:
    """Close the psycopg2 connection."""
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
        workflow_uuid = _adw_id_to_uuid(adw_id)
        metadata = json.dumps({"issue_number": issue_number, "adw_id": adw_id}) if issue_number else json.dumps({"adw_id": adw_id})
        cur = _conn.cursor()
        cur.execute(
            """INSERT INTO ai_developer_workflows
               (id, orchestrator_agent_id, adw_name, workflow_type, status,
                total_steps, completed_steps, started_at, created_at, updated_at, metadata)
               VALUES (%s, %s, %s, %s, 'in_progress', %s, 0, NOW(), NOW(), NOW(), %s)
               ON CONFLICT (id) DO UPDATE SET
                   status = 'in_progress',
                   total_steps = EXCLUDED.total_steps,
                   started_at = NOW(),
                   updated_at = NOW(),
                   metadata = EXCLUDED.metadata""",
            (
                workflow_uuid,
                ADW_ORCHESTRATOR_ID,
                adw_id,
                workflow_type,
                total_steps,
                metadata,
            ),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Workflow started: {adw_id} ({workflow_type})")
    except Exception as e:
        _conn.rollback()
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
        workflow_uuid = _adw_id_to_uuid(adw_id)
        cur = _conn.cursor()
        cur.execute(
            """UPDATE ai_developer_workflows
               SET current_step = %s, completed_steps = %s, status = 'in_progress',
                   updated_at = NOW()
               WHERE id = %s""",
            (phase_name, completed_steps, workflow_uuid),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Phase update: {adw_id} -> {phase_name} ({status})")
    except Exception as e:
        _conn.rollback()
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
        workflow_uuid = _adw_id_to_uuid(adw_id)
        cur = _conn.cursor()
        cur.execute(
            """UPDATE ai_developer_workflows
               SET status = %s, completed_at = NOW(), error_message = %s,
                   updated_at = NOW(),
                   duration_seconds = EXTRACT(EPOCH FROM (NOW() - started_at))::integer
               WHERE id = %s""",
            (status, error_message, workflow_uuid),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Workflow ended: {adw_id} -> {status}")
    except Exception as e:
        _conn.rollback()
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
        adw_id: Parent workflow identifier.
        agent_name: Name of the agent phase (e.g. adw_plan_iso).
        model: Model used by the agent.

    Returns:
        Agent ID (UUID) or empty string on failure.
    """
    if not _conn:
        return ""
    try:
        agent_id = str(uuid.uuid4())
        unique_name = f"{agent_name}_{adw_id}"
        cur = _conn.cursor()
        cur.execute(
            """INSERT INTO agents
               (id, orchestrator_agent_id, name, model, adw_id, status, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, 'executing', NOW(), NOW())
               ON CONFLICT (orchestrator_agent_id, name) DO UPDATE SET
                   status = 'executing', model = EXCLUDED.model, updated_at = NOW()
               RETURNING id""",
            (agent_id, ADW_ORCHESTRATOR_ID, unique_name, model, adw_id),
        )
        row = cur.fetchone()
        if row:
            agent_id = str(row[0])
        # Log agent start event
        cur.execute(
            """INSERT INTO agent_logs
               (id, agent_id, adw_id, event_category, event_type, content, payload, timestamp)
               VALUES (%s, %s, %s, 'adw_step', 'AgentStart', %s, %s, NOW())""",
            (
                str(uuid.uuid4()),
                agent_id,
                adw_id,
                f"Agent {agent_name} started (ADW: {adw_id})",
                json.dumps({"agent_name": agent_name, "model": model}),
            ),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Agent started: {agent_name} ({agent_id[:8]})")
        return agent_id
    except Exception as e:
        _conn.rollback()
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
        db_status = _map_agent_status(status)
        cur = _conn.cursor()
        cur.execute(
            """UPDATE agents
               SET status = %s, total_cost = %s, updated_at = NOW()
               WHERE id = %s""",
            (db_status, cost_usd, agent_id),
        )
        # Log agent end event
        event_type = "AgentFailed" if status == "failed" else "AgentCompleted"
        msg = f"Agent ended: {status}"
        if cost_usd > 0:
            msg += f" (cost: ${cost_usd:.4f})"
        if error_message:
            msg += f" - {error_message}"
        cur.execute(
            """INSERT INTO agent_logs
               (id, agent_id, event_category, event_type, content, payload, timestamp)
               VALUES (%s, %s, 'adw_step', %s, %s, %s, NOW())""",
            (
                str(uuid.uuid4()),
                agent_id,
                event_type,
                msg,
                json.dumps({"status": status, "cost_usd": cost_usd, "error": error_message}),
            ),
        )
        _conn.commit()
        logger.info(f"[DB Bridge] Agent ended: {agent_id[:8]} -> {status}")
    except Exception as e:
        _conn.rollback()
        logger.warning(f"[DB Bridge] track_agent_end failed: {e}")


# ---------------------------------------------------------------------------
# Agent logging (agent_logs table)
# ---------------------------------------------------------------------------

def log_agent_event(
    agent_id: str,
    message: str,
    log_type: str = "milestone",
    level: str = "INFO",
    details: Optional[str] = None,
) -> None:
    """Write an agent log entry.

    Args:
        agent_id: Agent UUID from track_agent_start.
        message: Log message.
        log_type: Event type (state_change, milestone, error, performance, tool_call).
        level: Log level (DEBUG, INFO, WARNING, ERROR).
        details: Additional JSON details.
    """
    if not _conn or not agent_id:
        return
    try:
        payload = json.dumps({"level": level, "details": details}) if details else "{}"
        cur = _conn.cursor()
        cur.execute(
            """INSERT INTO agent_logs
               (id, agent_id, event_category, event_type, content, payload, timestamp)
               VALUES (%s, %s, 'adw_step', %s, %s, %s, NOW())""",
            (str(uuid.uuid4()), agent_id, log_type, message, payload),
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        logger.warning(f"[DB Bridge] log_agent_event failed: {e}")


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
        level: Log level (DEBUG, INFO, WARNING, ERROR).
        details: Additional JSON details.
    """
    if not _conn:
        return
    try:
        metadata = json.dumps({"component": component, "details": details}) if details else json.dumps({"component": component})
        cur = _conn.cursor()
        cur.execute(
            """INSERT INTO system_logs
               (id, level, message, metadata, timestamp)
               VALUES (%s, %s, %s, %s, NOW())""",
            (str(uuid.uuid4()), level, message, metadata),
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        logger.warning(f"[DB Bridge] log_event failed: {e}")
