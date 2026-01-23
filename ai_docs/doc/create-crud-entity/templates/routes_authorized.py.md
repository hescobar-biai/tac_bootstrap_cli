# Routes Template (Authorized)

Template for creating FastAPI CRUD endpoints **with authorization**.

## Usage

Replace placeholders:
- `{{EntityName}}` - PascalCase entity name (e.g., `Product`)
- `{{entity_name}}` - snake_case entity name (e.g., `product`)
- `{{entities}}` - plural lowercase for URL (e.g., `products`)
- `{{tag}}` - API tag name (e.g., `Products`)
- `{{capability}}` - snake_case capability (e.g., `product_catalog`)
- `{{resource_type}}` - Resource type for permissions (e.g., `product`)

## Template

```python
"""
IDK: http-endpoint, rest-api, {{entity_name}}-routes, authorization, rbac

Module: routes

Responsibility:
- Define HTTP endpoints for {{EntityName}} with authorization
- Enforce permission-based access control
- Delegate to authorized service layer
- Filter results by user's access scope

Invariants:
- All endpoints require permissions
- AuthorizationContext injected via dependencies
- Row-level filtering by access scope
- Field-level filtering by permissions
- Audit trail maintained

Related Docs:
- docs/{{capability}}/api/routes.md
- docs/authorization/api-integration.md
"""

from fastapi import APIRouter, Depends, Query, status

from shared.api.responses import PaginatedResponse, SuccessResponse
from core.dependencies import get_{{entity_name}}_service

from authorization.api.dependencies import (
    get_authorization_context,
    require_permission,
    require_resource_permission,
)
from authorization.application.authorization_service import AuthorizationContext

from ..application.schemas import {{EntityName}}Create, {{EntityName}}Update, {{EntityName}}Response
from ..application.service import {{EntityName}}Service

router = APIRouter(prefix="/{{entities}}", tags=["{{tag}}"])


@router.post(
    "/",
    response_model={{EntityName}}Response,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new {{EntityName}}"
)
async def create_{{entity_name}}(
    data: {{EntityName}}Create,
    context: AuthorizationContext = Depends(require_permission("{{resource_type}}", "create")),
    service: {{EntityName}}Service = Depends(get_{{entity_name}}_service)
) -> {{EntityName}}Response:
    """
    IDK: http-endpoint, create-operation, authorization, permission-check

    Responsibility:
    - Create {{EntityName}} with ownership tracking
    - Require '{{resource_type}}:create' permission
    - Set owner to current user
    - Return field-filtered response

    Inputs:
    - data ({{EntityName}}Create): creation payload
    - context (AuthorizationContext): user permissions

    Outputs:
    - {{EntityName}}Response: 201 Created (field-filtered)

    Failure Modes:
    - 403 Forbidden: missing permission
    - 400 Bad Request: validation error
    - 409 Conflict: duplicate code

    Related Docs:
    - docs/{{capability}}/api/create.md
    - docs/authorization/permissions.md
    """
    return service.create(data, context)


@router.get(
    "/{{{entity_name}}_id}",
    response_model={{EntityName}}Response,
    summary="Get {{EntityName}} by ID"
)
async def get_{{entity_name}}(
    {{entity_name}}_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("{{resource_type}}", "read")),
    service: {{EntityName}}Service = Depends(get_{{entity_name}}_service)
) -> {{EntityName}}Response:
    """Retrieve a specific {{EntityName}} by ID. Requires '{{resource_type}}:read' permission."""
    return service.get_by_id({{entity_name}}_id, context)


@router.get(
    "/",
    response_model=PaginatedResponse[{{EntityName}}Response],
    summary="List all {{EntityName}}s"
)
async def list_{{entity_name}}s(
    context: AuthorizationContext = Depends(require_permission("{{resource_type}}", "read")),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    service: {{EntityName}}Service = Depends(get_{{entity_name}}_service)
) -> PaginatedResponse[{{EntityName}}Response]:
    """List {{EntityName}}s with pagination. Results filtered by user's access scope."""
    return service.get_all(
        context=context,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.put(
    "/{{{entity_name}}_id}",
    response_model={{EntityName}}Response,
    summary="Update a {{EntityName}}"
)
async def update_{{entity_name}}(
    {{entity_name}}_id: str,
    data: {{EntityName}}Update,
    context: AuthorizationContext = Depends(require_resource_permission("{{resource_type}}", "update")),
    service: {{EntityName}}Service = Depends(get_{{entity_name}}_service)
) -> {{EntityName}}Response:
    """Update an existing {{EntityName}}. Requires '{{resource_type}}:update' permission."""
    return service.update({{entity_name}}_id, data, context)


@router.delete(
    "/{{{entity_name}}_id}",
    response_model=SuccessResponse,
    summary="Delete a {{EntityName}}"
)
async def delete_{{entity_name}}(
    {{entity_name}}_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("{{resource_type}}", "delete")),
    service: {{EntityName}}Service = Depends(get_{{entity_name}}_service)
) -> SuccessResponse:
    """Delete a {{EntityName}} by ID. Requires '{{resource_type}}:delete' permission."""
    service.delete({{entity_name}}_id, context)
    return SuccessResponse(message=f"{{EntityName}} {{{entity_name}}_id} deleted successfully")
```

