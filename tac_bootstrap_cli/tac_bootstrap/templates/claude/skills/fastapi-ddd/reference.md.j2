# Celes DDD Lite - Reference

Screaming Architecture with vertical slices, Pydantic entities, sync SQLAlchemy, FastAPI presentation.

## Architecture Overview

> "Architecture should scream the use cases of the system." -- Robert C. Martin

Folder names reflect **business capabilities**, not technical layers. Each capability is a **vertical slice** with 4 layers: domain / application / infrastructure / presentation. Key characteristics:
- **Pydantic BaseModel** for entities (NOT dataclass)
- **int primary keys** (NOT UUID)
- **Sync SQLAlchemy Session** (NOT AsyncSession)
- **EntityState IntEnum** for lifecycle (NOT status strings)
- **presentation/** layer (NOT `interfaces/`)
- No domain events, event dispatchers, or entity-to-ORM mappers


## Directory Structure

```text
src/
  {capability}/                        # e.g., products, orders
    domain/
      aggregates/
        {entity}.py                    # Entity (Pydantic BaseModel)
        {entity}_repository.py         # Abstract repository interface
      value_objects/                    # Optional
    application/
      dtos/
        {entity}_schemas.py            # Create, Update, Response DTOs
      use_cases/
        {entity}_use_case.py           # Use case orchestration
    infrastructure/
      persistence/
        {entity}_model.py              # SQLAlchemy ORM model
        {entity}_repository.py         # Concrete repository impl
    presentation/
      api/
        {entity}_router.py             # FastAPI routes
  shared/
    domain/
      base_entity.py                   # Entity base + EntityState
    application/
      base_schemas.py                  # BaseCreate, BaseUpdate, BaseResponse
    infrastructure/
      database.py                      # Engine, SessionLocal, Base, get_db
  main.py
```

| Layer | Purpose | Depends On |
|-------|---------|------------|
| **Domain** | Entities, repository contracts | Nothing |
| **Application** | Use cases, DTOs | domain/ |
| **Infrastructure** | ORM models, repo implementations | domain/, application/ |
| **Presentation** | FastAPI routers | application/ |


## Entity Base Class

```python
from __future__ import annotations
from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Field

class EntityState(IntEnum):
    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2

class Entity(BaseModel):
    """Base entity. Uses int PK, NOT UUID. Server generates id and timestamps."""
    id: Optional[int] = Field(default=None, description="Auto-generated PK")
    code: Optional[str] = Field(default=None, description="Business code")
    name: str = Field(..., min_length=1, max_length=255)
    state: EntityState = Field(default=EntityState.ACTIVE)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def activate(self) -> None:
        self.state = EntityState.ACTIVE
    def deactivate(self) -> None:
        self.state = EntityState.INACTIVE
    def soft_delete(self) -> None:
        self.state = EntityState.DELETED
    def is_active(self) -> bool:
        return self.state == EntityState.ACTIVE
```

### Concrete Entity

```python
from shared.domain.base_entity import Entity
from pydantic import Field

class Product(Entity):
    """Product aggregate root."""
    sku: str = Field(..., min_length=1, max_length=50)
    unit_price: float = Field(..., ge=0)
    category: Optional[str] = Field(default=None, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)

    def apply_discount(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.unit_price = self.unit_price * (1 - percentage / 100)
```


## Repository Pattern

### Abstract Interface (domain/aggregates/{entity}_repository.py)

```python
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T: ...
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]: ...
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[T]: ...
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]: ...
    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]: ...
    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...
    @abstractmethod
    def soft_delete(self, entity_id: int) -> Optional[T]: ...
    @abstractmethod
    def activate(self, entity_id: int) -> Optional[T]: ...
    @abstractmethod
    def deactivate(self, entity_id: int) -> Optional[T]: ...
```

### Concrete Impl (infrastructure/persistence/{entity}_repository.py)

Named `{Entity}RepositoryImpl`. Uses **sync Session**.

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

class ProductRepositoryImpl(BaseRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, entity: ProductModel) -> ProductModel:
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def get_by_id(self, entity_id: int) -> ProductModel | None:
        return self._session.get(ProductModel, entity_id)

    def get_by_code(self, code: str) -> ProductModel | None:
        stmt = select(ProductModel).where(ProductModel.code == code)
        return self._session.execute(stmt).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductModel]:
        stmt = (
            select(ProductModel)
            .where(ProductModel.state != 2)  # Exclude DELETED
            .offset(skip).limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def update(self, entity_id: int, entity: ProductModel) -> ProductModel | None:
        existing = self.get_by_id(entity_id)
        if existing is None:
            return None
        self._session.merge(entity)
        self._session.commit()
        self._session.refresh(existing)
        return existing

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if entity is None:
            return False
        self._session.delete(entity)
        self._session.commit()
        return True

    def soft_delete(self, entity_id: int) -> ProductModel | None:
        return self._set_state(entity_id, 2)  # DELETED

    def activate(self, entity_id: int) -> ProductModel | None:
        return self._set_state(entity_id, 1)  # ACTIVE

    def deactivate(self, entity_id: int) -> ProductModel | None:
        return self._set_state(entity_id, 0)  # INACTIVE

    def _set_state(self, entity_id: int, state: int) -> ProductModel | None:
        entity = self.get_by_id(entity_id)
        if entity is None:
            return None
        entity.state = state
        self._session.commit()
        return entity
```


## Schema / DTO Pattern

### Base Schemas (shared/application/base_schemas.py)

```python
from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field
T = TypeVar("T")

class BaseCreate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)

class BaseUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: Optional[str] = None
    name: str
    state: int
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int = 0
    limit: int = 20
```

### Concrete DTOs

```python
from pydantic import Field
from src.shared.application.base_schemas import BaseCreate, BaseUpdate, BaseResponse

class ProductCreate(BaseCreate):
    sku: str = Field(..., min_length=1, max_length=50)
    unit_price: float = Field(..., ge=0)
    category: Optional[str] = Field(default=None, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)

class ProductUpdate(BaseUpdate):
    sku: Optional[str] = Field(default=None, min_length=1, max_length=50)
    unit_price: Optional[float] = Field(default=None, ge=0)
    category: Optional[str] = None
    stock_quantity: Optional[int] = Field(default=None, ge=0)

class ProductResponse(BaseResponse):
    sku: str
    unit_price: float
    category: Optional[str] = None
    stock_quantity: int
```


## Use Case Pattern

Single class per entity for simple CRUD. Split into commands/queries only for complex domains.

```python
from typing import List, Optional

class ProductUseCase:
    def __init__(self, repository) -> None:
        self._repository = repository

    # Commands (write)
    def create(self, payload: ProductCreate) -> object:
        entity = Product(code=payload.code, name=payload.name,
                         sku=payload.sku, unit_price=payload.unit_price,
                         category=payload.category, stock_quantity=payload.stock_quantity)
        model = self._to_model(entity)
        return self._repository.create(model)

    def update(self, entity_id: int, payload: ProductUpdate) -> Optional[object]:
        existing = self._repository.get_by_id(entity_id)
        if existing is None:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(existing, field):
                setattr(existing, field, value)
        return self._repository.update(entity_id, existing)

    def delete(self, entity_id: int) -> bool:
        return self._repository.delete(entity_id)

    # State operations delegate directly to repository
    def soft_delete(self, eid: int): return self._repository.soft_delete(eid)
    def activate(self, eid: int): return self._repository.activate(eid)
    def deactivate(self, eid: int): return self._repository.deactivate(eid)

    # Queries (read)
    def get_by_id(self, eid: int): return self._repository.get_by_id(eid)
    def get_by_code(self, code: str): return self._repository.get_by_code(code)
    def get_all(self, skip: int = 0, limit: int = 100) -> List[object]:
        return self._repository.get_all(skip=skip, limit=limit)

    def _to_model(self, entity: Product):
        from src.products.infrastructure.persistence.product_model import ProductModel
        return ProductModel(**entity.model_dump(exclude_none=True))
```

| Scenario | Approach |
|----------|----------|
| Simple CRUD | Single `{Entity}UseCase` class |
| Complex write rules | `commands/create_{entity}.py`, `commands/update_{entity}.py` |
| Read-heavy projections | `queries/get_{entity}.py`, `queries/list_{entities}.py` |
| Multi-aggregate workflows | `use_cases/{workflow_name}.py` |


## Routes / Presentation

All route functions are **sync** (`def`, NOT `async def`).

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["Products"])

def get_repository(db: Session = Depends(get_db)):
    return ProductRepositoryImpl(db)

def get_use_case(repository=Depends(get_repository)):
    return ProductUseCase(repository)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, use_case=Depends(get_use_case)):
    return use_case.create(payload)

@router.get("/", response_model=list[ProductResponse])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500),
                  use_case=Depends(get_use_case)):
    return use_case.get_all(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, use_case=Depends(get_use_case)):
    entity = use_case.get_by_id(product_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return entity

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, use_case=Depends(get_use_case)):
    entity = use_case.update(product_id, payload)
    if entity is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return entity

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, use_case=Depends(get_use_case)):
    if not use_case.delete(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

# activate / deactivate / soft-delete follow the same pattern:
@router.post("/{product_id}/activate", response_model=ProductResponse)
def activate_product(product_id: int, use_case=Depends(get_use_case)):
    entity = use_case.activate(product_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return entity
# POST /{id}/deactivate and DELETE /{id}/soft follow identical structure
```

### Standard Endpoints per Entity

| Method | Path | Description |
|--------|------|-------------|
| POST | `/{entities}/` | Create |
| GET | `/{entities}/` | List (paginated) |
| GET | `/{entities}/{id}` | Get by ID |
| PUT | `/{entities}/{id}` | Update |
| DELETE | `/{entities}/{id}` | Hard delete |
| POST | `/{entities}/{id}/activate` | State -> ACTIVE |
| POST | `/{entities}/{id}/deactivate` | State -> INACTIVE |
| DELETE | `/{entities}/{id}/soft` | State -> DELETED |


## Dependency Injection Chain

```text
get_db() --> get_repository(db) --> get_use_case(repo) --> route handler
 Session      RepositoryImpl         UseCase              endpoint
```

```python
# src/shared/infrastructure/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://user:pass@localhost:5432/mydb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```


## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Entity | PascalCase | `Product` |
| Repository Impl | `{Entity}RepositoryImpl` | `ProductRepositoryImpl` |
| Use Case | `{Entity}UseCase` | `ProductUseCase` |
| Create/Update/Response DTO | `{Entity}Create/Update/Response` | `ProductCreate` |
| ORM Model | `{Entity}Model` | `ProductModel` |
| Files | `{entity}_router.py`, `_schemas.py`, `_model.py`, `_repository.py`, `_use_case.py` |
| Table name | Plural snake_case | `products`, `order_items` |
| Primary key | `id` (int, autoincrement) | |


## Alembic Migrations

Sync engine only. Import `Base` from shared and all ORM models so Alembic detects them.

```python
# alembic/env.py - KEY: use engine_from_config (sync), NOT async_engine_from_config
from alembic import context
from sqlalchemy import engine_from_config, pool
from src.shared.infrastructure.database import Base
from src.products.infrastructure.persistence.product_model import ProductModel  # noqa

target_metadata = Base.metadata

def run_migrations_online() -> None:
    connectable = engine_from_config(context.config.get_section(
        context.config.config_ini_section, {}),
        prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
```

```bash
alembic revision --autogenerate -m "add products table"  # Generate
alembic upgrade head                                      # Apply
alembic downgrade -1                                      # Rollback
```


## Error Handling

Simple approach: `HTTPException` in routes, `ValueError` in use cases.

```python
# In routes
entity = use_case.get_by_id(product_id)
if entity is None:
    raise HTTPException(status_code=404, detail="Product not found")

# In use cases
existing = self._repository.get_by_code(payload.code)
if existing is not None:
    raise ValueError(f"Product with code '{payload.code}' already exists")
```

Only create domain exceptions for genuinely complex business rules:

```python
class InsufficientStockError(Exception):
    def __init__(self, product_id: int, requested: int, available: int) -> None:
        super().__init__(f"Product {product_id}: requested {requested}, available {available}")
```

| Code | Method | Use Case |
|------|--------|----------|
| 201 | POST | Created |
| 200 | GET, PUT | Success |
| 204 | DELETE | Hard deleted |
| 404 | GET, PUT, DELETE | Not found |
| 422 | POST, PUT | Validation error |


## Testing Patterns

All tests are **sync** with SQLite in-memory.

### Repository Test

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.database import Base

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()

def test_create_product(db_session):
    repo = ProductRepositoryImpl(db_session)
    model = ProductModel(code="W001", name="Widget", sku="SKU-001",
                         unit_price=9.99, stock_quantity=50)
    saved = repo.create(model)
    assert saved.id is not None
    assert saved.name == "Widget"

def test_soft_delete_excludes_from_list(db_session):
    repo = ProductRepositoryImpl(db_session)
    model = ProductModel(code="W003", name="Tool", sku="SKU-003",
                         unit_price=5.99, stock_quantity=100)
    saved = repo.create(model)
    repo.soft_delete(saved.id)
    assert len(repo.get_all()) == 0
```

### Use Case Test (Mock) and API Test

```python
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

def test_create_use_case():
    mock_repo = MagicMock()
    mock_repo.create.return_value = MagicMock(id=1, code="W001", name="Widget")
    result = ProductUseCase(mock_repo).create(
        ProductCreate(code="W001", name="Widget", sku="SKU-001", unit_price=9.99))
    assert result.name == "Widget"
    mock_repo.create.assert_called_once()

def test_api_create(client=TestClient(app)):
    resp = client.post("/products/", json={"code": "W001", "name": "Widget",
                                            "sku": "SKU-001", "unit_price": 9.99})
    assert resp.status_code == 201 and resp.json()["name"] == "Widget"
```


## Entity State Management

```text
        deactivate()          soft_delete()
INACTIVE <---------- ACTIVE ----------> DELETED
    |                  ^                   |
    |   activate()     |   activate()      |
    +------------------+-------------------+
```

| State | Value | Meaning | Query behavior |
|-------|-------|---------|---------------|
| INACTIVE | 0 | Temporarily disabled | Included |
| ACTIVE | 1 | Normal state | Included |
| DELETED | 2 | Soft-deleted | Excluded from `get_all()` |


## Anti-Patterns

| Anti-Pattern | Correct Pattern |
|--------------|----------------|
| Business logic in routes | Move to use cases |
| Business logic in ORM model | Keep in domain aggregates |
| DB queries in domain layer | Use repository pattern |
| async Session | Use sync Session |
| UUID primary keys | Use int autoincrement |
| dataclass entities | Use Pydantic BaseModel |
| `SQLAlchemy{Entity}Repository` | Use `{Entity}RepositoryImpl` |
| `interfaces/` layer | Use `presentation/` layer |
| Domain events / event dispatcher | Direct method calls |
| Entity-to-ORM mapper classes | Use `from_attributes=True` |
| Skip `exclude_unset=True` on updates | Always use `exclude_unset=True` |
| ORM relationships across slices | Use IDs and repo queries |
