# Feature: Template base_repository_async.py

## Metadata
issue_number: `119`
adw_id: `49f979da`
issue_json: `{"number":119,"title":"Tarea 1.5: Template base_repository_async.py","body":"/feature\n**Ganancia**: Version async del repositorio para proyectos que usen async SQLAlchemy (AsyncSession). Misma interfaz que sync pero con await.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`\n2. Crear renderizado en raiz: `src/shared/infrastructure/base_repository_async.py`\n2. Misma interfaz que base_repository.py pero con:\n   - `AsyncSession` en lugar de `Session`\n   - Todos los metodos son `async def`\n   - Usa `await session.execute()` en lugar de `session.query()`\n   - Usa `select()` statements (SQLAlchemy 2.0 style)\n3. Agregar metodos adicionales async-friendly:\n   - `bulk_create(models: list[TModel]) -> list[TModel]`\n   - `bulk_update(models: list[TModel]) -> list[TModel]`\n\n**Criterios de aceptacion**:\n- Usa SQLAlchemy 2.0 async API\n- Misma funcionalidad que sync repo\n- bulk operations usan `session.add_all()`"}`

## Feature Description

Create an async version of the base repository template that mirrors all functionality from the synchronous `base_repository.py` but uses SQLAlchemy 2.0 async API with `AsyncSession`. This enables the TAC Bootstrap CLI to generate async repositories for projects using async SQLAlchemy patterns.

The template will provide:
- Full CRUD operations (create, read, update, delete)
- Soft delete functionality (state=2 filtering)
- Pagination, filtering, and sorting
- Bulk operations (bulk_create, bulk_update) for efficient batch processing
- SQLAlchemy 2.0 async patterns with select() statements
- Unit of Work pattern (no commits in repository layer)

## User Story

As a developer using TAC Bootstrap
I want to generate async repositories using SQLAlchemy 2.0 async API
So that I can build FastAPI applications with async database operations following modern SQLAlchemy patterns and DDD architecture

## Problem Statement

Projects using async SQLAlchemy (AsyncSession) with FastAPI's async endpoints need async repository implementations. The current `base_repository.py` template uses synchronous SQLAlchemy 1.x patterns (`session.query()`), which:

1. Cannot be used with `AsyncSession` (requires different API)
2. Uses deprecated SQLAlchemy 1.x query API instead of 2.0 `select()` statements
3. Lacks bulk operations for efficient batch inserts/updates
4. Forces developers to manually adapt sync patterns to async

This creates friction when scaffolding async-first projects and prevents developers from following SQLAlchemy 2.0 best practices out of the box.

## Solution Statement

Create a parallel async template (`base_repository_async.py.j2`) that:

1. Uses `AsyncSession` instead of `Session`
2. Implements all methods as `async def` with `await` for database operations
3. Uses SQLAlchemy 2.0 `select()` API instead of legacy `session.query()`
4. Mirrors all functionality from sync version (CRUD, soft delete, pagination, filtering, sorting)
5. Adds bulk operations (`bulk_create`, `bulk_update`) using `session.add_all()`
6. Follows Unit of Work pattern (repository does not commit, caller manages transaction)
7. Returns models with DB-generated fields populated after flush

Following the Dual Creation Pattern:
- Template stored at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`
- Reference implementation rendered at `src/shared/infrastructure/base_repository_async.py`

## Relevant Files

Files needed for implementation:

### Existing Files (for reference)
- `src/shared/infrastructure/base_repository.py` - Synchronous repository to mirror
  - Contains all methods to replicate: get_by_id, create, update, delete, hard_delete, get_all, exists, count
  - Defines soft delete pattern (state=2 filtering)
  - Shows docstring format and IDK comments
- `config.yml` - Project configuration for rendering template
  - Contains values like project.name, paths.app_root, etc.
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` - Sync template (if exists, for pattern reference)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2` - Jinja2 template for async repository
- `src/shared/infrastructure/base_repository_async.py` - Rendered reference implementation

## Implementation Plan

### Phase 1: Foundation
1. Read existing `base_repository.py` to understand complete interface
2. Study docstring patterns, IDK comments, and soft delete logic
3. Verify directory structure exists for both template and rendered file
4. Load `config.yml` to understand rendering context

### Phase 2: Core Implementation
1. Create Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`
   - Include module-level docstring with IDK tags
   - Define imports for async SQLAlchemy (AsyncSession, select, etc.)
   - Create BaseRepositoryAsync[TModel] generic class
   - Implement all async methods mirroring sync interface
2. Implement CRUD methods using SQLAlchemy 2.0 async API:
   - `async def get_by_id()` - use select() with where() and filter state != 2
   - `async def create()` - add model, flush (no commit), refresh, return
   - `async def update()` - validate exists, merge, flush, refresh, return
   - `async def delete()` - soft delete (set state=2), flush, return bool
   - `async def hard_delete()` - physical delete, flush, return bool
3. Implement query methods:
   - `async def get_all()` - pagination, filtering, sorting, return (items, total)
   - `async def exists()` - return bool using select with exists()
   - `async def count()` - return count with filters
4. Implement bulk operations:
   - `async def bulk_create()` - use session.add_all(), flush, return models
   - `async def bulk_update()` - use session.merge() for each, flush, return models
