# Reference implementation - generated from dependencies.py.j2 template
# This file serves as documentation for the dependencies.py template output
# Not used by the CLI itself (tac-bootstrap has framework="none")

"""
IDK: dependency-injection, factory-pattern, fastapi-depends

Module: dependencies

Responsibility:
- Centralized dependency injection factory functions for FastAPI
- Provide get_db re-export for convenience
- Demonstrate service and repository factory patterns with Depends()
- Support authentication dependency patterns
- Enable clean separation between layers (API, application, infrastructure)

Key Components:
- get_db: Re-exported from database.py for convenience
- Service factories: Functions that create service instances with injected repositories
- Repository factories: Functions that create repository instances with injected sessions
- Auth factories: Commented examples for authentication/authorization

Invariants:
- Each factory creates fresh instances per request
- Dependencies are resolved by FastAPI's injection system
- Error handling delegated to base implementations (database.py, auth modules)
- Factories follow pattern: db → repository → service
- All factories use Depends() for automatic injection

Usage Examples:

```python
# Import dependencies in route handlers
from src.shared.infrastructure.dependencies import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

# Use get_db directly for simple queries
router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Direct database access for simple operations
    return {"status": "ok", "database": "connected"}

# Define entity-specific service factory
from src.products.application.service import ProductService
from src.products.infrastructure.repository import ProductRepository

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """
    Factory for ProductService with dependency injection.

    Args:
        db: Database session injected by FastAPI

    Returns:
        ProductService: Configured service instance

    Usage:
        @router.get("/products")
        def list_products(service: ProductService = Depends(get_product_service)):
            return service.get_all(page=1, page_size=10)
    """
    repository = ProductRepository(db)
    return ProductService(repository)

# Use in routes
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

# Use auth dependencies for protected routes
@router.delete("/products/{product_id}")
def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    service.delete(product_id, user_id=current_user.id)
    return {"message": "Product deleted successfully"}
```

Collaborators:
- FastAPI Depends(): automatic dependency injection system
- database.py: provides get_db session factory
- Service layer: business logic orchestration
- Repository layer: data access operations
- Auth modules: authentication and authorization

Failure Modes:
- DatabaseError: propagated from database.py's get_db
- AuthenticationError: propagated from auth dependencies
- All exceptions handled by FastAPI's exception handlers

Related Docs:
- docs/shared/infrastructure/dependency-injection.md
- docs/shared/infrastructure/factory-pattern.md
- ai_docs/doc/create-crud-entity/
"""

from sqlalchemy.orm import Session
from src.shared.infrastructure.database import get_db

# Re-export get_db for convenience
# Routes can import from dependencies.py instead of database.py
__all__ = ["get_db"]


# =============================================================================
# SERVICE FACTORY PATTERN
# =============================================================================
# Add your service factories here following this pattern:
#
# Example service factory (synchronous):
# def get_example_service(db: Session = Depends(get_db)) -> ExampleService:
#     """
#     Factory for ExampleService with dependency injection.
#
#     Responsibility:
#     - Create ExampleService instance with injected repository
#     - Manage dependency lifecycle per request
#     - Provide service to route handlers via Depends()
#
#     Invariants:
#     - Fresh service instance created per request
#     - Repository initialized with database session
#     - Session cleanup handled by get_db
#
#     Args:
#         db: Database session injected by FastAPI
#
#     Returns:
#         ExampleService: Configured service instance
#
#     Usage:
#         @router.get("/examples")
#         def list_examples(service: ExampleService = Depends(get_example_service)):
#             return service.list_all()
#
#     Related Docs:
#     - docs/shared/infrastructure/service-factories.md
#     """
#     repository = ExampleRepository(db)
#     return ExampleService(repository)


# =============================================================================
# REPOSITORY FACTORY PATTERN (for direct repository access)
# =============================================================================
# If you need to inject repositories directly (less common, prefer services):
#
# def get_example_repository(db: Session = Depends(get_db)) -> ExampleRepository:
#     """
#     Factory for ExampleRepository with dependency injection.
#
#     Note: Prefer service factories for business logic.
#     Use repository factories only for simple CRUD operations.
#
#     Args:
#         db: Database session injected by FastAPI
#
#     Returns:
#         ExampleRepository: Repository instance
#
#     Usage:
#         @router.get("/examples/{id}")
#         def get_example(id: str, repo: ExampleRepository = Depends(get_example_repository)):
#             return repo.get_by_id(id)
#     """
#     return ExampleRepository(db)


# =============================================================================
# AUTHENTICATION & AUTHORIZATION DEPENDENCIES
# =============================================================================
# Add your auth dependencies here following this pattern:
#
# from fastapi import HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#
# security = HTTPBearer()
#
# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Authenticate user from bearer token.
#
#     Responsibility:
#     - Extract and validate bearer token
#     - Retrieve authenticated user from database
#     - Raise 401 if token invalid or user not found
#
#     Invariants:
#     - Returns User object if token valid
#     - Raises HTTPException(401) if authentication fails
#     - Token verification delegated to auth module
#
#     Args:
#         credentials: HTTP authorization credentials (bearer token)
#         db: Database session for user lookup
#
#     Returns:
#         User: Authenticated user object
#
#     Raises:
#         HTTPException: 401 if token invalid or user not found
#
#     Usage:
#         @router.get("/protected")
#         def protected_route(user: User = Depends(get_current_user)):
#             return {"user_id": user.id, "username": user.username}
#
#     Related Docs:
#     - docs/shared/infrastructure/authentication.md
#     """
#     token = credentials.credentials
#
#     # Implement token verification (JWT, API key, etc.)
#     # Example with JWT:
#     # try:
#     #     payload = verify_jwt_token(token)
#     #     user_id = payload.get("sub")
#     # except InvalidTokenError:
#     #     raise HTTPException(status_code=401, detail="Invalid token")
#
#     # Retrieve user from database
#     # user = UserRepository(db).get_by_id(user_id)
#     # if not user:
#     #     raise HTTPException(status_code=401, detail="User not found")
#
#     # return user
#     pass
#
#
# # Role-based authorization example
# def require_admin(current_user: User = Depends(get_current_user)) -> User:
#     """
#     Require admin role for route access.
#
#     Responsibility:
#     - Verify user has admin role
#     - Raise 403 if user lacks permission
#
#     Args:
#         current_user: Authenticated user (injected)
#
#     Returns:
#         User: Admin user
#
#     Raises:
#         HTTPException: 403 if user is not admin
#
#     Usage:
#         @router.delete("/admin/users/{user_id}")
#         def delete_user(user_id: str, admin: User = Depends(require_admin)):
#             # Only admins can access this route
#             return {"message": "User deleted"}
#     """
#     if not hasattr(current_user, 'role') or current_user.role != 'admin':
#         raise HTTPException(status_code=403, detail="Admin access required")
#     return current_user
