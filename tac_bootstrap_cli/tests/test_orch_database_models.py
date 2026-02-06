"""
Unit tests for SQLite Database Models (TAC-14 Task 7)

Tests all 5 Pydantic models for:
- UUID validation
- Status enum validation
- DateTime serialization to ISO 8601
- Metadata JSON serialization
- Numeric field constraints
- Model instantiation and defaults
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

# Add adws/adw_modules to path to import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "adws" / "adw_modules"))

from orch_database_models import (
    Agent,
    AgentLog,
    OrchestratorAgent,
    Prompt,
    SystemLog,
)

# =============================================================================
# UUID VALIDATION TESTS
# =============================================================================


class TestUUIDValidation:
    """Test UUID format validation across all models."""

    def test_orchestrator_agent_valid_uuid(self):
        """Test OrchestratorAgent accepts valid UUID."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test-agent",
        )
        assert agent.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_orchestrator_agent_invalid_uuid(self):
        """Test OrchestratorAgent rejects invalid UUID."""
        with pytest.raises(ValidationError) as exc_info:
            OrchestratorAgent(
                id="not-a-uuid",
                name="test-agent",
            )
        assert "Invalid UUID format" in str(exc_info.value)

    def test_agent_valid_uuids(self):
        """Test Agent accepts valid UUIDs for all UUID fields."""
        agent = Agent(
            id="550e8400-e29b-41d4-a716-446655440001",
            orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
            session_id="550e8400-e29b-41d4-a716-446655440003",
        )
        assert agent.id == "550e8400-e29b-41d4-a716-446655440001"
        assert agent.orchestrator_agent_id == "550e8400-e29b-41d4-a716-446655440002"
        assert agent.session_id == "550e8400-e29b-41d4-a716-446655440003"

    def test_agent_invalid_uuid_id(self):
        """Test Agent rejects invalid UUID for id field."""
        with pytest.raises(ValidationError) as exc_info:
            Agent(
                id="invalid",
                orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
                session_id="550e8400-e29b-41d4-a716-446655440003",
            )
        assert "Invalid UUID format" in str(exc_info.value)

    def test_prompt_valid_uuids(self):
        """Test Prompt accepts valid UUIDs."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test prompt",
        )
        assert prompt.id == "550e8400-e29b-41d4-a716-446655440004"
        assert prompt.agent_id == "550e8400-e29b-41d4-a716-446655440005"

    def test_agent_log_valid_uuids(self):
        """Test AgentLog accepts valid UUIDs."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test log",
        )
        assert log.id == "550e8400-e29b-41d4-a716-446655440006"
        assert log.agent_id == "550e8400-e29b-41d4-a716-446655440007"

    def test_system_log_valid_uuid(self):
        """Test SystemLog accepts valid UUID."""
        log = SystemLog(
            id="550e8400-e29b-41d4-a716-446655440008",
            log_level="info",
            message="Test system log",
        )
        assert log.id == "550e8400-e29b-41d4-a716-446655440008"

    def test_empty_string_uuid(self):
        """Test empty string is rejected as UUID."""
        with pytest.raises(ValidationError) as exc_info:
            OrchestratorAgent(id="", name="test")
        assert "Invalid UUID format" in str(exc_info.value)

    def test_nil_uuid(self):
        """Test nil UUID (all zeros) is accepted."""
        agent = OrchestratorAgent(
            id="00000000-0000-0000-0000-000000000000",
            name="test-agent",
        )
        assert agent.id == "00000000-0000-0000-0000-000000000000"

    def test_uppercase_uuid(self):
        """Test uppercase UUID is accepted."""
        agent = OrchestratorAgent(
            id="550E8400-E29B-41D4-A716-446655440000",
            name="test-agent",
        )
        assert agent.id == "550E8400-E29B-41D4-A716-446655440000"


# =============================================================================
# STATUS ENUM VALIDATION TESTS
# =============================================================================


