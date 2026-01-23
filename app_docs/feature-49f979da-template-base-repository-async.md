# Template base_repository_async.py

**ADW ID:** 49f979da
**Date:** 2026-01-22
**Specification:** specs/issue-119-adw-49f979da-sdlc_planner-template-base-repository-async.md

## Overview

Created an async version of the base repository template using SQLAlchemy 2.0 async API with AsyncSession. This template enables TAC Bootstrap CLI to generate async repositories for FastAPI projects using modern async SQLAlchemy patterns, providing full CRUD operations with soft delete functionality and bulk operations.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2` - Template for generating async repositories
- **Reference Implementation**: `src/shared/infrastructure/base_repository_async.py` - Rendered example showing complete implementation
- **Async CRUD Operations**: All repository methods as async functions using SQLAlchemy 2.0 select() API
- **Bulk Operations**: Added `bulk_create()` and `bulk_update()` methods for efficient batch processing
- **Soft Delete Support**: Automatic state=2 filtering on all queries to exclude soft-deleted entities
- **Unit of Work Pattern**: Repository methods flush but never commit, allowing service layer to manage transactions

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`: Jinja2 template containing complete async repository implementation with comprehensive docstrings following IDK pattern
- `src/shared/infrastructure/base_repository_async.py`: Rendered reference implementation demonstrating usage in a FastAPI/SQLAlchemy project

### Key Changes

- **SQLAlchemy 2.0 Async API**: Uses `AsyncSession`, `select()`, `await session.execute()` instead of legacy `session.query()` patterns
- **Generic Type Support**: `BaseRepositoryAsync[TModel]` provides type-safe repository for any SQLAlchemy model
- **Async Methods Implemented**:
  - `get_by_id()` - Retrieve single entity by ID with soft-delete filtering
  - `create()` - Insert new entity with flush and refresh
  - `update()` - Update existing entity with validation
  - `delete()` - Soft delete (sets state=2)
  - `hard_delete()` - Physical deletion from database
  - `get_all()` - Paginated query with filtering, sorting, and total count
  - `exists()` - Check entity existence
  - `count()` - Count entities with optional filters
  - `bulk_create()` - Batch insert using `session.add_all()`
  - `bulk_update()` - Batch update using `session.merge()`
- **Comprehensive Documentation**: 791 lines including detailed docstrings, usage examples, invariants, and failure modes using IDK pattern
- **Transaction Management**: Follows Unit of Work pattern - repository never commits, only flushes to populate DB-generated fields

## How to Use

### Generating Async Repositories for Projects

When TAC Bootstrap CLI generates a project, this template will be used to create async repositories:

1. Configure project with async SQLAlchemy support
2. Run CLI to generate project structure (when CLI implementation is complete)
3. Template renders to `src/shared/infrastructure/base_repository_async.py` in target project

### Using Generated Repository

```python
# 1. Define entity-specific repository
from src.shared.infrastructure.base_repository_async import BaseRepositoryAsync
from src.products.infrastructure.models import ProductModel
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseRepositoryAsync[ProductModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductModel)

# 2. Use in service layer with transaction management
class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product: ProductModel):
        created = await self.repository.create(product)
        await self.repository.session.commit()  # Service manages commit
        return created

    async def list_products(self, page: int, page_size: int, category: str | None = None):
        filters = {"category": category} if category else {}
        items, total = await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by="created_at",
            sort_order="desc"
        )
        return items, total

# 3. Use with FastAPI dependency injection
from fastapi import Depends

async def get_product_repository(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db)

@router.post("/products")
async def create_product(
    product_data: ProductCreate,
    repo: ProductRepository = Depends(get_product_repository)
):
    product = ProductModel(**product_data.dict())
    created = await repo.create(product)
    await repo.session.commit()
    return created
```

## Configuration

No configuration required. The template uses Jinja2 variable substitution for project-specific values:

- `{{ config.project.name }}` - Project name in comments/documentation
- Template is framework-agnostic and works with any async SQLAlchemy project

## Testing

Template validation is performed through TAC Bootstrap CLI tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Manual validation checklist:
- Template syntax is valid Jinja2
- Rendered file is valid Python syntax
- All methods from sync repository are present
- Bulk operations use `session.add_all()` and `session.merge()`
- SQLAlchemy 2.0 async API patterns are used correctly
- All queries exclude state=2 entities
- Methods use `flush()` but never `commit()`

## Notes

### SQLAlchemy 2.0 Migration

The async repository exclusively uses modern SQLAlchemy 2.0 patterns:
- `select()` instead of deprecated `session.query()`
- `await session.execute()` for all database operations
- `session.scalars()` for fetching result sets
- `session.scalar()` for single values

### Unit of Work Pattern

Repository does NOT commit transactions. This allows:
- Composing multiple repository operations in single transaction
- Service layer controls transaction boundaries
- Atomic rollback on any failure in multi-step operations

Example:
```python
async def transfer_product_ownership(product_id: str, new_owner_id: str):
    # Both operations in single transaction
    product = await product_repo.get_by_id(product_id)
    product.owner_id = new_owner_id
    await product_repo.update(product)

    await ownership_history_repo.create(OwnershipChange(...))

    # Single commit for both operations
    await session.commit()
```

### Soft Delete Behavior

All query methods automatically exclude entities with `state=2`:
- `get_by_id()` returns `None` for soft-deleted entities
- `get_all()` excludes them from results
- `exists()` returns `False` for soft-deleted entities
- Use `hard_delete()` for physical removal if needed

### Bulk Operations

- `bulk_create()` and `bulk_update()` are atomic within session
- Empty list input returns empty list (no error)
- Failed validation/constraints can be rolled back by caller
- More efficient than individual create/update calls for large batches

### Future Enhancements

Consider adding in future iterations:
- Async context manager support (`async with repository.transaction()`)
- Support for complex filtering (OR conditions, comparison operators)
- Query builder pattern for advanced filtering
- Caching layer integration
- Event hooks for audit logging
