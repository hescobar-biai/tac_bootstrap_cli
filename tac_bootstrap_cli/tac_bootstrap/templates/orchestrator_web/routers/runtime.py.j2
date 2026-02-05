"""Runtime Router - Endpoints for runtime agents, prompts, and logs."""

from typing import Any
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adw_modules.adw_database import DatabaseManager
from dependencies import get_db_manager

router = APIRouter()


# Pydantic Models
class RuntimeAgentCreate(BaseModel):
    """Request model for creating runtime agent instance."""
    orchestrator_agent_id: str
    session_id: str
    status: str = Field(default="pending", description="Agent status: pending, executing, completed, failed")
    metadata: dict[str, Any] | None = None


# Runtime Agents Endpoints

@router.get("/runtime/agents")
async def list_runtime_agents(
    session_id: str | None = Query(None, description="Filter by session_id"),
    status: str | None = Query(None, description="Filter by status"),
    db: DatabaseManager = Depends(get_db_manager)
) -> list[dict[str, Any]]:
    """List all runtime agent instances."""
    agents = await db.list_agents()
    
    # Apply filters
    if session_id:
        agents = [a for a in agents if a.get("session_id") == session_id]
    if status:
        agents = [a for a in agents if a.get("status") == status]
    
    return agents


@router.post("/runtime/agents", status_code=201)
async def create_runtime_agent(
    agent: RuntimeAgentCreate,
    db: DatabaseManager = Depends(get_db_manager)
) -> dict[str, Any]:
    """Create new runtime agent instance."""
    # Verify orchestrator agent exists
    orchestrator = await db.get_orchestrator_agent(agent.orchestrator_agent_id)
    if not orchestrator:
        raise HTTPException(
            status_code=404,
            detail=f"Orchestrator agent {agent.orchestrator_agent_id} not found"
        )
    
    agent_id = await db.create_agent(
        orchestrator_agent_id=agent.orchestrator_agent_id,
        session_id=agent.session_id,
        status=agent.status,
        metadata=agent.metadata
    )
    
    # Return created agent
    created = await db.get_agent(agent_id)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to retrieve created runtime agent")
    
    return created


@router.get("/runtime/agents/{agent_id}")
async def get_runtime_agent(
    agent_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> dict[str, Any]:
    """Get runtime agent by ID."""
    agent = await db.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Runtime agent {agent_id} not found")
    return agent


# Prompts Endpoints

@router.get("/runtime/prompts")
async def list_prompts(
    agent_id: str | None = Query(None, description="Filter by agent_id"),
    db: DatabaseManager = Depends(get_db_manager)
) -> list[dict[str, Any]]:
    """List all prompts."""
    prompts = await db.list_prompts()
    
    # Apply filter
    if agent_id:
        prompts = [p for p in prompts if p.get("agent_id") == agent_id]
    
    return prompts


# Logs Endpoints

@router.get("/runtime/logs")
async def get_recent_logs(
    limit: int = Query(100, ge=1, le=1000, description="Max number of logs to return"),
    level: str | None = Query(None, description="Filter by log level: DEBUG, INFO, WARNING, ERROR"),
    db: DatabaseManager = Depends(get_db_manager)
) -> list[dict[str, Any]]:
    """Get recent logs across all agents."""
    logs = await db.get_recent_logs(limit=limit)
    
    # Apply level filter
    if level:
        logs = [l for l in logs if l.get("log_level") == level.upper()]
    
    return logs


@router.get("/runtime/logs/agent/{agent_id}")
async def get_agent_logs(
    agent_id: str,
    limit: int = Query(100, ge=1, le=1000),
    log_type: str | None = Query(None, description="Filter by log_type"),
    db: DatabaseManager = Depends(get_db_manager)
) -> list[dict[str, Any]]:
    """Get logs for specific runtime agent."""
    # Verify agent exists
    agent = await db.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Runtime agent {agent_id} not found")
    
    if log_type:
        logs = await db.get_agent_logs_by_type(agent_id, log_type, limit=limit)
    else:
        # Get all logs for agent (using recent_logs filtered)
        all_logs = await db.get_recent_logs(limit=1000)
        logs = [l for l in all_logs if l.get("agent_id") == agent_id][:limit]
    
    return logs
