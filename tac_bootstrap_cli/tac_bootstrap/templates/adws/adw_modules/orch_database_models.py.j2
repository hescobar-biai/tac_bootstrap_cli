"""
Pydantic Database Models for Multi-Agent Orchestration

These models map directly to the SQLite tables defined in schema_orchestrator.sql.
They provide:
- Automatic UUID handling (converts asyncpg UUID objects to Python UUID)
- Type safety and validation
- Automatic JSON serialization/deserialization
- Field validation and defaults

Usage:
    from orch_database_models import Agent, OrchestratorAgent, Prompt, AgentLog, SystemLog

    # Automatically handles UUID conversion from database
    agent = Agent(**row_dict)
    print(agent.id)  # Works with both UUID objects and strings
"""

import json
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, conint, confloat


# ═══════════════════════════════════════════════════════════
# ORCHESTRATOR_AGENT MODEL
# ═══════════════════════════════════════════════════════════


class OrchestratorAgent(BaseModel):
    """
    Singleton orchestrator agent that manages other agents.

    Maps to: orchestrator_agents table
    """

    id: Union[str, UUID]
    name: str
    description: Optional[str] = None
    agent_type: Optional[str] = None
    capabilities: Optional[str] = None
    default_model: Optional[str] = None
    status: Literal["active", "inactive", "archived"] = "active"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator("id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> str:
        """Validate UUID format and return as string"""
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status enum"""
        valid = ["active", "inactive", "archived"]
        if v not in valid:
            raise ValueError(f"Status must be one of {valid}")
        return v

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601"""
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# AGENT MODEL
# ═══════════════════════════════════════════════════════════


class Agent(BaseModel):
    """
    Agent registry and configuration for managed agents.

    Maps to: agents table
    """

    id: Union[str, UUID]
    orchestrator_agent_id: Union[str, UUID]
    name: Optional[str] = None
    model: Optional[str] = None
    session_id: Optional[Union[str, UUID]] = None
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @field_validator("id", "orchestrator_agent_id", "session_id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> Optional[str]:
        """Validate UUID format and return as string"""
        if v is None:
            return None
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status enum"""
        valid = ["pending", "running", "completed", "failed"]
        if v not in valid:
            raise ValueError(f"Status must be one of {valid}")
        return v

    @field_serializer("created_at", "started_at", "completed_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO 8601"""
        if value is None:
            return None
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# PROMPT MODEL
# ═══════════════════════════════════════════════════════════


class Prompt(BaseModel):
    """
    Prompts sent to agents from engineers or orchestrator.

    Maps to: prompts table
    """

    id: Union[str, UUID]
    agent_id: Optional[Union[str, UUID]] = None
    content: Optional[str] = None
    response: Optional[str] = None
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    tokens_input: int = Field(default=0, ge=0)
    tokens_output: int = Field(default=0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0.0)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @field_validator("id", "agent_id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> Optional[str]:
        """Validate UUID format and return as string"""
        if v is None:
            return None
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status enum"""
        valid = ["pending", "running", "completed", "failed"]
        if v not in valid:
            raise ValueError(f"Status must be one of {valid}")
        return v

    @field_serializer("created_at", "completed_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO 8601"""
        if value is None:
            return None
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# AGENT_LOG MODEL
# ═══════════════════════════════════════════════════════════


class AgentLog(BaseModel):
    """
    Unified event log for hooks and agent responses during task execution.

    Maps to: agent_logs table
    """

    id: Union[str, UUID]
    agent_id: Union[str, UUID]
    log_type: Literal["step_start", "step_end", "event", "error"]
    message: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("id", "agent_id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> str:
        """Validate UUID format and return as string"""
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("log_type", mode="before")
    @classmethod
    def validate_log_type(cls, v: str) -> str:
        """Validate log_type enum"""
        valid = ["step_start", "step_end", "event", "error"]
        if v not in valid:
            raise ValueError(f"Log type must be one of {valid}")
        return v

    @field_validator("metadata", mode="before")
    @classmethod
    def parse_metadata(cls, v: Any) -> Optional[Dict[str, Any]]:
        """Parse JSON string metadata to dict"""
        if v is None:
            return None
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_serializer("metadata")
    def serialize_metadata(self, value: Optional[Dict[str, Any]]) -> Optional[str]:
        """Serialize metadata dict to JSON string"""
        if value is None:
            return None
        return json.dumps(value)

    @field_serializer("created_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601"""
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# SYSTEM_LOG MODEL
# ═══════════════════════════════════════════════════════════


class SystemLog(BaseModel):
    """
    Application-level system logs (global application events only).

    For agent-related logs, use agent_logs table instead.

    Maps to: system_logs table
    """

    id: Union[str, UUID]
    log_level: Literal["debug", "info", "warning", "error", "critical"]
    message: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> Optional[str]:
        """Validate UUID format and return as string"""
        if v is None:
            return None
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log_level enum"""
        valid = ["debug", "info", "warning", "error", "critical"]
        if v not in valid:
            raise ValueError(f"Log level must be one of {valid}")
        return v

    @field_validator("metadata", mode="before")
    @classmethod
    def parse_metadata(cls, v: Any) -> Optional[Dict[str, Any]]:
        """Parse JSON string metadata to dict"""
        if v is None:
            return None
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_serializer("metadata")
    def serialize_metadata(self, value: Optional[Dict[str, Any]]) -> Optional[str]:
        """Serialize metadata dict to JSON string"""
        if value is None:
            return None
        return json.dumps(value)

    @field_serializer("created_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601"""
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# ORCHESTRATOR_CHAT MODEL
# ═══════════════════════════════════════════════════════════


class OrchestratorChat(BaseModel):
    """
    Append-only conversation log capturing 3-way communication: user ↔ orchestrator ↔ agents.

    Maps to: orchestrator_chat table
    """

    id: Union[str, UUID]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    orchestrator_agent_id: Union[str, UUID]
    sender_type: Literal["user", "orchestrator", "agent"]
    receiver_type: Literal["user", "orchestrator", "agent"]
    message: str
    summary: Optional[str] = None
    agent_id: Optional[Union[str, UUID]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("id", "orchestrator_agent_id", "agent_id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> Optional[str]:
        """Validate UUID format and return as string"""
        if v is None:
            return None
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("metadata", mode="before")
    @classmethod
    def parse_metadata(cls, v: Any) -> Dict[str, Any]:
        """Parse JSON string metadata to dict"""
        if isinstance(v, str):
            return json.loads(v)
        return v or {}

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO 8601"""
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# AI_DEVELOPER_WORKFLOW MODEL
# ═══════════════════════════════════════════════════════════


class AiDeveloperWorkflow(BaseModel):
    """
    Tracks AI Developer Workflow executions in the system.

    Maps to: ai_developer_workflows table
    """

    id: Union[str, UUID]
    orchestrator_agent_id: Optional[Union[str, UUID]] = None
    adw_name: str
    workflow_type: str
    description: Optional[str] = None
    status: Literal["pending", "in_progress", "completed", "failed", "cancelled"] = (
        "pending"
    )
    current_step: Optional[str] = None
    total_steps: int = 0
    completed_steps: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    error_step: Optional[str] = None
    error_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator("id", "orchestrator_agent_id", mode="before")
    @classmethod
    def validate_uuid_format(cls, v: Any) -> Optional[str]:
        """Validate UUID format and return as string"""
        if v is None:
            return None
        if isinstance(v, UUID):
            return str(v)
        uuid_str = str(v)
        try:
            UUID(uuid_str)  # Validate it's a valid UUID
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID format")
        return uuid_str

    @field_validator("input_data", "output_data", "metadata", mode="before")
    @classmethod
    def parse_jsonb(cls, v: Any) -> Dict[str, Any]:
        """Parse JSON string to dict"""
        if isinstance(v, str):
            return json.loads(v)
        return v or {}

    @field_serializer("created_at", "updated_at", "started_at", "completed_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO 8601"""
        if value is None:
            return None
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════
# EXPORT PUBLIC API
# ═══════════════════════════════════════════════════════════

__all__ = [
    "OrchestratorAgent",
    "Agent",
    "Prompt",
    "AgentLog",
    "SystemLog",
    "OrchestratorChat",
    "AiDeveloperWorkflow",
]
