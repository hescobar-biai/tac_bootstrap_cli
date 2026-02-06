"""Orchestrator Web Backend - FastAPI Application.

Zero-configuration FastAPI server for orchestrating ADW workflows with SQLite.
Provides REST API (CQRS) + WebSocket for real-time agent status updates.

Serves the tac-14 frontend API surface at root level (no /api prefix)
for compatibility with orchestrator_3_stream frontend.
"""

import asyncio
import json
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import aiosqlite
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Add adws directory to path for adw_modules import
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "adws"))

from adw_modules.adw_database import DatabaseManager
import dependencies
from config import DATABASE_PATH, CORS_ORIGINS, BACKEND_PORT
from routers import agents, runtime, websocket, compat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager - connects DatabaseManager on startup."""
    # Startup
    db_path = dependencies.get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[Orchestrator] Connecting to database: {db_path}")
    dependencies.db_manager = DatabaseManager(str(db_path))
    await dependencies.db_manager.connect()
    print("[Orchestrator] Database connected successfully")

    yield

    # Shutdown
    print("[Orchestrator] Closing database connection")
    await dependencies.db_manager.close()
    print("[Orchestrator] Shutdown complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Orchestrator Web Backend",
    description="FastAPI backend for TAC Bootstrap agent orchestration",
    version="0.9.0",
    lifespan=lifespan,
)

# Configure CORS for Web UI (origins loaded from config.yml)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
# Original CQRS routers under /api prefix
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(runtime.router, prefix="/api", tags=["Runtime"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket (Legacy)"])

# TAC-14 compatible router at root level (no prefix)
app.include_router(compat.router, tags=["TAC-14 Compatible"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "orchestrator-web",
        "version": "0.9.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Detailed health check with database status."""
    db_manager = dependencies.get_db_manager()
    return {
        "status": "healthy",
        "service": "orchestrator-web",
        "database": "connected" if db_manager.conn else "disconnected",
        "database_path": str(dependencies.get_database_path()),
        "websocket_connections": len(_ws_connections),
    }


# ═══════════════════════════════════════════════════════════
# WEBSOCKET at /ws (TAC-14 compatible)
# ═══════════════════════════════════════════════════════════

_ws_connections: list[WebSocket] = []


async def _broadcast_to_all(data: dict, exclude: WebSocket | None = None):
    """Broadcast a message to all connected WebSocket clients."""
    if "timestamp" not in data:
        data["timestamp"] = datetime.now().isoformat()

    disconnected = []
    for ws in _ws_connections:
        if ws == exclude:
            continue
        try:
            await ws.send_json(data)
        except Exception:
            disconnected.append(ws)

    for ws in disconnected:
        if ws in _ws_connections:
            _ws_connections.remove(ws)


async def _poll_adw_changes():
    """Background task that polls SQLite for ADW changes and broadcasts updates."""
    last_snapshot = ""

    while True:
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM ai_developer_workflows ORDER BY created_at DESC LIMIT 20"
                )
                rows = await cursor.fetchall()
                workflows = [dict(row) for row in rows]

            # Change detection
            snapshot = json.dumps(
                [(w.get("adw_name"), w.get("status"), w.get("current_step"),
                  w.get("completed_steps"), w.get("updated_at"))
                 for w in workflows],
                default=str,
            )

            if snapshot != last_snapshot and workflows:
                # Broadcast each workflow as an adw_updated event
                for wf in workflows:
                    await _broadcast_to_all({
                        "type": "adw_updated",
                        "adw_id": wf.get("id", wf.get("adw_name")),
                        "adw": wf,
                    })
                last_snapshot = snapshot

        except Exception as e:
            print(f"[WS Poll] Error: {e}")

        await asyncio.sleep(2)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint compatible with tac-14 frontend chatService.

    Sends real-time ADW updates by polling SQLite every 2 seconds.
    Also handles incoming messages (adw_broadcast, agent_broadcast).
    """
    await websocket.accept()
    _ws_connections.append(websocket)

    client_id = f"client_{len(_ws_connections)}"
    print(f"[WS] Client connected: {client_id} (total: {len(_ws_connections)})")

    # Send welcome message
    await websocket.send_json({
        "type": "connection_established",
        "client_id": client_id,
        "timestamp": datetime.now().isoformat(),
        "message": "Connected to Orchestrator Backend (SQLite mode)",
    })

    # Start background poller
    poll_task = asyncio.create_task(_poll_adw_changes())

    try:
        while True:
            data = await websocket.receive_text()
            if not data:
                continue

            try:
                message = json.loads(data)
                if not isinstance(message, dict) or "type" not in message:
                    continue

                msg_type = message.get("type")

                # Handle ADW broadcast requests (from workflow processes)
                if msg_type == "adw_broadcast":
                    broadcast_type = message.get("broadcast_type")
                    if broadcast_type == "adw_created":
                        await _broadcast_to_all(
                            {"type": "adw_created", "adw": message.get("adw", {})},
                            exclude=websocket,
                        )
                    elif broadcast_type == "adw_updated":
                        await _broadcast_to_all(
                            {"type": "adw_updated", "adw_id": message.get("adw_id", ""),
                             "adw": message.get("adw", {})},
                            exclude=websocket,
                        )
                    elif broadcast_type == "adw_event":
                        await _broadcast_to_all(
                            {"type": "adw_event", "adw_id": message.get("adw_id", ""),
                             "event": message.get("event", {})},
                            exclude=websocket,
                        )
                    elif broadcast_type == "adw_step_change":
                        await _broadcast_to_all(
                            {"type": "adw_step_change", "adw_id": message.get("adw_id", ""),
                             "step": message.get("step", ""),
                             "event_type": message.get("event_type", ""),
                             "payload": message.get("payload", {})},
                            exclude=websocket,
                        )
                    elif broadcast_type == "adw_status":
                        await _broadcast_to_all(
                            {"type": "adw_updated", "adw_id": message.get("adw_id", ""),
                             "adw": {
                                 "status": message.get("status"),
                                 "current_step": message.get("current_step"),
                                 "completed_steps": message.get("completed_steps"),
                                 "error_message": message.get("error_message"),
                             }},
                            exclude=websocket,
                        )

                # Handle agent broadcast requests
                elif msg_type == "agent_broadcast":
                    broadcast_type = message.get("broadcast_type")
                    if broadcast_type == "agent_created":
                        await _broadcast_to_all(
                            {"type": "agent_created", "agent": message.get("agent", {})},
                            exclude=websocket,
                        )
                    elif broadcast_type == "agent_status_changed":
                        await _broadcast_to_all(
                            {"type": "agent_status_changed",
                             "agent_id": message.get("agent_id", ""),
                             "old_status": message.get("old_status", ""),
                             "new_status": message.get("new_status", "")},
                            exclude=websocket,
                        )

            except json.JSONDecodeError:
                pass  # Plain text ping

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[WS] Error: {e}")
    finally:
        poll_task.cancel()
        if websocket in _ws_connections:
            _ws_connections.remove(websocket)
        print(f"[WS] Client disconnected (total: {len(_ws_connections)})")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=True,
        log_level="info"
    )