class TestStatusValidation:
    """Test status field enum validation."""

    def test_orchestrator_agent_valid_statuses(self):
        """Test OrchestratorAgent accepts all valid status values."""
        for status in ["active", "inactive", "archived"]:
            agent = OrchestratorAgent(
                id="550e8400-e29b-41d4-a716-446655440000",
                name=f"test-{status}",
                status=status,
            )
            assert agent.status == status

    def test_orchestrator_agent_invalid_status(self):
        """Test OrchestratorAgent rejects invalid status."""
        with pytest.raises(ValidationError) as exc_info:
            OrchestratorAgent(
                id="550e8400-e29b-41d4-a716-446655440000",
                name="test",
                status="invalid",
            )
        assert "Status must be one of" in str(exc_info.value)

    def test_orchestrator_agent_default_status(self):
        """Test OrchestratorAgent defaults to 'active' status."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test",
        )
        assert agent.status == "active"

    def test_agent_valid_statuses(self):
        """Test Agent accepts all valid status values."""
        for status in ["pending", "running", "completed", "failed"]:
            agent = Agent(
                id="550e8400-e29b-41d4-a716-446655440001",
                orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
                session_id="550e8400-e29b-41d4-a716-446655440003",
                status=status,
            )
            assert agent.status == status

    def test_agent_default_status(self):
        """Test Agent defaults to 'pending' status."""
        agent = Agent(
            id="550e8400-e29b-41d4-a716-446655440001",
            orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
            session_id="550e8400-e29b-41d4-a716-446655440003",
        )
        assert agent.status == "pending"

    def test_prompt_valid_statuses(self):
        """Test Prompt accepts all valid status values."""
        for status in ["pending", "running", "completed", "failed"]:
            prompt = Prompt(
                id="550e8400-e29b-41d4-a716-446655440004",
                agent_id="550e8400-e29b-41d4-a716-446655440005",
                content="Test",
                status=status,
            )
            assert prompt.status == status

    def test_agent_log_valid_log_types(self):
        """Test AgentLog accepts all valid log_type values."""
        for log_type in ["step_start", "step_end", "event", "error"]:
            log = AgentLog(
                id="550e8400-e29b-41d4-a716-446655440006",
                agent_id="550e8400-e29b-41d4-a716-446655440007",
                log_type=log_type,
                message="Test",
            )
            assert log.log_type == log_type

    def test_agent_log_invalid_log_type(self):
        """Test AgentLog rejects invalid log_type."""
        with pytest.raises(ValidationError) as exc_info:
            AgentLog(
                id="550e8400-e29b-41d4-a716-446655440006",
                agent_id="550e8400-e29b-41d4-a716-446655440007",
                log_type="invalid",
                message="Test",
            )
        assert "Log type must be one of" in str(exc_info.value)

    def test_system_log_valid_log_levels(self):
        """Test SystemLog accepts all valid log_level values."""
        for log_level in ["debug", "info", "warning", "error", "critical"]:
            log = SystemLog(
                id="550e8400-e29b-41d4-a716-446655440008",
                log_level=log_level,
                message="Test",
            )
            assert log.log_level == log_level

    def test_system_log_invalid_log_level(self):
        """Test SystemLog rejects invalid log_level."""
        with pytest.raises(ValidationError) as exc_info:
            SystemLog(
                id="550e8400-e29b-41d4-a716-446655440008",
                log_level="invalid",
                message="Test",
            )
        assert "Log level must be one of" in str(exc_info.value)


# =============================================================================
# DATETIME SERIALIZATION TESTS
# =============================================================================


class TestDateTimeSerialization:
    """Test datetime fields serialize to ISO 8601 format."""

    def test_orchestrator_agent_datetime_serialization(self):
        """Test OrchestratorAgent datetime fields serialize to ISO 8601."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test",
            created_at=datetime(2026, 2, 4, 10, 30, 0),
            updated_at=datetime(2026, 2, 4, 11, 30, 0),
        )
        json_data = agent.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["created_at"] == "2026-02-04T10:30:00"
        assert parsed["updated_at"] == "2026-02-04T11:30:00"

    def test_agent_datetime_serialization(self):
        """Test Agent datetime fields serialize to ISO 8601."""
        agent = Agent(
            id="550e8400-e29b-41d4-a716-446655440001",
            orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
            session_id="550e8400-e29b-41d4-a716-446655440003",
            created_at=datetime(2026, 2, 4, 10, 30, 0),
            started_at=datetime(2026, 2, 4, 10, 35, 0),
            completed_at=datetime(2026, 2, 4, 10, 45, 0),
        )
        json_data = agent.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["created_at"] == "2026-02-04T10:30:00"
        assert parsed["started_at"] == "2026-02-04T10:35:00"
        assert parsed["completed_at"] == "2026-02-04T10:45:00"

    def test_prompt_datetime_serialization(self):
        """Test Prompt datetime fields serialize to ISO 8601."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            created_at=datetime(2026, 2, 4, 10, 30, 0),
            completed_at=datetime(2026, 2, 4, 10, 35, 0),
        )
        json_data = prompt.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["created_at"] == "2026-02-04T10:30:00"
        assert parsed["completed_at"] == "2026-02-04T10:35:00"

    def test_agent_log_datetime_serialization(self):
        """Test AgentLog datetime serialization."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            created_at=datetime(2026, 2, 4, 10, 30, 0),
        )
        json_data = log.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["created_at"] == "2026-02-04T10:30:00"

    def test_system_log_datetime_serialization(self):
        """Test SystemLog datetime serialization."""
        log = SystemLog(
            id="550e8400-e29b-41d4-a716-446655440008",
            log_level="info",
            message="Test",
            created_at=datetime(2026, 2, 4, 10, 30, 0),
        )
        json_data = log.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["created_at"] == "2026-02-04T10:30:00"

    def test_default_datetime_generation(self):
        """Test default datetime fields are generated."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test",
        )
        assert isinstance(agent.created_at, datetime)
        assert isinstance(agent.updated_at, datetime)


# =============================================================================
# METADATA JSON TESTS
# =============================================================================


class TestMetadataJSON:
    """Test metadata fields accept valid dicts and serialize to JSON."""

    def test_agent_log_metadata_valid_dict(self):
        """Test AgentLog accepts valid metadata dict."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            metadata={"step": 1, "action": "start"},
        )
        assert log.metadata == {"step": 1, "action": "start"}

    def test_agent_log_metadata_none(self):
        """Test AgentLog accepts None metadata."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            metadata=None,
        )
        assert log.metadata is None

    def test_agent_log_metadata_serialization(self):
        """Test AgentLog metadata serializes to JSON."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            metadata={"step": 1, "action": "start"},
        )
        json_data = log.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["metadata"] == '{"step": 1, "action": "start"}'

    def test_system_log_metadata_valid_dict(self):
        """Test SystemLog accepts valid metadata dict."""
        log = SystemLog(
            id="550e8400-e29b-41d4-a716-446655440008",
            log_level="info",
            message="Test",
            metadata={"source": "orchestrator", "version": "0.9.2"},
        )
        assert log.metadata == {"source": "orchestrator", "version": "0.9.2"}

    def test_system_log_metadata_serialization(self):
        """Test SystemLog metadata serializes to JSON."""
        log = SystemLog(
            id="550e8400-e29b-41d4-a716-446655440008",
            log_level="info",
            message="Test",
            metadata={"source": "orchestrator"},
        )
        json_data = log.model_dump_json()
        parsed = json.loads(json_data)
        assert parsed["metadata"] == '{"source": "orchestrator"}'

    def test_metadata_nested_structures(self):
        """Test metadata with nested JSON structures."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            metadata={
                "step": 1,
                "details": {"action": "start", "params": {"force": True}},
            },
        )
        assert log.metadata["details"]["params"]["force"] is True

    def test_metadata_empty_dict(self):
        """Test metadata with empty dict vs None."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test",
            metadata={},
        )
        assert log.metadata == {}


