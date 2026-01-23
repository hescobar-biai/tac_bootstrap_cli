# Base Schema Template - Pydantic DTOs for API Layer

**ADW ID:** 08b00a3f
**Date:** 2026-01-22
**Specification:** specs/issue-113-adw-08b00a3f-sdlc_planner-template-base-schema.md

## Overview

This feature implements standardized Pydantic base schema classes (DTOs) that separate API-layer concerns from domain entity models. The template provides reusable foundation classes for Create, Update, and Response patterns in CRUD operations, eliminating 30+ lines of boilerplate per entity across generated projects.

## What Was Built

- **BaseCreate**: Empty foundation class for entity creation DTOs (POST requests)
- **BaseUpdate**: Independent foundation class for partial update DTOs (PATCH requests)
- **BaseResponse**: Response DTO with common fields (id, state, version, timestamps, audit trail)
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_schema.py.j2`
- **Rendered Implementation**: `src/shared/domain/base_schema.py` (dogfooding pattern for tac_bootstrap itself)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_schema.py.j2`: Jinja2 template for base schema classes (255 lines, new file)
- `src/shared/domain/base_schema.py`: Rendered implementation used by tac_bootstrap (255 lines, new file)
- `specs/issue-113-adw-08b00a3f-sdlc_planner-template-base-schema.md`: Planning specification (238 lines)
- `specs/issue-113-adw-08b00a3f-sdlc_planner-template-base-schema-checklist.md`: Review checklist (78 lines)

### Key Changes

**1. BaseCreate Class (src/shared/domain/base_schema.py:56-105)**
- Empty Pydantic BaseModel serving as foundation for creation DTOs
- No common fields - entities inherit and add their specific required fields
- Excludes system-managed fields (id, timestamps, audit data)
- Service layer injects audit fields based on authenticated user context

**2. BaseUpdate Class (src/shared/domain/base_schema.py:108-159)**
- Independent Pydantic BaseModel for partial updates (no inheritance from BaseCreate)
- Pattern supports PATCH operations with selective field updates
- Entities inherit and add fields as `Optional[T]`
- Enables clients to send only changed fields

**3. BaseResponse Class (src/shared/domain/base_schema.py:162-255)**
- Pydantic BaseModel with 7 common response fields:
  - `id: UUID` - Unique identifier
  - `state: str` - Entity state (active, inactive, deleted)
  - `version: int` - Version number for optimistic locking
  - `created_at: datetime` - UTC creation timestamp
  - `updated_at: datetime` - UTC last update timestamp
  - `created_by: UUID` - User ID who created the resource
  - `updated_by: UUID` - User ID who last updated the resource
- `model_config = ConfigDict(from_attributes=True)` enables ORM model conversion
- Each field uses `Field()` with descriptions and examples

**4. Comprehensive IDK Documentation**
- Module-level docstring explaining responsibilities and usage
- Each class includes extensive IDK pattern documentation:
  - Responsibility and invariants
  - Usage patterns and collaborators
  - Code examples showing inheritance patterns
  - Failure modes and related documentation

**5. Design Decisions**
- **No template variables**: Template is project-agnostic, renders identically to source
- **Audit field separation**: created_by/updated_by excluded from Create/Update (security concern)
- **BaseUpdate independence**: No inheritance from BaseCreate (different purposes)
- **Field types**: UUID for ids, datetime for timestamps, str for state, int for version

## How to Use

### For Project Generation

When generating a new project with TAC Bootstrap CLI, the base_schema.py template will be rendered to `src/shared/domain/base_schema.py` in the generated project.

### Creating Entity Schemas

```python
# 1. Define Create schema (user input for POST)
class ProductCreate(BaseCreate):
    name: str
    price: float
    category: str

# 2. Define Update schema (partial updates for PATCH)
class ProductUpdate(BaseUpdate):
    name: str | None = None
    price: float | None = None
    category: str | None = None

# 3. Define Response schema (API responses for GET/POST/PATCH)
class ProductResponse(BaseResponse):
    name: str
    price: float
    category: str
```

### Service Layer Integration

```python
# POST /products - Create resource
def create_product(data: ProductCreate, current_user: User) -> ProductResponse:
    entity = Product(
        code=generate_code(),
        name=data.name,
        price=data.price,
        category=data.category,
        created_by=current_user.id  # injected by service
    )
    repository.save(entity)
    return ProductResponse.model_validate(entity)

# PATCH /products/{id} - Partial update
def update_product(id: UUID, data: ProductUpdate, current_user: User) -> ProductResponse:
    entity = repository.get(id)
    if data.name is not None:
        entity.name = data.name
    if data.price is not None:
        entity.price = data.price
    entity.mark_updated(current_user.id)  # injected by service
    repository.save(entity)
    return ProductResponse.model_validate(entity)

# GET /products/{id} - Retrieve resource
def get_product(id: UUID) -> ProductResponse:
    entity = repository.get(id)
    return ProductResponse.model_validate(entity)
```

## Configuration

No configuration required. The template is static and project-agnostic.

### Customization Options

To customize for specific entity needs:

1. **State enum**: Override `state: str` with entity-specific enum
   ```python
   class ProductResponse(BaseResponse):
       state: ProductState  # enum instead of str
   ```

2. **Additional fields**: Add entity-specific fields to each schema
   ```python
   class ProductResponse(BaseResponse):
       name: str
       sku: str
       tags: list[str]
   ```

## Testing

### Validation Commands

```bash
# Validate imports
python -c "from src.shared.domain.base_schema import BaseCreate, BaseUpdate, BaseResponse; print('Import successful')"

# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing

```python
# Test BaseResponse from_attributes
from src.shared.domain.base_schema import BaseResponse
from uuid import uuid4
from datetime import datetime

# Create mock entity data
entity_data = {
    "id": uuid4(),
    "state": "active",
    "version": 1,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "created_by": uuid4(),
    "updated_by": uuid4(),
}

# Validate ORM compatibility
response = BaseResponse.model_validate(entity_data)
print(f"BaseResponse validated: {response.id}")
```

## Notes

### Architecture Pattern

This template follows the **DTO (Data Transfer Object)** pattern to separate concerns:

- **Domain Layer** (base_entity.py): Business logic, validation, entity lifecycle
- **API Layer** (base_schema.py): Request/response DTOs, API contracts
- **Service Layer**: Maps between schemas and entities, injects audit data

### Security Considerations

Audit fields (created_by, updated_by) are intentionally excluded from BaseCreate and BaseUpdate to prevent users from manipulating audit data. The service layer should inject these fields based on the authenticated user context.

### Dogfooding Pattern

The rendered `src/shared/domain/base_schema.py` serves dual purpose:
1. Example for developers using the template
2. Actual implementation used by tac_bootstrap itself

### Related Features

- **Issue #111**: base_entity.py template (domain layer counterpart)
- `app_docs/feature-a1a5289c-base-entity-template.md`: Entity implementation reference
- `ai_docs/doc/create-crud-entity/`: Full CRUD entity documentation

### Future Enhancements

- Add Jinja2 variables for optional field customization
- Generate example schemas for common entities (User, Product)
- Add validation rules base classes
- Support for nested schemas and relationships
- Pagination response wrappers
- OpenAPI schema generation utilities
