"""CQRS endpoints for orchestrator agents."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from adws.adw_modules.adw_database import DatabaseManager
from orchestrator_web.dependencies import get_db_manager


router = APIRouter()


class CreateOrchestratorAgentRequest(BaseModel):
    """Request model for creating an orchestrator agent."""
    name: str
    description: str
    type: str
    capabilities: dict
    model: str = "claude-sonnet-4"


class UpdateOrchestratorAgentRequest(BaseModel):
    """Request model for updating an orchestrator agent."""
    name: str | None = None
    description: str | None = None
    type: str | None = None
    capabilities: dict | None = None
    model: str | None = None


@router.get("/agents")
async def list_agents(
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """List all orchestrator agents."""
    agents = await db.list_orchestrator_agents()
    return {"agents": agents}


@router.post("/agents", status_code=201)
async def create_agent(
    request: CreateOrchestratorAgentRequest,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Create a new orchestrator agent."""
    agent_id = await db.create_orchestrator_agent(
        name=request.name,
        description=request.description,
        type=request.type,
        capabilities=request.capabilities,
        model=request.model
    )
    return {"id": agent_id, "message": "Agent created successfully"}


@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Get a specific orchestrator agent by ID."""
    agent = await db.get_orchestrator_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/agents/{agent_id}")
async def update_agent(
    agent_id: str,
    request: UpdateOrchestratorAgentRequest,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Update an orchestrator agent."""
    # Build update dict with only provided fields
    updates = {}
    if request.name is not None:
        updates["name"] = request.name
    if request.description is not None:
        updates["description"] = request.description
    if request.type is not None:
        updates["type"] = request.type
    if request.capabilities is not None:
        updates["capabilities"] = request.capabilities
    if request.model is not None:
        updates["model"] = request.model

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    await db.update_orchestrator_agent(agent_id, **updates)
    return {"message": "Agent updated successfully"}


@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: Annotated[DatabaseManager, Depends(get_db_manager)]
):
    """Delete an orchestrator agent."""
    await db.delete_orchestrator_agent(agent_id)
    return {"message": "Agent deleted successfully"}
