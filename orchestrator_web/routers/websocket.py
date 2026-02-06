"""WebSocket Router - Real-time workflow status updates."""

import asyncio
import json
from datetime import datetime
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import DATABASE_PATH

router = APIRouter()

# Phase definitions per workflow type
WORKFLOW_PHASES = {
    "sdlc_zte": ["plan", "build", "test", "review", "document", "ship"],
    "sdlc": ["plan", "build", "test", "review", "document"],
    "ship": ["merge"],
}


def _map_workflow_status(status: str) -> str:
    """Map DB workflow status to frontend AgentStatus."""
    mapping = {
        "pending": "pending",
        "in_progress": "running",
        "completed": "completed",
        "failed": "failed",
        "cancelled": "failed",
    }
    return mapping.get(status, "pending")


def _map_phase_status(phase: str, current_step: str | None, completed_steps: int, phases: list[str]) -> str:
    """Determine phase status based on workflow progress."""
    phase_index = phases.index(phase) if phase in phases else -1
    if phase_index < completed_steps:
        return "completed"
    if current_step and phase == current_step:
        return "running"
    return "pending"


async def _get_workflows(db_path: str) -> list[dict[str, Any]]:
    """Read ai_developer_workflows directly from SQLite."""
    try:
        async with aiosqlite.connect(db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM ai_developer_workflows ORDER BY created_at DESC LIMIT 20"
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[WebSocket] Error reading workflows: {e}")
        return []


def _workflow_to_agent(wf: dict) -> dict:
    """Convert a workflow record to a frontend Agent object."""
    issue = ""
    try:
        meta = json.loads(wf.get("metadata", "{}") or "{}")
        issue = meta.get("issue_number", "")
    except (json.JSONDecodeError, TypeError):
        pass

    wf_type = wf.get("workflow_type", "sdlc")
    name = f"{wf_type.upper()} #{issue}" if issue else f"{wf_type.upper()} ({wf['adw_name']})"

    return {
        "id": wf["adw_name"],
        "name": name,
        "status": _map_workflow_status(wf.get("status", "pending")),
        "createdAt": wf.get("created_at", datetime.utcnow().isoformat()),
    }


def _workflow_to_tasks(wf: dict) -> list[dict]:
    """Generate task cards for each phase of the workflow."""
    wf_type = wf.get("workflow_type", "sdlc")
    phases = WORKFLOW_PHASES.get(wf_type, ["plan", "build", "test", "review", "document"])
    current_step = wf.get("current_step")
    completed_steps = wf.get("completed_steps", 0) or 0
    adw_name = wf["adw_name"]
    updated_at = wf.get("updated_at", wf.get("created_at", ""))

    tasks = []
    for phase in phases:
        status = _map_phase_status(phase, current_step, completed_steps, phases)
        tasks.append({
            "id": f"{adw_name}-{phase}",
            "agentId": adw_name,
            "description": phase.capitalize(),
            "status": status,
            "timestamp": updated_at,
        })
    return tasks


@router.websocket("/orchestrator")
async def websocket_agent_status(websocket: WebSocket):
    """WebSocket endpoint for real-time workflow status updates.

    Polls ai_developer_workflows every 2 seconds and sends:
    - agent_update: one message per workflow (mapped to frontend Agent)
    - task_update: one message per phase (mapped to frontend Task)
    """
    await websocket.accept()

    try:
        last_state: str = ""

        while True:
            workflows = await _get_workflows(DATABASE_PATH)

            # Build snapshot for change detection
            current_state = json.dumps(
                [(w.get("adw_name"), w.get("status"), w.get("current_step"), w.get("completed_steps"))
                 for w in workflows],
                default=str,
            )

            if current_state != last_state:
                # Send agent updates (one per workflow)
                for wf in workflows:
                    agent = _workflow_to_agent(wf)
                    await websocket.send_json({
                        "type": "agent_update",
                        "data": {"agent": agent},
                    })

                    # Send task updates (one per phase)
                    tasks = _workflow_to_tasks(wf)
                    for task in tasks:
                        await websocket.send_json({
                            "type": "task_update",
                            "data": {"task": task},
                        })

                last_state = current_state

            # Poll every 2 seconds
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")
    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        try:
            await websocket.close()
        except:
            pass
