# Generate Entity Command

**ADW ID:** feature_2_4
**Date:** 2026-01-23
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/feature_2_4/specs/issue-146-adw-feature_2_4-sdlc_planner-generate-entity-command.md

## Overview

The `generate entity` command provides a CLI-based code generator that creates complete CRUD vertical slices for entities in DDD architecture projects. It supports both interactive wizard-based field definition and non-interactive command-line argument-based generation, creating domain models, Pydantic schemas, service layer, repository layer, and FastAPI routes with a single command.

## What Was Built

- **CLI Command**: `tac-bootstrap generate entity` with comprehensive options for entity generation
- **Entity Generator Service**: Orchestrates validation, conflict detection, plan building, and file creation
- **Interactive Field Wizard**: Loop-based wizard for defining entity fields with name, type, and required flag
- **Jinja2 Templates**: Complete set of templates for entity, schemas, service, repository (sync/async), routes, and events
- **Comprehensive Test Suite**: 993 lines of tests covering service, wizard, and CLI integration

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Added `generate` command with entity subcommand support
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`: Updated template discovery for entity templates
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Cleaned up domain models (removed old CRUD template models)

### Files Created

**Application Layer:**
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py`: Service orchestrating entity generation with validation, conflict detection, and plan execution

**Interface Layer:**
- `tac_bootstrap_cli/tac_bootstrap/interfaces/entity_wizard.py`: Interactive wizard for field definition with support for 9 field types

**Templates:**
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/entity.py.j2`: Domain entity model template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/schemas.py.j2`: Pydantic schemas (Create, Update, Response)
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/service.py.j2`: Service layer template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/repository.py.j2`: Synchronous repository template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/repository_async.py.j2`: Asynchronous repository template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/routes.py.j2`: FastAPI routes with CRUD endpoints
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/events.py.j2`: Domain events template (conditional)

**Tests:**
- `tac_bootstrap_cli/tests/test_entity_generator_service.py`: Tests for entity generation service (344 lines)
- `tac_bootstrap_cli/tests/test_entity_wizard.py`: Tests for interactive wizard (153 lines)
- `tac_bootstrap_cli/tests/test_cli_generate.py`: Integration tests for CLI command (496 lines)

### Key Changes

- **Auto-capability Generation**: Converts PascalCase entity names to kebab-case capabilities using regex (e.g., `ProductCategory` → `product-category`)
- **Field Type Support**: Supports 9 field types: str, int, float, bool, datetime, UUID, text, decimal, json
- **Dual Mode Operation**: Interactive wizard mode for exploratory development, non-interactive mode for scripting/automation
- **Validation Pipeline**: Validates project configuration (config.yml exists, architecture=ddd), checks for conflicts, validates field names
- **Template-based Generation**: Uses Jinja2 templates to ensure consistent code structure across all generated files
- **Dry-run Support**: Preview mode shows what would be created without actually creating files

## How to Use

### Interactive Mode (Default)

Launch the wizard to define fields interactively:

```bash
cd your-project/
tac-bootstrap generate entity Product
```

The wizard will:
1. Auto-suggest capability name (e.g., `product`)
2. Prompt for each field (name, type, required flag)
3. Continue until you choose to finish
4. Generate all files

### Non-Interactive Mode

Provide all parameters via command line:

```bash
tac-bootstrap generate entity Product \
  -c catalog \
  --no-interactive \
  --fields "name:str:required,price:float:required,description:text"
```

### Preview with Dry-run

See what would be created without actually creating files:

```bash
tac-bootstrap generate entity Product --dry-run
```

### Advanced Options

**Async Repository:**
```bash
tac-bootstrap generate entity Product --async
```
Generates `repository_async.py` instead of `repository.py`

**With Domain Events:**
```bash
tac-bootstrap generate entity Product --with-events
```
Creates `events.py` with Created, Updated, Deleted event classes

**With Authorization:**
```bash
tac-bootstrap generate entity Product --authorized
```
Adds `@requires_auth` decorator to create/update/delete endpoints

**Force Overwrite:**
```bash
tac-bootstrap generate entity Product --force
```
Overwrites existing files without error

## Configuration

**Project Requirements:**
- Must have `config.yml` in project root
- `architecture` must be set to `ddd`, `clean`, or `hexagonal`
- Project must follow DDD directory structure

**Field Definition Format (Non-interactive):**
```
--fields "name:type:constraint,name:type:constraint,..."
```

- **name**: Field name in snake_case
- **type**: One of: str, int, float, bool, datetime, uuid, text, decimal, json
- **constraint**: `required` (optional, defaults to required if omitted)

**Example:**
```bash
--fields "name:str:required,price:float,description:text,is_active:bool"
```

## Generated File Structure

After running the command, the following structure is created:

```
your-project/
└── domain/
    └── {capability}/
        ├── entities/
        │   └── {entity_name}.py          # Domain entity model
        ├── schemas/
        │   └── {entity_name}_schemas.py  # Pydantic DTOs
        ├── services/
        │   └── {entity_name}_service.py  # Service layer
        ├── repositories/
        │   └── {entity_name}_repository.py  # Repository layer
        ├── routes/
        │   └── {entity_name}_routes.py   # API routes
        └── events/
            └── {entity_name}_events.py   # Domain events (if --with-events)
```

## Testing

Run the complete test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v
```

Run specific test modules:

```bash
# Entity generator service tests
cd tac_bootstrap_cli && uv run pytest tests/test_entity_generator_service.py -v

# Wizard tests
cd tac_bootstrap_cli && uv run pytest tests/test_entity_wizard.py -v

# CLI integration tests
cd tac_bootstrap_cli && uv run pytest tests/test_cli_generate.py -v
```

## Next Steps After Generation

After generating an entity, the CLI displays next steps:

1. **Register Router**: Import and include the generated router in your `main.py`:
   ```python
   from domain.{capability}.routes.{entity_name}_routes import router as {entity_name}_router
   app.include_router({entity_name}_router)
   ```

2. **Run Database Migrations**: If using a database, create and apply migrations:
   ```bash
   alembic revision --autogenerate -m "Add {entity_name} entity"
   alembic upgrade head
   ```

3. **Import Events** (if `--with-events` was used): Register event handlers:
   ```python
   from domain.{capability}.events.{entity_name}_events import (
       {EntityName}Created,
       {EntityName}Updated,
       {EntityName}Deleted
   )
   ```

## Notes

**Design Decisions:**
- Subcommand parameter uses simple string validation instead of nested Typer apps for future extensibility
- Field type mapping supports basic types; advanced types (Decimal with precision, Enum, relationships) require manual editing
- Templates are separate from shared templates because they're for generation, not scaffolding
- Wizard only collects name, type, and required flag; validators, defaults, and relationships are future enhancements
- Conflict detection only checks domain entity file existence to prevent partial overwrites

**Limitations:**
- Does not generate database migration files (must be done manually)
- Does not support relationships (foreign keys, many-to-many)
- Does not support validators or default values in wizard
- Does not generate test files for the entity
- Only supports DDD-compatible architectures

**Future Enhancements:**
- Automatic Alembic migration generation
- Support for relationships and foreign keys
- Validator and default value support in wizard
- Test file generation
- Support for additional architectures (simple, hexagonal)
- YAML-based entity specs for bulk generation
