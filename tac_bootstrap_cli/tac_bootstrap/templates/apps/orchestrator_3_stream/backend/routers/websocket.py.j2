"""WebSocket Router - Real-time agent status updates."""

import asyncio
import json
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dependencies import get_db_manager

router = APIRouter()


@router.websocket("/orchestrator")
async def websocket_agent_status(websocket: WebSocket):
    """WebSocket endpoint for real-time agent status updates.
    
    Accepts connection and broadcasts agent status changes every 2 seconds.
    Sends JSON messages: {"type": "agent_update", "data": {...}}
    """
    await websocket.accept()
    
    try:
        db = get_db_manager()
        last_state: dict[str, Any] = {}
        
        while True:
            # Poll database for current agent state
            agents = await db.list_agents()
            
            # Create current state snapshot
            current_state = {
                agent["id"]: {
                    "id": agent["id"],
                    "orchestrator_agent_id": agent["orchestrator_agent_id"],
                    "session_id": agent["session_id"],
                    "status": agent["status"],
                    "started_at": agent["started_at"],
                    "completed_at": agent.get("completed_at"),
                }
                for agent in agents
            }
            
            # Detect changes
            if current_state != last_state:
                # Send update to client
                message = {
                    "type": "agent_update",
                    "data": {
                        "agents": list(current_state.values()),
                        "timestamp": agents[0]["started_at"] if agents else None
                    }
                }
                
                await websocket.send_json(message)
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
