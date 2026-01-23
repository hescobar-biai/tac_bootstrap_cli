# CRUD Templates Capability

**ADW ID:** feature_2_2
**Date:** 2026-01-23
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/feature_2_2/specs/issue-142-adw-feature_2_2-sdlc_planner-crud-templates-capability.md

## Overview

This feature implements a complete set of Jinja2 templates that generate vertical slice CRUD functionality for entities. The templates transform an `EntitySpec` (entity specification with name, fields, and metadata) into production-ready Python code following DDD patterns and FastAPI + SQLAlchemy best practices.

## What Was Built

- **Domain Models**: Extended `models.py` with `FieldSpec` and `EntitySpec` classes for entity specification
- **6 Jinja2 Templates** in `templates/capabilities/crud_basic/`:
  - `domain_entity.py.j2` - Domain entity with business logic
  - `schemas.py.j2` - Pydantic schemas (Create, Update, Response)
  - `orm_model.py.j2` - SQLAlchemy ORM model
  - `repository.py.j2` - Repository with conditional query methods
  - `service.py.j2` - Service layer with business rules
  - `routes.py.j2` - FastAPI REST endpoints
- **Comprehensive Tests**: 656 lines of tests validating template rendering and code generation

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Added `FieldType`, `FieldSpec`, and `EntitySpec` models with validation for field names, type conversion properties (snake_name, plural_name, table_name), and comprehensive docstrings

### New Files Created

Templates:
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/domain_entity.py.j2`: Domain entity class inheriting from `Entity` base with type discriminator, fields mapped from `FieldSpec`, and business logic methods (validate, calculate_totals)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/schemas.py.j2`: Pydantic schemas for Create (required fields), Update (all optional), and Response (includes base fields like id, created_at, etc.)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/orm_model.py.j2`: SQLAlchemy model with automatic type mapping from `FieldType` to SQLAlchemy column types, conditional indexes based on `indexed` flag
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/repository.py.j2`: Repository extending `BaseRepository` with conditional query methods (`get_by_X` for indexed fields, `search` for text fields)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/service.py.j2`: Service layer with dependency injection and business rules application
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/routes.py.j2`: FastAPI router with 5 CRUD endpoints (create, get, list, update, delete)

Tests:
- `tac_bootstrap_cli/tests/test_crud_templates.py`: Comprehensive test suite with 656 lines covering all templates, edge cases, and validation scenarios

### Key Changes

**Domain Models** (tac_bootstrap_cli/tac_bootstrap/domain/models.py:132-625):
- Added `FieldType` enum with 9 supported data types (str, int, float, bool, datetime, uuid, text, decimal, json)
- Implemented `FieldSpec` with validation for snake_case field names and reserved name checking
- Implemented `EntitySpec` with computed properties for name transformations (snake_name, plural_name, table_name)

**Template Design Patterns**:
- All templates use IDK (Intent-Dependency-Knowledge) docstring format
- Conditional imports based on field types (e.g., only import UUID if uuid fields present)
- Type mapping dictionaries in Jinja2 for consistent Python and SQLAlchemy types
- Conditional method generation (repository methods only for indexed fields)
- Comprehensive Field() validation with max_length, nullable, and default value handling

**Test Coverage**:
- Rendering validation for all 6 templates
- Syntax validation using Python's compile()
- Content validation for classes, methods, imports
- Edge case testing (nullable fields, indexed fields, max_length, all field types)
- End-to-end integration tests validating complete vertical slice

## How to Use

### 1. Define an Entity Specification

```python
from tac_bootstrap.domain.models import EntitySpec, FieldSpec, FieldType

entity_spec = EntitySpec(
    name="Product",  # PascalCase
    capability="inventory",  # kebab-case
    fields=[
        FieldSpec(name="code", type=FieldType.STR, indexed=True, max_length=50),
        FieldSpec(name="name", type=FieldType.STR, max_length=200),
        FieldSpec(name="price", type=FieldType.DECIMAL),
        FieldSpec(name="stock", type=FieldType.INT, default=0),
        FieldSpec(name="active", type=FieldType.BOOL, default=True),
    ]
)
```

