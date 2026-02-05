---
doc_type: feature
adw_id: feature_Tac_14_Task_7
date: 2026-02-04
idk:
  - pydantic
  - sqlite
  - domain-model
  - validation
  - serialization
  - orm
  - database
tags:
  - feature
  - database
  - models
related_code:
  - adws/adw_modules/orch_database_models.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/orch_database_models.py.j2
  - tac_bootstrap_cli/tests/test_orch_database_models.py
  - templates/adws/adw_modules/orch_database_models.py.j2
---

# SQLite Database Models for Orchestrator Persistence

**ADW ID:** feature_Tac_14_Task_7
**Date:** 2026-02-04
**Specification:** specs/issue-628-adw-feature_Tac_14_Task_7-sdlc_planner-sqlite-database-models.md

## Overview

Implemented 5 pure Pydantic domain models that map to SQLite database tables for orchestrator state persistence. These models support TAC-14's migration from PostgreSQL to SQLite by providing SQLite-compatible type mappings (UUID as TEXT, datetime as ISO 8601, JSON as TEXT) with comprehensive field validation. The implementation follows DDD architecture with models existing in both BASE (functional code) and TEMPLATES (Jinja2 templates for project generation).

## What Was Built

- **OrchestratorAgent Model**: Defines orchestrator agent types (e.g., scout, planner, build-agent) with lifecycle status tracking
- **Agent Model**: Tracks runtime instances of orchestrator agents during execution with session management
- **Prompt Model**: Records prompt/response interactions in ADW workflows with token usage and cost tracking
- **AgentLog Model**: Captures detailed agent execution events for debugging and monitoring
- **SystemLog Model**: Records system-wide events across all orchestrator operations
- **Comprehensive Test Suite**: 609 lines of unit tests covering UUID validation, status enums, datetime serialization, metadata JSON, and numeric constraints
- **Dual-Path Implementation**: Models in BASE location (adws/adw_modules/) and TEMPLATES location (templates/adws/adw_modules/)

## Technical Implementation

### Files Modified

- `adws/adw_modules/orch_database_models.py`: 343 lines - 5 Pydantic models with SQLite-compatible field validators and serializers
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/orch_database_models.py.j2`: 343 lines - Jinja2 template version (static, no variables)
- `templates/adws/adw_modules/orch_database_models.py.j2`: 343 lines - Template copy for backward compatibility
- `tac_bootstrap_cli/tests/test_orch_database_models.py`: 609 lines - Comprehensive unit tests for all models
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: 1 line - Template registration

### Key Changes

- **SQLite Type Mappings**: UUID stored as TEXT, datetime serialized to ISO 8601 format, JSON metadata stored as TEXT
- **Field Validators**: Custom `@field_validator` decorators for UUID format validation, status enum enforcement, and JSON serializability
- **Pydantic v2 ConfigDict**: Uses `model_config = ConfigDict(json_encoders={...})` for datetime and dict serialization
- **Numeric Constraints**: Pydantic's `ge=0` constraint for tokens_input, tokens_output, and cost_usd fields in Prompt model
- **Pure Domain Models**: Zero database operations - models only handle data validation and serialization (database CRUD operations reserved for Task 8)
- **DDD Architecture**: Models in domain layer, separate from infrastructure layer (adw_database.py)

## How to Use

### Creating Model Instances

```python
from datetime import datetime
import uuid
from adws.adw_modules.orch_database_models import (
    OrchestratorAgent,
    Agent,
    Prompt,
    AgentLog,
    SystemLog
)

# Create orchestrator agent definition
agent = OrchestratorAgent(
    id=str(uuid.uuid4()),
    name="scout-report-suggest",
    description="Scouts codebase and suggests fixes",
    status="active"
)

# Create runtime agent instance
runtime_agent = Agent(
    id=str(uuid.uuid4()),
    orchestrator_agent_id=agent.id,
    session_id=str(uuid.uuid4()),
    status="running"
)

# Create prompt execution record
prompt = Prompt(
    id=str(uuid.uuid4()),
    agent_id=runtime_agent.id,
    content="Analyze the codebase for potential improvements",
    tokens_input=150,
    tokens_output=500,
    cost_usd=0.02
)

# Create agent log entry
agent_log = AgentLog(
    id=str(uuid.uuid4()),
    agent_id=runtime_agent.id,
    log_type="step_start",
    message="Starting codebase analysis",
    metadata={"step": 1, "phase": "exploration"}
)

# Create system log entry
system_log = SystemLog(
    id=str(uuid.uuid4()),
    log_level="info",
    message="Orchestrator initialized successfully",
    source="orchestrator",
    metadata={"version": "0.8.0"}
)
```

### Serialization to JSON

```python
# Serialize to JSON with ISO 8601 timestamps
json_data = agent.model_dump_json()
# Output: {"id": "550e8400-...", "name": "scout-report-suggest",
#          "created_at": "2026-02-04T10:30:00.000000", ...}

# Parse JSON data
parsed = json.loads(json_data)
assert parsed["created_at"] == "2026-02-04T10:30:00.000000"
```

### Validation Examples

```python
from pydantic import ValidationError

