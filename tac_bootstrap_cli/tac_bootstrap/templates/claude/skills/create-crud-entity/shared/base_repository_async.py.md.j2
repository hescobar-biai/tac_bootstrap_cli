# Base Repository Async Template

Async generic CRUD repository for SQLAlchemy with asyncpg. Place at `src/shared/infrastructure/base_repository_async.py`.

## Template

```python
"""
IDK: repository, async-io, data-access

Module: base_repository_async

Responsibility:
- Provide generic async CRUD operations for all repositories
- Abstract async database access patterns
- Support pagination, filtering, and sorting with asyncio
- Enable concurrent database operations

Key Components:
- BaseRepositoryAsync: Generic async repository with CRUD operations

Invariants:
- All queries use SQLAlchemy async ORM
- Soft delete operations set state=2
- Pagination is 1-indexed
- All operations are non-blocking

Related Docs:
- docs/shared/infrastructure/base-repository-async.md
"""

from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, asc, desc, update, delete
from sqlalchemy.orm import selectinload
from datetime import datetime, UTC

T = TypeVar("T")


class BaseRepositoryAsync(Generic[T]):
    """
    IDK: repository, async-io, orm-abstraction

    Responsibility:
    - Provide async CRUD operations for ORM models
    - Abstract SQLAlchemy async session management
    - Support filtering, sorting, and pagination asynchronously
    - Enable eager loading of relationships

    Invariants:
    - All operations use single async db session
    - Pagination pages are 1-indexed
    - Filters only apply to existing model attributes
    - Soft delete sets state=2
    - All methods are coroutines

    Collaborators:
    - AsyncSession: SQLAlchemy async database session
    - ORM Model: entity-specific model class

    Failure Modes:
    - SQLAlchemyError: database operation failures
    - AttributeError: invalid filter/sort fields

    Related Docs:
    - docs/shared/infrastructure/base-repository-async.md
    """

    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, entity: T) -> T:
        """
        IDK: entity-creation, async-io, persistence

        Responsibility:
        - Persist new entity to database asynchronously
        - Commit transaction
        - Refresh entity with generated values

        Invariants:
        - Entity added to session and committed
        - Entity refreshed with database-generated fields

        Inputs:
        - entity (T): ORM model instance to persist

        Outputs:
        - T: persisted entity with generated fields

        Failure Modes:
        - IntegrityError: constraint violations
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def create_many(self, entities: list[T]) -> list[T]:
        """
        IDK: bulk-creation, async-io, batch-operation

        Responsibility:
        - Persist multiple entities in single transaction
        - Commit all entities atomically
        - Refresh all entities with generated values

        Invariants:
        - All entities added to session
        - Single commit for all entities
        - All entities refreshed

        Inputs:
        - entities (list[T]): list of ORM models to persist

        Outputs:
        - list[T]: list of persisted entities

        Failure Modes:
        - IntegrityError: constraint violations on any entity
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        """
        self.db.add_all(entities)
        await self.db.commit()
        for entity in entities:
            await self.db.refresh(entity)
        return entities

    async def get_by_id(
        self,
        entity_id: str,
        load_relations: list[str] | None = None,
    ) -> T | None:
        """
        IDK: entity-retrieval, async-io, eager-loading

        Responsibility:
        - Retrieve single entity by primary key asynchronously
        - Optionally eager load relationships
        - Return None if not found

        Invariants:
        - Returns None if not found
        - Returns first match (should be unique)
        - Eager loads specified relationships

        Inputs:
        - entity_id (str): unique identifier
        - load_relations (list[str] | None): relationship names to eager load

        Outputs:
        - T | None: entity or None

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        query = select(self.model).where(self.model.id == entity_id)

        if load_relations:
            for relation in load_relations:
                if hasattr(self.model, relation):
                    query = query.options(selectinload(getattr(self.model, relation)))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> T | None:
        """
        IDK: business-key-lookup, async-io, query

        Responsibility:
        - Retrieve entity by business code asynchronously
        - Support code-based lookups

        Invariants:
        - Returns None if not found
        - Code should be unique per entity type

        Inputs:
        - code (str): business identifier

        Outputs:
        - T | None: entity or None

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        query = select(self.model).where(self.model.code == code)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        load_relations: list[str] | None = None,
    ) -> tuple[list[T], int]:
        """
        IDK: pagination, async-io, query-builder

        Responsibility:
        - Retrieve paginated entity list asynchronously
        - Apply dynamic filters and sorting
        - Return total count for pagination
        - Support eager loading of relationships

        Invariants:
        - Page is 1-indexed
        - Filters only apply to existing attributes
        - Returns (items, total) tuple
        - Default sort by created_at desc

        Inputs:
        - page (int): page number (1-indexed)
        - page_size (int): items per page
        - filters (dict | None): field:value filter pairs
        - sort_by (str | None): field to sort by
        - sort_order (str): 'asc' or 'desc'
        - load_relations (list[str] | None): relationships to eager load

        Outputs:
        - tuple[list[T], int]: (items, total_count)

        Failure Modes:
        - AttributeError: invalid filter/sort field

        Related Docs:
        - docs/shared/infrastructure/pagination.md
        """
        # Base query
        query = select(self.model)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        # Count query (before pagination)
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        else:
            # Default sort by created_at desc
            query = query.order_by(desc(self.model.created_at))

        # Apply eager loading
        if load_relations:
            for relation in load_relations:
                if hasattr(self.model, relation):
                    query = query.options(selectinload(getattr(self.model, relation)))

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return items, total

    async def update(self, entity_id: str, data: dict) -> T | None:
        """
        IDK: entity-update, async-io, partial-update

        Responsibility:
        - Update entity fields from dictionary asynchronously
        - Auto-update audit trail (updated_at, version)
        - Persist changes to database

        Invariants:
        - Only updates existing attributes
        - updated_at set to current UTC
        - version incremented automatically
        - Returns None if entity not found

        Inputs:
        - entity_id (str): entity identifier
        - data (dict): field:value pairs to update

        Outputs:
        - T | None: updated entity or None

        Failure Modes:
        - EntityNotFound: entity_id doesn't exist
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        entity = await self.get_by_id(entity_id)
        if not entity:
            return None

        # Update fields
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        # Update modified timestamp and version
        entity.updated_at = datetime.now(UTC)
        entity.version = entity.version + 1

        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update_many(self, ids: list[str], data: dict) -> int:
        """
        IDK: bulk-update, async-io, batch-operation

        Responsibility:
        - Update multiple entities in single operation
        - Auto-update audit trail
        - Return count of updated entities

        Invariants:
        - updated_at automatically set
        - Single database operation
        - Returns count of affected rows

        Inputs:
        - ids (list[str]): entity identifiers to update
        - data (dict): field:value pairs to update

        Outputs:
        - int: number of entities updated

        Failure Modes:
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        """
        data["updated_at"] = datetime.now(UTC)

        stmt = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(**data)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount

    async def delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, async-io, permanent-removal

        Responsibility:
        - Permanently remove entity from database asynchronously
        - Not recoverable after commit

        Invariants:
        - Returns False if entity not found
        - Returns True if deleted successfully
        - Changes committed immediately

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - bool: True if deleted, False if not found

        Failure Modes:
        - SQLAlchemyError: database failures
        - IntegrityError: foreign key constraints

        Related Docs:
        - docs/shared/infrastructure/delete-operations.md
        """
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False

        await self.db.delete(entity)
        await self.db.commit()
        return True

    async def delete_many(self, ids: list[str]) -> int:
        """
        IDK: bulk-delete, async-io, permanent-removal

        Responsibility:
        - Permanently remove multiple entities
        - Single database operation
        - Return count of deleted entities

        Invariants:
        - Single database operation
        - Returns count of affected rows
        - Not recoverable after commit

        Inputs:
        - ids (list[str]): entity identifiers to delete

        Outputs:
        - int: number of entities deleted

        Failure Modes:
        - SQLAlchemyError: database failures
        - IntegrityError: foreign key constraints

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        """
        stmt = delete(self.model).where(self.model.id.in_(ids))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount

    async def soft_delete(self, entity_id: str) -> T | None:
        """
        IDK: soft-delete, async-io, recoverable

        Responsibility:
        - Mark entity as deleted (state=2) asynchronously
        - Preserve data for recovery
        - Update audit trail

        Invariants:
        - Sets state to 2 (DELETED)
        - Data remains in database
        - Returns None if not found

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - T | None: updated entity or None

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        return await self.update(entity_id, {"state": 2})

    async def soft_delete_many(self, ids: list[str]) -> int:
        """
        IDK: bulk-soft-delete, async-io, recoverable

        Responsibility:
        - Mark multiple entities as deleted
        - Preserve data for recovery
        - Single database operation

        Invariants:
        - Sets state to 2 for all entities
        - Data remains in database
        - Returns count of affected entities

        Inputs:
        - ids (list[str]): entity identifiers

        Outputs:
        - int: number of entities soft deleted

        Related Docs:
        - docs/shared/infrastructure/bulk-operations.md
        """
        return await self.update_many(ids, {"state": 2})

    async def restore(self, entity_id: str) -> T | None:
        """
        IDK: entity-restore, async-io, state-transition

        Responsibility:
        - Restore soft-deleted entity (set state=1)
        - Reactivate entity
        - Update audit trail

        Invariants:
        - Sets state to 1 (ACTIVE)
        - Returns None if not found
        - Updates version and timestamps

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - T | None: restored entity or None

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        return await self.update(entity_id, {"state": 1})

    async def exists(self, entity_id: str) -> bool:
        """
        IDK: existence-check, async-io, predicate

        Responsibility:
        - Check if entity exists in database asynchronously
        - Fast check without loading entity

        Invariants:
        - Returns boolean
        - Does not load full entity

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - bool: True if exists, False otherwise

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        query = select(func.count()).where(self.model.id == entity_id)
        result = await self.db.execute(query)
        return (result.scalar() or 0) > 0

    async def count(self, filters: dict | None = None) -> int:
        """
        IDK: aggregation, async-io, count-query

        Responsibility:
        - Count entities with optional filters asynchronously
        - Support filtered counting

        Invariants:
        - Returns non-negative integer
        - Filters only apply to existing attributes

        Inputs:
        - filters (dict | None): field:value filter pairs

        Outputs:
        - int: count of matching entities

        Failure Modes:
        - AttributeError: invalid filter field

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        query = select(func.count()).select_from(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def get_active(self) -> list[T]:
        """
        IDK: query-filter, async-io, active-entities

        Responsibility:
        - Get all active entities (state=1) asynchronously
        - Filter by active state

        Invariants:
        - Returns only entities with state=1
        - Returns empty list if none found

        Outputs:
        - list[T]: list of active entities

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        query = select(self.model).where(self.model.state == 1)
        result = await self.db.execute(query)
        return list(result.scalars().all())
```