### 2. Render Templates

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

template_repo = TemplateRepository()

# Prepare context
context = {
    "config": tac_config,  # TACConfig instance
    "entity": entity_spec
}

# Render each template
domain_code = template_repo.render("capabilities/crud_basic/domain_entity.py.j2", context)
schemas_code = template_repo.render("capabilities/crud_basic/schemas.py.j2", context)
orm_code = template_repo.render("capabilities/crud_basic/orm_model.py.j2", context)
repository_code = template_repo.render("capabilities/crud_basic/repository.py.j2", context)
service_code = template_repo.render("capabilities/crud_basic/service.py.j2", context)
routes_code = template_repo.render("capabilities/crud_basic/routes.py.j2", context)
```

### 3. Generated Code Structure

The templates generate a complete vertical slice:

```
inventory/product/
├── domain.py          # Product(Entity) with business logic
├── schemas.py         # ProductCreate, ProductUpdate, ProductResponse
├── orm_model.py       # ProductModel(Base) for SQLAlchemy
├── repository.py      # ProductRepository with get_by_code()
├── service.py         # ProductService with business rules
└── routes.py          # FastAPI router with /products endpoints
```

## Configuration

### Field Type Mapping

The templates automatically map `FieldType` to appropriate types:

**Python Types** (domain_entity.py.j2):
- `str` → `str`
- `int` → `int`
- `float` → `float`
- `bool` → `bool`
- `datetime` → `datetime`
- `uuid` → `UUID`
- `text` → `str`
- `decimal` → `Decimal`
- `json` → `Dict[str, Any]`

**SQLAlchemy Types** (orm_model.py.j2):
- `str` → `String(max_length)` (default 255)
- `int` → `Integer`
- `float` → `Float`
- `bool` → `Boolean`
- `datetime` → `DateTime(timezone=True)`
- `uuid` → `String(36)`
- `text` → `Text`
- `decimal` → `Numeric(precision=10, scale=2)`
- `json` → `JSON`

### Conditional Generation

**Repository Methods**:
- `get_by_{field_name}()` generated only for fields with `indexed=True`
- `search()` method generated only if entity has string/text fields

**ORM Indexes**:
- Database indexes created only for fields with `indexed=True`

**Nullable Fields**:
- Create schema: required (no default)
- Update schema: all fields Optional
- Domain entity: `type | None = None` if nullable=True

## Testing

Run the complete test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py -v
```

Run specific test categories:

```bash
# Test domain entity template
cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py::test_domain_entity_renders -v

# Test all templates with edge cases
cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py -v -k "edge_cases"

# Test conditional generation
cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py -v -k "conditional"
```

Run full validation (tests + linting + type checking):

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

**Design Decisions**:

1. **IDK Documentation Pattern**: All generated code uses Intent-Dependency-Knowledge docstrings for consistent documentation across the codebase
2. **Base Class Dependencies**: Templates assume shared base classes exist (`Entity`, `BaseRepository`, `BaseService`, etc.) - the CLI should validate these before generation
3. **Relative Imports**: Templates use relative imports within the generated module (`.domain`, `.schemas`) for portability
4. **No Authentication**: Route templates don't include auth decorators - authentication is a cross-cutting concern handled at the application level
5. **Soft Delete**: DELETE endpoints use soft delete (mark deleted_at) rather than physical deletion
6. **Simple Pagination**: List endpoints use basic offset/limit pagination
7. **Conditional Complexity**: Repository and ORM templates include conditional logic to generate only relevant methods/indexes based on field properties

**Limitations**:

- Simple pluralization (name + "s") - no irregular plurals (person → people)
- No support for relationships between entities (foreign keys, joins)
- No complex validations in domain entity (placeholders only)
- No business calculations implemented (placeholders only)

**Next Steps**:

This feature is part of Phase 2 (CRUD Generation) in the TAC Bootstrap roadmap. Following features:
- Task 2.3: `GenerateService` to orchestrate template rendering and file writing
- Task 2.4: CLI command `tac-bootstrap generate entity` to expose generation functionality
- Task 2.5: Interactive entity wizard to build `EntitySpec` from user prompts
