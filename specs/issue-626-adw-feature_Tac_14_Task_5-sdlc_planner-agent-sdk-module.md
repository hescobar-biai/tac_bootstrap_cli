# Feature: Agent SDK Module (BASE + TEMPLATES)

## Metadata
issue_number: `626`
adw_id: `feature_Tac_14_Task_5`
issue_json: `{"number": 626, "title": "Implementar Agent SDK module (BASE + TEMPLATES)", "body": "file: plan_tasks_Tac_14.md\n\n**Descripción**:\nCrear módulo adw_agent_sdk.py con modelos Pydantic para control programático de agentes, en BASE y templates.\n\n**Pasos técnicos**:\n\n**BASE**:\n1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py`\n2. Validar PEP 723 dependencies header\n3. Incluir enums: ModelName, SettingSource, HookEventName, PermissionDecision\n4. Incluir modelos Pydantic completos\n5. Agregar docstrings\n\n**TEMPLATES**:\n6. Copiar a template .j2 sin modificaciones\n7. Registrar en scaffold_service.py\n\n**Criterios de aceptación**:\n- adw_agent_sdk.py creado en BASE\n- Todos los enums definidos\n- Pydantic models con validators\n- Template .j2 creado\n- Registro completo\n\n**Rutas impactadas**:\n\n**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):\n```\nadws/adw_modules/adw_agent_sdk.py  [CREAR]\n```\n\n**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):\n```\nadws/adw_modules/adw_agent_sdk.py.j2  [CREAR]\n```\n\n**CLI**:\n```\napplication/scaffold_service.py  [MODIFICAR]\n```\n\n**Metadata**:\n- Categoría: Agent SDK\n- Prioridad: Alta\n- Estimación: 2h\n- Dependencias: Ninguna\n\n**Keywords**: agent-sdk, pydantic-models, type-safety, programmatic-agents, class-2\n\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_5`"}`

## Feature Description
Create the adw_agent_sdk.py module in both BASE and TEMPLATES locations. This module provides a typed Pydantic layer for programmatic control of Claude Agent SDK, enabling ADW workflows to configure and orchestrate agents in a type-safe, validated manner.

The module is foundational infrastructure for TAC-14's Class 2 (Outloop Systems) capabilities, providing the abstractions needed for database-backed workflows and orchestration patterns.

## User Story
As a TAC Bootstrap user
I want adw_agent_sdk.py with complete Pydantic models for Agent SDK control
So that my generated projects can programmatically configure agents, hooks, settings, and messages with full type safety and validation

## Problem Statement
TAC-14 introduces database-backed ADW workflows and orchestration capabilities (Tasks 6-14) that require programmatic control of the Claude Agent SDK. Without a typed SDK layer:
- Workflows cannot reliably configure agent settings, models, or tools
- Hook event handling lacks type safety and validation
- Message construction is error-prone and unvalidated
- Integration with database models and WebSockets is fragile

The existing TAC-13 implementation lacks this abstraction layer, making Class 2 and Class 3 features impossible to implement safely.

## Solution Statement
Copy the complete adw_agent_sdk.py module from the TAC-14 reference codebase to BASE location, validate the PEP 723 dependencies header for Python 3.10+ compatibility, and create a static .j2 template copy for project generation.

This approach:
1. Reuses proven, battle-tested SDK abstractions from TAC-14
2. Ensures Python 3.10+ compatibility per project requirements
3. Preserves all enums, Pydantic models, validators, and docstrings unchanged
4. Enables immediate integration by later tasks (6-14) that depend on these types
5. Provides identical SDK capabilities to all generated projects via template

## Relevant Files
Files necessary for implementing the feature:

### Source Reference
- `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py` - Source module to copy (1655 lines, confirmed accessible)

### BASE Location
- `adws/adw_modules/adw_agent_sdk.py` - Target location in BASE repository

