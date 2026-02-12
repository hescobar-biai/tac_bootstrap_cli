# Base Service Template

The foundation for all application services. This file should be placed at `src/shared/application/base_service.py`.

## Template

```python
"""
IDK: use-case, orchestration, business-logic

Module: base_service

Responsibility:
- Provide foundation for all application services
- Orchestrate business logic and CRUD operations
- Enforce domain invariants
- Coordinate repository and domain layers

Key Components:
- BaseService: Generic service with CRUD operations

Invariants:
- All mutations go through service layer
- Entity uniqueness enforced on code field
- Audit fields always populated
- Soft delete by default

Related Docs:
- docs/shared/application/base-service.md
"""

from typing import TypeVar, Generic, Type, Callable
from datetime import datetime, UTC

from shared.infrastructure.base_repository import BaseRepository
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse, PaginatedResponse
from shared.api.exceptions import EntityNotFoundError, DuplicateEntityError

TCreate = TypeVar("TCreate", bound=BaseCreate)
TUpdate = TypeVar("TUpdate", bound=BaseUpdate)
TResponse = TypeVar("TResponse", bound=BaseResponse)
TModel = TypeVar("TModel")
TDomain = TypeVar("TDomain")


class BaseService(Generic[TCreate, TUpdate, TResponse, TModel, TDomain]):
    """
    IDK: use-case, orchestration, crud-operations

    Responsibility:
    - Orchestrate entity business logic
    - Enforce domain invariants
    - Coordinate with repository layer
    - Provide CRUD operations with validation

    Invariants:
    - All mutations go through this service
    - Entity code uniqueness enforced
    - Audit fields always populated
    - Soft delete by default (state=2)
    - Entity not found raises exception

    Collaborators:
    - BaseRepository: data persistence
    - Domain entities: business logic
    - DTO schemas: data transfer

    Failure Modes:
    - EntityNotFoundError: entity doesn't exist
    - DuplicateEntityError: code already taken

    Related Docs:
    - docs/shared/application/base-service.md
    """

    def __init__(
        self,
        repository: BaseRepository[TModel],
        response_class: Type[TResponse],
        domain_class: Type[TDomain],
        entity_name: str,
        model_class: Type[TModel] | None = None,
    ):
        self.repository = repository
        self.response_class = response_class
        self.domain_class = domain_class
        self.entity_name = entity_name
        self.model_class = model_class or repository.model

    def create(
        self,
        data: TCreate,
        user_id: str | None = None,
    ) -> TResponse:
        """
        IDK: entity-creation, duplicate-check, audit-trail

        Responsibility:
        - Create new entity with validation
        - Check for duplicate codes
        - Set audit fields (created_by, created_at)
        - Persist to database via repository

        Invariants:
        - Code must be unique
        - created_at/created_by always set
        - Returns persisted entity

        Inputs:
        - data (TCreate): creation payload
        - user_id (str | None): creator ID for audit

        Outputs:
        - TResponse: created entity

        Failure Modes:
        - DuplicateEntityError: code exists
        - ValidationError: invalid data

        Related Docs:
        - docs/shared/application/service.md
        """
        # Check for duplicate code
        existing = self.repository.get_by_code(data.code)
        if existing:
            raise DuplicateEntityError(
                f"{self.entity_name} with code '{data.code}' already exists"
            )

        # Create domain entity
        now = datetime.now(UTC)
        entity_data = data.model_dump()
        entity_data.update({
            "created_at": now,
            "updated_at": now,
            "created_by": user_id,
            "updated_by": user_id,
        })

        domain_entity = self.domain_class(**entity_data)

        # Convert to ORM model and save
        db_model = self._to_model(domain_entity)
        saved = self.repository.create(db_model)

        return self.response_class.model_validate(saved)

    def get_by_id(self, entity_id: str) -> TResponse:
        """
        IDK: entity-retrieval, query, not-found-handling

        Responsibility:
        - Retrieve entity by primary key
        - Raise exception if not found
        - Return response DTO

        Invariants:
        - Raises EntityNotFoundError if not found
        - Never returns None

        Inputs:
        - entity_id (str): unique identifier

        Outputs:
        - TResponse: entity response

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist

        Related Docs:
        - docs/shared/application/service.md
        """
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFoundError(
                f"{self.entity_name} with ID '{entity_id}' not found"
            )
        return self.response_class.model_validate(entity)

    def get_by_code(self, code: str) -> TResponse:
        """
        IDK: business-key-lookup, query, not-found-handling

        Responsibility:
        - Retrieve entity by business code
        - Raise exception if not found
        - Return response DTO

        Invariants:
        - Raises EntityNotFoundError if not found
        - Never returns None

        Inputs:
        - code (str): business identifier

        Outputs:
        - TResponse: entity response

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist

        Related Docs:
        - docs/shared/application/service.md
        """
        entity = self.repository.get_by_code(code)
        if not entity:
            raise EntityNotFoundError(
                f"{self.entity_name} with code '{code}' not found"
            )
        return self.response_class.model_validate(entity)

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        include_deleted: bool = False,
    ) -> PaginatedResponse[TResponse]:
        """
        IDK: pagination, filtering, query-list

        Responsibility:
        - Retrieve paginated entity list
        - Apply dynamic filters and sorting
        - Exclude soft-deleted by default
        - Return total count for pagination

        Invariants:
        - Page is 1-indexed
        - Excludes state=2 by default
        - Returns PaginatedResponse wrapper
        - Calculates total pages

        Inputs:
        - page (int): page number (1-indexed)
        - page_size (int): items per page
        - filters (dict | None): field:value filter pairs
        - sort_by (str | None): field to sort by
        - sort_order (str): 'asc' or 'desc'
        - include_deleted (bool): include soft-deleted entities

        Outputs:
        - PaginatedResponse[TResponse]: paginated response

        Related Docs:
        - docs/shared/application/pagination.md
        """
        # Exclude soft-deleted by default
        effective_filters = filters.copy() if filters else {}
        if not include_deleted and "state" not in effective_filters:
            effective_filters["state"] = 1  # Active only

        items, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=effective_filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return PaginatedResponse(
            data=[self.response_class.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )

    def update(
        self,
        entity_id: str,
        data: TUpdate,
        user_id: str | None = None,
    ) -> TResponse:
        """
        IDK: entity-update, partial-update, audit-trail

        Responsibility:
        - Update existing entity
        - Support partial updates
        - Update audit trail (updated_by, updated_at, version)
        - Validate entity exists

        Invariants:
        - Entity must exist (raises if not)
        - updated_at/updated_by always set
        - version incremented
        - Only provided fields updated

        Inputs:
        - entity_id (str): entity ID to update
        - data (TUpdate): update payload
        - user_id (str | None): updater ID for audit

        Outputs:
        - TResponse: updated entity

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist

        Related Docs:
        - docs/shared/application/service.md
        """
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(
                f"{self.entity_name} with ID '{entity_id}' not found"
            )

        update_data = data.model_dump(exclude_unset=True)
        if user_id:
            update_data["updated_by"] = user_id

        updated = self.repository.update(entity_id, update_data)
        return self.response_class.model_validate(updated)

    def delete(
        self,
        entity_id: str,
        user_id: str | None = None,
    ) -> bool:
        """
        IDK: soft-delete, state-transition, recoverable

        Responsibility:
        - Soft delete entity (set state=2)
        - Preserve data for recovery
        - Update audit trail
        - Validate entity exists

        Invariants:
        - Sets state to 2 (DELETED)
        - Data remains in database
        - Raises if entity not found

        Inputs:
        - entity_id (str): entity ID to delete
        - user_id (str | None): deleter ID for audit

        Outputs:
        - bool: True if deleted

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist

        Related Docs:
        - docs/shared/application/soft-delete.md
        """
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(
                f"{self.entity_name} with ID '{entity_id}' not found"
            )

        update_data = {"state": 2}  # DELETED
        if user_id:
            update_data["updated_by"] = user_id

        self.repository.update(entity_id, update_data)
        return True

    def hard_delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, permanent-removal, irreversible

        Responsibility:
        - Permanently delete entity from database
        - Not recoverable after deletion
        - Validate entity exists

        Invariants:
        - Entity removed from database
        - Not recoverable
        - Raises if entity not found

        Inputs:
        - entity_id (str): entity ID to delete

        Outputs:
        - bool: True if deleted

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist
        - IntegrityError: foreign key constraints

        Related Docs:
        - docs/shared/application/delete-operations.md
        """
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(
                f"{self.entity_name} with ID '{entity_id}' not found"
            )

        return self.repository.delete(entity_id)

    def activate(self, entity_id: str, user_id: str | None = None) -> TResponse:
        """
        IDK: state-transition, activation, lifecycle

        Responsibility:
        - Activate entity (set state=1)
        - Update audit trail

        Outputs:
        - TResponse: activated entity
        """
        return self._change_state(entity_id, 1, user_id)

    def deactivate(self, entity_id: str, user_id: str | None = None) -> TResponse:
        """
        IDK: state-transition, deactivation, lifecycle

        Responsibility:
        - Deactivate entity (set state=0)
        - Update audit trail

        Outputs:
        - TResponse: deactivated entity
        """
        return self._change_state(entity_id, 0, user_id)

    def restore(self, entity_id: str, user_id: str | None = None) -> TResponse:
        """
        IDK: entity-restore, soft-delete-recovery, state-transition

        Responsibility:
        - Restore soft-deleted entity (set state=1)
        - Update audit trail

        Outputs:
        - TResponse: restored entity
        """
        return self._change_state(entity_id, 1, user_id)

    def _change_state(
        self,
        entity_id: str,
        state: int,
        user_id: str | None = None,
    ) -> TResponse:
        """
        IDK: state-transition, internal-helper, audit-trail

        Responsibility:
        - Change entity state
        - Update audit trail
        - Validate entity exists

        Inputs:
        - entity_id (str): entity ID
        - state (int): new state value (0, 1, or 2)
        - user_id (str | None): user making change

        Outputs:
        - TResponse: updated entity

        Failure Modes:
        - EntityNotFoundError: entity doesn't exist
        """
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(
                f"{self.entity_name} with ID '{entity_id}' not found"
            )

        update_data = {"state": state}
        if user_id:
            update_data["updated_by"] = user_id

        updated = self.repository.update(entity_id, update_data)
        return self.response_class.model_validate(updated)

    def exists(self, entity_id: str) -> bool:
        """
        IDK: existence-check, query, predicate

        Responsibility:
        - Check if entity exists
        - Delegate to repository

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - bool: True if exists, False otherwise
        """
        return self.repository.exists(entity_id)

    def count(self, filters: dict | None = None) -> int:
        """
        IDK: aggregation, count-query, filtering

        Responsibility:
        - Count entities with optional filters
        - Delegate to repository

        Inputs:
        - filters (dict | None): field:value filter pairs

        Outputs:
        - int: count of matching entities
        """
        return self.repository.count(filters)

    def _to_model(self, entity: TDomain) -> TModel:
        """
        IDK: domain-to-orm, mapping, internal-helper

        Responsibility:
        - Convert domain entity to ORM model
        - Map all fields

        Inputs:
        - entity (TDomain): domain entity

        Outputs:
        - TModel: ORM model instance
        """
        return self.model_class(**entity.model_dump())
```

