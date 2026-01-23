# Dependencies Template

FastAPI dependency injection factories. This file should be placed at `src/core/dependencies.py`.

## Template

```python
"""
IDK: dependency-injection, fastapi-dependencies, service-factory

Module: dependencies

Responsibility:
- Provide FastAPI dependency factories for all services
- Wire repositories, services, and infrastructure components
- Manage dependency lifecycle and cleanup
- Support testing with dependency overrides

Key Components:
- get_db: Database session dependency
- get_settings: Configuration dependency
- Service factory functions for each entity

Invariants:
- Dependencies are request-scoped
- Resources cleaned up after request
- Database sessions auto-close
- Circular dependencies avoided

Related Docs:
- docs/core/dependencies.md
- docs/core/dependency-injection.md
"""

from typing import Generator, Annotated
from functools import lru_cache

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from core.config import Settings, get_settings
from shared.infrastructure.database import get_db

# ================================================
# Core Dependencies
# ================================================


def get_config() -> Settings:
    """
    IDK: configuration-injection, settings-dependency

    Responsibility:
    - Provide application settings to endpoints
    - Return cached settings instance

    Invariants:
    - Returns same settings instance (cached)
    - Settings loaded from environment

    Outputs:
    - Settings: application configuration

    Usage:
        @router.get("/info")
        def get_info(settings: Settings = Depends(get_config)):
            return {"app_name": settings.app_name}

    Related Docs:
    - docs/core/configuration.md
    """
    return get_settings()


def get_current_user_id(
    x_user_id: str = Header(..., alias="X-User-ID")
) -> str:
    """
    IDK: user-identification, audit-trail, request-context

    Responsibility:
    - Extract user ID from request headers
    - Validate user ID is provided
    - Support audit trail in services

    Invariants:
    - Returns non-empty user ID
    - Raises 401 if header missing
    - Header name: X-User-ID

    Inputs:
    - x_user_id (str): user ID from header

    Outputs:
    - str: validated user ID

    Failure Modes:
    - HTTPException 401: X-User-ID header missing

    Usage:
        @router.post("/products")
        def create_product(
            data: ProductCreate,
            user_id: str = Depends(get_current_user_id),
            service: ProductService = Depends(get_product_service),
        ):
            return service.create(data, user_id=user_id)

    Related Docs:
    - docs/core/authentication.md
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-ID header is required"
        )
    return x_user_id


def get_optional_user_id(
    x_user_id: str | None = Header(None, alias="X-User-ID")
) -> str | None:
    """
    IDK: user-identification, optional-auth, request-context

    Responsibility:
    - Extract user ID from headers if present
    - Allow anonymous requests
    - Support optional audit trail

    Invariants:
    - Returns None if header not present
    - Does not raise exceptions
    - Header name: X-User-ID

    Inputs:
    - x_user_id (str | None): optional user ID

    Outputs:
    - str | None: user ID or None

    Usage:
        @router.get("/public/products")
        def list_products(
            user_id: str | None = Depends(get_optional_user_id),
        ):
            # user_id may be None for public access
            pass

    Related Docs:
    - docs/core/authentication.md
    """
    return x_user_id


# ================================================
# Common Pagination Dependencies
# ================================================


def get_pagination_params(
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """
    IDK: pagination, query-params, list-endpoint

    Responsibility:
    - Parse and validate pagination parameters
    - Enforce page size limits
    - Provide defaults for pagination

    Invariants:
    - page >= 1
    - page_size between 1 and 100
    - Returns dict with page and page_size

    Inputs:
    - page (int): page number (1-indexed)
    - page_size (int): items per page

    Outputs:
    - dict: {"page": int, "page_size": int}

    Failure Modes:
    - HTTPException 400: invalid page or page_size

    Usage:
        @router.get("/products")
        def list_products(
            pagination: dict = Depends(get_pagination_params),
            service: ProductService = Depends(get_product_service),
        ):
            return service.get_all(**pagination)

    Related Docs:
    - docs/core/pagination.md
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be >= 1"
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 100"
        )

    return {"page": page, "page_size": page_size}


def get_sort_params(
    sort_by: str | None = None,
    sort_order: str = "asc",
) -> dict:
    """
    IDK: sorting, query-params, list-endpoint

    Responsibility:
    - Parse and validate sorting parameters
    - Normalize sort order
    - Provide defaults for sorting

    Invariants:
    - sort_order is either 'asc' or 'desc'
    - sort_by can be None

    Inputs:
    - sort_by (str | None): field to sort by
    - sort_order (str): 'asc' or 'desc'

    Outputs:
    - dict: {"sort_by": str | None, "sort_order": str}

    Failure Modes:
    - HTTPException 400: invalid sort_order

    Usage:
        @router.get("/products")
        def list_products(
            sort: dict = Depends(get_sort_params),
            service: ProductService = Depends(get_product_service),
        ):
            return service.get_all(**sort)

    Related Docs:
    - docs/core/sorting.md
    """
    normalized_order = sort_order.lower()
    if normalized_order not in ("asc", "desc"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sort order must be 'asc' or 'desc'"
        )

    return {"sort_by": sort_by, "sort_order": normalized_order}


# ================================================
# Service Factory Examples
# ================================================

# NOTE: These are example patterns. Replace with actual entity services.

# Example: Product Service
# Uncomment and adapt for your entities:

# from product_catalog.infrastructure.repository import ProductRepository
# from product_catalog.infrastructure.models import ProductModel
# from product_catalog.application.service import ProductService
#
# def get_product_service(
#     db: Session = Depends(get_db)
# ) -> ProductService:
#     """
#     IDK: service-factory, product-service, dependency-injection
#
#     Responsibility:
#     - Create and wire ProductService with dependencies
#     - Inject database session into repository
#     - Return configured service instance
#
#     Invariants:
#     - New service instance per request
#     - Repository uses request-scoped session
#
#     Inputs:
#     - db (Session): database session
#
#     Outputs:
#     - ProductService: configured service
#
#     Usage:
#         @router.get("/products")
#         def list_products(
#             service: ProductService = Depends(get_product_service)
#         ):
#             return service.get_all()
#
#     Related Docs:
#     - docs/product_catalog/service.md
#     """
#     repository = ProductRepository(db)
#     return ProductService(repository)


# Example: Order Service (with multiple dependencies)
# Uncomment and adapt for your entities:

# from order_management.infrastructure.repository import OrderRepository
# from order_management.application.service import OrderService
# from product_catalog.application.service import ProductService
#
# def get_order_service(
#     db: Session = Depends(get_db),
#     product_service: ProductService = Depends(get_product_service),
# ) -> OrderService:
#     """
#     IDK: service-factory, order-service, cross-capability
#
#     Responsibility:
#     - Create OrderService with cross-capability dependencies
#     - Wire order repository and product service
#     - Support service composition
#
#     Invariants:
#     - New service instance per request
#     - Dependencies properly injected
#
#     Inputs:
#     - db (Session): database session
#     - product_service (ProductService): product service dependency
#
#     Outputs:
#     - OrderService: configured service with dependencies
#
#     Usage:
#         @router.post("/orders")
#         def create_order(
#             data: OrderCreate,
#             service: OrderService = Depends(get_order_service),
#         ):
#             return service.create(data)
#
#     Related Docs:
#     - docs/order_management/service.md
#     """
#     repository = OrderRepository(db)
#     return OrderService(
#         repository=repository,
#         product_service=product_service,
#     )


# ================================================
# Authorization Dependencies (for Authorized Entities)
# ================================================

# Uncomment if using authorization:

# from shared.authorization.service import AuthorizationService
# from shared.authorization.repository import (
#     PermissionRepository,
#     RoleRepository,
#     UserRoleRepository,
# )
# from shared.authorization.context import AuthorizationContext
#
# def get_authorization_service(
#     db: Session = Depends(get_db)
# ) -> AuthorizationService:
#     """
#     IDK: authorization-service, rbac, permission-check
#
#     Responsibility:
#     - Create authorization service with repositories
#     - Provide permission checking capability
#     - Wire RBAC infrastructure
#
#     Invariants:
#     - New service instance per request
#     - All RBAC repositories injected
#
#     Inputs:
#     - db (Session): database session
#
#     Outputs:
#     - AuthorizationService: configured authorization service
#
#     Related Docs:
#     - docs/authorization/service.md
#     """
#     permission_repo = PermissionRepository(db)
#     role_repo = RoleRepository(db)
#     user_role_repo = UserRoleRepository(db)
#
#     return AuthorizationService(
#         permission_repository=permission_repo,
#         role_repository=role_repo,
#         user_role_repository=user_role_repo,
#     )
#
#
# def get_auth_context(
#     user_id: str = Depends(get_current_user_id),
#     auth_service: AuthorizationService = Depends(get_authorization_service),
# ) -> AuthorizationContext:
#     """
#     IDK: auth-context, user-permissions, request-context
#
#     Responsibility:
#     - Create authorization context for current user
#     - Load user permissions and roles
#     - Provide context for permission checks
#
#     Invariants:
#     - Context tied to current user
#     - Permissions loaded from database
#     - New context per request
#
#     Inputs:
#     - user_id (str): current user ID
#     - auth_service (AuthorizationService): authorization service
#
#     Outputs:
#     - AuthorizationContext: user authorization context
#
#     Usage:
#         @router.get("/products/{id}")
#         def get_product(
#             id: str,
#             context: AuthorizationContext = Depends(get_auth_context),
#             service: ProductService = Depends(get_product_service),
#         ):
#             return service.get_by_id(id, context=context)
#
#     Related Docs:
#     - docs/authorization/context.md
#     """
#     return auth_service.create_context(user_id)


# ================================================
# Type Aliases for Common Dependencies
# ================================================

# These type aliases provide cleaner type hints in route functions

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
OptionalUserId = Annotated[str | None, Depends(get_optional_user_id)]
PaginationParams = Annotated[dict, Depends(get_pagination_params)]
SortParams = Annotated[dict, Depends(get_sort_params)]
AppSettings = Annotated[Settings, Depends(get_config)]

# Example usage with type aliases:
# @router.get("/products")
# def list_products(
#     db: DatabaseSession,
#     user_id: OptionalUserId,
#     pagination: PaginationParams,
#     sort: SortParams,
# ):
#     pass


# ================================================
# Testing Support
# ================================================


def override_get_db(test_db: Session):
    """
    IDK: testing, dependency-override, test-fixture

    Responsibility:
    - Create dependency override for testing
    - Replace production database with test database
    - Support integration testing

    Invariants:
    - Returns function that yields test_db
    - Compatible with FastAPI dependency override

    Inputs:
    - test_db (Session): test database session

    Outputs:
    - Callable: dependency function for testing

    Usage:
        # In conftest.py
        @pytest.fixture
        def client(test_db):
            app.dependency_overrides[get_db] = lambda: test_db
            with TestClient(app) as client:
                yield client
            app.dependency_overrides.clear()

    Related Docs:
    - docs/testing/integration-tests.md
    """
    def _override():
        try:
            yield test_db
        finally:
            pass
    return _override
```

