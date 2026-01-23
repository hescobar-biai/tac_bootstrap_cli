"""
IDK: repository-layer, data-access, orm-abstraction, async-sqlalchemy

Module: base_repository_async

Responsibility:
- Provide generic async CRUD operations for all domain entities
- Abstract SQLAlchemy async ORM complexity from service layer
- Enforce soft-delete transparency (exclude state=2 by default)
- Support Unit of Work pattern (no commits, only flush)
- Support dynamic filtering, sorting, and pagination
- Use SQLAlchemy 2.0 async API with select() statements

Key Components:
- BaseRepositoryAsync[TModel]: Generic async repository with full CRUD operations
- Soft-delete enforcement: All queries exclude state=2 entities
- Unit of Work: Repository does NOT commit, caller manages transactions
- Dynamic filtering: Apply equality filters from dict
- Pagination: offset/limit with total count
- Bulk operations: bulk_create and bulk_update for batch processing

Invariants:
- All queries filter out state=2 (soft-deleted) entities by default
- Methods use flush() but NEVER commit() - caller manages transaction lifecycle
- Pagination uses 1-indexed pages (page=1 is first page)
- sort_by field must exist in model (validated via hasattr)
- Filters apply equality (==) operator only
- delete() sets state=2 (soft delete), hard_delete() removes physically
- All methods are async and use SQLAlchemy 2.0 select() API

Usage Examples:

```python
# Define entity-specific repository by inheriting BaseRepositoryAsync
from src.shared.infrastructure.base_repository_async import BaseRepositoryAsync
from src.products.infrastructure.models import ProductModel
from src.shared.infrastructure.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseRepositoryAsync[ProductModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductModel)

# Use in service layer with transaction management
from src.products.infrastructure.repositories import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_product(self, product_id: str):
        # Returns None if product has state=2 (soft-deleted)
        return await self.repository.get_by_id(product_id)

    async def list_products(self, page: int, page_size: int, category: str | None = None):
        filters = {"category": category} if category else {}
        # Excludes products with state=2
        items, total = await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by="created_at",
            sort_order="desc"
        )
        return items, total

    async def create_product(self, product: ProductModel):
        # Repository flushes but doesn't commit
        created = await self.repository.create(product)
        # Service commits the transaction
        await self.repository.session.commit()
        return created

    async def soft_delete_product(self, product_id: str):
        # Sets state=2 instead of physical deletion
        success = await self.repository.delete(product_id)
        if success:
            await self.repository.session.commit()
        return success

    async def permanent_delete_product(self, product_id: str):
        # Physical deletion from database
        success = await self.repository.hard_delete(product_id)
        if success:
            await self.repository.session.commit()
        return success

# Use with FastAPI dependency injection
from fastapi import Depends

async def get_product_repository(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db)

@router.get("/products/{product_id}")
async def get_product(
    product_id: str,
    repository: ProductRepository = Depends(get_product_repository)
):
    product = await repository.get_by_id(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product
```

Collaborators:
- SQLAlchemy AsyncSession: async database connection and transaction management
- ORM Models: entity classes mapped to database tables
- Service Layer: orchestrates business logic using repository and manages commits

Failure Modes:
- ValueError: invalid pagination inputs (page < 1, page_size < 1)
- ValueError: invalid sort_by field (not an attribute of model)
- ValueError: entity not found during update operation
- DatabaseError: constraint violations, connection errors (propagated, caller handles rollback)

Related Docs:
- docs/shared/infrastructure/base-repository-async.md
- docs/shared/infrastructure/unit-of-work-pattern.md
- ai_docs/doc/create-crud-entity/
"""

from typing import Generic, TypeVar, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc

# Generic type variable for ORM models
TModel = TypeVar('TModel')


