"""Endpoints for runtime agents, prompts, and logs."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from adws.adw_modules.adw_database import DatabaseManager
from orchestrator_web.dependencies import get_db_manager


router = APIRouter()


class CreateAgentRequest(BaseModel):
    """Request model for creating a runtime agent."""
    orchestrator_agent_id: str
    session_id: str


@router.get("/runtime/agents")
async def list_runtime_agents(
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """List all runtime agents."""
    agents = await db.list_agents()
    return {"agents": agents}


@router.post("/runtime/agents", status_code=201)
async def create_runtime_agent(
    request: CreateAgentRequest,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Create a new runtime agent."""
    agent_id = await db.create_agent(
        orchestrator_agent_id=request.orchestrator_agent_id,
        session_id=request.session_id
    )
    return {"id": agent_id, "message": "Runtime agent created successfully"}


@router.get("/runtime/agents/{agent_id}")
async def get_runtime_agent(
    agent_id: str,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Get a specific runtime agent by ID."""
    agent = await db.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Runtime agent not found")
    return agent


@router.get("/runtime/prompts")
async def list_prompts(
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """List all prompts."""
    prompts = await db.list_prompts()
    return {"prompts": prompts}


@router.get("/runtime/logs")
async def get_recent_logs(
    limit: int = 100,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Get recent system logs."""
    logs = await db.get_recent_logs(limit=limit)
    return {"logs": logs}
