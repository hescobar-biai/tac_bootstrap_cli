"""
SQLite Database Models for Orchestrator Persistence (TAC-14 v2)

This module defines 5 pure Pydantic models that map to the SQLite database schema
for orchestrator state persistence. These are domain models with NO database operations.

SQLite Type Mappings:
--------------------
Python Type      → SQLite Type → Storage Example
-------------------------------------------------
str (UUID)       → TEXT         → "550e8400-e29b-41d4-a716-446655440000"
datetime         → TEXT         → "2026-02-04T10:30:00.000000" (ISO 8601)
dict (JSON)      → TEXT         → '{"key": "value"}'
int              → INTEGER      → 42
float            → REAL         → 3.14159

Architecture:
-------------
- Pure data models (Domain layer in DDD)
- Validation via Pydantic field_validator
- Serialization via model_config json_encoders
- NO database operations (see adw_database.py for CRUD - Task 8)

Usage Example:
--------------
```python
from datetime import datetime
import uuid
from orch_database_models import OrchestratorAgent, Agent, Prompt

# Create orchestrator agent
agent = OrchestratorAgent(
    id=str(uuid.uuid4()),
    name="scout-report-suggest",
    description="Scouts codebase and suggests fixes",
    status="active"
)

# Serialize to JSON with ISO 8601 timestamps
json_data = agent.model_dump_json()
# {"id": "550e8400-...", "created_at": "2026-02-04T10:30:00.000000", ...}

# Create runtime agent instance
runtime_agent = Agent(
    id=str(uuid.uuid4()),
    orchestrator_agent_id=agent.id,
    session_id=str(uuid.uuid4()),
    status="running"
)
```

Schema Reference:
-----------------
See: ai_docs/doc/plan_tasks_Tac_14_v2_SQLITE.md
Tables: orchestrator_agents, agents, prompts, agent_logs, system_logs
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import uuid as uuid_lib
import json


class OrchestratorAgent(BaseModel):
    """
    Orchestrator Agent Definition Model.

    Maps to: orchestrator_agents table (SQLite)
    Purpose: Defines available agent types in the orchestrator (e.g., scout, planner, build-agent)

    Fields:
        id: UUID stored as TEXT in SQLite
        name: Unique agent type name (e.g., "scout-report-suggest")
        description: Human-readable description of agent capabilities
        status: Lifecycle status - 'active', 'inactive', or 'archived'
        created_at: ISO 8601 timestamp of creation
        updated_at: ISO 8601 timestamp of last update
    """

    id: str = Field(..., description="UUID as string (stored as TEXT in SQLite)")
    name: str = Field(..., description="Unique agent type name")
    description: Optional[str] = Field(None, description="Agent capabilities description")
    status: str = Field(default="active", description="Status: active, inactive, archived")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @field_validator('id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format (stored as TEXT in SQLite)."""
        try:
            uuid_lib.UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is one of allowed values."""
        allowed = {'active', 'inactive', 'archived'}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}, got: {v}")
        return v

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class Agent(BaseModel):
    """
    Runtime Agent Instance Model.

    Maps to: agents table (SQLite)
    Purpose: Tracks runtime instances of orchestrator agents during execution

    Fields:
        id: UUID stored as TEXT
        orchestrator_agent_id: Foreign key to orchestrator_agents.id
        session_id: UUID identifying the execution session
        status: Execution status - 'pending', 'running', 'completed', 'failed'
        created_at: ISO 8601 timestamp when instance was created
        started_at: ISO 8601 timestamp when execution started (optional)
        completed_at: ISO 8601 timestamp when execution finished (optional)
    """

    id: str = Field(..., description="UUID as string")
    orchestrator_agent_id: str = Field(..., description="Foreign key to orchestrator_agents.id")
    session_id: str = Field(..., description="Session UUID")
    status: str = Field(default="pending", description="Status: pending, running, completed, failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Instance creation time")
    started_at: Optional[datetime] = Field(None, description="Execution start time")
    completed_at: Optional[datetime] = Field(None, description="Execution completion time")

    @field_validator('id', 'orchestrator_agent_id', 'session_id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format for all UUID fields."""
        try:
            uuid_lib.UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is one of allowed values."""
        allowed = {'pending', 'running', 'completed', 'failed'}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}, got: {v}")
        return v

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class Prompt(BaseModel):
    """
    ADW Execution Record Model.

    Maps to: prompts table (SQLite)
    Purpose: Records each prompt/response interaction in ADW workflows

    Fields:
        id: UUID stored as TEXT
        agent_id: Foreign key to agents.id
        content: The prompt content sent to the agent
        response: The agent's response (optional until completed)
        status: Execution status - 'pending', 'running', 'completed', 'failed'
        tokens_input: Number of input tokens consumed
        tokens_output: Number of output tokens generated
        cost_usd: Cost in USD for this prompt execution
        created_at: ISO 8601 timestamp when prompt was created
        completed_at: ISO 8601 timestamp when execution finished (optional)
    """

    id: str = Field(..., description="UUID as string")
    agent_id: str = Field(..., description="Foreign key to agents.id")
    content: str = Field(..., description="Prompt content")
    response: Optional[str] = Field(None, description="Agent response")
    status: str = Field(default="pending", description="Status: pending, running, completed, failed")
    tokens_input: int = Field(default=0, description="Input token count", ge=0)
    tokens_output: int = Field(default=0, description="Output token count", ge=0)
    cost_usd: float = Field(default=0.0, description="Cost in USD", ge=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Prompt creation time")
    completed_at: Optional[datetime] = Field(None, description="Execution completion time")

    @field_validator('id', 'agent_id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format for UUID fields."""
        try:
            uuid_lib.UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is one of allowed values."""
        allowed = {'pending', 'running', 'completed', 'failed'}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}, got: {v}")
        return v

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class AgentLog(BaseModel):
    """
    Agent Event Logging Model.

    Maps to: agent_logs table (SQLite)
    Purpose: Records detailed events during agent execution for debugging and monitoring

    Fields:
        id: UUID stored as TEXT
        agent_id: Foreign key to agents.id
        log_type: Event type - 'step_start', 'step_end', 'event', 'error'
        message: Log message text
        metadata: Optional JSON metadata (stored as TEXT in SQLite)
        created_at: ISO 8601 timestamp of log entry
    """

    id: str = Field(..., description="UUID as string")
    agent_id: str = Field(..., description="Foreign key to agents.id")
    log_type: str = Field(..., description="Log type: step_start, step_end, event, error")
    message: str = Field(..., description="Log message")
    metadata: Optional[dict] = Field(None, description="JSON metadata (stored as TEXT)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Log timestamp")

    @field_validator('id', 'agent_id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format for UUID fields."""
        try:
            uuid_lib.UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @field_validator('log_type')
    @classmethod
    def validate_log_type(cls, v: str) -> str:
        """Validate log_type is one of allowed values."""
        allowed = {'step_start', 'step_end', 'event', 'error'}
        if v not in allowed:
            raise ValueError(f"Log type must be one of {allowed}, got: {v}")
        return v

    @field_validator('metadata')
    @classmethod
    def validate_metadata_json(cls, v: Optional[dict]) -> Optional[dict]:
        """Validate metadata is JSON-serializable (will be stored as TEXT in SQLite)."""
        if v is None:
            return v
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError) as e:
            raise ValueError(f"Metadata must be JSON-serializable: {e}")

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            dict: lambda v: json.dumps(v) if v else None,
        }
    )


