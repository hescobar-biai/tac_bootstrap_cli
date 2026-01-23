# Template base_service.py - Generic CRUD Service Layer

**ADW ID:** bad795f3
**Date:** 2026-01-22
**Specification:** specs/issue-115-adw-bad795f3-sdlc_planner-template-base-service.md

## Overview

This feature implements a comprehensive, type-safe generic base service class that provides complete CRUD operations for all domain entities in TAC Bootstrap-generated FastAPI projects. Using Python generics, entity-specific services can inherit from `BaseService` and instantly gain full CRUD functionality with zero code duplication. The template enforces business logic patterns including audit trails, soft delete, and version control across all entities.

## What Was Built

- **Jinja2 template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2` - Template for FastAPI projects
- **Rendered reference implementation**: `src/shared/application/base_service.py` - Example implementation for documentation
- **PaginatedResponse[T]**: Generic pagination wrapper for list responses with metadata
- **BaseService[TCreate, TUpdate, TResponse, TModel, TDomain]**: Generic service class with 6 CRUD methods:
  - `create()` - Create entity with audit fields
  - `get_by_id()` - Retrieve single entity with 404 handling
  - `get_all()` - Paginated list with filtering and sorting
  - `update()` - Partial update with version control
  - `delete()` - Soft delete (sets state=2)
  - `hard_delete()` - Physical deletion for admin operations

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2`: Jinja2 template for base service class (584 lines)
- `src/shared/application/base_service.py`: Rendered reference implementation showing template output (585 lines)
- `specs/issue-115-adw-bad795f3-sdlc_planner-template-base-service.md`: Feature specification
- `specs/issue-115-adw-bad795f3-sdlc_planner-template-base-service-checklist.md`: Validation checklist

### Key Changes

**Generic Type System**
- Defined 5 TypeVars for complete type safety across service layer:
  - `TCreate` (bound=BaseModel) - Create DTO schema
  - `TUpdate` (bound=BaseModel) - Update DTO schema
  - `TResponse` (bound=BaseModel) - Response DTO schema
  - `TModel` - ORM model class (SQLAlchemy)
  - `TDomain` - Domain entity class
- Enables full type inference and IDE autocomplete in inherited services

**PaginatedResponse Implementation**
- Generic pagination wrapper with 5 fields: `items`, `total`, `page`, `page_size`, `total_pages`
- 1-indexed page numbers (starts at 1, not 0)
- Automatic total_pages calculation using `ceil(total / page_size)`
- Standardizes pagination across all list endpoints

**Business Logic Patterns**
- **Audit Trail**: All create/update operations automatically set `created_by`/`updated_by` from `user_id` parameter
- **Soft Delete**: `delete()` sets `state=2` instead of physical deletion, preserving data for audit and recovery
- **Version Control**: `update()` explicitly increments `version` field for optimistic locking support
- **Repository Pattern**: Service layer is database-agnostic, delegates persistence to repository via dependency injection

**Error Handling**
- Raises `HTTPException(404)` when entity not found or soft-deleted (state=2)
- Raises `HTTPException(400)` for invalid filter/sort columns (caught from repository ValueError)
- Consistent error responses across all CRUD operations