# =============================================================================
# NUMERIC VALIDATION TESTS
# =============================================================================


class TestNumericValidation:
    """Test numeric field constraints for Prompt model."""

    def test_prompt_tokens_input_positive(self):
        """Test Prompt accepts positive tokens_input."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            tokens_input=1000,
        )
        assert prompt.tokens_input == 1000

    def test_prompt_tokens_input_zero(self):
        """Test Prompt accepts zero tokens_input."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            tokens_input=0,
        )
        assert prompt.tokens_input == 0

    def test_prompt_tokens_input_negative(self):
        """Test Prompt rejects negative tokens_input."""
        with pytest.raises(ValidationError) as exc_info:
            Prompt(
                id="550e8400-e29b-41d4-a716-446655440004",
                agent_id="550e8400-e29b-41d4-a716-446655440005",
                content="Test",
                tokens_input=-100,
            )
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_prompt_tokens_output_positive(self):
        """Test Prompt accepts positive tokens_output."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            tokens_output=2000,
        )
        assert prompt.tokens_output == 2000

    def test_prompt_tokens_output_negative(self):
        """Test Prompt rejects negative tokens_output."""
        with pytest.raises(ValidationError) as exc_info:
            Prompt(
                id="550e8400-e29b-41d4-a716-446655440004",
                agent_id="550e8400-e29b-41d4-a716-446655440005",
                content="Test",
                tokens_output=-200,
            )
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_prompt_cost_usd_positive(self):
        """Test Prompt accepts positive cost_usd."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            cost_usd=0.05,
        )
        assert prompt.cost_usd == 0.05

    def test_prompt_cost_usd_zero(self):
        """Test Prompt accepts zero cost_usd."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
            cost_usd=0.0,
        )
        assert prompt.cost_usd == 0.0

    def test_prompt_cost_usd_negative(self):
        """Test Prompt rejects negative cost_usd."""
        with pytest.raises(ValidationError) as exc_info:
            Prompt(
                id="550e8400-e29b-41d4-a716-446655440004",
                agent_id="550e8400-e29b-41d4-a716-446655440005",
                content="Test",
                cost_usd=-1.0,
            )
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_prompt_default_numeric_values(self):
        """Test Prompt numeric fields default to zero."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test",
        )
        assert prompt.tokens_input == 0
        assert prompt.tokens_output == 0
        assert prompt.cost_usd == 0.0