### TEMPLATES Location
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2` - Template for project generation

### Registration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that registers templates for rendering (modify `_add_adw_files` method around line 640-661)

### New Files
1. `adws/adw_modules/adw_agent_sdk.py` (BASE)
2. `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2` (TEMPLATES)

## Implementation Plan

### Phase 1: Source Validation
Validate source file accessibility and PEP 723 header compatibility before proceeding.

**Tasks:**
1. Confirm `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py` is readable
2. Read PEP 723 dependencies header (lines 1-8)
3. Verify Python version requirement matches project baseline (Python 3.10+)
4. If header requires Python 3.11+, fail fast with clear error message for user to provide adjusted version
5. Document required dependencies from header: pydantic, claude-agent-sdk, rich versions

**Acceptance Criteria:**
- Source file readable (1655 lines)
- PEP 723 header validated for Python 3.10+ compatibility
- Dependencies documented

### Phase 2: BASE Implementation
Copy complete module to BASE location preserving all content.

**Tasks:**
1. Create directory `adws/adw_modules/` if not exists
2. Copy entire source file to `adws/adw_modules/adw_agent_sdk.py`
3. Verify copied file integrity (same line count, no corruption)
4. Validate PEP 723 header is intact
5. Spot-check key enums present: ModelName, SettingSource, HookEventName, PermissionDecision
6. Verify imports and structure unchanged

**Acceptance Criteria:**
- `adws/adw_modules/adw_agent_sdk.py` exists in BASE
- File contains 1655 lines (matching source)
- PEP 723 header present and valid
- All 4 enums defined (ModelName, SettingSource, HookEventName, PermissionDecision)
- Pydantic models with validators preserved
- Docstrings intact

### Phase 3: TEMPLATES Implementation
Create static .j2 template copy for project generation.

**Tasks:**
1. Create directory `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/` if not exists
2. Copy `adws/adw_modules/adw_agent_sdk.py` to `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2`
3. Verify .j2 file is byte-identical to BASE file (no Jinja2 variables added per "sin modificaciones" requirement)
4. Confirm PEP 723 header preserved in template

**Acceptance Criteria:**
- `.j2` template file exists in TEMPLATES location
- Template is static copy with NO Jinja2 variable substitutions
- PEP 723 header preserved
- File integrity verified (same line count)

### Phase 4: Template Registration
Register template in scaffold_service.py following existing adw_modules pattern.

**Tasks:**
1. Read `scaffold_service.py` to understand existing registration pattern (line ~640-661)
2. Locate `modules` list in `_add_adw_files` method
3. Add tuple entry: `("adw_agent_sdk.py", "Agent SDK type-safe layer")`
4. Verify registration follows alphabetical/logical ordering
5. Confirm template path matches: `adws/adw_modules/adw_agent_sdk.py.j2`

**Acceptance Criteria:**
- Template registered in `scaffold_service.py`
- Entry added to `modules` list in `_add_adw_files` method
- Template path correctly references `.j2` file
- Registration follows existing pattern

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Validate Source File
- Confirm source file `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py` exists and is readable
- Read and validate PEP 723 dependencies header (lines 1-8)
- Verify `requires-python = ">=3.10"` or `>=3.11"` (if 3.11+, document for potential adjustment)
- Extract dependency versions: pydantic, claude-agent-sdk, rich
- Verify file has expected structure (enums, models, validators, docstrings)

### Task 2: Copy to BASE Location
- Create directory `adws/adw_modules/` if missing
- Copy entire file from source to `adws/adw_modules/adw_agent_sdk.py`
- Verify line count matches source (1655 lines)
- Spot-check critical components:
  - PEP 723 header intact (lines 1-8)
  - ModelName enum (lines ~43-54)
  - SettingSource enum (lines ~57-62)
  - HookEventName enum (lines ~69-87)
  - PermissionDecision enum (lines ~89-94)
  - Pydantic BaseModel imports and usage
- Confirm file is syntactically valid Python