## Directory Setup

```
src/
└── core/
    ├── __init__.py
    ├── config.py
    └── dependencies.py  # <-- This file
```

**`src/core/__init__.py`**:
```python
"""Core application configuration and dependencies."""
from .config import Settings, get_settings, settings
from .dependencies import (
    get_db,
    get_config,
    get_current_user_id,
    get_optional_user_id,
    get_pagination_params,
    get_sort_params,
    DatabaseSession,
    CurrentUserId,
    OptionalUserId,
    PaginationParams,
    SortParams,
    AppSettings,
)

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "settings",
    # Dependencies
    "get_db",
    "get_config",
    "get_current_user_id",
    "get_optional_user_id",
    "get_pagination_params",
    "get_sort_params",
    # Type aliases
    "DatabaseSession",
    "CurrentUserId",
    "OptionalUserId",
    "PaginationParams",
    "SortParams",
    "AppSettings",
]
```

## Usage in Routes

### Basic CRUD Endpoints

```python
# src/product_catalog/api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import (
    get_db,
    get_current_user_id,
    get_pagination_params,
    get_sort_params,
)
from ..application.service import ProductService
from ..application.schemas import ProductCreate, ProductUpdate, ProductResponse
from ..infrastructure.repository import ProductRepository


router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Factory for ProductService."""
    repository = ProductRepository(db)
    return ProductService(repository)


@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    user_id: str = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    """Create a new product."""
    return service.create(data, user_id=user_id)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
):
    """Get product by ID."""
    return service.get_by_id(product_id)


@router.get("/", response_model=list[ProductResponse])
def list_products(
    pagination: dict = Depends(get_pagination_params),
    sort: dict = Depends(get_sort_params),
    service: ProductService = Depends(get_product_service),
):
    """List all products with pagination and sorting."""
    return service.get_all(**pagination, **sort)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    data: ProductUpdate,
    user_id: str = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    """Update a product."""
    return service.update(product_id, data, user_id=user_id)


@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    """Soft delete a product."""
    service.delete(product_id, user_id=user_id)
    return {"message": "Product deleted successfully"}
```