5. Add comprehensive docstrings following IDK pattern from base_repository.py
6. Use Jinja2 variables for dynamic content ({{ config.project.name }}, etc.)

### Phase 3: Integration
1. Render template to create reference file at `src/shared/infrastructure/base_repository_async.py`
   - Use values from config.yml (project.name = "tac-bootstrap", etc.)
   - Verify imports are correctly rendered (even though framework="none")
2. Verify both files exist and are consistent
3. Ensure docstrings and IDK comments match sync repository style
4. Validate that template can be used by CLI to generate for other projects

## Step by Step Tasks

### Task 1: Read and analyze existing base_repository.py
- Read `src/shared/infrastructure/base_repository.py` completely
- Identify all methods to replicate: get_by_id, create, update, delete, hard_delete, get_all, exists, count
- Note soft delete pattern (state != 2 filtering)
- Document docstring style, IDK tags, and invariants
- List failure modes and examples

### Task 2: Create directory structure
- Ensure `tac_bootstrap_cli/tac_bootstrap/templates/shared/` exists
- Ensure `src/shared/infrastructure/` exists

### Task 3: Create Jinja2 template base_repository_async.py.j2
- Write module-level docstring with IDK tags and responsibility
- Import AsyncSession, select, and other SQLAlchemy 2.0 async utilities
- Define generic TypeVar TModel
- Create BaseRepositoryAsync[TModel] class with constructor
- Implement all async CRUD methods using select() API
- Implement get_all with pagination, filtering, sorting
- Implement exists and count query methods
- Implement bulk_create and bulk_update
- Add comprehensive docstrings for each method following sync repo style
- Use Jinja2 syntax for config variables where appropriate
- Follow Unit of Work pattern: no session.commit(), use flush() instead

### Task 4: Render reference implementation
- Load config.yml to get rendering values
- Render template with config values:
  - config.project.name → "tac-bootstrap"
  - config.project.language → "python"
  - config.paths.app_root → "tac_bootstrap_cli"
- Write rendered file to `src/shared/infrastructure/base_repository_async.py`
- Verify file contains working Python code (even if imports are reference-only)

### Task 5: Validate dual creation
- Verify template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`
- Verify rendered file exists at `src/shared/infrastructure/base_repository_async.py`
- Check consistency between template and rendered file
- Verify all methods from sync repo are present in async version
- Verify docstrings and IDK comments are complete

### Task 6: Run validation commands
- Execute all validation commands to ensure no regressions
- Verify template can be used by CLI (if CLI implementation exists)

## Testing Strategy

### Unit Tests
No unit tests required for this task (templates are tested when CLI generates them). Manual validation:
- Template syntax is valid Jinja2
- Rendered file is valid Python syntax
- All methods from sync repository are present
- Bulk operations use session.add_all() and session.merge()
- SQLAlchemy 2.0 async API is used correctly

### Edge Cases
Template should handle:
- Empty list inputs for bulk_create and bulk_update (return empty list)
- Missing entity on update (raise ValueError)
- Soft delete idempotency (deleting already deleted entity returns False)
- Pagination with page=1 and various page_size values
- Filters with None/empty dict
- Sort by invalid field (raise ValueError)

## Acceptance Criteria

1. Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`
2. Reference file rendered at `src/shared/infrastructure/base_repository_async.py`
3. All methods from sync repository mirrored in async version:
   - get_by_id, create, update, delete, hard_delete
   - get_all (with pagination, filtering, sorting)
   - exists, count
4. Bulk operations implemented:
   - bulk_create(models: list[TModel]) -> list[TModel]
   - bulk_update(models: list[TModel]) -> list[TModel]
5. SQLAlchemy 2.0 async API used:
   - AsyncSession instead of Session
   - select() statements instead of session.query()
   - await session.execute() for all queries
6. Unit of Work pattern followed:
   - Repository methods do NOT call session.commit()
   - Use session.flush() to populate DB-generated fields
   - Caller manages transaction lifecycle
7. Soft delete functionality preserved (state != 2 filtering)
8. Docstrings follow IDK pattern from base_repository.py
9. bulk_create and bulk_update use session.add_all() and session.merge()
10. Both files exist and are consistent

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test (if CLI exists)

## Notes

1. **Framework Consideration**: This project has `framework: "none"` but templates target FastAPI projects. The rendered reference file at `src/shared/infrastructure/base_repository_async.py` serves as documentation/reference and won't execute in this project.

2. **SQLAlchemy 2.0 Migration**: The async repository uses modern SQLAlchemy 2.0 patterns exclusively:
   - `select()` instead of `session.query()`
   - `await session.execute()` instead of direct queries
   - `session.scalars()` for fetching results
   - `session.scalar()` for single values

3. **Unit of Work Pattern**: Repository does NOT commit transactions. Services/controllers manage commit/rollback. This allows composing multiple repository operations in a single transaction.

4. **Bulk Operations Atomicity**: bulk_create and bulk_update are atomic within the session. If any model fails validation or constraints, the session can be rolled back by the caller, preventing partial updates.

5. **Template Variables**: Use Jinja2 syntax sparingly - most code is static Python. Only use `{{ config.* }}` for values that genuinely differ between projects (like project name in comments).

6. **Future Enhancement**: Consider adding async context manager support (`async with repository.transaction()`) in future iterations for more ergonomic transaction management.