### Task 3: Create TEMPLATES Copy
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/` if missing
- Copy `adws/adw_modules/adw_agent_sdk.py` to `adw_agent_sdk.py.j2`
- Verify .j2 file is byte-identical to BASE version (NO modifications)
- Confirm PEP 723 header preserved in template
- Verify no Jinja2 syntax accidentally introduced

### Task 4: Register Template in scaffold_service.py
- Read `_add_adw_files` method in `scaffold_service.py`
- Locate the `modules` list (around line 641-653)
- Add entry: `("adw_agent_sdk.py", "Agent SDK type-safe layer")`
- Position entry logically in list (alphabetically or by dependency order)
- Verify template path resolves correctly: `f"adws/adw_modules/adw_agent_sdk.py.j2"`
- Ensure existing registration pattern followed exactly

### Task 5: Validation and Testing
- Run validation commands to ensure no regressions
- Verify template can be rendered by template engine
- Confirm no syntax errors in Python files
- Check that registration doesn't break existing scaffold operations

## Testing Strategy

### Unit Tests
Not applicable for this task - this is a direct copy operation with no new logic. Testing will be covered by:
1. File integrity checks (line counts, byte comparisons)
2. Syntax validation (Python parser)
3. Template rendering validation (Jinja2 engine)

### Integration Tests
- Verify `scaffold_service.py` can discover and render the template
- Confirm template renders to valid Python file
- Validate rendered file has correct PEP 723 header
- Check that existing tests still pass after registration

### Edge Cases
1. **Source file inaccessible**: Fail early with clear error message directing user to provide alternative source
2. **PEP 723 requires Python 3.11+**: Document discrepancy, proceed with copy, note in plan output for user review
3. **Template directory missing**: Create directory structure before copying
4. **Registration conflict**: Verify no duplicate entries in modules list

## Acceptance Criteria
✓ Source file `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py` validated and accessible
✓ `adws/adw_modules/adw_agent_sdk.py` created in BASE with 1655 lines
✓ PEP 723 dependencies header present and validated (Python 3.10+ compatible)
✓ All 4 enums defined: ModelName, SettingSource, HookEventName, PermissionDecision
✓ Pydantic models with validators preserved unchanged
✓ Docstrings intact and complete
✓ Template `adws/adw_modules/adw_agent_sdk.py.j2` created in TEMPLATES location
✓ Template is static copy with NO Jinja2 variable substitutions ("sin modificaciones")
✓ Template registered in `scaffold_service.py` `_add_adw_files` method
✓ Registration follows existing adw_modules pattern
✓ No regressions in existing functionality

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `ls -la adws/adw_modules/adw_agent_sdk.py` - Verify BASE file exists
- `wc -l adws/adw_modules/adw_agent_sdk.py` - Confirm line count (should be 1655)
- `head -n 8 adws/adw_modules/adw_agent_sdk.py` - Validate PEP 723 header
- `python3 -m py_compile adws/adw_modules/adw_agent_sdk.py` - Syntax check BASE file
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2` - Verify template exists
- `wc -l tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2` - Confirm template line count
- `grep -n "adw_agent_sdk.py" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Verify registration
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### PEP 723 Dependencies Header
The source file uses PEP 723 inline script metadata (lines 1-8):
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.0",
#   "claude-agent-sdk>=0.1.18",
#   "rich>=13.0",
# ]
# ///
```

**IMPORTANT**: The source requires Python 3.11+, but project baseline is Python 3.10+. Options:
1. **Copy as-is** (recommended): Preserve exact source, note discrepancy in validation output
2. **Adjust to 3.10+**: Change header to `requires-python = ">=3.10"` if code is compatible

**Decision**: Copy as-is per "sin modificaciones" requirement. Document the 3.11+ requirement for user awareness.

### Module Purpose
Per source docstring: "Abstract typed layer for Claude Agent SDK control. Intentionally abstract and can be used for any Agent SDK use case - ADW-specific concerns belong in higher-level adw_agents.py."

This is pure infrastructure - no business logic, no ADW-specific code. Safe to copy unchanged.

### Template Strategy
Per issue: "Copiar a template .j2 sin modificaciones" - no Jinja2 variables needed.
SDK module should be identical across all generated projects (no project-specific customization).

### Dependencies for Future Tasks
This module enables:
- **Task 7**: Database models need SDK enums for agent configuration
- **Task 8**: Database operations need SDK types for CRUD
- **Task 9**: Logging needs SDK message types
- **Task 10**: Workflows need full SDK for agent orchestration
- **Task 11**: WebSockets need SDK types for event streaming

All subsequent Class 2 and Class 3 tasks depend on these type definitions.

### Registration Pattern
The `scaffold_service.py` uses a simple list-based registration:
```python
modules = [
    ("__init__.py", "Package init"),
    ("agent.py", "Claude Code wrapper"),
    # ... add here ...
    ("adw_agent_sdk.py", "Agent SDK type-safe layer"),
]
```

No complex configuration needed - just append to list.
