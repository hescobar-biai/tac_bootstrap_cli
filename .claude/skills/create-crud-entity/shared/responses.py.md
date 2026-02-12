# Response Models Template

Common API response schemas. Place at `src/shared/api/responses.py`.

## Template

```python
"""
IDK: response-models, api-responses, http-schemas

Module: responses

Responsibility:
- Define common API response schemas
- Provide generic response wrappers
- Support pagination and error responses
- Ensure consistent response structure

Key Components:
- SuccessResponse: generic success message
- ErrorResponse: generic error message
- PaginatedResponse: paginated list wrapper
- DeleteResponse: delete operation confirmation
- BulkResponse: bulk operation results

Invariants:
- All responses use Pydantic BaseModel
- Consistent structure across all endpoints
- Type-safe with generics

Related Docs:
- docs/shared/api/responses.md
"""

from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')


class SuccessResponse(BaseModel):
    """
    IDK: success-response, confirmation-message, http-response

    Responsibility:
    - Provide generic success response
    - Indicate operation success
    - Return confirmation message

    Related Docs:
    - docs/shared/api/responses.md
    """

    success: bool = True
    message: str = "Operation completed successfully"


class ErrorResponse(BaseModel):
    """
    IDK: error-response, error-details, http-error

    Responsibility:
    - Provide generic error response
    - Include error code and message
    - Support additional error details

    Related Docs:
    - docs/shared/api/responses.md
    """

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    detail: list | dict | None = Field(default=None, description="Additional error details")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    IDK: pagination-response, generic-wrapper, list-response

    Responsibility:
    - Wrap paginated list responses
    - Provide pagination metadata
    - Support generic item types

    Related Docs:
    - docs/shared/api/pagination.md
    """

    items: list[T] = Field(default_factory=list, description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    pages: int = Field(..., ge=0, description="Total number of pages")

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1


class DeleteResponse(BaseModel):
    """Response for delete operations."""

    success: bool = True
    message: str
    id: str = Field(..., description="ID of deleted entity")


class BulkResponse(BaseModel, Generic[T]):
    """Response for bulk operations."""

    success: bool = True
    processed: int = Field(..., description="Number of items processed")
    failed: int = Field(default=0, description="Number of items that failed")
    items: list[T] = Field(default_factory=list, description="Processed items")
    errors: list[str] = Field(default_factory=list, description="Error messages for failed items")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
    database: str = "connected"


class CountResponse(BaseModel):
    """Count response for aggregate queries."""

    count: int = Field(..., ge=0, description="Total count")
    filters: dict = Field(default_factory=dict, description="Applied filters")
```

## Usage Examples

### In Routes

```python
from shared.api.responses import PaginatedResponse, SuccessResponse

@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
) -> PaginatedResponse[ProductResponse]:
    return service.get_all(page=page, page_size=page_size)


@router.delete("/{product_id}", response_model=SuccessResponse)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
) -> SuccessResponse:
    service.delete(product_id)
    return SuccessResponse(message=f"Product {product_id} deleted")
```

### In Services

```python
from shared.api.responses import PaginatedResponse

class ProductService:
    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> PaginatedResponse[ProductResponse]:
        items, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters or {},
            sort_by=sort_by,
            sort_order=sort_order
        )

        pages = (total + page_size - 1) // page_size  # Ceiling division

        return PaginatedResponse(
            items=[ProductResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )
```

## Directory Setup

```
src/
└── shared/
    └── api/
        ├── __init__.py
        ├── exceptions.py
        └── responses.py    # <-- This file
```