# UUID validation - raises ValidationError for invalid format
try:
    invalid_agent = OrchestratorAgent(
        id="not-a-uuid",
        name="test"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
    # Output: Invalid UUID format: not-a-uuid

# Status enum validation - enforces allowed values
try:
    invalid_status = Agent(
        id=str(uuid.uuid4()),
        orchestrator_agent_id=str(uuid.uuid4()),
        session_id=str(uuid.uuid4()),
        status="invalid_status"
    )
except ValidationError as e:
    print(f"Status error: {e}")
    # Output: Status must be one of {'pending', 'running', 'completed', 'failed'}

# Numeric constraints - tokens and cost must be >= 0
try:
    invalid_tokens = Prompt(
        id=str(uuid.uuid4()),
        agent_id=str(uuid.uuid4()),
        content="Test",
        tokens_input=-100
    )
except ValidationError as e:
    print(f"Token error: {e}")
    # Output: Input should be greater than or equal to 0
```

## Configuration

No configuration required. Models are pure Python classes with no external dependencies beyond Pydantic (already in project dependencies).

### SQLite Type Mappings Reference

```
Python Type      → SQLite Type → Storage Example
-------------------------------------------------
str (UUID)       → TEXT         → "550e8400-e29b-41d4-a716-446655440000"
datetime         → TEXT         → "2026-02-04T10:30:00.000000" (ISO 8601)
dict (JSON)      → TEXT         → '{"key": "value"}'
int              → INTEGER      → 42
float            → REAL         → 3.14159
```

### Allowed Status Values

- **OrchestratorAgent.status**: `active`, `inactive`, `archived`
- **Agent.status**: `pending`, `running`, `completed`, `failed`
- **Prompt.status**: `pending`, `running`, `completed`, `failed`
- **AgentLog.log_type**: `step_start`, `step_end`, `event`, `error`
- **SystemLog.log_level**: `debug`, `info`, `warning`, `error`, `critical`

## Testing

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_orch_database_models.py -v --tb=short
```

This runs 609 lines of tests covering:
- UUID validation for all models (valid/invalid formats, nil UUID, uppercase/lowercase)
- Status enum validation (all allowed values, invalid values, defaults)
- DateTime serialization to ISO 8601 format
- Metadata JSON serialization (nested structures, empty dict vs None)
- Numeric constraints (positive, zero, negative values)
- Model instantiation (minimal required fields, full fields, defaults)

### Integration Test - Model Instantiation

```bash
cd tac_bootstrap_cli && uv run python -c "
import sys
sys.path.insert(0, '../adws/adw_modules')
from orch_database_models import OrchestratorAgent, Agent, Prompt, AgentLog, SystemLog
from datetime import datetime
import uuid

# Test OrchestratorAgent
agent = OrchestratorAgent(
    id=str(uuid.uuid4()),
    name='test-agent',
    description='Test agent',
    status='active'
)
print(f'✓ OrchestratorAgent: {agent.model_dump_json()}')

# Test Agent
runtime_agent = Agent(
    id=str(uuid.uuid4()),
    orchestrator_agent_id=agent.id,
    session_id=str(uuid.uuid4()),
    status='pending'
)
print(f'✓ Agent: {runtime_agent.model_dump_json()}')

# Test Prompt
prompt = Prompt(
    id=str(uuid.uuid4()),
    agent_id=runtime_agent.id,
    content='Test prompt',
    status='pending'
)
print(f'✓ Prompt: {prompt.model_dump_json()}')

# Test AgentLog
agent_log = AgentLog(
    id=str(uuid.uuid4()),
    agent_id=runtime_agent.id,
    log_type='step_start',
    message='Starting step',
    metadata={'step': 1}
)
print(f'✓ AgentLog: {agent_log.model_dump_json()}')

# Test SystemLog
system_log = SystemLog(
    id=str(uuid.uuid4()),
    log_level='info',
    message='System initialized',
    source='orchestrator'
)
print(f'✓ SystemLog: {system_log.model_dump_json()}')

print('✓ All models instantiated successfully')
"
```

### Validation Commands

```bash
# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# CLI smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Architecture Decisions

- **Pure Domain Models**: Models contain ONLY data validation and serialization logic. Database operations (CRUD) are deferred to Task 8 (adw_database.py) following DDD separation of concerns.
- **Dual-Path Implementation**: Models exist in both BASE (adws/adw_modules/) for the generator CLI itself and TEMPLATES (templates/adws/adw_modules/) for generated projects. This follows TAC Bootstrap's architectural constraint.
- **SQLite-First Design**: All type mappings optimized for SQLite's type system (no SERIAL, no UUID type, no native JSON type). This enables zero-configuration deployment.
- **Validation Strategy**: Uses Pydantic's `@field_validator` for custom validation and `Field(..., ge=0)` for numeric constraints. Validation errors use Pydantic's built-in `ValidationError` - no custom exceptions.

### Future Work (NOT in this task)

- **Task 8**: Implement database operations (CRUD) in `adw_database.py` using these models
- **Task 19**: Create SQLite schema initialization script `setup_database.sh` with DDL for all 5 tables
- **v0.9.0+**: Potential enhancement to add Jinja2 variables for custom model extensions in generated projects

### Limitations

- Models use `datetime.utcnow()` for default timestamps (timezone-naive). Consider `datetime.now(timezone.utc)` for timezone-aware timestamps in future versions.
- Metadata JSON validation only checks serializability, not structure. Consider JSON schema validation for stricter metadata constraints.
- No foreign key constraint validation at model level - this is handled by SQLite schema (Task 19).

### Dependencies

- **Pydantic**: Already in project dependencies (pyproject.toml)
- **Python stdlib**: uuid, datetime, json - no additional dependencies required
