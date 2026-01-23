"""
IDK: api-schema, dto, request-response

Module: base_schema

Responsibility:
- Provide foundation for API request/response DTOs
- Separate API layer concerns from domain entity models
- Standardize Create/Update/Response patterns for CRUD operations

Key Components:
- BaseCreate: Empty foundation for entity creation DTOs
- BaseUpdate: Independent foundation for partial update DTOs
- BaseResponse: Common response fields with ORM compatibility

Invariants:
- BaseCreate has no common fields (entity-specific creation data)
- BaseUpdate has no common fields (entities add their fields as Optional)
- BaseResponse includes id, state, version, timestamps, and audit fields
- BaseResponse uses from_attributes=True for ORM model conversion

Usage Examples:

```python
# Creating a Product schema
class ProductCreate(BaseCreate):
    name: str
    price: float
    category: str

class ProductUpdate(BaseUpdate):
    name: str | None = None
    price: float | None = None
    category: str | None = None

class ProductResponse(BaseResponse):
    name: str
    price: float
    category: str

# Service layer usage
product_entity = Product(code="PROD-001", name="Laptop", price=999.99)
response = ProductResponse.model_validate(product_entity)
```

Related Docs:
- docs/shared/domain/base-schema.md
- ai_docs/doc/create-crud-entity/
"""

from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class BaseCreate(BaseModel):
    """
    IDK: api-schema, create-dto, request-model

    Responsibility:
    - Serve as foundation for entity creation DTOs
    - Capture user input for resource creation
    - Exclude system-managed fields (id, timestamps, audit data)

    Invariants:
    - No common fields by default (creation data is entity-specific)
    - Does not include audit fields (created_by, updated_by)
    - Does not include system fields (id, version, timestamps)

    Usage Pattern:
    - Entities inherit and add their required creation fields
    - Used in POST endpoints for resource creation
    - Service layer maps to domain entities and injects system fields

    Example:

    ```python
    class ProductCreate(BaseCreate):
        name: str
        price: float
        category: str

    # POST /products
    def create_product(data: ProductCreate) -> ProductResponse:
        entity = Product(
            code=generate_code(),
            name=data.name,
            price=data.price,
            category=data.category,
            created_by=current_user.id  # injected by service
        )
        return ProductResponse.model_validate(entity)
    ```

    Collaborators:
    - Pydantic BaseModel: validation and serialization
    - Service layer: maps to domain entities

    Failure Modes:
    - ValidationError: invalid field values from user input

    Related Docs:
    - docs/shared/domain/base-schema.md
    - ai_docs/doc/create-crud-entity/
    """
    pass


class BaseUpdate(BaseModel):
    """
    IDK: api-schema, update-dto, partial-update

    Responsibility:
    - Serve as foundation for partial update DTOs
    - Support PATCH operations with selective field updates
    - Exclude system-managed fields (id, version, timestamps, audit data)

    Invariants:
    - Independent from BaseCreate (no inheritance)
    - All fields in subclasses should be Optional
    - Does not include audit fields (updated_by)
    - Does not include immutable fields (id, created_at, created_by)

    Usage Pattern:
    - Entities inherit and add their fields as Optional[T]
    - Used in PATCH endpoints for partial updates
    - Service layer applies only non-None fields to entity
    - Enables clients to send only changed fields

    Example:

    ```python
    class ProductUpdate(BaseUpdate):
        name: str | None = None
        price: float | None = None
        category: str | None = None

    # PATCH /products/{id}
    def update_product(id: UUID, data: ProductUpdate) -> ProductResponse:
        entity = repository.get(id)
        if data.name is not None:
            entity.name = data.name
        if data.price is not None:
            entity.price = data.price
        entity.mark_updated(current_user.id)  # injected by service
        return ProductResponse.model_validate(entity)
    ```

    Collaborators:
    - Pydantic BaseModel: validation and serialization
    - Service layer: applies partial updates to entities

    Failure Modes:
    - ValidationError: invalid field values from user input

    Related Docs:
    - docs/shared/domain/base-schema.md
    - ai_docs/doc/create-crud-entity/
    """
    pass


class BaseResponse(BaseModel):
    """
    IDK: api-schema, response-dto, orm-mapping

    Responsibility:
    - Serve as foundation for entity response DTOs
    - Provide common response fields for all CRUD operations
    - Enable ORM model to DTO conversion via from_attributes

    Invariants:
    - All response DTOs include id, state, version
    - All response DTOs include timestamps (created_at, updated_at)
    - All response DTOs include audit fields (created_by, updated_by)
    - Uses ConfigDict(from_attributes=True) for ORM compatibility

    Usage Pattern:
    - Entities inherit and add their specific response fields
    - Used in all GET/POST/PUT/PATCH responses
    - Service layer converts entity to response: Response.model_validate(entity)
    - Supports both dict and ORM model instantiation

    Example:

    ```python
    class ProductResponse(BaseResponse):
        name: str
        price: float
        category: str

    # GET /products/{id}
    def get_product(id: UUID) -> ProductResponse:
        entity = repository.get(id)
        return ProductResponse.model_validate(entity)

    # POST /products
    def create_product(data: ProductCreate) -> ProductResponse:
        entity = Product(**data.model_dump(), created_by=current_user.id)
        repository.save(entity)
        return ProductResponse.model_validate(entity)
    ```

    Collaborators:
    - Pydantic BaseModel: validation and serialization
    - Domain Entity: source of response data
    - Service layer: performs entity to response conversion

    Failure Modes:
    - ValidationError: entity data doesn't match schema

    Related Docs:
    - docs/shared/domain/base-schema.md
    - ai_docs/doc/create-crud-entity/
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        ...,
        description="Unique identifier (UUID v4)",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )

    state: str = Field(
        ...,
        description="Entity state (inactive, active, deleted)",
        examples=["active", "inactive", "deleted"]
    )

    version: int = Field(
        ...,
        ge=1,
        description="Version number for optimistic locking"
    )

    created_at: datetime = Field(
        ...,
        description="UTC timestamp of creation"
    )

    updated_at: datetime = Field(
        ...,
        description="UTC timestamp of last update"
    )

    created_by: UUID = Field(
        ...,
        description="User ID who created this resource"
    )

    updated_by: UUID = Field(
        ...,
        description="User ID who last updated this resource"
    )