class SystemLog(BaseModel):
    """
    System-Wide Logging Model.

    Maps to: system_logs table (SQLite)
    Purpose: Records system-level events across all orchestrator operations

    Fields:
        id: UUID stored as TEXT
        log_level: Log severity - 'debug', 'info', 'warning', 'error', 'critical'
        message: Log message text
        source: Optional source identifier (e.g., 'orchestrator', 'database')
        metadata: Optional JSON metadata (stored as TEXT in SQLite)
        created_at: ISO 8601 timestamp of log entry
    """

    id: str = Field(..., description="UUID as string")
    log_level: str = Field(..., description="Log level: debug, info, warning, error, critical")
    message: str = Field(..., description="Log message")
    source: Optional[str] = Field(None, description="Log source identifier")
    metadata: Optional[dict] = Field(None, description="JSON metadata (stored as TEXT)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Log timestamp")

    @field_validator('id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            uuid_lib.UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log_level is one of allowed values."""
        allowed = {'debug', 'info', 'warning', 'error', 'critical'}
        if v not in allowed:
            raise ValueError(f"Log level must be one of {allowed}, got: {v}")
        return v

    @field_validator('metadata')
    @classmethod
    def validate_metadata_json(cls, v: Optional[dict]) -> Optional[dict]:
        """Validate metadata is JSON-serializable (will be stored as TEXT in SQLite)."""
        if v is None:
            return v
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError) as e:
            raise ValueError(f"Metadata must be JSON-serializable: {e}")

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            dict: lambda v: json.dumps(v) if v else None,
        }
    )
