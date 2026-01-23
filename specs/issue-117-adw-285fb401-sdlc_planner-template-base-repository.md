# Feature: Template base_repository.py

## Metadata
issue_number: `117`
adw_id: `285fb401`
issue_json: `{"number":117,"title":"Tarea 1.4: Template base_repository.py","body":"/feature\n**Ganancia**: Repositorio generico que abstrae SQLAlchemy. Elimina queries repetitivas y garantiza que soft-deleted items no aparezcan por default.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2`\n2. Crear renderizado en raiz: `src/shared/infrastructure/base_repository.py`\n2. Definir `BaseRepository[TModel]` con SQLAlchemy Session\n3. Metodos:\n   - `get_by_id(entity_id: str) -> TModel | None` (excluye state=2)\n   - `get_all(page, page_size, filters, sort_by, sort_order) -> tuple[list[TModel], int]`\n   - `create(model: TModel) -> TModel`\n   - `update(model: TModel) -> TModel`\n   - `delete(entity_id: str) -> bool` (SET state=2)\n   - `hard_delete(entity_id: str) -> bool` (DELETE fisico)\n   - `exists(entity_id: str) -> bool`\n   - `count(filters: dict) -> int`\n4. Filtros dinamicos: recibe dict y aplica `==` por cada key/value\n5. Ordenamiento: valida que sort_by es un campo del modelo\n\n**Criterios de aceptacion**:\n- Todas las queries excluyen state=2 por default\n- Paginacion usa offset/limit correctamente\n- Maneja session commit/rollback\n\n# PLAN: TAC Bootstrap v0.3 - Version Robusta\n\n## Objetivo\n\nEvolucionar `tac_bootstrap_cli` de un generador de estructura agentic a una herramienta completa que tambien genera codigo de aplicacion (entidades CRUD con DDD), documentacion fractal automatica, y validacion multi-capa. Basado en los patrones documentados en `ai_docs/doc/create-crud-entity/`.\n\n## Estructura del Plan\n\n- **7 Fases**, **3 Iteraciones** de ejecucion\n- Cada tarea tiene: tipo (feature/chore/bug), descripcion, ganancia, instrucciones, criterios de aceptacion\n- Fases 1-5 (codigo) y Fases 6-7 (docs fractal) son independientes\n\n## REGLA CRITICA: Dual Creation Pattern\n\n**IMPORTANTE**: Este proyecto es TANTO el generador como un proyecto de referencia. Por lo tanto, cada tarea que cree un template DEBE crear DOS archivos:\n\n1. **Template Jinja2** en `tac_bootstrap_cli/tac_bootstrap/templates/` → usado por el CLI para generar en OTROS proyectos\n2. **Archivo renderizado** en la raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/`) → para que ESTE proyecto tambien lo tenga\n\n### Mapeo de rutas (template → archivo en raiz):\n\n| Template (tac_bootstrap_cli/tac_bootstrap/templates/) | Archivo en raiz (/Volumes/MAc1/Celes/tac_bootstrap/) |\n|---|---|\n| `shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |\n| `shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |\n| `shared/base_service.py.j2` | `src/shared/application/base_service.py` |\n| `shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |\n| `shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |\n| `shared/database.py.j2` | `src/shared/infrastructure/database.py` |\n| `shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |\n| `shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |\n| `shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |\n| `shared/health.py.j2` | `src/shared/api/health.py` |\n| `capabilities/crud_basic/domain_entity.py.j2` | *(se genera bajo demanda con `generate entity`)* |\n| `capabilities/crud_basic/schemas.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/service.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/repository.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/routes.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/orm_model.py.j2` | *(se genera bajo demanda)* |\n| `scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |\n| `scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |\n| `scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |\n| `claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |\n| `config/canonical_idk.yml.j2` | `canonical_idk.yml` |\n\n### Excepcion: Templates de capabilities (crud_basic, crud_authorized)\nLos templates de `capabilities/` NO se renderizan automaticamente en la raiz. Solo se generan cuando el usuario ejecuta `tac-bootstrap generate entity <name>`. Por eso no tienen archivo en raiz.\n\n### Contexto: config.yml de ESTE proyecto\n\nEl archivo `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` contiene la configuracion real de este proyecto. Los templates usan estas variables con la sintaxis `{{ config.project.name }}`, `{{ config.project.language }}`, `{{ config.paths.app_root }}`, etc.\n\n**Valores actuales relevantes para renderizado:**\n```yaml\nproject:\n  name: \"tac-bootstrap\"\n  language: \"python\"\n  framework: \"none\"         # NOTA: no es FastAPI, pero architecture=ddd\n  architecture: \"ddd\"\n  package_manager: \"uv\"\n\npaths:\n  app_root: \"tac_bootstrap_cli\"   # Codigo del CLI vive aqui\n  scripts_dir: \"scripts\"\n  adws_dir: \"adws\"\n\ncommands:\n  test: \"uv run pytest\"\n  lint: \"uv run ruff check .\"\n```\n\n**IMPORTANTE - Consideracion de framework:**\n- Este proyecto tiene `framework: \"none\"` (no es una app FastAPI, es un CLI)\n- Las base classes (Fase 1) son templates para proyectos FastAPI que el CLI GENERA\n- Para la dual creation en la raiz: renderizar los templates como **ejemplo/referencia** usando los valores de config.yml, pero los imports de FastAPI/SQLAlchemy son de referencia (no se ejecutan en este proyecto)\n- Los scripts de Fase 6 SI son funcionales en este proyecto (Python, language=python)\n\n### Como implementar la dual creation:\n1. Crear el template `.j2` con variables Jinja2 (`{{ config.project.name }}`, etc.)\n2. Para renderizar el archivo en raiz, usar los valores de `config.yml`:\n   - `config.project.name` → `\"tac-bootstrap\"`\n   - `config.project.language` → `\"python\"`\n   - `config.paths.app_root` → `\"tac_bootstrap_cli\"`\n   - `config.commands.test` → `\"uv run pytest\"`\n3. Guardar el resultado en la ruta correspondiente de la raiz\n4. Verificar que AMBOS archivos existen y son consistentes\n\n### Ejemplo concreto de renderizado:\n\n**Template** (`templates/scripts/run_generators.sh.j2`):\n```bash\nREPO_ROOT=\"{{ config.paths.app_root | default('.') }}\"\n```\n\n**Renderizado en raiz** (`scripts/run_generators.sh`):\n```bash\nREPO_ROOT=\"tac_bootstrap_cli\"\n```\n\n**Template** (`templates/config/canonical_idk.yml.j2`):\n```yaml\n# Canonical IDK Vocabulary for {{ config.project.name }}\n{% if config.project.language == \"python\" %}\n  backend:\n    - api-gateway, routing, ...\n{% endif %}\n```\n\n**Renderizado en raiz** (`canonical_idk.yml`):\n```yaml\n# Canonical IDK Vocabulary for tac-bootstrap\n  backend:\n    - api-gateway, routing, ...\n```"}`