## Directory Setup

```
src/
└── shared/
    └── application/
        ├── __init__.py
        ├── base_schema.py
        └── base_service.py  # <-- This file
```

**`src/shared/application/__init__.py`** (updated):
```python
"""Shared application layer - base schemas, services, and common DTOs."""
from .base_schema import (
    BaseCreate,
    BaseUpdate,
    BaseResponse,
    PaginatedResponse,
    MessageResponse,
    ErrorDetail,
    ErrorResponse,
)
from .base_service import BaseService

__all__ = [
    "BaseCreate",
    "BaseUpdate",
    "BaseResponse",
    "PaginatedResponse",
    "MessageResponse",
    "ErrorDetail",
    "ErrorResponse",
    "BaseService",
]
```

## Usage Example

### Entity Service Implementation

```python
# src/product_catalog/application/service.py
"""Product service implementation."""

from shared.application.base_service import BaseService
from ..domain.product import Product
from ..infrastructure.repository import ProductRepository
from ..infrastructure.models import ProductModel
from .schemas import ProductCreate, ProductUpdate, ProductResponse


class ProductService(BaseService[
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductModel,
    Product
]):
    """Service for Product business logic."""

    def __init__(self, repository: ProductRepository):
        super().__init__(
            repository=repository,
            response_class=ProductResponse,
            domain_class=Product,
            entity_name="Product",
            model_class=ProductModel,
        )

    # Custom business methods

    def get_available(self) -> list[ProductResponse]:
        """Get all available products."""
        items = self.repository.get_available()
        return [ProductResponse.model_validate(item) for item in items]

    def get_by_category(self, category: str) -> list[ProductResponse]:
        """Get products by category."""
        items = self.repository.get_by_category(category)
        return [ProductResponse.model_validate(item) for item in items]

    def update_stock(
        self,
        entity_id: str,
        quantity: int,
        user_id: str | None = None,
    ) -> ProductResponse:
        """Update product stock quantity."""
        return self.update(
            entity_id,
            ProductUpdate(stock_quantity=quantity),
            user_id=user_id,
        )

    def check_low_stock(self, threshold: int = 10) -> list[ProductResponse]:
        """Get products with stock below threshold."""
        items = self.repository.get_low_stock(threshold)
        return [ProductResponse.model_validate(item) for item in items]
```

## Benefits

1. **DRY**: Common CRUD logic defined once
2. **Consistency**: All services behave the same way
3. **Audit Trail**: Built-in support for created_by/updated_by
4. **Soft Delete**: Default behavior is soft delete
5. **Type Safety**: Full generic type support
6. **Extensibility**: Easy to add custom methods in derived classes
