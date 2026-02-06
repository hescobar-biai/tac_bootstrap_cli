"""TAC-14 Compatible Router - Endpoints matching the tac-14 frontend API surface.

Provides the exact endpoint paths and response formats that the
orchestrator_3_stream frontend (from tac-14) expects.
All endpoints read from SQLite (data/orchestrator.db).
"""

import json
import uuid
from datetime import datetime
from typing import Any, Optional

import aiosqlite
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from config import DATABASE_PATH

router = APIRouter()


# ═══════════════════════════════════════════════════════════
# REQUEST MODELS
# ═══════════════════════════════════════════════════════════

class ListAdwsRequest(BaseModel):
    orchestrator_agent_id: str
    status: Optional[str] = None
    limit: Optional[int] = 20


class GetAdwEventsRequest(BaseModel):
    adw_id: str
    limit: Optional[int] = 2000
    event_type: Optional[str] = None
    include_payload: Optional[bool] = True


class LoadChatRequest(BaseModel):
    orchestrator_agent_id: str
    limit: Optional[int] = 50


class SendChatRequest(BaseModel):
    message: str
    orchestrator_agent_id: str


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

async def _query_db(sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    """Execute a SELECT query and return rows as dicts."""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(sql, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[compat] DB error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _query_one(sql: str, params: tuple = ()) -> Optional[dict[str, Any]]:
    """Execute a SELECT query and return a single row or None."""
    rows = await _query_db(sql, params)
    return rows[0] if rows else None


def _get_orchestrator_id() -> str:
    """Get or create a default orchestrator ID for SQLite mode."""
    return "sqlite-orchestrator-default"


def _transform_agent(row: dict[str, Any]) -> dict[str, Any]:
    """Transform agents DB row to match frontend Agent interface.

    DB columns: id, orchestrator_agent_id, session_id, parent_agent_id,
                status, context, config, started_at, completed_at, cost_usd, error_message
    Frontend expects: id, name, model, status, adw_id, adw_step, total_cost,
                      input_tokens, output_tokens, metadata, created_at, updated_at, ...
    """
    context = row.get("context") or ""
    # Derive adw_step from context (e.g. "adw_plan_iso" -> "plan")
    adw_step = ""
    if context.startswith("adw_") and context.endswith("_iso"):
        adw_step = context.replace("adw_", "").replace("_iso", "")

    return {
        "id": row.get("id", ""),
        "name": context or "unknown",
        "model": "claude-sonnet-4-5-20250929",
        "system_prompt": None,
        "working_dir": None,
        "git_worktree": None,
        "status": row.get("status", "initializing"),
        "session_id": row.get("session_id"),
        "adw_id": row.get("session_id"),
        "adw_step": adw_step,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_cost": row.get("cost_usd", 0.0) or 0.0,
        "archived": False,
        "metadata": {},
        "task": adw_step,
        "created_at": row.get("started_at", ""),
        "updated_at": row.get("completed_at") or row.get("started_at", ""),
        "error_message": row.get("error_message"),
    }


# Map DB log_type to frontend event_category
_LOG_TYPE_TO_CATEGORY = {
    "state_change": "response",
    "milestone": "response",
    "error": "response",
    "performance": "response",
    "tool_call": "hook",
    "cost_update": "response",
}


def _transform_agent_log(row: dict[str, Any]) -> dict[str, Any]:
    """Transform agent_logs DB row to match frontend AgentLog interface.

    DB columns: id, agent_id, log_level, log_type, message, details, created_at
    Frontend expects: id, agent_id, agent_name, event_category, event_type,
                      content, summary, payload, timestamp, ...
    """
    log_type = row.get("log_type", "milestone")
    details_raw = row.get("details")
    payload = {}
    if details_raw:
        try:
            payload = json.loads(details_raw)
        except (json.JSONDecodeError, TypeError):
            payload = {"text": details_raw}

    return {
        "id": str(row.get("id", "")),
        "agent_id": row.get("agent_id", ""),
        "agent_name": None,
        "session_id": None,
        "task_slug": None,
        "entry_index": None,
        "event_category": _LOG_TYPE_TO_CATEGORY.get(log_type, "response"),
        "event_type": log_type,
        "content": row.get("message", ""),
        "summary": row.get("message", ""),
        "payload": payload,
        "timestamp": row.get("created_at", ""),
        "log_level": row.get("log_level", "INFO"),
    }


# ═══════════════════════════════════════════════════════════
# ORCHESTRATOR INFO
# ═══════════════════════════════════════════════════════════

@router.get("/get_orchestrator")
async def get_orchestrator_info():
    """Get orchestrator info - required by frontend on initialization."""
    orch_id = _get_orchestrator_id()

    # Try to find an orchestrator in the DB
    orch = await _query_one(
        "SELECT * FROM orchestrator_agents LIMIT 1"
    )

    if orch:
        orch_id = orch["id"]

    return {
        "status": "success",
        "orchestrator": {
            "id": orch_id,
            "session_id": None,
            "status": "active",
            "working_dir": str(Path(DATABASE_PATH).parent.parent),
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0,
            "metadata": {
                "system_message_info": {
                    "session_id": None,
                    "cwd": str(Path(DATABASE_PATH).parent.parent),
                    "captured_at": None,
                    "subtype": "sqlite_mode"
                }
            },
        },
        "slash_commands": [],
        "agent_templates": [],
        "orchestrator_tools": [],
        "adw_workflows": [],
    }


@router.get("/get_headers")
async def get_headers():
    """Get header info for the frontend."""
    return {
        "status": "success",
        "cwd": str(Path(DATABASE_PATH).parent.parent)
    }


# ═══════════════════════════════════════════════════════════
# AGENTS
# ═══════════════════════════════════════════════════════════

@router.get("/list_agents")
async def list_agents():
    """List all agents for sidebar display."""
    rows = await _query_db(
        "SELECT * FROM agents ORDER BY started_at DESC LIMIT 50"
    )

    agents = []
    for row in rows:
        agent = _transform_agent(row)
        # Enrich with log count
        log_rows = await _query_db(
            "SELECT COUNT(*) as cnt FROM agent_logs WHERE agent_id = ?",
            (row["id"],)
        )
        agent["log_count"] = log_rows[0]["cnt"] if log_rows else 0
        agents.append(agent)

    return {"status": "success", "agents": agents}


# ═══════════════════════════════════════════════════════════
# EVENTS
# ═══════════════════════════════════════════════════════════

@router.get("/get_events")
async def get_events(
    agent_id: Optional[str] = None,
    task_slug: Optional[str] = None,
    event_types: str = "all",
    limit: int = 50,
    offset: int = 0,
):
    """Get events from all sources for EventStream component."""
    requested_types = (
        event_types.split(",")
        if event_types != "all"
        else ["agent_logs", "orchestrator_chat"]
    )

    all_events: list[dict] = []

    if "agent_logs" in requested_types:
        if agent_id:
            log_rows = await _query_db(
                "SELECT * FROM agent_logs WHERE agent_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (agent_id, limit, offset)
            )
        else:
            log_rows = await _query_db(
                "SELECT * FROM agent_logs ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
        for row in log_rows:
            event = _transform_agent_log(row)
            event["sourceType"] = "agent_log"
            all_events.append(event)

    if "system_logs" in requested_types:
        sys_logs = await _query_db(
            "SELECT * FROM system_logs ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        for log in sys_logs:
            log["sourceType"] = "system_log"
            log["timestamp"] = log.get("created_at")
            all_events.append(log)

    if "orchestrator_chat" in requested_types:
        chats = await _query_db(
            "SELECT * FROM orchestrator_chat ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        for chat in chats:
            chat["sourceType"] = "orchestrator_chat"
            chat["timestamp"] = chat.get("created_at")
            all_events.append(chat)

    # Sort by timestamp newest first, take limit, then reverse for oldest-first display
    all_events.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    all_events = all_events[:limit]
    all_events.reverse()

    return {"status": "success", "events": all_events, "count": len(all_events)}


# ═══════════════════════════════════════════════════════════
# CHAT (STUBS)
# ═══════════════════════════════════════════════════════════

@router.post("/load_chat")
async def load_chat(request: LoadChatRequest):
    """Load chat history. Returns messages from orchestrator_chat table."""
    messages = await _query_db(
        "SELECT * FROM orchestrator_chat WHERE orchestrator_agent_id = ? ORDER BY created_at ASC LIMIT ?",
        (request.orchestrator_agent_id, request.limit or 50)
    )
    return {
        "status": "success",
        "messages": messages,
        "turn_count": len(messages),
    }


@router.post("/send_chat")
async def send_chat(request: SendChatRequest):
    """Send chat message - stub for SQLite mode."""
    return {
        "status": "success",
        "message": "Chat not available in SQLite mode. Use the ADW workflows view.",
    }


# ═══════════════════════════════════════════════════════════
# ADW ENDPOINTS
# ═══════════════════════════════════════════════════════════

@router.post("/adws")
async def list_adws(request: ListAdwsRequest):
    """List AI Developer Workflows."""
    if request.status:
        adws = await _query_db(
            "SELECT * FROM ai_developer_workflows WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (request.status, request.limit or 20)
        )
    else:
        adws = await _query_db(
            "SELECT * FROM ai_developer_workflows ORDER BY created_at DESC LIMIT ?",
            (request.limit or 20,)
        )

    return {"status": "success", "adws": adws, "count": len(adws)}


@router.get("/adws/{adw_id}")
async def get_adw(adw_id: str):
    """Get a single ADW by ID."""
    adw = await _query_one(
        "SELECT * FROM ai_developer_workflows WHERE id = ?",
        (adw_id,)
    )

    if not adw:
        # Also try by adw_name
        adw = await _query_one(
            "SELECT * FROM ai_developer_workflows WHERE adw_name = ?",
            (adw_id,)
        )

    if not adw:
        raise HTTPException(status_code=404, detail=f"ADW not found: {adw_id}")

    return {"status": "success", "adw": adw}


@router.post("/adws/{adw_id}/events")
async def get_adw_events(adw_id: str, request: GetAdwEventsRequest):
    """Get events for an ADW (swimlane squares)."""
    # The adw_id might be stored as text in agent_logs and system_logs
    # Check both the UUID id and the adw_name

    # Get the adw_name for this workflow (agent_logs reference by adw_name)
    adw = await _query_one(
        "SELECT adw_name FROM ai_developer_workflows WHERE id = ? OR adw_name = ?",
        (adw_id, adw_id)
    )
    adw_name = adw["adw_name"] if adw else adw_id

    events: list[dict] = []

    # System logs don't have adw_id in our SQLite schema, but we can check
    # if the component matches the adw_name
    sys_logs = await _query_db(
        "SELECT * FROM system_logs WHERE component = ? ORDER BY created_at ASC LIMIT ?",
        (adw_name, request.limit or 2000)
    )
    for log in sys_logs:
        log["sourceType"] = "system_log"
        log["timestamp"] = log.get("created_at")
        log["adw_step"] = "_workflow"
        events.append(log)

    # Sort by timestamp (oldest first for swimlane rendering)
    events.sort(key=lambda e: e.get("timestamp", ""))

    # Group by step
    steps: dict[str, list[dict]] = {}
    for event in events:
        step = event.get("adw_step") or "_workflow"
        if step not in steps:
            steps[step] = []
        steps[step].append(event)

    return {
        "status": "success",
        "adw_id": adw_id,
        "events": events,
        "events_by_step": steps,
        "count": len(events),
    }


@router.get("/adws/{adw_id}/summary")
async def get_adw_summary(adw_id: str):
    """Get ADW summary with step breakdown."""
    adw = await _query_one(
        "SELECT * FROM ai_developer_workflows WHERE id = ? OR adw_name = ?",
        (adw_id, adw_id)
    )

    if not adw:
        raise HTTPException(status_code=404, detail=f"ADW not found: {adw_id}")

    return {
        "status": "success",
        "adw": adw,
        "steps": [],
        "total_events": 0,
    }
