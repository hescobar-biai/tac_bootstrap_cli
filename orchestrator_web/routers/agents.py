"""Orchestrator Agents Router - CQRS endpoints for orchestrator_agents table."""

from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adw_modules.adw_database import DatabaseManager
from dependencies import get_db_manager

router = APIRouter()


# Pydantic Models for Request/Response
class OrchestratorAgentCreate(BaseModel):
    """Request model for creating orchestrator agent."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    agent_type: str = Field(..., description="Agent type: 'skill', 'custom', 'orchestrator'")
    capabilities: str = Field(..., description="Comma-separated capabilities")
    default_model: str = Field(default="claude-sonnet-3.5")
    metadata: dict[str, Any] | None = None


class OrchestratorAgentUpdate(BaseModel):
    """Request model for updating orchestrator agent."""
    description: str | None = None
    agent_type: str | None = None
    capabilities: str | None = None
    default_model: str | None = None
    is_active: bool | None = None
    metadata: dict[str, Any] | None = None


# CQRS Endpoints

@router.get("/agents")
async def list_orchestrator_agents(
    db: DatabaseManager = Depends(get_db_manager)
) -> list[dict[str, Any]]:
    """List all orchestrator agents (query side)."""
    agents = await db.list_orchestrator_agents()
    return agents


@router.post("/agents", status_code=201)
async def create_orchestrator_agent(
    agent: OrchestratorAgentCreate,
    db: DatabaseManager = Depends(get_db_manager)
) -> dict[str, Any]:
    """Create new orchestrator agent (command side)."""
    agent_id = await db.create_orchestrator_agent(
        name=agent.name,
        description=agent.description,
        agent_type=agent.agent_type,
        capabilities=agent.capabilities,
        default_model=agent.default_model,
        metadata=agent.metadata
    )
    
    # Return created agent
    created = await db.get_orchestrator_agent(agent_id)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to retrieve created agent")
    
    return created


@router.get("/agents/{agent_id}")
async def get_orchestrator_agent(
    agent_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> dict[str, Any]:
    """Get orchestrator agent by ID (query side)."""
    agent = await db.get_orchestrator_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return agent


@router.put("/agents/{agent_id}")
async def update_orchestrator_agent(
    agent_id: str,
    updates: OrchestratorAgentUpdate,
    db: DatabaseManager = Depends(get_db_manager)
) -> dict[str, Any]:
    """Update orchestrator agent (command side)."""
    # Check agent exists
    existing = await db.get_orchestrator_agent(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    # Build update dict (only provided fields)
    update_data = updates.model_dump(exclude_unset=True)
    
    await db.update_orchestrator_agent(agent_id, **update_data)
    
    # Return updated agent
    updated = await db.get_orchestrator_agent(agent_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated agent")
    
    return updated


@router.delete("/agents/{agent_id}", status_code=204)
async def delete_orchestrator_agent(
    agent_id: str,
    db: DatabaseManager = Depends(get_db_manager)
):
    """Delete orchestrator agent (command side)."""
    # Check agent exists
    existing = await db.get_orchestrator_agent(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    await db.delete_orchestrator_agent(agent_id)
    return None