## Feature Description

This feature creates a generic repository base class that abstracts SQLAlchemy operations for Domain-Driven Design (DDD) patterns. The `BaseRepository` eliminates repetitive query code, enforces soft-delete patterns (state=2 excluded by default), and provides transactional CRUD operations with pagination, filtering, and sorting capabilities.

The repository follows the Dual Creation Pattern: creating both a Jinja2 template for code generation and a rendered reference implementation in the project root.

## User Story

As a developer using TAC Bootstrap CLI
I want a generic repository base class template
So that I can generate projects with clean, consistent data access patterns that automatically handle soft deletes, pagination, and common CRUD operations without repetitive boilerplate code.

## Problem Statement

When building DDD applications with SQLAlchemy, developers repeatedly write:
- Boilerplate CRUD operations for each entity
- Soft-delete filtering logic (`WHERE state != 2`) in every query
- Pagination calculations with offset/limit
- Dynamic filtering and sorting logic
- Transaction management (commit/rollback) in every method

This leads to code duplication, inconsistencies in soft-delete enforcement, and increased maintenance burden. A generic base repository eliminates this repetition and guarantees consistent behavior across all entities.

## Solution Statement

Create a `BaseRepository[TModel]` generic class using Python's TypeVar and Generic features. The class will:

1. **Enforce soft-delete transparency**: Automatically filter out `state=2` entities in all queries
2. **Provide transactional methods**: Each method handles its own commit/rollback for safety
3. **Support dynamic filtering**: Accept dict of filters and apply equality checks
4. **Enable sorting with validation**: Validate sort fields against model attributes
5. **Handle pagination correctly**: Use offset/limit with total count calculation
6. **Distinguish logical vs physical deletes**: `delete()` for soft-delete, `hard_delete()` for physical removal

The implementation follows established patterns from `base_entity.py.j2` and `base_service.py.j2` templates, ensuring consistency across the DDD layers.

## Relevant Files

### Existing Templates (for pattern reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2` - Entity base class with state enumeration (EntityState: INACTIVE=0, ACTIVE=1, DELETED=2)
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2` - Service layer patterns, shows how repository is consumed
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_schema.py.j2` - Schema patterns for request/response models

