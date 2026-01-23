# Template base_repository.py

**ADW ID:** 285fb401
**Date:** 2026-01-22
**Specification:** specs/issue-117-adw-285fb401-sdlc_planner-template-base-repository.md

## Overview

This feature implements a generic repository base class template that abstracts SQLAlchemy operations for Domain-Driven Design (DDD) patterns. The `BaseRepository[TModel]` eliminates repetitive CRUD query code, automatically enforces soft-delete patterns (state=2 excluded by default), and provides transactional operations with pagination, filtering, and sorting capabilities. Following the Dual Creation Pattern, both a Jinja2 template and a rendered reference implementation were created.

## What Was Built

- Generic `BaseRepository[TModel]` class using Python TypeVar for type safety
- 8 core CRUD methods with automatic soft-delete filtering
- Transaction management with commit/rollback in all mutation operations
- Dynamic filtering system accepting Dict[str, Any] with equality operators
- Pagination with offset/limit and total count calculation
- Sort validation to prevent SQL injection
- Comprehensive IDK documentation with usage examples
- Dual file creation: Jinja2 template + rendered reference implementation

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2`: Jinja2 template for code generation in target projects (625 lines)
- `src/shared/infrastructure/base_repository.py`: Rendered reference implementation for this project (625 lines)

### Key Changes

**Generic Type System:**
- Implements `TModel = TypeVar("TModel")` for type-safe repository operations
- `BaseRepository(Generic[TModel])` allows inheritance with specific model types
- Type hints throughout ensure IDE autocomplete and type checking work correctly

**Soft-Delete Enforcement:**
- All query methods include `.filter(self.model_class.state != 2)` before applying user filters
- Methods affected: `get_by_id()`, `get_all()`, `exists()`, `count()`
- Ensures soft-deleted entities (state=2) never appear in query results
- Separate `hard_delete()` method for physical deletion when needed

**Transaction Management:**
- Each mutation method (create, update, delete, hard_delete) wraps operations in try/except
- Successful operations call `self.session.commit()`
- Exceptions trigger `self.session.rollback()` and re-raise
- Ensures database consistency even when operations fail

**Dynamic Filtering:**
- Accepts `filters: Dict[str, Any] | None` parameter
- Iterates over dict items and applies `getattr(self.model_class, key) == value` for each filter
- Combines user filters with state != 2 filter using `.filter()` chaining
- Example: `{"category": "electronics", "status": "active"}` becomes `WHERE state != 2 AND category = 'electronics' AND status = 'active'`

**Pagination Implementation:**
- Uses 1-indexed pages (page=1 is first page)
- Calculates `offset = (page - 1) * page_size`
- Returns tuple of `(list[TModel], total_count)`
- Total count query excludes soft-deleted entities
- Validates page >= 1 and page_size >= 1

**Sort Validation:**
- Uses `hasattr(self.model_class, sort_by)` to validate sort field exists
- Prevents SQL injection from malicious sort_by values
- Raises `ValueError` with descriptive message for invalid fields
- Supports "asc" and "desc" sort order

**Method Signatures:**
1. `get_by_id(entity_id: str) -> TModel | None` - Single entity retrieval
2. `get_all(page: int, page_size: int, filters: Dict[str, Any] | None, sort_by: str | None, sort_order: str) -> tuple[list[TModel], int]` - Paginated list with total
3. `create(model: TModel) -> TModel` - Insert new entity
4. `update(model: TModel) -> TModel` - Update existing entity (validates not soft-deleted)
5. `delete(entity_id: str) -> bool` - Soft delete (set state=2)
6. `hard_delete(entity_id: str) -> bool` - Physical deletion
7. `exists(entity_id: str) -> bool` - Check existence (excludes state=2)
8. `count(filters: Dict[str, Any] | None) -> int` - Count entities (excludes state=2)

## How to Use

### 1. Define Entity-Specific Repository

Create a repository by inheriting from `BaseRepository` and specifying the model type:

```python
from src.shared.infrastructure.base_repository import BaseRepository
from src.products.infrastructure.models import ProductModel
from sqlalchemy.orm import Session

class ProductRepository(BaseRepository[ProductModel]):
    def __init__(self, session: Session):
        super().__init__(session, ProductModel)
```

### 2. Use in Service Layer

Inject repository into service classes:

```python
class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product(self, product_id: str):
        # Returns None if product has state=2
        return self.repository.get_by_id(product_id)

    def list_products(self, page: int, page_size: int, category: str | None = None):
        filters = {"category": category} if category else {}
        items, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by="created_at",
            sort_order="desc"
        )
        return items, total
```

### 3. Integrate with FastAPI

Use dependency injection for repositories:

```python
from fastapi import Depends, HTTPException
from src.shared.infrastructure.database import get_db

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)

