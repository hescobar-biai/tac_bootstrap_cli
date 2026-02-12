# Base Schema Template

The foundation for all application schemas (DTOs). This file should be placed at `src/shared/application/base_schema.py`.

## Template

```python
"""
IDK: dto, schema-validation, application-layer

Module: base_schema

Responsibility:
- Provide foundation for all application DTOs
- Define consistent request/response patterns
- Support type-safe validation with Pydantic
- Align with Entity base class structure

Key Components:
- BaseCreate: Base schema for creation requests
- BaseUpdate: Base schema for update requests
- BaseResponse: Base schema for API responses
- PaginatedResponse: Generic paginated response wrapper
- MessageResponse: Simple message responses
- ErrorResponse: Standard error responses

Invariants:
- All schemas use Pydantic BaseModel
- Create schemas require code and name
- Update schemas allow partial updates
- Response schemas include full entity data

Related Docs:
- docs/shared/application/base-schema.md
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseCreate(BaseModel):
    """
    IDK: dto, create-schema, input-validation

    Responsibility:
    - Provide base schema for entity creation
    - Define common required fields
    - Validate creation input data
    - Support entity-specific field extension

    Invariants:
    - code is required and non-empty
    - name is required and non-empty
    - Extra fields are forbidden
    - String whitespace is stripped

    Collaborators:
    - Pydantic BaseModel: validation engine
    - Service layer: consumes creation DTOs

    Related Docs:
    - docs/shared/application/schemas.md
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    code: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Business code/reference (unique identifier)",
        examples=["PROD-001", "USR-2024-001"],
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable name",
        examples=["Product Name", "User Name"],
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Detailed description",
    )


class BaseUpdate(BaseModel):
    """
    IDK: dto, update-schema, partial-update

    Responsibility:
    - Provide base schema for entity updates
    - Support partial update patterns
    - Validate update input data
    - Allow optional field updates

    Invariants:
    - All fields are optional (nullable)
    - Extra fields are forbidden
    - String whitespace is stripped
    - Supports partial updates via exclude_unset

    Collaborators:
    - Pydantic BaseModel: validation engine
    - Service layer: consumes update DTOs

    Related Docs:
    - docs/shared/application/schemas.md
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Human-readable name",
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Detailed description",
    )


class BaseResponse(BaseModel):
    """
    IDK: dto, response-schema, serialization

    Responsibility:
    - Provide base schema for API responses
    - Include all standard Entity fields
    - Support ORM model serialization
    - Enable entity-specific field extension

    Invariants:
    - Contains all base Entity fields
    - Supports from_attributes (ORM mode)
    - Extra fields are ignored
    - All audit fields included

    Collaborators:
    - Pydantic BaseModel: serialization engine
    - ORM models: data source via from_attributes
    - API layer: response serialization

    Related Docs:
    - docs/shared/application/schemas.md
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    # Core Identity Fields
    id: str = Field(description="Unique identifier (UUID)")
    code: str = Field(description="Business code/reference")
    name: str = Field(description="Human-readable name")
    description: str | None = Field(description="Detailed description")
    type: str | None = Field(description="Entity type discriminator")

    # Audit Trail
    created_at: datetime = Field(description="UTC timestamp of creation")
    created_by: str | None = Field(description="User who created this entity")
    updated_at: datetime = Field(description="UTC timestamp of last update")
    updated_by: str | None = Field(description="User who last updated this entity")

    # State Management
    state: int = Field(description="Entity state: 0=inactive, 1=active, 2=deleted")
    status: str | None = Field(description="Business status (domain-specific)")
    version: int = Field(description="Version number for optimistic locking")

    # Multi-tenancy & Ownership
    organization_id: str | None = Field(description="Organization/tenant identifier")
    project_id: str | None = Field(description="Project identifier")
    owner: str | None = Field(description="Owner user ID")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    IDK: pagination, response-wrapper, generic-type

    Responsibility:
    - Wrap paginated list responses
    - Provide pagination metadata
    - Support generic item types
    - Calculate pagination helpers

    Invariants:
    - page is 1-indexed and >= 1
    - page_size is between 1 and 100
    - total is >= 0
    - pages is >= 0
    - data is a list of items

    Collaborators:
    - Generic type T: item type
    - Service layer: pagination logic

    Related Docs:
    - docs/shared/application/pagination.md
    """

    model_config = ConfigDict(from_attributes=True)

    data: list[T] = Field(description="List of items")
    total: int = Field(ge=0, description="Total number of items")
    page: int = Field(ge=1, description="Current page number")
    page_size: int = Field(ge=1, le=100, description="Items per page")
    pages: int = Field(ge=0, description="Total number of pages")

    @property
    def has_next(self) -> bool:
        """
        IDK: pagination, predicate, navigation

        Responsibility:
        - Check if next page exists
        - Support pagination navigation

        Outputs:
        - bool: True if next page exists
        """
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        """
        IDK: pagination, predicate, navigation

        Responsibility:
        - Check if previous page exists
        - Support pagination navigation

        Outputs:
        - bool: True if previous page exists
        """
        return self.page > 1


class MessageResponse(BaseModel):
    """
    IDK: response-message, success-indicator, simple-response

    Responsibility:
    - Provide simple message responses
    - Indicate operation success
    - Return confirmation messages

    Invariants:
    - message is required string
    - success defaults to True
    - Used for operations without data return

    Related Docs:
    - docs/shared/application/responses.md
    """

    message: str = Field(description="Response message")
    success: bool = Field(default=True, description="Operation success status")


class ErrorDetail(BaseModel):
    """
    IDK: error-detail, validation-error, field-error

    Responsibility:
    - Provide detailed error information
    - Identify error field and message
    - Support validation error responses

    Invariants:
    - message is required
    - field is optional (may be global error)
    - code is optional error code

    Related Docs:
    - docs/shared/application/error-handling.md
    """

    field: str | None = Field(default=None, description="Field that caused the error")
    message: str = Field(description="Error message")
    code: str | None = Field(default=None, description="Error code")


class ErrorResponse(BaseModel):
    """
    IDK: error-response, exception-handling, api-error

    Responsibility:
    - Provide standard error responses
    - Include error details
    - Support structured error handling

    Invariants:
    - detail is required
    - errors is optional list of ErrorDetail
    - Used for exception responses

    Related Docs:
    - docs/shared/application/error-handling.md
    """

    detail: str = Field(description="Error description")
    errors: list[ErrorDetail] | None = Field(
        default=None, description="Detailed error list"
    )
```