class BaseRepositoryAsync(Generic[TModel]):
    """
    IDK: repository-pattern, crud-operations, soft-delete, async-sqlalchemy, unit-of-work

    Responsibility:
    - Provide generic async CRUD operations for domain entities
    - Abstract SQLAlchemy async operations from service layer
    - Enforce soft-delete filtering (exclude state=2)
    - Support Unit of Work pattern (flush only, no commits)
    - Support pagination, filtering, sorting, and bulk operations
    - Use SQLAlchemy 2.0 async API with select() statements

    Invariants:
    - All queries exclude entities with state=2 (soft-deleted)
    - Methods flush() but NEVER commit() - caller manages transaction
    - Pagination is 1-indexed (page=1 is first page)
    - Filters use equality operator (==) only
    - sort_by field must be valid model attribute
    - All database operations use await with AsyncSession
    - Uses select() statements instead of session.query()

    Generic Type Parameters:
    - TModel: ORM model class (e.g., ProductModel, UserModel)

    Usage Pattern:
    - Entity repositories inherit and specify model type
    - AsyncSession injected via constructor
    - Used by service layer for data access
    - Service layer manages transaction commits/rollbacks

    Example:

    ```python
    class ProductRepository(BaseRepositoryAsync[ProductModel]):
        def __init__(self, session: AsyncSession):
            super().__init__(session, ProductModel)

        # Add entity-specific queries if needed
        async def get_by_sku(self, sku: str) -> ProductModel | None:
            stmt = select(self.model_class).where(
                self.model_class.sku == sku,
                self.model_class.state != 2
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
    ```

    Collaborators:
    - SQLAlchemy AsyncSession: async database connection
    - ORM Models: entity classes
    - Service Layer: business logic and transaction management

    Failure Modes:
    - ValueError: invalid inputs (page < 1, invalid sort_by, entity not found)
    - DatabaseError: database errors (propagated, caller handles rollback)

    Related Docs:
    - docs/shared/infrastructure/repository-pattern.md
    - docs/shared/infrastructure/async-patterns.md
    """

    def __init__(self, session: AsyncSession, model_class: type[TModel]):
        """
        IDK: dependency-injection, constructor

        Responsibility:
        - Initialize repository with async database session and model class
        - Enable testability via dependency injection

        Invariants:
        - session must be active SQLAlchemy AsyncSession
        - model_class must be ORM-mapped model

        Inputs:
        - session: SQLAlchemy async database session
        - model_class: ORM model type

        Outputs:
        - None (initializes instance)

        Related Docs:
        - docs/shared/infrastructure/dependency-injection.md
        """
        self.session = session
        self.model_class = model_class

    async def get_by_id(self, entity_id: str) -> TModel | None:
        """
        IDK: read-operation, retrieval, soft-delete-filter, async

        Responsibility:
        - Retrieve single entity by ID asynchronously
        - Exclude soft-deleted entities (state=2)
        - Return None if not found or deleted

        Invariants:
        - Returns None if entity.state == 2
        - Returns None if entity_id doesn't exist
        - No exception raised on missing entity
        - Uses SQLAlchemy 2.0 select() API

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - TModel | None: entity if found and not deleted, None otherwise

        Example:

        ```python
        product = await repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        if product is None:
            # Not found or soft-deleted
            raise HTTPException(404, "Product not found")
        ```

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        stmt = select(self.model_class).where(
            self.model_class.id == entity_id,
            self.model_class.state != 2
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int,
        page_size: int,
        filters: Dict[str, Any] | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> tuple[list[TModel], int]:
        """
        IDK: list-operation, pagination, filtering, sorting, async

        Responsibility:
        - Retrieve paginated list of entities asynchronously
        - Apply dynamic filters with equality operator
        - Sort by specified field
        - Exclude soft-deleted entities (state=2)
        - Return items and total count

        Invariants:
        - Excludes entities with state=2
        - page must be >= 1
        - page_size must be >= 1
        - sort_by must be valid model attribute if provided
        - Offset calculated as (page - 1) * page_size
        - Total count reflects all matching entities (not just current page)
        - Uses SQLAlchemy 2.0 select() API

        Inputs:
        - page: page number (1-indexed)
        - page_size: number of items per page
        - filters: dict of field:value for equality filtering
        - sort_by: field name to sort by (None for no sorting)
        - sort_order: "asc" or "desc"

        Outputs:
        - tuple[list[TModel], int]: (items in current page, total count)

        Failure Modes:
        - ValueError: page < 1 or page_size < 1
        - ValueError: sort_by is not a valid model attribute

        Example:

        ```python
        # Get page 2 with 10 items, filter by category, sort by price descending
        items, total = await repository.get_all(
            page=2,
            page_size=10,
            filters={"category": "Electronics", "status": "active"},
            sort_by="price",
            sort_order="desc"
        )
        # items = [product11, product12, ..., product20]
        # total = 150 (total matching entities across all pages)
        ```

        Related Docs:
        - docs/shared/infrastructure/pagination.md
        - docs/shared/infrastructure/filtering.md
        """
        # Validate inputs
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        # Validate sort_by field if provided
        if sort_by and not hasattr(self.model_class, sort_by):
            raise ValueError(f"Invalid sort field: {sort_by}")

        # Base query excludes soft-deleted entities
        stmt = select(self.model_class).where(self.model_class.state != 2)

        # Apply filters (equality only)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    stmt = stmt.where(getattr(self.model_class, key) == value)

        # Get total count before pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        # Apply sorting
        if sort_by:
            sort_column = getattr(self.model_class, sort_by)
            if sort_order.lower() == "desc":
                stmt = stmt.order_by(desc(sort_column))
            else:
                stmt = stmt.order_by(asc(sort_column))

        # Apply pagination
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)

        # Execute query
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def create(self, model: TModel) -> TModel:
        """
        IDK: create-operation, persistence, unit-of-work, async

        Responsibility:
        - Insert new entity into database asynchronously
        - Flush session to populate DB-generated fields
        - Return persisted entity with generated fields
        - Does NOT commit (caller manages transaction)

        Invariants:
        - Flushes session but does NOT commit
        - Returns entity with database-generated fields (id, timestamps)
        - Caller is responsible for commit/rollback
        - Uses async session operations

        Inputs:
        - model: entity instance to persist

        Outputs:
        - TModel: persisted entity with database-generated values

        Failure Modes:
        - DatabaseError: constraint violation (unique, foreign key, etc.)
        - Exception propagated to caller for rollback

        Example:

        ```python
        new_product = ProductModel(
            code="PROD-001",
            name="Laptop",
            price=999.99,
            category="Electronics"
        )
        created = await repository.create(new_product)
        # created.id is now set by database after flush
        # Service layer commits the transaction
        await session.commit()
        ```

        Related Docs:
        - docs/shared/infrastructure/create-operations.md
        - docs/shared/infrastructure/unit-of-work-pattern.md
        """
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def update(self, model: TModel) -> TModel:
        """
        IDK: update-operation, persistence, unit-of-work, async

        Responsibility:
        - Update existing entity in database asynchronously
        - Validate entity exists and is not deleted (state != 2)
        - Flush session to persist changes
        - Return updated entity
        - Does NOT commit (caller manages transaction)

        Invariants:
        - Entity must exist in database
        - Entity must not be soft-deleted (state != 2)
        - Flushes session but does NOT commit
        - Raises ValueError if entity not found or deleted
        - Caller is responsible for commit/rollback
        - Uses async session operations

        Inputs:
        - model: entity instance with updated fields

        Outputs:
        - TModel: updated entity

        Failure Modes:
        - ValueError: entity not found or soft-deleted
        - DatabaseError: constraint violation
        - Exception propagated to caller for rollback

        Example:

        ```python
        product = await repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        if not product:
            raise ValueError("Product not found")

        product.price = 899.99
        product.mark_updated(user_id="user-123")
        updated = await repository.update(product)
        # Service layer commits the transaction
        await session.commit()
        ```

        Related Docs:
        - docs/shared/infrastructure/update-operations.md
        - docs/shared/infrastructure/unit-of-work-pattern.md
        """
        # Validate entity exists and is not deleted
        existing = await self.get_by_id(model.id)
        if not existing:
            raise ValueError(f"Entity with id {model.id} not found or is deleted")

        # Merge changes and flush
        await self.session.merge(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def delete(self, entity_id: str) -> bool:
        """
        IDK: soft-delete, state-transition, data-preservation, async

        Responsibility:
        - Soft delete entity by setting state=2 asynchronously
        - Preserve data in database for audit trail
        - Flush session to persist change
        - Return success status
        - Does NOT commit (caller manages transaction)

        Invariants:
        - Sets state=2 instead of physical deletion
        - Data remains in database
        - Returns True if entity found and deleted
        - Returns False if entity not found or already deleted
        - Idempotent: deleting already-deleted entity returns False
        - Flushes session but does NOT commit
        - Caller is responsible for commit/rollback

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if deleted, False if not found or already deleted

        Example:

        ```python
        # Soft delete product
        success = await repository.delete("550e8400-e29b-41d4-a716-446655440000")
        if not success:
            raise HTTPException(404, "Product not found")

        # Service layer commits the transaction
        await session.commit()

        # Subsequent queries won't return this entity (state=2)
        product = await repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        # product is None
        ```

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False

        entity.state = 2
        await self.session.flush()
        return True

    async def hard_delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, physical-deletion, permanent-removal, async

        Responsibility:
        - Physically delete entity from database asynchronously
        - Remove data permanently (no recovery)
        - Flush session to persist deletion
        - Return success status
        - Does NOT commit (caller manages transaction)

        Invariants:
        - Performs physical DELETE from database
        - Data is permanently removed
        - Returns True if entity found and deleted
        - Returns False if entity not found
        - Flushes session but does NOT commit
        - Caller is responsible for commit/rollback

        WARNING: This operation is irreversible. Use with caution.
        Prefer soft delete (delete() method) for most use cases.

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if deleted, False if not found

        Example:

        ```python
        # Permanently delete product (admin operation)
        success = await repository.hard_delete("550e8400-e29b-41d4-a716-446655440000")
        if not success:
            raise HTTPException(404, "Product not found")

        # Service layer commits the transaction
        await session.commit()

        # Entity is completely removed from database
        ```

        Related Docs:
        - docs/shared/infrastructure/hard-delete.md
        """
        # Query without state filter for hard delete
        stmt = select(self.model_class).where(self.model_class.id == entity_id)
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()

        if not entity:
            return False

        await self.session.delete(entity)
        await self.session.flush()
        return True

    async def exists(self, entity_id: str) -> bool:
        """
        IDK: existence-check, query-method, soft-delete-filter, async

        Responsibility:
        - Check if entity exists in database asynchronously
        - Exclude soft-deleted entities (state=2)
        - Return boolean result

        Invariants:
        - Returns False for soft-deleted entities (state=2)
        - Returns False for non-existent entities
        - Returns True only for active/inactive entities (state=0 or 1)
        - Uses SQLAlchemy 2.0 select() API

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if exists and not deleted, False otherwise

        Example:

        ```python
        if await repository.exists("550e8400-e29b-41d4-a716-446655440000"):
            # Entity exists and is not soft-deleted
            product = await repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        else:
            raise HTTPException(404, "Product not found")
        ```

        Related Docs:
        - docs/shared/infrastructure/query-methods.md
        """
        stmt = select(func.count(self.model_class.id)).where(
            self.model_class.id == entity_id,
            self.model_class.state != 2
        )
        result = await self.session.execute(stmt)
        count = result.scalar_one()
        return count > 0

    async def count(self, filters: Dict[str, Any] | None = None) -> int:
        """
        IDK: count-operation, aggregation, soft-delete-filter, async

        Responsibility:
        - Count entities matching filters asynchronously
        - Exclude soft-deleted entities (state=2)
        - Apply dynamic filters with equality operator
        - Return total count

        Invariants:
        - Excludes entities with state=2
        - Returns 0 if no matches
        - Filters use equality operator (==) only
        - Uses SQLAlchemy 2.0 select() API

        Inputs:
        - filters: dict of field:value for equality filtering

        Outputs:
        - int: count of matching entities

        Example:

        ```python
        # Count all active products in Electronics category
        total = await repository.count({"category": "Electronics", "state": 1})
        # total = 42

        # Count all active entities (not deleted)
        total = await repository.count({})
        # total = 150
        ```

        Related Docs:
        - docs/shared/infrastructure/count-operations.md
        """
        # Base query excludes soft-deleted entities
        stmt = select(func.count(self.model_class.id)).where(
            self.model_class.state != 2
        )

        # Apply filters (equality only)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    stmt = stmt.where(getattr(self.model_class, key) == value)

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def bulk_create(self, models: list[TModel]) -> list[TModel]:
        """
        IDK: bulk-operation, batch-insert, unit-of-work, async

        Responsibility:
        - Insert multiple entities into database asynchronously
        - Flush session to populate DB-generated fields
        - Return persisted entities with generated fields
        - Does NOT commit (caller manages transaction)
        - Atomic operation within session

        Invariants:
        - All entities inserted in single database round-trip
        - Flushes session but does NOT commit
        - Returns entities with database-generated fields (id, timestamps)
        - Empty list input returns empty list
        - Caller is responsible for commit/rollback
        - If flush fails, no entities are persisted (atomic)

        Inputs:
        - models: list of entity instances to persist

        Outputs:
        - list[TModel]: persisted entities with database-generated values

        Failure Modes:
        - DatabaseError: constraint violation on any entity
        - Exception propagated to caller for rollback
        - All-or-nothing: if one fails, none are persisted

        Example:

        ```python
        products = [
            ProductModel(code="PROD-001", name="Laptop", price=999.99),
            ProductModel(code="PROD-002", name="Mouse", price=29.99),
            ProductModel(code="PROD-003", name="Keyboard", price=79.99),
        ]
        created = await repository.bulk_create(products)
        # All products now have database-generated IDs
        # Service layer commits the transaction
        await session.commit()
        ```

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        - docs/shared/infrastructure/unit-of-work-pattern.md
        """
        if not models:
            return []

        self.session.add_all(models)
        await self.session.flush()
        for model in models:
            await self.session.refresh(model)
        return models

    async def bulk_update(self, models: list[TModel]) -> list[TModel]:
        """
        IDK: bulk-operation, batch-update, unit-of-work, async

        Responsibility:
        - Update multiple entities in database asynchronously
        - Flush session to persist changes
        - Return updated entities
        - Does NOT commit (caller manages transaction)
        - Atomic operation within session

        Invariants:
        - All entities updated in single database round-trip
        - Flushes session but does NOT commit
        - Returns updated entities
        - Empty list input returns empty list
        - Caller is responsible for commit/rollback
        - If flush fails, no entities are updated (atomic)
        - Does NOT validate entity existence (assumes valid entities)

        Inputs:
        - models: list of entity instances to update

        Outputs:
        - list[TModel]: updated entities

        Failure Modes:
        - DatabaseError: constraint violation on any entity
        - Exception propagated to caller for rollback
        - All-or-nothing: if one fails, none are updated

        Example:

        ```python
        # Fetch products to update
        products = await repository.get_all(page=1, page_size=10)
        items, _ = products

        # Apply bulk price increase
        for product in items:
            product.price *= 1.1  # 10% increase
            product.mark_updated(user_id="admin-123")

        updated = await repository.bulk_update(items)
        # All products updated
        # Service layer commits the transaction
        await session.commit()
        ```

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        - docs/shared/infrastructure/unit-of-work-pattern.md
        """
        if not models:
            return []

        for model in models:
            await self.session.merge(model)

        await self.session.flush()

        for model in models:
            await self.session.refresh(model)

        return models
