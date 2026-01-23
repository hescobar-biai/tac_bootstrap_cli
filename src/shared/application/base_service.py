"""
IDK: service-layer, business-logic, crud-operations

Module: base_service

Responsibility:
- Provide generic CRUD operations for all domain entities
- Orchestrate business logic between API routes and repository layer
- Enforce audit trail, versioning, and soft delete patterns

Key Components:
- PaginatedResponse[T]: Generic pagination wrapper for list responses
- BaseService[TCreate, TUpdate, TResponse, TModel, TDomain]: Generic service with full CRUD

Invariants:
- All mutations update audit fields (created_by, updated_by)
- All updates increment version for optimistic locking
- Soft delete sets state=2 instead of physical deletion
- All queries exclude entities with state=2 (handled by repository)
- Missing entities raise HTTPException(404)

Usage Examples:

```python
# Define entity-specific service by inheriting BaseService
from src.shared.application.base_service import BaseService
from src.products.domain.schemas import ProductCreate, ProductUpdate, ProductResponse
from src.products.infrastructure.models import ProductModel
from src.products.domain.entities import Product

class ProductService(BaseService[ProductCreate, ProductUpdate, ProductResponse, ProductModel, Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

# Use in FastAPI routes
@router.post("/products", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(data, user_id=current_user.id)

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    return service.get_by_id(product_id)

@router.get("/products", response_model=PaginatedResponse[ProductResponse])
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str | None = Query(None),
    service: ProductService = Depends(get_product_service)
):
    filters = {"category": category} if category else {}
    return service.get_all(page, page_size, filters, sort_by="created_at", sort_order="desc")

@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(product_id, data, user_id=current_user.id)

@router.delete("/products/{product_id}")
def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    service.delete(product_id, user_id=current_user.id)
    return {"message": "Product deleted successfully"}
```

Related Docs:
- docs/shared/application/base-service.md
- ai_docs/doc/create-crud-entity/
"""

from typing import Generic, TypeVar, Any
from math import ceil
from pydantic import BaseModel
from fastapi import HTTPException

# Generic type variables for service layer
TCreate = TypeVar('TCreate', bound=BaseModel)      # Create schema (e.g., ProductCreate)
TUpdate = TypeVar('TUpdate', bound=BaseModel)      # Update schema (e.g., ProductUpdate)
TResponse = TypeVar('TResponse', bound=BaseModel)  # Response schema (e.g., ProductResponse)
TModel = TypeVar('TModel')                         # ORM model (e.g., ProductModel)
TDomain = TypeVar('TDomain')                       # Domain entity (e.g., Product)