## Directory Setup

```
src/
└── shared/
    └── infrastructure/
        ├── __init__.py
        ├── database.py
        ├── database_async.py
        ├── base_repository.py
        └── base_repository_async.py  # <-- This file
```

## Async Database Setup

**`src/shared/infrastructure/database_async.py`**:
```python
"""Async database connection and session management."""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# Create async engine
async_engine = create_async_engine(
    settings.database_url_async,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_async_db() -> None:
    """Initialize database (create tables)."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_async_db() -> None:
    """Close database connections."""
    await async_engine.dispose()
```

## Usage Example

### Async Repository

```python
# src/product_catalog/infrastructure/repository.py
"""Product async repository implementation."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from shared.infrastructure.base_repository_async import BaseRepositoryAsync
from .models import ProductModel


class ProductRepository(BaseRepositoryAsync[ProductModel]):
    """Async repository for Product entities."""

    def __init__(self, db: AsyncSession):
        super().__init__(ProductModel, db)

    async def get_by_sku(self, sku: str) -> ProductModel | None:
        """Get Product by SKU."""
        query = select(self.model).where(self.model.sku == sku)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_available(self) -> list[ProductModel]:
        """Get all available products."""
        query = (
            select(self.model)
            .where(self.model.is_available == True)
            .where(self.model.state == 1)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_category(self, category: str) -> list[ProductModel]:
        """Get products by category."""
        query = (
            select(self.model)
            .where(self.model.category == category)
            .where(self.model.state == 1)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
```

