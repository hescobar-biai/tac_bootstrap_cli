# Feature: Integrate Base Classes in ScaffoldService

## Metadata
issue_number: `135`
adw_id: `feature_1_11`
issue_json: `{"number":135,"title":"Tarea 1.11: Integrar base classes en ScaffoldService","body":"/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_1_11\n\n*Tipo**: feature\n**Ganancia**: Al ejecutar `tac-bootstrap init` con `--architecture ddd` y `--framework fastapi`, el proyecto incluye automaticamente todas las base classes en `src/shared/`.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n2. En el metodo `build_plan()`, agregar logica condicional:\n   ```python\n   if config.project.architecture in [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]:\n       if config.project.framework == Framework.FASTAPI:\n           self._add_shared_infrastructure(plan, config)\n   ```\n3. Crear metodo `_add_shared_infrastructure(plan, config)` que agregue:\n   - Directorio `src/shared/`\n   - Directorio `src/shared/domain/`\n   - Directorio `src/shared/infrastructure/`\n   - Cada template de `templates/shared/*.py.j2` como FileOperation\n4. Los archivos se generan en:\n   - `src/shared/domain/base_entity.py`\n   - `src/shared/domain/base_schema.py`\n   - `src/shared/application/base_service.py`\n   - `src/shared/infrastructure/base_repository.py`\n   - `src/shared/infrastructure/base_repository_async.py`\n   - `src/shared/infrastructure/database.py`\n   - `src/shared/infrastructure/exceptions.py`\n   - `src/shared/infrastructure/responses.py`\n   - `src/shared/infrastructure/dependencies.py`\n   - `src/shared/api/health.py`\n\n5. **Dual creation**: Como parte de esta tarea, crear la estructura `src/shared/` completa en la raiz de este proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`) con los archivos renderizados de las tareas 1.1-1.10. Esto asegura que este proyecto sirve como referencia funcional.\n\n**Criterios de aceptacion**:\n- `tac-bootstrap init my-app -l python -f fastapi -a ddd --no-interactive` genera `src/shared/` con todos los archivos\n- `tac-bootstrap init my-app -l python -f fastapi -a simple --no-interactive` NO genera `src/shared/`\n- La raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`) tiene todos los archivos renderizados\n- Tests existentes siguen pasando\n- Nuevo test verifica la inclusion condicional\n"}`

## Feature Description

This feature integrates the shared infrastructure base classes (tasks 1.1-1.10) into the ScaffoldService, enabling automatic generation of DDD/Clean/Hexagonal architecture scaffolding when using FastAPI. The feature implements conditional file generation based on architecture and framework choices, and performs dual creation: generating both the template integration logic in the CLI AND the rendered reference files in this project's root.

**Value**: When developers run `tac-bootstrap init` with DDD-style architecture and FastAPI, they automatically get a complete set of base classes for domain entities, schemas, services, repositories, and infrastructure utilities in `src/shared/`, eliminating boilerplate setup work.

## User Story

As a developer using TAC Bootstrap CLI
I want to automatically generate shared infrastructure base classes when initializing a DDD/Clean/Hexagonal architecture project with FastAPI
So that I can immediately start building features on top of well-structured, battle-tested base classes without writing boilerplate

## Problem Statement

Currently, the ScaffoldService generates the agentic layer structure (.claude/, adws/, scripts/) but doesn't generate application code scaffolding. Templates for base classes (base_entity, base_repository, etc.) exist in `templates/shared/*.j2` from tasks 1.1-1.10, but they're not integrated into the scaffold plan. Developers must manually create these base classes or start from scratch, losing the value of standardized patterns.

Additionally, this project (tac_bootstrap) should serve as a reference implementation, but the `src/shared/` directory doesn't exist in the repository root with rendered examples.

## Solution Statement

Extend ScaffoldService.build_plan() with conditional logic that detects when a project uses DDD/Clean/Hexagonal architecture with FastAPI framework, then invokes a new `_add_shared_infrastructure()` method to add FileOperations for all shared base classes. The method will:

1. Add directory operations for `src/shared/` and its subdirectories
2. Add file operations for all 10 template files with proper action=CREATE
3. Include `__init__.py` files to make Python packages valid
4. Position operations early in the plan (after base directories, before feature code)

**Dual Creation**: After implementing the CLI logic, render all templates using this project's `config.yml` values and write them to `/Volumes/MAc1/Celes/tac_bootstrap/src/shared/` as non-executable reference files.

## Relevant Files

### Files to Modify

- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** (scaffold_service.py:51-85)
  - Main implementation: add conditional call to `_add_shared_infrastructure()` in `build_plan()`
  - Create new method `_add_shared_infrastructure()` following patterns from `_add_claude_files()`, `_add_adw_files()`

### Files to Reference

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** (models.py:73-81)
  - Import Architecture enum (DDD, CLEAN, HEXAGONAL) and Framework enum (FASTAPI)

- **tac_bootstrap_cli/tac_bootstrap/domain/plan.py**
  - FileAction enum for CREATE action
  - ScaffoldPlan.add_directory() and add_file() methods

- **tac_bootstrap_cli/tac_bootstrap/templates/shared/*.j2** (10 templates)
  - base_entity.py.j2, base_schema.py.j2, base_service.py.j2
  - base_repository.py.j2, base_repository_async.py.j2
  - database.py.j2, exceptions.py.j2, responses.py.j2, dependencies.py.j2, health.py.j2

- **config.yml**
  - Values for rendering templates: project.name="tac-bootstrap", project.language="python", framework="none", architecture="ddd"

### Files to Test

- **tac_bootstrap_cli/tests/test_scaffold_service.py**
  - Add new integration tests for conditional generation

### New Files

- **src/shared/domain/__init__.py** (rendered, empty)
- **src/shared/domain/base_entity.py** (rendered from template)
- **src/shared/domain/base_schema.py** (rendered from template)
- **src/shared/application/__init__.py** (rendered, empty)
- **src/shared/application/base_service.py** (rendered from template)
- **src/shared/infrastructure/__init__.py** (rendered, empty)
- **src/shared/infrastructure/base_repository.py** (rendered from template)
- **src/shared/infrastructure/base_repository_async.py** (rendered from template)
- **src/shared/infrastructure/database.py** (rendered from template)
- **src/shared/infrastructure/exceptions.py** (rendered from template)
- **src/shared/infrastructure/responses.py** (rendered from template)
- **src/shared/infrastructure/dependencies.py** (rendered from template)
- **src/shared/api/__init__.py** (rendered, empty)
- **src/shared/api/health.py** (rendered from template)

## Implementation Plan

### Phase 1: Foundation - ScaffoldService Integration

Add the core logic to ScaffoldService that conditionally generates shared infrastructure based on architecture and framework.

**Tasks:**
1. Import Architecture and Framework enums in scaffold_service.py
2. Add conditional call in build_plan() after _add_directories()
3. Implement _add_shared_infrastructure() method following existing patterns
4. Add directory operations for src/shared/ hierarchy with __init__.py files
5. Add file operations for all 10 templates

### Phase 2: Dual Creation - Reference Implementation

Render all templates from tasks 1.1-1.10 into this project's root using config.yml values.

**Tasks:**
1. Create src/shared/ directory structure in project root
2. Load and parse /Volumes/MAc1/Celes/tac_bootstrap/config.yml
3. Render each of the 10 templates using Jinja2 with config values
4. Write rendered content to corresponding paths in src/shared/
5. Create __init__.py files for Python packages
6. Verify all files exist and contain rendered content (not template variables)

### Phase 3: Testing and Validation

Verify the feature works correctly with integration tests covering multiple scenarios.

**Tasks:**
1. Add integration test: DDD + FastAPI → generates src/shared/
2. Add integration test: SIMPLE + FastAPI → does NOT generate src/shared/
3. Add integration test: DDD + DJANGO → does NOT generate src/shared/
4. Add integration test: CLEAN + FastAPI → generates src/shared/
5. Add integration test: HEXAGONAL + FastAPI → generates src/shared/
6. Verify existing tests still pass
7. Run validation commands

## Step by Step Tasks

### Task 1: Import Required Types
- Open tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
- Add imports at top: `from tac_bootstrap.domain.models import Architecture, Framework`
- Verify imports resolve correctly

### Task 2: Add Conditional Call in build_plan()
- Locate the build_plan() method (scaffold_service.py:51-85)
- After the `self._add_directories(plan, config)` call (line 68)
- Add conditional logic:
  ```python
  # Add shared infrastructure for DDD-style architectures with FastAPI
  if config.project.architecture in [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]:
      if config.project.framework == Framework.FASTAPI:
          self._add_shared_infrastructure(plan, config)
  ```

### Task 3: Implement _add_shared_infrastructure() Method
- Add new method after _add_directories() (around line 110)
- Follow the pattern of _add_claude_files() and _add_adw_files()
- Method signature: `def _add_shared_infrastructure(self, plan: ScaffoldPlan, config: TACConfig) -> None:`
- Add docstring: "Add shared infrastructure base classes for DDD/Clean/Hexagonal architectures."
- Set `action = FileAction.CREATE` (only creates if file doesn't exist)

### Task 4: Add Directory Operations
- Add directories with plan.add_directory():
  - `src/shared` → "Shared infrastructure"
  - `src/shared/domain` → "Domain base classes"
  - `src/shared/application` → "Application base classes"
  - `src/shared/infrastructure` → "Infrastructure base classes"
  - `src/shared/api` → "Shared API utilities"

### Task 5: Add __init__.py Files
- Add file operations for Python package markers:
  - `src/shared/__init__.py` with empty content
  - `src/shared/domain/__init__.py` with empty content
  - `src/shared/application/__init__.py` with empty content
  - `src/shared/infrastructure/__init__.py` with empty content
  - `src/shared/api/__init__.py` with empty content
- Use action=CREATE, no template, content=""

### Task 6: Add Template File Operations
- Add file operations for domain templates:
  - `src/shared/domain/base_entity.py` → template="shared/base_entity.py.j2"
  - `src/shared/domain/base_schema.py` → template="shared/base_schema.py.j2"
- Add file operation for application template:
  - `src/shared/application/base_service.py` → template="shared/base_service.py.j2"
- Add file operations for infrastructure templates:
  - `src/shared/infrastructure/base_repository.py` → template="shared/base_repository.py.j2"
  - `src/shared/infrastructure/base_repository_async.py` → template="shared/base_repository_async.py.j2"
  - `src/shared/infrastructure/database.py` → template="shared/database.py.j2"
  - `src/shared/infrastructure/exceptions.py` → template="shared/exceptions.py.j2"
  - `src/shared/infrastructure/responses.py` → template="shared/responses.py.j2"
  - `src/shared/infrastructure/dependencies.py` → template="shared/dependencies.py.j2"
- Add file operation for API template:
  - `src/shared/api/health.py` → template="shared/health.py.j2"
- All with action=CREATE and appropriate reason strings

### Task 7: Create Root src/shared/ Directory Structure
- Create directories in project root:
  - /Volumes/MAc1/Celes/tac_bootstrap/src/shared/domain/
  - /Volumes/MAc1/Celes/tac_bootstrap/src/shared/application/
  - /Volumes/MAc1/Celes/tac_bootstrap/src/shared/infrastructure/
  - /Volumes/MAc1/Celes/tac_bootstrap/src/shared/api/
- Create empty __init__.py files in each subdirectory

### Task 8: Render Templates to Root src/shared/
- Load config.yml from /Volumes/MAc1/Celes/tac_bootstrap/config.yml
- For each of the 10 templates in tac_bootstrap_cli/tac_bootstrap/templates/shared/:
  - Read template file
  - Render with Jinja2 using config values (project.name="tac-bootstrap", etc.)
  - Write to corresponding path in /Volumes/MAc1/Celes/tac_bootstrap/src/shared/
  - Verify rendered content does not contain "{{" or "{%" (template syntax)
- Expected output files:
  - src/shared/domain/base_entity.py
  - src/shared/domain/base_schema.py
  - src/shared/application/base_service.py
  - src/shared/infrastructure/base_repository.py
  - src/shared/infrastructure/base_repository_async.py
  - src/shared/infrastructure/database.py
  - src/shared/infrastructure/exceptions.py
  - src/shared/infrastructure/responses.py
  - src/shared/infrastructure/dependencies.py
  - src/shared/api/health.py

### Task 9: Add Integration Test - DDD + FastAPI (generates shared)
- Open tac_bootstrap_cli/tests/test_scaffold_service.py
- Add test function: `test_scaffold_ddd_fastapi_includes_shared_infrastructure()`
- Create TACConfig with architecture=DDD, framework=FASTAPI
- Call scaffold_service.build_plan(config)
- Assert plan contains directory operations for src/shared/* (5 directories)
- Assert plan contains file operations for all 10 shared templates
- Assert plan contains __init__.py files

### Task 10: Add Integration Test - SIMPLE + FastAPI (no shared)
- Add test function: `test_scaffold_simple_fastapi_excludes_shared_infrastructure()`
- Create TACConfig with architecture=SIMPLE, framework=FASTAPI
- Call scaffold_service.build_plan(config)
- Assert plan does NOT contain any src/shared/ operations
- Use list comprehension to check: `assert not any("src/shared" in op.path for op in plan.files)`

### Task 11: Add Integration Test - DDD + Django (no shared)
- Add test function: `test_scaffold_ddd_django_excludes_shared_infrastructure()`
- Create TACConfig with architecture=DDD, framework=DJANGO
- Assert plan does NOT contain any src/shared/ operations
- Validates that framework must be FastAPI

### Task 12: Add Integration Tests - CLEAN and HEXAGONAL
- Add test function: `test_scaffold_clean_fastapi_includes_shared_infrastructure()`
- Add test function: `test_scaffold_hexagonal_fastapi_includes_shared_infrastructure()`
- Both with FastAPI framework, different architectures
- Assert both generate src/shared/ infrastructure

### Task 13: Run Existing Tests
- Execute: `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v`
- Verify all existing tests pass (no regressions)
- Fix any failures before proceeding

### Task 14: Validate with Full Test Suite and Validation Commands
- Run all validation commands:
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
  - `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- All must pass with zero errors

## Testing Strategy

### Unit Tests

Not applicable - this feature requires integration tests due to end-to-end nature of ScaffoldService.build_plan() → template rendering → file creation.

### Integration Tests

**Test 1: DDD + FastAPI → Generates Shared Infrastructure**
- Config: architecture=DDD, framework=FASTAPI, language=python
- Assertions:
  - plan.directories contains "src/shared", "src/shared/domain", "src/shared/application", "src/shared/infrastructure", "src/shared/api"
  - plan.files contains all 10 template files + 5 __init__.py files
  - FileAction is CREATE for all operations

**Test 2: SIMPLE + FastAPI → Does NOT Generate Shared Infrastructure**
- Config: architecture=SIMPLE, framework=FASTAPI
- Assertion: no operations with path containing "src/shared"

**Test 3: DDD + Django → Does NOT Generate Shared Infrastructure**
- Config: architecture=DDD, framework=DJANGO
- Assertion: no operations with path containing "src/shared"
- Validates framework-specific behavior

**Test 4: CLEAN + FastAPI → Generates Shared Infrastructure**
- Config: architecture=CLEAN, framework=FASTAPI
- Same assertions as Test 1

**Test 5: HEXAGONAL + FastAPI → Generates Shared Infrastructure**
- Config: architecture=HEXAGONAL, framework=FASTAPI
- Same assertions as Test 1

### Edge Cases

1. **Existing src/shared/ Directory**: CREATE action won't overwrite existing files
2. **Missing Templates**: If templates don't exist, render phase will fail with clear error (no validation needed in build_plan)
3. **Non-FastAPI DDD Projects**: Correctly excluded (e.g., Django, Flask)
4. **Framework=NONE with DDD**: Correctly excluded (no FastAPI imports)

### Manual Verification

After implementation, manually verify dual creation:
1. Check that /Volumes/MAc1/Celes/tac_bootstrap/src/shared/ exists with all files
2. Open rendered files and verify no Jinja2 syntax ({{ or {%})
3. Verify FastAPI/SQLAlchemy imports are present (non-executable reference)
4. Run: `find /Volumes/MAc1/Celes/tac_bootstrap/src/shared -name "*.py" | wc -l` → expect 14 files (10 + 4 __init__.py)

## Acceptance Criteria

1. ✅ **CLI Generates Shared Infrastructure (DDD + FastAPI)**
   - Command: `tac-bootstrap init my-app -l python -f fastapi -a ddd --no-interactive`
   - Creates: `my-app/src/shared/` with all 10 base class files + __init__.py files
   - All files are created with FileAction.CREATE (won't overwrite existing)

2. ✅ **CLI Does NOT Generate Shared Infrastructure (SIMPLE + FastAPI)**
   - Command: `tac-bootstrap init my-app -l python -f fastapi -a simple --no-interactive`
   - Does not create: `my-app/src/shared/`
   - Validates architecture filter

3. ✅ **CLI Does NOT Generate Shared Infrastructure (DDD + Django)**
   - Command: `tac-bootstrap init my-app -l python -f django -a ddd --no-interactive`
   - Does not create: `my-app/src/shared/`
   - Validates framework filter (FastAPI-only)

4. ✅ **Root Project Has Rendered Reference Files**
   - Path: `/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`
   - Contains all 10 rendered .py files using config.yml values
   - Files include FastAPI/SQLAlchemy imports (non-executable reference)
   - No Jinja2 template syntax remains ({{ or {%})

5. ✅ **Existing Tests Pass**
   - All tests in tac_bootstrap_cli/tests/ pass
   - No regressions in scaffold_service behavior

6. ✅ **New Integration Tests Pass**
   - test_scaffold_ddd_fastapi_includes_shared_infrastructure ✓
   - test_scaffold_simple_fastapi_excludes_shared_infrastructure ✓
   - test_scaffold_ddd_django_excludes_shared_infrastructure ✓
   - test_scaffold_clean_fastapi_includes_shared_infrastructure ✓
   - test_scaffold_hexagonal_fastapi_includes_shared_infrastructure ✓

7. ✅ **Code Quality Checks Pass**
   - Ruff linting: 0 errors
   - Mypy type checking: 0 errors
   - CLI smoke test: `tac-bootstrap --help` succeeds

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Unit and integration tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Verify dual creation (manual)
find /Volumes/MAc1/Celes/tac_bootstrap/src/shared -name "*.py" | wc -l
# Expected: 14 (10 base classes + 4 __init__.py)

# Verify no template syntax remains (manual)
grep -r "{{" /Volumes/MAc1/Celes/tac_bootstrap/src/shared/
# Expected: no matches (or only in comments/docstrings explaining templating)
```

## Notes

### Template Rendering Context
The 10 templates use Jinja2 variables like `{{ config.project.name }}`. When rendering to root src/shared/, use these values from config.yml:
- `config.project.name` → "tac-bootstrap"
- `config.project.language` → "python"
- `config.project.framework` → "none"
- `config.project.architecture` → "ddd"
- `config.paths.app_root` → "tac_bootstrap_cli"

### Non-Executable Reference
The rendered files in root src/shared/ contain FastAPI/SQLAlchemy imports that won't execute (this project is a CLI, not a FastAPI app). This is intentional - they serve as reference examples showing what the CLI GENERATES for FastAPI projects.

### Future Extensibility
This feature establishes the pattern for conditional scaffolding. Future tasks can add:
- Django-specific base classes (models.py, views.py, serializers.py)
- Flask-specific base classes (blueprints, extensions)
- TypeScript/NestJS base classes (decorators, DTOs, services)

### Dependencies
This task consolidates tasks 1.1-1.10 (template creation). If any templates are missing, the render phase will fail. Ensure all 10 templates exist in `tac_bootstrap_cli/tac_bootstrap/templates/shared/` before implementation.

### Git Worktree Note
This feature is being implemented in a git worktree at `/Volumes/MAc1/Celes/tac_bootstrap/trees/feature_1_11`. The dual creation writes files to the MAIN repository root at `/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`, not the worktree. This is correct behavior - the main repo should have the reference files.