@router.get("/products/{product_id}")
def get_product(
    product_id: str,
    repository: ProductRepository = Depends(get_product_repository)
):
    product = repository.get_by_id(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product
```

### 4. Soft Delete vs Hard Delete

```python
# Soft delete - sets state=2, entity still in database
success = repository.delete(product_id)  # Returns bool

# Hard delete - physically removes from database
success = repository.hard_delete(product_id)  # Returns bool
```

### 5. Filtering and Pagination

```python
# Filter by multiple criteria
filters = {
    "category": "electronics",
    "status": "active",
    "vendor_id": "vendor123"
}

# Get page 2 with 20 items, sorted by price descending
items, total = repository.get_all(
    page=2,
    page_size=20,
    filters=filters,
    sort_by="price",
    sort_order="desc"
)

# Calculate total pages
total_pages = (total + page_size - 1) // page_size
```

## Configuration

This template uses minimal configuration as it's a shared base class. The following aspects are configurable through inheritance:

**Model Class:**
- Pass specific model class (e.g., `ProductModel`, `UserModel`) to `__init__`
- Model must have `state` field (integer) for soft-delete support
- Model must have `id` field (string) for entity identification

**Session Management:**
- SQLAlchemy `Session` injected via `__init__`
- Session lifecycle managed by caller (typically FastAPI dependency)
- Repository commits/rollbacks within each method for safety

**Filter Operators:**
- Currently supports equality (`==`) only
- Advanced operators (>, <, LIKE, IN) can be added in subclasses

## Testing

The base repository is a template for code generation. Testing should be performed in projects that use this template. Key test scenarios:

### Soft-Delete Filtering Tests
```bash
# Verify get_by_id returns None for state=2 entities
# Verify get_all excludes state=2 entities
# Verify exists returns False for state=2 entities
# Verify count excludes state=2 entities
```

### CRUD Operation Tests
```bash
# Verify create successfully inserts and returns model
# Verify update raises ValueError if entity not found or state=2
# Verify delete sets state=2 and returns True
# Verify hard_delete physically removes entity
```

### Pagination Tests
```bash
# Verify correct offset/limit calculation
# Verify total count accuracy
# Verify empty list for out-of-range pages
```

### Edge Case Tests
```bash
# Invalid pagination: page=0, page_size=0 should raise ValueError
# Invalid sort_by field should raise ValueError
# Already soft-deleted entity: delete() returns False (idempotent)
# Non-existent entity_id: get_by_id returns None
```

For TAC Bootstrap CLI itself:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

**Synchronous Implementation:**
This task creates the synchronous version using standard SQLAlchemy `Session`. An async version (`base_repository_async.py`) will be implemented in a separate task.

**Transaction Scope:**
Each repository method is a unit of work - it commits or rolls back within the method. The service layer can orchestrate multi-repository transactions if needed by managing the session lifecycle.

**Equality-Only Filtering:**
Per requirements, filters use `==` operator only. Advanced filtering (>, <, LIKE, IN, BETWEEN) can be added in repository subclasses or future enhancements.

**Boolean Returns for Delete:**
`delete()` and `hard_delete()` return boolean for idempotent behavior. The service layer decides whether `False` should raise an exception (e.g., 404 Not Found).

**State Filter Placement:**
The state != 2 filter is applied BEFORE user filters in the query chain. This ensures soft-deleted entities never appear, even with complex filter combinations.

### Dual Creation Pattern

Following TAC Bootstrap's dual creation requirement:
1. **Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` (for generating in other projects)
2. **Reference**: `src/shared/infrastructure/base_repository.py` (rendered for this project)

Both files are 625 lines and functionally identical. The template uses minimal Jinja2 variables since it's a shared base class.

### Consistency with DDD Layers

**Entity Layer** (`base_entity.py`):
- Defines `EntityState` enum: INACTIVE=0, ACTIVE=1, DELETED=2
- Repository respects this by filtering state != 2

**Service Layer** (`base_service.py`):
- Consumes repository methods
- Orchestrates business logic
- Handles validation and exception mapping

**Schema Layer** (`base_schema.py`):
- Request/response DTOs
- Validation rules
- Serialization for API

### Future Enhancements

- Advanced filtering with operators (>, <, LIKE, IN, BETWEEN, IS NULL)
- Bulk operations (bulk_create, bulk_update, bulk_delete)
- Query optimization hints (eager loading, join strategies)
- Audit log integration for tracking changes
- Cache layer integration for read performance
- Async version with asyncio and SQLAlchemy async sessions
- Soft-delete restoration method (undelete)
- Support for composite primary keys
- Custom exception types for repository errors
