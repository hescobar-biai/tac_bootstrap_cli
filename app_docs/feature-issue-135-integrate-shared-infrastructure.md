# Shared Infrastructure Base Classes Integration

**ADW ID:** feature_1_11
**Date:** 2026-01-23
**Specification:** specs/issue-135-adw-feature_1_11-sdlc_planner-integrate-shared-infrastructure.md

## Overview

This feature integrates shared infrastructure base classes into the TAC Bootstrap CLI's scaffold generation. When initializing projects with DDD, Clean, or Hexagonal architecture using FastAPI, the CLI now automatically generates a complete set of domain entities, schemas, services, repositories, and infrastructure utilities in `src/shared/`, eliminating boilerplate setup work.

## What Was Built

- **Conditional Scaffold Logic**: Added architecture + framework detection in ScaffoldService
- **Shared Infrastructure Method**: New `_add_shared_infrastructure()` generates 10 base class files
- **Base Classes**:
  - Domain: `base_entity.py`, `base_schema.py`
  - Application: `base_service.py`
  - Infrastructure: `base_repository.py`, `base_repository_async.py`, `database.py`, `exceptions.py`, `responses.py`, `dependencies.py`
  - API: `health.py`
- **Comprehensive Test Suite**: 6 integration tests covering inclusion/exclusion scenarios
- **Database Template Fix**: Corrected `database.py.j2` template variable reference

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added conditional logic and `_add_shared_infrastructure()` method (109 lines added)
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`: Fixed template variable for project name
- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Added 259 lines of integration tests

### Key Changes

1. **Architecture Detection**: Imported `Architecture` and `Framework` enums, added conditional check for `[DDD, CLEAN, HEXAGONAL] + FASTAPI` combinations in `build_plan()` method (scaffold_service.py:70-73)

2. **Infrastructure Method**: Implemented `_add_shared_infrastructure()` following the pattern of existing methods like `_add_claude_files()`. Uses `FileAction.CREATE` to avoid overwriting existing files (scaffold_service.py:117-215)

3. **Directory Structure**: Generates 5 directories (`src/shared/`, `src/shared/domain/`, `src/shared/application/`, `src/shared/infrastructure/`, `src/shared/api/`) with Python package markers (`__init__.py`)

4. **File Operations**: Adds 10 template-based file operations with descriptive reason strings for each base class

5. **Test Coverage**: Created `TestScaffoldServiceSharedInfrastructure` class with 6 tests verifying:
   - Inclusion for DDD + FastAPI
   - Exclusion for SIMPLE + FastAPI
   - Exclusion for DDD + Django
   - Inclusion for CLEAN + FastAPI
   - Inclusion for HEXAGONAL + FastAPI
   - File creation and valid Python rendering

## How to Use

### Generate Project with Shared Infrastructure

Initialize a new project with DDD architecture and FastAPI framework:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap init my-app -l python -f fastapi -a ddd --no-interactive
```

This creates:
```
my-app/
├── src/
│   └── shared/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── base_entity.py
│       │   └── base_schema.py
│       ├── application/
│       │   ├── __init__.py
│       │   └── base_service.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── base_repository.py
│       │   ├── base_repository_async.py
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   ├── responses.py
│       │   └── dependencies.py
│       └── api/
│           ├── __init__.py
│           └── health.py
```

### Architectures That Include Shared Infrastructure

The following architecture + framework combinations generate shared infrastructure:
- DDD + FastAPI ✓
- Clean + FastAPI ✓
- Hexagonal + FastAPI ✓

### Architectures That Exclude Shared Infrastructure

These combinations do NOT generate shared infrastructure:
- Simple + FastAPI (architecture filter)
- DDD + Django (framework filter)
- DDD + Flask (framework filter)
- Any architecture + None framework

## Configuration

No additional configuration required. The feature detects architecture and framework from:

```yaml
# config.yml
project:
  architecture: ddd  # or clean, hexagonal
  framework: fastapi
```

Or via CLI flags:
```bash
--architecture ddd    # -a ddd
--framework fastapi   # -f fastapi
```

## Testing

Run the integration tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceSharedInfrastructure -v
```

Run all tests to verify no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### FileAction.CREATE Behavior
All shared infrastructure files use `FileAction.CREATE`, which only creates files if they don't already exist. Running `tac-bootstrap init` in an existing directory will NOT overwrite user-modified base classes.

### Framework-Specific Design
This feature is FastAPI-specific because the base classes use FastAPI dependencies (`Depends`), SQLAlchemy ORM, and Pydantic schemas. Future tasks may add Django/Flask equivalents with framework-specific patterns (Django ORM models, Flask Blueprints, etc.).

### Template Dependencies
The feature depends on 10 Jinja2 templates created in tasks 1.1-1.10, located in `tac_bootstrap_cli/tac_bootstrap/templates/shared/`. Missing templates will cause rendering failures with clear error messages.

### Reference Implementation
This repository (tac_bootstrap) can serve as a reference by manually rendering templates to `/Volumes/MAc1/Celes/tac_bootstrap/src/shared/` using the project's `config.yml` values. This was planned but not executed in the current implementation - files remain templates only.

### Future Extensibility
This establishes the pattern for conditional scaffolding based on architecture + framework. Future extensions could add:
- TypeScript/NestJS base classes (decorators, DTOs, services)
- Django base classes (abstract models, managers, serializers)
- Go base interfaces (repositories, services, handlers)