# =============================================================================
# MODEL INSTANTIATION TESTS
# =============================================================================


class TestModelInstantiation:
    """Test model instantiation with required and optional fields."""

    def test_orchestrator_agent_minimal_instantiation(self):
        """Test OrchestratorAgent with minimal required fields."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test-agent",
        )
        assert agent.id == "550e8400-e29b-41d4-a716-446655440000"
        assert agent.name == "test-agent"
        assert agent.description is None
        assert agent.status == "active"

    def test_orchestrator_agent_full_instantiation(self):
        """Test OrchestratorAgent with all fields."""
        agent = OrchestratorAgent(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="test-agent",
            description="Test description",
            status="inactive",
            created_at=datetime(2026, 2, 4, 10, 0, 0),
            updated_at=datetime(2026, 2, 4, 11, 0, 0),
        )
        assert agent.description == "Test description"
        assert agent.status == "inactive"

    def test_agent_minimal_instantiation(self):
        """Test Agent with minimal required fields."""
        agent = Agent(
            id="550e8400-e29b-41d4-a716-446655440001",
            orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
            session_id="550e8400-e29b-41d4-a716-446655440003",
        )
        assert agent.status == "pending"
        assert agent.started_at is None
        assert agent.completed_at is None

    def test_agent_full_instantiation(self):
        """Test Agent with all fields."""
        agent = Agent(
            id="550e8400-e29b-41d4-a716-446655440001",
            orchestrator_agent_id="550e8400-e29b-41d4-a716-446655440002",
            session_id="550e8400-e29b-41d4-a716-446655440003",
            status="completed",
            started_at=datetime(2026, 2, 4, 10, 0, 0),
            completed_at=datetime(2026, 2, 4, 10, 30, 0),
        )
        assert agent.status == "completed"
        assert agent.started_at is not None
        assert agent.completed_at is not None

    def test_prompt_minimal_instantiation(self):
        """Test Prompt with minimal required fields."""
        prompt = Prompt(
            id="550e8400-e29b-41d4-a716-446655440004",
            agent_id="550e8400-e29b-41d4-a716-446655440005",
            content="Test prompt content",
        )
        assert prompt.content == "Test prompt content"
        assert prompt.response is None
        assert prompt.status == "pending"

    def test_agent_log_minimal_instantiation(self):
        """Test AgentLog with minimal required fields."""
        log = AgentLog(
            id="550e8400-e29b-41d4-a716-446655440006",
            agent_id="550e8400-e29b-41d4-a716-446655440007",
            log_type="event",
            message="Test message",
        )
        assert log.message == "Test message"
        assert log.metadata is None

    def test_system_log_minimal_instantiation(self):
        """Test SystemLog with minimal required fields."""
        log = SystemLog(
            id="550e8400-e29b-41d4-a716-446655440008",
            log_level="info",
            message="System initialized",
        )
        assert log.message == "System initialized"
        assert log.source is None
        assert log.metadata is None