### Configuration
- `config.yml` - Project configuration with values for template rendering (project.name, paths.app_root, etc.)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` - Jinja2 template for BaseRepository (to be created)
- `src/shared/infrastructure/base_repository.py` - Rendered reference implementation (to be created)

## Implementation Plan

### Phase 1: Foundation
1. Read existing templates to understand patterns:
   - IDK documentation format (Module, Responsibility, Key Components, Invariants, Usage Examples)
   - EntityState enumeration values (0=INACTIVE, 1=ACTIVE, 2=DELETED)
   - Type annotation patterns using Generic[T]
   - Error handling patterns
2. Create directory structure if needed: `src/shared/infrastructure/`
3. Review config.yml to prepare for template rendering

### Phase 2: Core Implementation
1. Create `base_repository.py.j2` template with:
   - Comprehensive IDK docstring following established format
   - Generic type parameter: `TModel = TypeVar("TModel")`
   - SQLAlchemy Session injection in `__init__`
   - All 8 required methods with proper type annotations
   - Soft-delete filter logic in all query methods
   - Transaction management (commit on success, rollback on exception)
   - Input validation (page >= 1, page_size >= 1, valid sort_by field)
   - Dynamic filtering using equality operators
2. Implement each method following these specifications:
   - `get_by_id(entity_id: str) -> TModel | None`: Filter by id AND state != 2
   - `get_all(page: int, page_size: int, filters: Dict[str, Any] | None, sort_by: str | None, sort_order: str) -> tuple[list[TModel], int]`: Pagination with total count, apply filters, validate sort field
   - `create(model: TModel) -> TModel`: Insert and commit
   - `update(model: TModel) -> TModel`: Validate exists (state != 2), merge, commit
   - `delete(entity_id: str) -> bool`: Set state=2, return True if successful, False if not found
   - `hard_delete(entity_id: str) -> bool`: Physical DELETE, return True if successful
   - `exists(entity_id: str) -> bool`: Check existence with state != 2 filter
   - `count(filters: Dict[str, Any] | None) -> int`: Count with state != 2 filter + user filters

### Phase 3: Integration
1. Render template to `src/shared/infrastructure/base_repository.py` using config.yml values
2. Verify both files (template and rendered) exist and are consistent
3. Validate that patterns align with existing base_entity.py and base_service.py

## Step by Step Tasks

### Task 1: Research existing patterns
- Read `base_entity.py.j2` to understand EntityState enum and audit field patterns
- Read `base_service.py.j2` to understand how repository is consumed by service layer
- Read `config.yml` to identify values for template rendering
- Document key patterns: IDK format, type annotations, error handling

### Task 2: Create base_repository.py.j2 template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2`
- Add comprehensive IDK docstring with Module, Responsibility, Key Components, Invariants, Usage Examples
- Import required types: `Generic, TypeVar, Dict, Any` from typing, `Session` from SQLAlchemy
- Define `TModel = TypeVar("TModel")` and `class BaseRepository(Generic[TModel])`
- Implement `__init__(self, session: Session, model_class: type[TModel])`
- Implement all 8 methods with proper docstrings, type hints, and error handling
- Add soft-delete filter `.filter(TModel.state != 2)` to all query methods
- Add transaction management with try/except/rollback pattern
- Validate inputs: page >= 1, page_size >= 1, sort_by in model attributes
- Use Jinja2 variables where appropriate (though minimal in this shared base class)

### Task 3: Render reference implementation
- Create directory `src/shared/infrastructure/` if it doesn't exist
- Render template to `src/shared/infrastructure/base_repository.py` using config.yml values
- Since this is a shared base class, rendering mostly removes Jinja2 syntax (minimal variables used)
- Verify file structure matches DDD conventions

### Task 4: Validate consistency
- Compare template and rendered file for consistency
- Verify all 8 methods are present with correct signatures
- Check that soft-delete filtering appears in all query methods
- Verify transaction management in all mutation methods
- Ensure input validation in get_all, update methods

### Task 5: Execute validation commands
- Run `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run `cd tac_bootstrap_cli && uv run ruff check .`
- Run `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests

While unit tests are not created in this task (repository is a template for generation), the following test scenarios should be considered for projects using this template:

1. **Soft-delete filtering**:
   - `get_by_id()` returns None for state=2 entities
   - `get_all()` excludes state=2 entities
   - `exists()` returns False for state=2 entities
   - `count()` excludes state=2 entities

2. **CRUD operations**:
   - `create()` successfully inserts and returns model
   - `update()` raises ValueError if entity not found or state=2
   - `delete()` sets state=2 and returns True
   - `delete()` returns False if entity not found
   - `hard_delete()` physically removes entity

