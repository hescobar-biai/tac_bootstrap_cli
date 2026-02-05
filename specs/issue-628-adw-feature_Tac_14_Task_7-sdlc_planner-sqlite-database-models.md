# Feature: Implementar Database Models para SQLite (BASE + TEMPLATES)

## Metadata
issue_number: `628`
adw_id: `feature_Tac_14_Task_7`
issue_json: `{"number": 628, "title": "Implementar Database Models para SQLite (BASE + TEMPLATES)", "body": "file: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md \n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_7`\n\n**Cambios**:\n```diff\n+ field_validator para UUID como string, Decimal como float\n+ json_encoders para SQLite types\n```\n\n**Ejemplo de modelo adaptado**:\n```python\nfrom pydantic import BaseModel, Field, field_validator\nfrom typing import Optional\nfrom datetime import datetime\nimport json\n\nclass OrchestratorAgent(BaseModel):\n    \"\"\"Orchestrator Agent model for SQLite.\"\"\"\n    id: str = Field(..., description=\"UUID as string\")\n    name: str\n    description: Optional[str] = None\n    status: str = \"active\"\n    created_at: datetime = Field(default_factory=datetime.utcnow)\n    updated_at: datetime = Field(default_factory=datetime.utcnow)\n\n    @field_validator('id')\n    def validate_uuid(cls, v):\n        \"\"\"Validate UUID format (stored as TEXT in SQLite).\"\"\"\n        import uuid\n        try:\n            uuid.UUID(v)\n            return v\n        except ValueError:\n            raise ValueError(\"Invalid UUID format\")\n\n    class Config:\n        json_encoders = {\n            datetime: lambda v: v.isoformat(),\n        }"}`

## Feature Description

Implement 5 pure Pydantic models for SQLite database operations as part of TAC-14's transition to SQLite-first approach. These models will be created in DUAL locations following TAC Bootstrap's architectural constraint: BASE (functional code for the generator CLI itself) and TEMPLATES (Jinja2 templates for generated projects).

The models represent the 5-table schema for orchestrator persistence: `OrchestratorAgent`, `Agent`, `Prompt`, `AgentLog`, and `SystemLog`. They use SQLite-compatible types (UUID as TEXT, datetime as ISO 8601, JSON as TEXT) and include field validators for type safety while maintaining complete separation from database operations (which belong to Task 8).

## User Story

As a TAC Bootstrap developer
I want to implement pure Pydantic domain models that map to SQLite tables
So that both the generator CLI and generated projects can persist orchestrator state with zero-configuration SQLite backend while maintaining type safety and validation

## Problem Statement

TAC-14 requires migrating from PostgreSQL to SQLite for v0.8.0 to eliminate setup barriers. The current plan (Task 7) needs 5 Pydantic models that:

1. Map to SQLite's 5-table schema (orchestrator_agents, agents, prompts, agent_logs, system_logs)
2. Use SQLite-compatible types (TEXT for UUIDs, TEXT for ISO 8601 timestamps, TEXT for JSON)
3. Include field validators for UUID format, datetime handling, and status enums
4. Maintain DDD separation: pure data models with NO database operations
5. Exist in TWO locations: BASE (adws/adw_modules/) and TEMPLATES (templates/adws/adw_modules/)

Without these models, Task 8 (database operations) cannot proceed, and the orchestrator cannot persist state.

## Solution Statement

Create 5 Pydantic models in `adws/adw_modules/orch_database_models.py` (BASE) and `templates/adws/adw_modules/orch_database_models.py.j2` (TEMPLATES):

1. **OrchestratorAgent**: Definition of orchestrator agent types (id, name, description, status, timestamps)
2. **Agent**: Runtime agent instances (id, orchestrator_agent_id, session_id, status, timestamps)
3. **Prompt**: ADW execution records (id, agent_id, content, response, status, tokens, cost, timestamps)
4. **AgentLog**: Agent event logging (id, agent_id, log_type, message, metadata, timestamp)
5. **SystemLog**: System-wide logging (id, log_level, message, source, metadata, timestamp)

Each model includes:
- UUID validators for `id` fields (stored as TEXT in SQLite)
- Datetime fields with ISO 8601 serialization
- Status fields with enum-like constraints
- JSON metadata fields (stored as TEXT)
- Pydantic's built-in ValidationError handling
- Docstrings mapping to SQL DDL for reference

## Relevant Files

### Existing Files

- `plan_tasks_Tac_14_v2_SQLITE.md` - SQLite schema definitions (5 tables with complete DDL)
- `plan_tasks_Tac_14.md` - Original TAC-14 plan with dual-path implementation requirements
- `CLAUDE.md` - DDD architecture guidelines (domain/ for models, infrastructure/ for database)