## Directory Setup

Create the file at:
```
src/
└── shared/
    ├── __init__.py
    ├── domain/
    │   └── base_entity.py
    └── application/
        ├── __init__.py
        └── base_schema.py  # <-- This file
```

**`src/shared/application/__init__.py`**:
```python
"""Shared application layer - base schemas and common DTOs."""
from .base_schema import (
    BaseCreate,
    BaseUpdate,
    BaseResponse,
    PaginatedResponse,
    MessageResponse,
    ErrorDetail,
    ErrorResponse,
)

__all__ = [
    "BaseCreate",
    "BaseUpdate",
    "BaseResponse",
    "PaginatedResponse",
    "MessageResponse",
    "ErrorDetail",
    "ErrorResponse",
]
```

## Usage Example

### Entity-Specific Schemas

```python
# src/product_catalog/application/schemas.py
"""Product request/response schemas."""

from pydantic import Field
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse


class ProductCreate(BaseCreate):
    """Schema for creating a new Product."""

    # Entity-specific required fields
    sku: str = Field(..., min_length=1, max_length=50, description="Stock Keeping Unit")
    unit_price: float = Field(..., ge=0, description="Price per unit")

    # Entity-specific optional fields
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool = Field(default=True)
    stock_quantity: int = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list)


class ProductUpdate(BaseUpdate):
    """Schema for updating a Product (all fields optional)."""

    sku: str | None = Field(default=None, min_length=1, max_length=50)
    unit_price: float | None = Field(default=None, ge=0)
    category: str | None = None
    brand: str | None = None
    is_available: bool | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    tags: list[str] | None = None


class ProductResponse(BaseResponse):
    """Schema for Product API response."""

    # Entity-specific fields (inherited fields come from BaseResponse)
    sku: str
    unit_price: float
    category: str | None
    brand: str | None
    is_available: bool
    stock_quantity: int
    tags: list[str]
```

### Using in Routes

```python
# src/product_catalog/api/routes.py
from fastapi import APIRouter, Query
from shared.application.base_schema import PaginatedResponse, MessageResponse
from ..application.schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """List products with pagination."""
    # ... implementation
    pass


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(product_id: str):
    """Delete a product."""
    # ... implementation
    return MessageResponse(message=f"Product {product_id} deleted successfully")
```

## Benefits

1. **DRY**: Common fields defined once, inherited everywhere
2. **Consistency**: All entities have the same base structure
3. **Type Safety**: Full type hints and IDE autocomplete
4. **Validation**: Centralized validation rules for common fields
5. **Maintainability**: Change base schema, all entities update
6. **Documentation**: OpenAPI schemas are consistent and complete