### Async Service

```python
# src/product_catalog/application/service.py
"""Product async service implementation."""

from shared.application.base_service_async import BaseServiceAsync
from ..domain.product import Product
from ..infrastructure.repository import ProductRepository
from ..infrastructure.models import ProductModel
from .schemas import ProductCreate, ProductUpdate, ProductResponse


class ProductService(BaseServiceAsync[
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductModel,
    Product
]):
    """Async service for Product business logic."""

    def __init__(self, repository: ProductRepository):
        super().__init__(
            repository=repository,
            response_class=ProductResponse,
            domain_class=Product,
            entity_name="Product",
            model_class=ProductModel,
        )

    async def get_available(self) -> list[ProductResponse]:
        """Get all available products."""
        items = await self.repository.get_available()
        return [ProductResponse.model_validate(item) for item in items]
```

### Async Routes

```python
# src/product_catalog/api/routes.py
"""Product async CRUD endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure.database_async import get_async_db
from shared.application.base_schema import PaginatedResponse, MessageResponse
from ..application.schemas import ProductCreate, ProductUpdate, ProductResponse
from ..application.service import ProductService
from ..infrastructure.repository import ProductRepository

router = APIRouter(prefix="/products", tags=["Products"])


async def get_product_service(
    db: AsyncSession = Depends(get_async_db),
) -> ProductService:
    """Dependency for ProductService."""
    repository = ProductRepository(db)
    return ProductService(repository)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """Create a new Product."""
    return await service.create(data)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """Get Product by ID."""
    return await service.get_by_id(product_id)


@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
) -> PaginatedResponse[ProductResponse]:
    """List Products with pagination."""
    return await service.get_all(page=page, page_size=page_size)
```

## Main Application with Async

```python
# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from shared.infrastructure.database_async import init_async_db, close_async_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    await init_async_db()
    yield
    await close_async_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
```