class PaginatedResponse(BaseModel, Generic[TResponse]):
    """
    IDK: pagination, response-wrapper, list-response

    Responsibility:
    - Wrap paginated list responses with metadata
    - Provide navigation info for UI pagination controls
    - Standardize pagination across all list endpoints

    Invariants:
    - items contains the current page of results
    - total reflects total count across all pages
    - page is 1-indexed (starts at 1, not 0)
    - total_pages calculated as ceil(total / page_size)

    Usage Pattern:
    - Service layer returns this from get_all() methods
    - API routes use as response_model for list endpoints
    - Clients use total_pages and page for navigation

    Example:

    ```python
    # Service returns paginated response
    response = PaginatedResponse[ProductResponse](
        items=[product1, product2, product3],
        total=150,
        page=1,
        page_size=10,
        total_pages=15
    )

    # FastAPI route
    @router.get("/products", response_model=PaginatedResponse[ProductResponse])
    def list_products(page: int = 1, page_size: int = 10):
        return service.get_all(page, page_size, {}, "created_at", "desc")
    ```

    Collaborators:
    - BaseService: generates paginated responses
    - FastAPI: serializes to JSON

    Failure Modes:
    - None (simple data container)

    Related Docs:
    - docs/shared/application/pagination.md
    """

    items: list[TResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BaseService(Generic[TCreate, TUpdate, TResponse, TModel, TDomain]):
    """
    IDK: service-layer, crud-operations, business-logic

    Responsibility:
    - Provide generic CRUD operations for domain entities
    - Orchestrate business logic between routes and repository
    - Enforce audit trail, versioning, and soft delete patterns
    - Handle error cases and raise appropriate HTTP exceptions

    Invariants:
    - All create operations set created_by and updated_by
    - All update operations set updated_by and increment version
    - Soft delete sets state=2, preserves data
    - Hard delete performs physical deletion
    - All queries exclude state=2 entities (repository enforces)
    - Missing or deleted entities raise HTTPException(404)

    Generic Type Parameters:
    - TCreate: Pydantic schema for creation (e.g., ProductCreate)
    - TUpdate: Pydantic schema for updates (e.g., ProductUpdate)
    - TResponse: Pydantic schema for responses (e.g., ProductResponse)
    - TModel: ORM model class (e.g., ProductModel)
    - TDomain: Domain entity class (e.g., Product)

    Usage Pattern:
    - Entity-specific services inherit and specify types
    - Repository injected via constructor
    - Used by FastAPI route handlers

    Example:

    ```python
    class ProductService(BaseService[ProductCreate, ProductUpdate, ProductResponse, ProductModel, Product]):
        def __init__(self, repository: ProductRepository):
            super().__init__(repository)

        # Add entity-specific business logic methods if needed
        def calculate_discount(self, product_id: str, discount_percent: float) -> ProductResponse:
            product = self.repository.get_by_id(product_id)
            if not product or product.state == 2:
                raise HTTPException(404, "Product not found")
            product.price = product.price * (1 - discount_percent / 100)
            product.mark_updated()
            updated = self.repository.update(product)
            return ProductResponse.model_validate(updated)
    ```

    Collaborators:
    - Repository: persistence layer for entities
    - Pydantic schemas: DTOs for API layer
    - FastAPI: web framework for routes

    Failure Modes:
    - HTTPException(404): entity not found or deleted
    - HTTPException(400): invalid filters or sort columns (from repository)
    - ValidationError: invalid schema data (caught by Pydantic/FastAPI)

    Related Docs:
    - docs/shared/application/base-service.md
    - ai_docs/doc/create-crud-entity/
    """

    def __init__(self, repository: Any):
        """
        IDK: dependency-injection, constructor

        Responsibility:
        - Initialize service with repository dependency
        - Enable testability via dependency injection

        Invariants:
        - Repository must implement CRUD interface

        Inputs:
        - repository: persistence layer for entities

        Outputs:
        - None (initializes instance)

        Related Docs:
        - docs/shared/application/dependency-injection.md
        """
        self.repository = repository

    def create(self, data: TCreate, user_id: str | None = None) -> TResponse:
        """
        IDK: create-operation, audit-trail, persistence

        Responsibility:
        - Create new entity from DTO
        - Set audit fields (created_by, updated_by)
        - Persist entity via repository
        - Return response DTO

        Invariants:
        - created_by and updated_by set to user_id
        - If user_id is None, allows system/anonymous operations
        - Repository handles transaction and ID generation

        Inputs:
        - data: create DTO with entity data
        - user_id: user performing the operation (None for system)

        Outputs:
        - TResponse: created entity as response DTO

        Failure Modes:
        - ValidationError: invalid data (caught by Pydantic)
        - RepositoryError: database constraint violation

        Example:

        ```python
        product_data = ProductCreate(name="Laptop", price=999.99, category="Electronics")
        product = service.create(product_data, user_id="user-123")
        ```

        Related Docs:
        - docs/shared/application/crud-operations.md
        """
        # Convert DTO to domain entity
        entity_data = data.model_dump()
        entity_data['created_by'] = user_id
        entity_data['updated_by'] = user_id

        # Create entity via repository
        created = self.repository.create(entity_data)

        # Return response DTO
        return TResponse.model_validate(created)

    def get_by_id(self, entity_id: str) -> TResponse:
        """
        IDK: read-operation, retrieval, not-found-handling

        Responsibility:
        - Retrieve single entity by ID
        - Raise 404 if not found or soft-deleted (state=2)
        - Return response DTO

        Invariants:
        - Raises HTTPException(404) if entity not found
        - Raises HTTPException(404) if entity.state == 2 (soft-deleted)
        - Repository excludes state=2 entities automatically

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - TResponse: entity as response DTO

        Failure Modes:
        - HTTPException(404): entity not found or deleted

        Example:

        ```python
        product = service.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        ```

        Related Docs:
        - docs/shared/application/error-handling.md
        """
        entity = self.repository.get_by_id(entity_id)

        if not entity or (hasattr(entity, 'state') and entity.state == 2):
            raise HTTPException(status_code=404, detail="Entity not found")

        return TResponse.model_validate(entity)

    def get_all(
        self,
        page: int,
        page_size: int,
        filters: dict | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse[TResponse]:
        """
        IDK: list-operation, pagination, filtering, sorting

        Responsibility:
        - Retrieve paginated list of entities
        - Apply filters and sorting (validated by repository)
        - Exclude soft-deleted entities (state=2)
        - Return paginated response with metadata

        Invariants:
        - Repository excludes state=2 entities automatically
        - Repository validates filter columns and sort columns
        - page is 1-indexed (starts at 1)
        - total_pages calculated as ceil(total / page_size)
        - Invalid filters/sort columns raise ValueError → HTTPException(400)

        Inputs:
        - page: page number (1-indexed)
        - page_size: items per page
        - filters: dict of column:value for exact match filtering
        - sort_by: column name to sort by
        - sort_order: "asc" or "desc"

        Outputs:
        - PaginatedResponse[TResponse]: paginated results with metadata

        Failure Modes:
        - HTTPException(400): invalid filter column or sort column (from repository)

        Example:

        ```python
        # Get page 2 of products in Electronics category, sorted by price
        response = service.get_all(
            page=2,
            page_size=10,
            filters={"category": "Electronics"},
            sort_by="price",
            sort_order="asc"
        )
        ```

        Related Docs:
        - docs/shared/application/pagination.md
        - docs/shared/application/filtering.md
        """
        filters = filters or {}

        try:
            # Repository validates columns and excludes state=2
            items, total = self.repository.get_all(
                page=page,
                page_size=page_size,
                filters=filters,
                sort_by=sort_by,
                sort_order=sort_order
            )
        except ValueError as e:
            # Invalid filter/sort column
            raise HTTPException(status_code=400, detail=str(e))

        # Convert entities to response DTOs
        response_items = [TResponse.model_validate(item) for item in items]

        # Calculate total pages
        total_pages = ceil(total / page_size) if page_size > 0 else 0

        return PaginatedResponse[TResponse](
            items=response_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    def update(
        self,
        entity_id: str,
        data: TUpdate,
        user_id: str | None = None
    ) -> TResponse:
        """
        IDK: update-operation, partial-update, versioning

        Responsibility:
        - Update entity with partial data (PATCH semantics)
        - Set updated_by and increment version
        - Persist changes via repository
        - Return updated entity as response DTO

        Invariants:
        - Entity must exist and not be deleted (checked via get_by_id)
        - Only non-None fields from TUpdate are applied
        - updated_by set to user_id
        - version incremented by 1
        - Raises HTTPException(404) if entity not found

        Inputs:
        - entity_id: unique identifier of entity
        - data: update DTO with partial data (None fields ignored)
        - user_id: user performing the operation (None for system)

        Outputs:
        - TResponse: updated entity as response DTO

        Failure Modes:
        - HTTPException(404): entity not found or deleted
        - ValidationError: invalid data (caught by Pydantic)

        Example:

        ```python
        # Update only price (other fields unchanged)
        update_data = ProductUpdate(price=899.99)
        product = service.update("550e8400-e29b-41d4-a716-446655440000", update_data, user_id="user-123")
        ```

        Related Docs:
        - docs/shared/application/partial-updates.md
        - docs/shared/application/versioning.md
        """
        # Fetch entity (raises 404 if not found or deleted)
        entity = self.repository.get_by_id(entity_id)
        if not entity or (hasattr(entity, 'state') and entity.state == 2):
            raise HTTPException(status_code=404, detail="Entity not found")

        # Apply non-None fields from update DTO
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None and hasattr(entity, field):
                setattr(entity, field, value)

        # Set audit fields
        if hasattr(entity, 'updated_by'):
            entity.updated_by = user_id
        if hasattr(entity, 'version'):
            entity.version += 1

        # Mark as updated (sets updated_at)
        if hasattr(entity, 'mark_updated'):
            entity.mark_updated(user_id)

        # Persist via repository
        updated = self.repository.update(entity)

        return TResponse.model_validate(updated)

    def delete(self, entity_id: str, user_id: str | None = None) -> bool:
        """
        IDK: soft-delete, state-transition, data-preservation

        Responsibility:
        - Soft delete entity by setting state=2
        - Preserve data for audit trail and recovery
        - Set updated_by to track who deleted
        - Return success status

        Invariants:
        - Entity must exist (checked via get_by_id)
        - state set to 2 (DELETED)
        - updated_by set to user_id
        - Data remains in database
        - Raises HTTPException(404) if entity not found

        Inputs:
        - entity_id: unique identifier of entity
        - user_id: user performing the deletion (None for system)

        Outputs:
        - bool: True on success

        Failure Modes:
        - HTTPException(404): entity not found

        Example:

        ```python
        # Soft delete product
        service.delete("550e8400-e29b-41d4-a716-446655440000", user_id="user-123")
        ```

        Related Docs:
        - docs/shared/application/soft-delete.md
        """
        # Fetch entity (raises 404 if not found)
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")

        # Set state to DELETED
        if hasattr(entity, 'state'):
            entity.state = 2

        # Set audit fields
        if hasattr(entity, 'updated_by'):
            entity.updated_by = user_id

        # Mark as updated (sets updated_at)
        if hasattr(entity, 'mark_updated'):
            entity.mark_updated(user_id)

        # Persist via repository
        self.repository.update(entity)

        return True

    def hard_delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, physical-deletion, permanent-removal

        Responsibility:
        - Physically delete entity from database
        - Remove data permanently (no recovery)
        - Return success status

        Invariants:
        - Entity must exist (even if state=2)
        - Data is permanently removed
        - Raises HTTPException(404) if entity not found

        WARNING: This operation is irreversible. Use with caution.
        Prefer soft delete (delete() method) for most use cases.

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True on success

        Failure Modes:
        - HTTPException(404): entity not found

        Example:

        ```python
        # Permanently delete product (admin operation)
        service.hard_delete("550e8400-e29b-41d4-a716-446655440000")
        ```

        Related Docs:
        - docs/shared/application/hard-delete.md
        """
        # Fetch entity (even if deleted)
        entity = self.repository.get_by_id(entity_id, include_deleted=True) if hasattr(self.repository.get_by_id, '__code__') and 'include_deleted' in self.repository.get_by_id.__code__.co_varnames else self.repository.get_by_id(entity_id)

        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")

        # Physical deletion
        self.repository.delete(entity_id)

        return True
