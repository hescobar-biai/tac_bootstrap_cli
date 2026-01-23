# GenerateService - Entity Generation Orchestration

**ADW ID:** feature_2_3
**Date:** 2026-01-23
**Specification:** specs/issue-143-adw-feature_2_3-sdlc_planner-generate-service.md

## Overview

GenerateService is a core application service that orchestrates the generation of CRUD entities following vertical slice architecture. It validates preconditions, renders entity templates, manages filesystem operations, and ensures safe, idempotent entity generation with comprehensive error handling.

## What Was Built

- **GenerateService Class**: Application service that coordinates entity generation
- **EntitySpec Model**: Domain model defining entity specifications (name, capability, fields)
- **GenerateResult Model**: Result model containing generation metadata
- **Custom Exception Hierarchy**: ValidationError, PreconditionError, FileSystemError
- **Validation Logic**: Validates entity names, capability names, and base class preconditions
- **Template Rendering**: Renders 6 entity templates (domain, schemas, service, repository, models, routes)
- **Filesystem Operations**: Creates directory structure and writes files with all-or-nothing approach

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py` (NEW): Main service implementation with 418 lines
  - GenerateService class with generate_entity() orchestration method
  - Custom exception classes (ValidationError, PreconditionError, FileSystemError)
  - GenerateResult Pydantic model
  - Private methods for validation, rendering, and file writing

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Added EntitySpec domain model
  - EntitySpec with name, capability, fields, description
  - snake_name property for converting PascalCase to snake_case
  - Field validators for name and capability format validation

### Key Changes

1. **Validation-First Approach**: Service validates all inputs (EntitySpec format, base classes existence, file conflicts) before any filesystem writes to prevent partial/corrupted state

2. **All-or-Nothing File Check**: When force=False, the service checks that NONE of the target files exist. If ANY file exists, it raises FileExistsError with the complete list of conflicting files

3. **Vertical Slice Structure**: Creates complete directory structure (domain/, application/, infrastructure/, api/) with __init__.py files in each subdirectory

4. **Template Orchestration**: Renders 6 entity templates (domain.py, schemas.py, service.py, repository.py, models.py, routes.py) with context containing entity and config

5. **Pure Business Logic**: No logging or side effects - service focuses solely on orchestration logic, leaving event handling to CLI layer

## How to Use

### Basic Usage

```python
from pathlib import Path
from tac_bootstrap.application.generate_service import GenerateService
from tac_bootstrap.domain.models import EntitySpec, TACConfig
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.infrastructure.fs import FileSystem

# Initialize dependencies
template_repo = TemplateRepository(templates_dir=Path("templates"))
fs = FileSystem()
service = GenerateService(template_repo, fs)

# Define entity
entity = EntitySpec(
    name="User",
    capability="users",
    fields=[
        {"name": "email", "type": "str"},
        {"name": "name", "type": "str"}
    ],
    description="User entity for authentication"
)

# Load config
config = TACConfig.from_yaml(Path("tac_config.yaml"))

# Generate entity
result = service.generate_entity(
    entity=entity,
    project_root=Path("/path/to/project"),
    config=config,
    force=False  # Set to True to overwrite existing files
)

print(f"Generated {result.entity_name} in {result.directory}")
print(f"Created {len(result.files_created)} files:")
for file_path in result.files_created:
    print(f"  - {file_path}")
```

### EntitySpec Definition

The EntitySpec model defines the entity to generate:

- **name**: Entity name in PascalCase (e.g., "User", "BlogPost")
  - Must be a valid Python identifier
  - Cannot start with a number

- **capability**: Capability name in snake_case (e.g., "users", "blog_posts")
  - Must be lowercase
  - Must start with a letter
  - Can contain alphanumeric characters and underscores
  - Maximum 50 characters

- **fields**: Optional list of field specifications (used by templates)
- **description**: Optional human-readable description

### Generated File Structure

The service generates the following structure:

```
{app_root}/{capability}/
├── domain/
│   ├── __init__.py
│   └── {entity_snake_name}.py
├── application/
│   ├── __init__.py
│   ├── schemas.py
│   └── service.py
├── infrastructure/
│   ├── __init__.py
│   ├── models.py
│   └── repository.py
└── api/
    ├── __init__.py
    └── routes.py
```

## Configuration

### Prerequisites

Before using GenerateService, ensure the following base classes exist:

- `{app_root}/shared/domain/base_entity.py`
- `{app_root}/shared/domain/base_schema.py`
- `{app_root}/shared/application/base_service.py`
- `{app_root}/shared/infrastructure/base_repository.py`

If any base class is missing, the service raises PreconditionError with the list of missing files.

### Force Mode

- **force=False** (default): Raises FileExistsError if ANY target file exists
- **force=True**: Overwrites existing files (useful for iterative development)

### Template Context

Templates receive the following context:

```python
{
    "entity": EntitySpec,  # Entity specification
    "config": TACConfig    # Project configuration
}
```

Templates can access:
- `entity.name` - PascalCase entity name
- `entity.snake_name` - snake_case entity name (computed property)
- `entity.capability` - Capability name
- `entity.fields` - List of field specifications
- `config.paths.app_root` - Application root directory
- All other config fields

## Testing

The implementation includes comprehensive unit tests covering:

- Happy path with valid EntitySpec
- Invalid entity name validation (starts with number, contains spaces)
- Invalid capability name validation (uppercase, special chars)
- Missing base classes (PreconditionError)
- Existing files with force=False (FileExistsError)
- Existing files with force=True (overwrite success)
- App root creation (mkdir -p behavior)
- __init__.py file generation
- Template rendering with correct context
- GenerateResult metadata accuracy

Run tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_generate_service.py -v
```

All validation commands pass:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short  # 329 passed, 2 skipped
cd tac_bootstrap_cli && uv run ruff check .                  # PASSED
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/          # PASSED
cd tac_bootstrap_cli && uv run tac-bootstrap --help         # PASSED
```

## Notes

### Design Decisions

1. **No Rollback Logic**: Service uses fail-fast approach. If an error occurs after partial file creation, the service does not attempt to clean up. Users can manually remove directories or re-run with force=True.

2. **Pure Business Logic**: Service contains no logging, events, or side effects beyond filesystem writes. CLI layer should handle logging and user feedback.

3. **Validation-First**: All validation happens before any filesystem writes to minimize chance of partial/corrupted state.

4. **All-or-Nothing File Check**: Prevents scenarios where some files from a previous generation exist and others don't, which could lead to inconsistent state.

5. **App Root Auto-Creation**: Service creates app_root directory if missing (mkdir -p behavior) for better user experience.

### Future Enhancements

- This service provides the foundation for the CLI `generate entity` command (separate task)
- Entity templates (domain.py.j2, schemas.py.j2, etc.) are created in separate tasks
- Service is designed to be testable in isolation with mocked dependencies
- Force flag enables overwriting for iterative development workflows

### Limitations

- No validation of entity fields structure (delegated to templates)
- No duplicate entity detection (relies on file existence check)
- No support for partial generation (all files are generated together)

### Related Components

- **TemplateRepository** (infrastructure/template_repo.py): Renders Jinja2 templates
- **FileSystem** (infrastructure/fs.py): Safe, idempotent filesystem operations
- **TACConfig** (domain/models.py): Project configuration model
- **EntitySpec** (domain/models.py): Entity specification model