3. **Pagination**:
   - `get_all()` returns correct page with offset/limit
   - Total count is accurate regardless of page
   - Empty list returned if page exceeds total pages

4. **Filtering and sorting**:
   - Dynamic filters apply correctly with equality operator
   - Invalid sort_by field raises ValueError
   - Sort order (asc/desc) works correctly

5. **Transaction management**:
   - Successful operations commit
   - Exceptions trigger rollback
   - Session state is consistent after errors

### Edge Cases

1. **Invalid pagination inputs**: page=0, page_size=0, page=-1 should raise ValueError
2. **Non-existent entity_id**: get_by_id returns None, update/delete handle gracefully
3. **Already soft-deleted entity**: delete() returns False (idempotent), update() raises ValueError
4. **Empty filters dict**: Should work as no-op, return all active entities
5. **Invalid sort_by field**: Should raise ValueError with clear message
6. **Database connection errors**: Should rollback and propagate exception
7. **Concurrent updates**: Repository doesn't handle locking (service layer responsibility with version field)

## Acceptance Criteria

1. **Template creation**:
   - [x] File exists at `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2`
   - [x] Template uses Jinja2 syntax for configurable elements
   - [x] Follows IDK documentation format with comprehensive docstrings

2. **Rendered file creation**:
   - [x] File exists at `src/shared/infrastructure/base_repository.py`
   - [x] Rendered using values from `config.yml`
   - [x] Follows DDD directory structure

3. **Soft-delete enforcement**:
   - [x] All queries include `.filter(TModel.state != 2)` by default
   - [x] `get_by_id()` returns None for soft-deleted entities
   - [x] `get_all()`, `exists()`, `count()` exclude state=2

4. **Method implementations**:
   - [x] All 8 methods implemented with correct signatures
   - [x] Type annotations use `TModel` generic, `Dict[str, Any]` for filters
   - [x] Each method has comprehensive docstring

5. **Pagination**:
   - [x] Uses `offset = (page - 1) * page_size` and `limit = page_size`
   - [x] Returns tuple of (list[TModel], total_count)
   - [x] Validates page >= 1, page_size >= 1

6. **Transaction management**:
   - [x] Each mutation method (create, update, delete, hard_delete) commits on success
   - [x] Exception handling with rollback in all mutation methods
   - [x] Session state is clean after operations

7. **Dynamic filtering**:
   - [x] Accepts `Dict[str, Any]` for filters
   - [x] Applies equality (`==`) operator for each key/value pair
   - [x] Combines with state != 2 filter

8. **Sorting validation**:
   - [x] Validates `sort_by` is an attribute of TModel
   - [x] Raises ValueError with descriptive message for invalid field
   - [x] Supports asc/desc sort order

9. **Error handling**:
   - [x] `update()` raises ValueError if entity not found or soft-deleted
   - [x] Invalid inputs raise ValueError with clear messages
   - [x] Database exceptions propagate after rollback

## Validation Commands

Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions

1. **Synchronous vs Async**: This task creates the synchronous version (`base_repository.py`). Async version (`base_repository_async.py`) will be a separate task per the plan.

2. **Transaction scope**: Each repository method is a unit of work (commits/rolls back within the method). Service layer can orchestrate multi-repository transactions if needed.

3. **Equality-only filtering**: Per requirements, filters use `==` operator only. Advanced filtering (>, <, LIKE, IN) can be added in subclasses or future enhancements.

4. **Sort validation**: Using `hasattr(model_class, sort_by)` to validate sort fields prevents SQL injection and provides clear error messages.

5. **Boolean returns for delete**: `delete()` and `hard_delete()` return bool for idempotent behavior. Service layer decides if False should raise exception.

6. **State filter placement**: State filter applied BEFORE user filters ensures soft-deleted entities never appear, even with complex filter combinations.

### Auto-Resolved Clarifications Summary

Key decisions made during planning:
- Use synchronous SQLAlchemy sessions (sync version)
- Return None for soft-deleted entities in get_by_id
- Always exclude state=2 in all queries before applying user filters
- Return False for delete operations on non-existent/already-deleted entities
- exists() only returns True for active entities (state != 2)
- Raise ValueError for invalid sort_by fields
- Repository handles commit/rollback per method
- Use Dict[str, Any] for filters, equality-only operators
- update() validates existence and raises ValueError if not found
- Validate pagination inputs, return empty list for out-of-range pages

### Future Enhancements

- Advanced filtering with operators (>, <, LIKE, IN, BETWEEN)
- Bulk operations (bulk_create, bulk_update, bulk_delete)
- Query optimization hints (eager loading, join strategies)
- Audit log integration
- Cache layer integration
- Async version (separate task: base_repository_async.py)