**IDK Documentation Pattern**
- All classes and methods include comprehensive "IDK" (I Don't Know) docstrings
- Documents: Responsibility, Invariants, Inputs, Outputs, Failure Modes, Collaborators, Examples
- Enables rapid codebase comprehension and maintenance

## How to Use

### Generating Projects with Base Service Template

When using TAC Bootstrap CLI to generate a FastAPI project:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap init my-project

# Select framework: FastAPI
# Template automatically includes src/shared/application/base_service.py
```

### Creating Entity-Specific Services

1. **Define your entity service by inheriting BaseService**:

```python
# src/products/application/product_service.py
from src.shared.application.base_service import BaseService
from src.products.domain.schemas import ProductCreate, ProductUpdate, ProductResponse
from src.products.infrastructure.models import ProductModel
from src.products.domain.entities import Product

class ProductService(BaseService[ProductCreate, ProductUpdate, ProductResponse, ProductModel, Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

    # Add entity-specific business logic if needed
    def apply_discount(self, product_id: str, discount_percent: float, user_id: str) -> ProductResponse:
        product = self.repository.get_by_id(product_id)
        if not product or product.state == 2:
            raise HTTPException(404, "Product not found")

        product.price = product.price * (1 - discount_percent / 100)
        product.mark_updated(user_id)
        updated = self.repository.update(product)
        return ProductResponse.model_validate(updated)
```

2. **Use in FastAPI route handlers**:

```python
# src/products/interfaces/routes.py
from fastapi import APIRouter, Depends, Query
from src.products.application.product_service import ProductService
from src.shared.application.base_service import PaginatedResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(data, user_id=current_user.id)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, service: ProductService = Depends(get_product_service)):
    return service.get_by_id(product_id)

@router.get("", response_model=PaginatedResponse[ProductResponse])
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str | None = Query(None),
    service: ProductService = Depends(get_product_service)
):
    filters = {"category": category} if category else {}
    return service.get_all(page, page_size, filters, sort_by="created_at", sort_order="desc")

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(product_id, data, user_id=current_user.id)

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    service.delete(product_id, user_id=current_user.id)
    return {"message": "Product deleted successfully"}
```

3. **Zero additional CRUD code required** - Inheritance provides complete functionality with type safety.

## Configuration

The base service template works with TAC Bootstrap project configuration:

**config.yml settings**:
- `framework: "fastapi"` - Required for FastAPI-specific imports (HTTPException, Pydantic)
- `language: "python"` - Uses Python 3.10+ features (union types with `|`)

**Dependencies required in generated projects**:
```toml
[dependencies]
fastapi = "^0.100.0"
pydantic = "^2.0.0"
```

**Repository interface contract**:
The service expects repositories to implement:
- `create(entity_data: dict) -> TModel`
- `get_by_id(entity_id: str, include_deleted: bool = False) -> TModel | None`
- `get_all(page: int, page_size: int, filters: dict, sort_by: str, sort_order: str) -> tuple[list[TModel], int]`
- `update(entity: TDomain) -> TModel`
- `delete(entity_id: str) -> None`

## Testing

### Template Validation

Verify the template renders correctly and produces valid Python:

```bash
# Validate Python syntax
python -c "import ast; ast.parse(open('src/shared/application/base_service.py').read()); print('Syntax valid')"

# Run TAC Bootstrap CLI tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Usage in Generated Projects

When testing entity-specific services in generated projects:

```python
# tests/products/test_product_service.py
import pytest
from unittest.mock import Mock
from src.products.application.product_service import ProductService
from src.products.domain.schemas import ProductCreate, ProductUpdate

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def service(mock_repository):
    return ProductService(repository=mock_repository)

def test_create_sets_audit_fields(service, mock_repository):
    # Arrange
    data = ProductCreate(name="Laptop", price=999.99, category="Electronics")
    mock_repository.create.return_value = Mock(id="123", name="Laptop", price=999.99)

    # Act
    result = service.create(data, user_id="user-456")

    # Assert
    call_args = mock_repository.create.call_args[0][0]
    assert call_args["created_by"] == "user-456"
    assert call_args["updated_by"] == "user-456"

def test_get_by_id_raises_404_when_not_found(service, mock_repository):
    # Arrange
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        service.get_by_id("nonexistent-id")
    assert exc.value.status_code == 404

def test_delete_performs_soft_delete(service, mock_repository):
    # Arrange
    mock_entity = Mock(id="123", state=0)
    mock_repository.get_by_id.return_value = mock_entity

    # Act
    service.delete("123", user_id="user-789")

    # Assert
    assert mock_entity.state == 2  # Soft deleted
    assert mock_entity.updated_by == "user-789"
    mock_repository.update.assert_called_once()
```

## Notes

### Design Decisions

**user_id = None Support**
- Allows system/anonymous operations for migrations, background jobs, health checks
- `created_by`/`updated_by` set to `None` indicates system action

**Filter Validation in Repository**
- Service passes filters directly to repository without validation
- Repository has schema knowledge and validates column names
- Invalid filters raise ValueError → caught and converted to HTTPException(400)

**Explicit Version Increment**
- BaseService explicitly increments version in `update()` method
- Makes version control framework-agnostic and visible in business logic
- Repository can still add optimistic locking checks at persistence layer

**No Authorization in Service**
- Authorization happens at route layer via FastAPI dependencies
- Service handles business logic only, maintaining separation of concerns

**Transaction Management**
- Repository handles transactions (each method is atomic)
- Service stays clean and database-agnostic
- Multi-operation transactions use UnitOfWork pattern (future enhancement)

### Related Features

- **Issue #111**: Template base_entity.py (domain layer with state, version, audit fields)
- **Issue #113**: Template base_schema.py (DTO schemas: BaseCreate, BaseUpdate, BaseResponse)
- **ai_docs/doc/create-crud-entity/WORKFLOW.md**: Complete CRUD entity creation workflow

### Architecture Pattern

The base service implements the **Service Layer** pattern in Domain-Driven Design (DDD):

```
┌─────────────────────────────────────────┐
│ Routes (FastAPI)                         │  ← Authorization, request validation
├─────────────────────────────────────────┤
│ Service (BaseService)                    │  ← Business logic, audit, versioning
├─────────────────────────────────────────┤
│ Repository                               │  ← Persistence, queries, transactions
├─────────────────────────────────────────┤
│ ORM Models (SQLAlchemy)                  │  ← Database mapping
└─────────────────────────────────────────┘
```

### Future Enhancements

- Async variants of CRUD methods for high-performance APIs
- Complex filtering operators (gt, lt, contains, between)
- Bulk operations (create_many, update_many, delete_many)
- Transaction context manager for multi-operation atomicity
- Domain event publishing from service methods
- Caching layer integration (Redis, in-memory)
- Automated audit log generation

### Zero Regression Validation

All validation commands passed with zero regressions:
- ✅ Python syntax validation
- ✅ Unit tests (pytest)
- ✅ Linting (ruff)
- ✅ Type checking (mypy)
- ✅ CLI smoke test

Implementation fully meets all 18 acceptance criteria from specification.