### Using Type Aliases

```python
# Cleaner syntax with type aliases
from core.dependencies import (
    DatabaseSession,
    CurrentUserId,
    PaginationParams,
    SortParams,
)

@router.get("/")
def list_products(
    db: DatabaseSession,
    user_id: CurrentUserId,
    pagination: PaginationParams,
    sort: SortParams,
):
    """List products with clean dependency injection."""
    # Implementation
    pass
```

### Cross-Capability Dependencies

```python
# src/order_management/api/routes.py
from core.dependencies import get_db, get_current_user_id
from ..application.service import OrderService
from product_catalog.application.service import ProductService

def get_order_service(
    db: Session = Depends(get_db),
) -> OrderService:
    """Factory for OrderService with product dependency."""
    from ..infrastructure.repository import OrderRepository
    from product_catalog.infrastructure.repository import ProductRepository

    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    product_service = ProductService(product_repo)

    return OrderService(
        repository=order_repo,
        product_service=product_service,
    )


@router.post("/")
def create_order(
    data: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    service: OrderService = Depends(get_order_service),
):
    """Create order with product validation."""
    return service.create(data, user_id=user_id)
```

## Testing with Dependency Overrides

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from core.dependencies import get_db, get_current_user_id
from shared.infrastructure.database import Base


@pytest.fixture(scope="function")
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with overridden dependencies."""

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    def override_get_user():
        return "test-user-id"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_id] = override_get_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Test usage
def test_create_product(client):
    """Test product creation."""
    response = client.post(
        "/api/v1/products/",
        json={
            "code": "PROD001",
            "name": "Test Product",
            "description": "A test product",
        }
    )
    assert response.status_code == 200
    assert response.json()["code"] == "PROD001"
```

## Best Practices

1. **Keep dependencies focused**: Each factory should create one service
2. **Avoid circular dependencies**: Structure imports carefully
3. **Use type aliases**: Improves readability in route signatures
4. **Scope appropriately**: Most dependencies are request-scoped
5. **Test with overrides**: Use dependency overrides for testing
6. **Document factories**: Each factory should have IDK docstring
7. **Lazy imports**: Import inside factory if circular dependency risk
8. **Reuse common patterns**: Use type aliases for repeated dependencies

## Anti-Patterns to Avoid

**Don't create global service instances:**
```python
# BAD: Service created once at module level
product_service = ProductService(ProductRepository(SessionLocal()))

# GOOD: Service created per request
def get_product_service(db: Session = Depends(get_db)):
    return ProductService(ProductRepository(db))
```

**Don't mix concerns in dependencies:**
```python
# BAD: Dependency does too much
def get_product_and_validate(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(404)
    return product

# GOOD: Dependency provides service, let service handle logic
def get_product_service(db: Session = Depends(get_db)):
    return ProductService(ProductRepository(db))
```

**Don't skip dependency injection:**
```python
# BAD: Hardcoded database connection
@router.get("/products")
def list_products():
    db = SessionLocal()  # Manual session management
    products = db.query(Product).all()
    db.close()
    return products

# GOOD: Use dependency injection
@router.get("/products")
def list_products(service: ProductService = Depends(get_product_service)):
    return service.get_all()
```
