"""WebSocket endpoint for real-time agent status updates."""

import asyncio
import json
from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from adws.adw_modules.adw_database import DatabaseManager
from orchestrator_web.dependencies import get_db_manager


router = APIRouter()


@router.websocket("/agent-status")
async def websocket_agent_status(
    websocket: WebSocket,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """WebSocket endpoint for broadcasting agent status updates.

    Polls the database every 2 seconds and sends updates to connected clients.
    """
    await websocket.accept()

    try:
        while True:
            # Poll database for agent updates
            agents = await db.list_agents()

            # Broadcast update
            message = {
                "type": "agent_update",
                "data": agents
            }
            await websocket.send_text(json.dumps(message))

            # Wait 2 seconds before next poll
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