## Example: Product Routes (Authorized)

```python
"""Product CRUD endpoints with authorization."""

from fastapi import APIRouter, Depends, Query, status

from shared.api.responses import PaginatedResponse, SuccessResponse
from core.dependencies import get_product_service

from authorization.api.dependencies import (
    get_authorization_context,
    require_permission,
    require_resource_permission,
)
from authorization.application.authorization_service import AuthorizationContext

from ..application.schemas import ProductCreate, ProductUpdate, ProductResponse
from ..application.service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Product"
)
async def create_product(
    data: ProductCreate,
    context: AuthorizationContext = Depends(require_permission("product", "create")),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Create a new Product. Requires 'product:create' permission."""
    return service.create(data, context)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get Product by ID"
)
async def get_product(
    product_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("product", "read")),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Retrieve a specific Product by ID. Requires 'product:read' permission."""
    return service.get_by_id(product_id, context)


@router.get(
    "/",
    response_model=PaginatedResponse[ProductResponse],
    summary="List all Products"
)
async def list_products(
    context: AuthorizationContext = Depends(require_permission("product", "read")),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: str | None = Query(None, description="Filter by category"),
    is_available: bool | None = Query(None, description="Filter by availability"),
    sort_by: str | None = Query(None, description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    service: ProductService = Depends(get_product_service)
) -> PaginatedResponse[ProductResponse]:
    """List Products with pagination. Results filtered by user's access scope."""
    filters = {}
    if category:
        filters["category"] = category
    if is_available is not None:
        filters["is_available"] = is_available

    return service.get_all(
        context=context,
        page=page,
        page_size=page_size,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a Product"
)
async def update_product(
    product_id: str,
    data: ProductUpdate,
    context: AuthorizationContext = Depends(require_resource_permission("product", "update")),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Update an existing Product. Requires 'product:update' permission."""
    return service.update(product_id, data, context)


@router.delete(
    "/{product_id}",
    response_model=SuccessResponse,
    summary="Delete a Product"
)
async def delete_product(
    product_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("product", "delete")),
    service: ProductService = Depends(get_product_service)
) -> SuccessResponse:
    """Delete a Product by ID. Requires 'product:delete' permission."""
    service.delete(product_id, context)
    return SuccessResponse(message=f"Product {product_id} deleted successfully")
```

## Custom Actions with Permissions

```python
@router.post(
    "/{product_id}/approve",
    response_model=ProductResponse,
    summary="Approve a Product"
)
async def approve_product(
    product_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("product", "approve")),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Approve a product. Requires 'product:approve' permission."""
    return service.approve(product_id, context)


@router.post(
    "/{product_id}/export",
    summary="Export Product data"
)
async def export_product(
    product_id: str,
    context: AuthorizationContext = Depends(require_resource_permission("product", "export")),
    service: ProductService = Depends(get_product_service)
):
    """Export product data. Requires 'product:export' permission."""
    return service.export(product_id, context)
```

## Permission Requirements

| Endpoint | Permission Required |
|----------|---------------------|
| `POST /` | `{resource}:create` |
| `GET /{id}` | `{resource}:read` |
| `GET /` | `{resource}:read` |
| `PUT /{id}` | `{resource}:update` |
| `DELETE /{id}` | `{resource}:delete` |
| Custom actions | `{resource}:{action}` |