### New Files

**BASE Location:**
- `adws/adw_modules/orch_database_models.py` - 5 Pydantic models for SQLite

**TEMPLATES Location:**
- `templates/adws/adw_modules/orch_database_models.py.j2` - Jinja2 template version (no variables needed)

**Registration:**
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Register template for generation

## Implementation Plan

### Phase 1: Schema Analysis
Extract complete schema definitions from SQLite plan to understand all fields, constraints, and relationships.

### Phase 2: BASE Models Implementation
Create functional Pydantic models in BASE location with all validators and serializers.

### Phase 3: TEMPLATES Creation
Copy models to TEMPLATES location as Jinja2 template and register in scaffold service.

## Step by Step Tasks

### Task 1: Create BASE directory structure
- Create directory `adws/adw_modules/` if it doesn't exist
- Prepare to create `orch_database_models.py` in this location

### Task 2: Implement OrchestratorAgent model
- Create `OrchestratorAgent` class with fields: id (str), name (str), description (Optional[str]), status (str with default 'active'), created_at (datetime), updated_at (datetime)
- Add `@field_validator('id')` for UUID format validation
- Add `@field_validator('status')` to enforce allowed values: 'active', 'inactive', 'archived'
- Configure `model_config` with `json_encoders` for datetime serialization to ISO 8601
- Add docstring mapping to SQL table: "Maps to orchestrator_agents table. UUID stored as TEXT, timestamps as ISO 8601."

### Task 3: Implement Agent model
- Create `Agent` class with fields: id (str), orchestrator_agent_id (str), session_id (str), status (str with default 'pending'), created_at (datetime), started_at (Optional[datetime]), completed_at (Optional[datetime])
- Add UUID validators for `id` and `orchestrator_agent_id`
- Add status validator for allowed values: 'pending', 'running', 'completed', 'failed'
- Configure datetime serialization
- Add docstring mapping to SQL table: "Maps to agents table. Runtime agent instances."

### Task 4: Implement Prompt model
- Create `Prompt` class with fields: id (str), agent_id (str), content (str), response (Optional[str]), status (str with default 'pending'), tokens_input (int with default 0), tokens_output (int with default 0), cost_usd (float with default 0.0), created_at (datetime), completed_at (Optional[datetime])
- Add UUID validators for `id` and `agent_id`
- Add status validator for allowed values: 'pending', 'running', 'completed', 'failed'
- Add validators to ensure tokens_input >= 0, tokens_output >= 0, cost_usd >= 0.0
- Configure datetime serialization
- Add docstring mapping to SQL table: "Maps to prompts table. ADW execution records."

### Task 5: Implement AgentLog model
- Create `AgentLog` class with fields: id (str), agent_id (str), log_type (str), message (str), metadata (Optional[dict]), created_at (datetime)
- Add UUID validators for `id` and `agent_id`
- Add log_type validator for allowed values: 'step_start', 'step_end', 'event', 'error'
- Add metadata validator to ensure it's JSON-serializable (will be stored as TEXT in SQLite)
- Configure datetime serialization and dict serialization for metadata
- Add docstring mapping to SQL table: "Maps to agent_logs table. Metadata stored as JSON TEXT."

### Task 6: Implement SystemLog model
- Create `SystemLog` class with fields: id (str), log_level (str), message (str), source (Optional[str]), metadata (Optional[dict]), created_at (datetime)
- Add UUID validator for `id`
- Add log_level validator for allowed values: 'debug', 'info', 'warning', 'error', 'critical'
- Add metadata validator for JSON-serializability
- Configure datetime and dict serialization
- Add docstring mapping to SQL table: "Maps to system_logs table. System-wide logging."

### Task 7: Add module-level documentation
- Add module docstring explaining SQLite type mappings: UUID→TEXT, datetime→ISO 8601, JSON→TEXT
- Document that these are pure data models with NO database operations
- Reference Task 8 for database operations (adw_database.py)
- Add examples showing model instantiation and validation

### Task 8: Create TEMPLATES version
- Create directory `templates/adws/adw_modules/` if it doesn't exist
- Copy `orch_database_models.py` to `templates/adws/adw_modules/orch_database_models.py.j2`
- Preserve all code exactly (no Jinja2 variables needed - models are static)
- Keep .j2 extension to indicate it's a template

### Task 9: Register template in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate the template registration section
- Add entry for `adws/adw_modules/orch_database_models.py.j2`
- Ensure template renders to `adws/adw_modules/orch_database_models.py` in generated projects
- Test template registration (if scaffold_service has a test mode)

### Task 10: Run validation commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues before considering task complete

## Testing Strategy

### Unit Tests

Create `tac_bootstrap_cli/tests/test_orch_database_models.py` with:

1. **UUID Validation Tests**
   - Test valid UUID strings are accepted
   - Test invalid UUID strings raise ValidationError
   - Test UUID validation for all models with id fields

2. **Status Enum Tests**
   - Test allowed status values for OrchestratorAgent ('active', 'inactive', 'archived')
   - Test allowed status values for Agent ('pending', 'running', 'completed', 'failed')
   - Test allowed status values for Prompt (same as Agent)
   - Test invalid status values raise ValidationError

3. **DateTime Serialization Tests**
   - Test datetime fields serialize to ISO 8601 format
   - Test `model_dump_json()` produces ISO 8601 timestamps
   - Test deserialization from ISO 8601 strings

4. **Metadata JSON Tests**
   - Test metadata fields accept valid dicts
   - Test metadata serialization to JSON strings
   - Test None metadata is allowed

5. **Numeric Validation Tests**
   - Test tokens_input/tokens_output >= 0 for Prompt
   - Test cost_usd >= 0.0 for Prompt
   - Test negative values raise ValidationError

6. **Model Instantiation Tests**
   - Test each model can be instantiated with required fields
   - Test default values are applied correctly
   - Test optional fields work as expected

### Edge Cases

1. **UUID Edge Cases**
   - Empty string UUID
   - Malformed UUID (wrong format)
   - UUID with uppercase/lowercase variations
   - Nil UUID (all zeros)

2. **Status Edge Cases**
   - Empty string status
   - Mixed case status ('Active' vs 'active')
   - Whitespace in status
   - Invalid status values

3. **DateTime Edge Cases**
   - Timezone-aware vs timezone-naive datetimes
   - Future timestamps
   - Very old timestamps (year < 1900)
   - Leap seconds

4. **Metadata Edge Cases**
   - Nested JSON structures (deep nesting)
   - Very large metadata dicts
   - Non-serializable objects in metadata
   - Empty dict vs None

5. **Numeric Edge Cases**
   - Extremely large token counts
   - Very small cost_usd (precision issues)
   - Zero values
   - Float vs int for cost_usd

## Acceptance Criteria

1. ✅ `adws/adw_modules/orch_database_models.py` exists in BASE with 5 complete Pydantic models
2. ✅ All models include UUID validators using `@field_validator`
3. ✅ Status fields have enum-like validation for allowed values
4. ✅ DateTime fields configured for ISO 8601 serialization via `model_config`
5. ✅ Metadata fields validated for JSON-serializability
6. ✅ Numeric fields (tokens, cost) validated for non-negative values
7. ✅ Each model has docstring mapping to SQL table
8. ✅ Module-level documentation explains SQLite type mappings
9. ✅ Template `templates/adws/adw_modules/orch_database_models.py.j2` created
10. ✅ Template registered in `scaffold_service.py`
11. ✅ All validation commands pass (pytest, ruff, mypy)
12. ✅ Unit tests cover UUID validation, status enums, datetime serialization, metadata JSON
13. ✅ Models are pure data classes with NO database operations (Task 8 responsibility)
14. ✅ Code follows DDD architecture (domain models separate from infrastructure)

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Unit tests - ensure models validate correctly
cd tac_bootstrap_cli && uv run pytest tests/test_orch_database_models.py -v --tb=short

# Linting - ensure code quality
cd tac_bootstrap_cli && uv run ruff check .

# Type checking - ensure type safety
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test - ensure CLI still works
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Integration test - test model instantiation
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

## Notes

### Dependencies
- No new dependencies required - uses standard Pydantic (already in project)
- Models rely only on Python stdlib (uuid, datetime, json) and Pydantic

### Future Work (NOT in this task)
- Task 8 will implement database operations (CRUD) in `adw_database.py`
- Task 19 will create schema initialization in `setup_database.sh`
- Models remain pure data classes - database logic stays separate per DDD

### SQLite Type Mappings Reference
```
Python Type      → SQLite Type → Storage
-------------------------------------------------
str (UUID)       → TEXT         → "550e8400-e29b-41d4-a716-446655440000"
datetime         → TEXT         → "2026-02-04T10:30:00.000000"
dict (JSON)      → TEXT         → "{\"key\": \"value\"}"
int              → INTEGER      → 42
float            → REAL         → 3.14159
```

### Validation Error Handling
- Use Pydantic's built-in `ValidationError` - no custom exceptions needed
- Error messages are clear and actionable (e.g., "Invalid UUID format")
- Validation happens at model instantiation - fail fast principle

### Template Generation Notes
- Template is static (no Jinja2 variables) because models don't need project-specific customization
- Projects generated with `tac-bootstrap init` will get exact copy of BASE models
- Future enhancement (v0.9.0+): Could add variables for custom model extensions
