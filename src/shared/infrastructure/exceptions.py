# Reference implementation - generated from exceptions.py.j2 template
# This file serves as documentation for the exceptions.py template output
# Not used by the CLI itself (tac-bootstrap has framework="none")

"""
IDK: exception-handling, error-responses, http-status-codes, fastapi-handlers

Module: exceptions

Responsibility:
- Provide typed exceptions for common API error scenarios
- Map domain exceptions to appropriate HTTP status codes
- Ensure consistent JSON error response format across all endpoints
- Centralize error handling logic to avoid repetitive try/except blocks
- Register FastAPI exception handlers automatically
- Prevent stack trace leaks with catch-all handler for unexpected errors
- Support structured logging for security and debugging

Key Components:
- AppError: Base exception class with message and details attributes
- EntityNotFoundError: 404 - Entity with specific ID not found
- DuplicateEntityError: 409 - Entity with unique field already exists
- ValidationError: 422 - Input validation failed with field-level details
- UnauthorizedError: 401 - Authentication required or failed
- ForbiddenError: 403 - Authenticated but lacks permission
- BusinessRuleError: 400 - Business logic constraint violated
- Exception handlers: Convert exceptions to JSONResponse with consistent format
- register_exception_handlers(): Single function to set up all handlers

Invariants:
- All custom exceptions inherit from AppError
- Error responses always use format: {"error": {"type": "...", "message": "...", "details": {...}}}
- Error type names use snake_case (e.g., "entity_not_found")
- 4xx errors log at WARNING level
- 5xx errors log at ERROR level with full stack trace
- Catch-all handler never exposes internal error details to client
- details dict defaults to {} when not provided
- Registration function called once during app startup

Usage Examples:

```python
# Import exceptions in domain/application layers
from src.shared.infrastructure.exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
    ValidationError,
    BusinessRuleError,
)

# Raise typed exceptions in repository
class ProductRepository:
    def get_by_id(self, product_id: str) -> Product:
        result = self.session.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if not result:
            raise EntityNotFoundError("Product", product_id)
        return Product.from_model(result)

    def save(self, product: Product) -> None:
        existing = self.session.query(ProductModel).filter(
            ProductModel.sku == product.sku
        ).first()
        if existing and existing.id != product.id:
            raise DuplicateEntityError("Product", "sku", product.sku)
        # Save logic...

# Raise validation errors in application services
class CreateProductService:
    def execute(self, data: dict) -> Product:
        errors = {}
        if not data.get("name"):
            errors["name"] = "Name is required"
        if data.get("price", 0) <= 0:
            errors["price"] = "Price must be positive"

        if errors:
            raise ValidationError(
                "Product validation failed",
                {"fields": errors}
            )
        # Continue with creation...

# Register all handlers in main.py
from fastapi import FastAPI
from src.shared.infrastructure.exceptions import register_exception_handlers

app = FastAPI(title="tac-bootstrap")

# Register exception handlers (call once at startup)
register_exception_handlers(app)

# Now all endpoints automatically handle exceptions
@app.get("/products/{product_id}")
def get_product(product_id: str):
    # If EntityNotFoundError is raised, FastAPI returns 404 automatically
    return product_service.get_by_id(product_id)
```

Collaborators:
- FastAPI: Exception handler registration and request/response handling
- Domain/Application layers: Raise typed exceptions for business errors
- Python logging: Structured logging for errors and warnings
- JSONResponse: Return consistent error format to clients

Failure Modes:
- Unhandled exception types: Caught by catch-all handler, returns 500
- Invalid JSON in details: JSONResponse serialization may fail (rare)
- Logger not configured: Defaults to root logger, may not output as expected
- Handler registration after routes defined: May not catch all exceptions (order matters)

Related Docs:
- docs/shared/infrastructure/exception-handling.md
- docs/shared/infrastructure/error-responses.md
- ai_docs/doc/exception-patterns/
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


class AppError(Exception):
    """
    Base exception class for all application errors.

    All custom exceptions should inherit from this class to enable
    centralized exception handling and consistent error responses.

    Attributes:
        message: Human-readable error message
        details: Optional dict with additional error context
    """

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundError(AppError):
    """
    Exception raised when an entity is not found in the database.
    Maps to HTTP 404 Not Found.

    Args:
        entity_type: Type of entity (e.g., "Product", "User")
        entity_id: ID of the entity that was not found
    """

    def __init__(self, entity_type: str, entity_id: str):
        message = f"Entity {entity_type} with id {entity_id} not found"
        super().__init__(message)


class DuplicateEntityError(AppError):
    """
    Exception raised when attempting to create an entity with a duplicate unique field.
    Maps to HTTP 409 Conflict.

    Args:
        entity_type: Type of entity (e.g., "Product", "User")
        field: Name of the field that has a duplicate value
        value: The duplicate value
    """

    def __init__(self, entity_type: str, field: str, value: str):
        message = f"Entity {entity_type} with {field}={value} already exists"
        super().__init__(message)


class ValidationError(AppError):
    """
    Exception raised when input validation fails.
    Maps to HTTP 422 Unprocessable Entity.

    Args:
        message: Validation error message
        details: Dict with validation error details (e.g., field-level errors)
    """

    def __init__(self, message: str, details: dict):
        super().__init__(message, details)


class UnauthorizedError(AppError):
    """
    Exception raised when authentication is required or has failed.
    Maps to HTTP 401 Unauthorized.

    Args:
        message: Error message describing why authentication failed
    """

    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenError(AppError):
    """
    Exception raised when user is authenticated but lacks permission.
    Maps to HTTP 403 Forbidden.

    Args:
        message: Error message describing what permission is missing
    """

    def __init__(self, message: str):
        super().__init__(message)


class BusinessRuleError(AppError):
    """
    Exception raised when a business rule or constraint is violated.
    Maps to HTTP 400 Bad Request.

    Args:
        message: Error message describing which business rule was violated
    """

    def __init__(self, message: str):
        super().__init__(message)


def handle_entity_not_found(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    """Handle EntityNotFoundError and return 404 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "type": "entity_not_found",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_duplicate_entity(request: Request, exc: DuplicateEntityError) -> JSONResponse:
    """Handle DuplicateEntityError and return 409 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "type": "duplicate_entity",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_validation_error(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle ValidationError and return 422 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_unauthorized(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handle UnauthorizedError and return 401 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "type": "unauthorized",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_forbidden(request: Request, exc: ForbiddenError) -> JSONResponse:
    """Handle ForbiddenError and return 403 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=403,
        content={
            "error": {
                "type": "forbidden",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_business_rule(request: Request, exc: BusinessRuleError) -> JSONResponse:
    """Handle BusinessRuleError and return 400 JSON response."""
    logger.warning(f"Exception occurred: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "type": "business_rule",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions.

    Logs the full exception with stack trace but returns a sanitized
    generic error to the client to prevent information disclosure.

    Maps to HTTP 500 Internal Server Error.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_server_error",
                "message": "An internal error occurred",
                "details": {},
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    IDK: exception-registration, fastapi-middleware, error-handling-setup

    Register all exception handlers with the FastAPI application.

    This function should be called once during application startup,
    after creating the FastAPI app instance but before defining routes.

    The catch-all handler for generic Exception is registered last to
    ensure custom exceptions are matched first.

    Usage Example:

    ```python
    from fastapi import FastAPI
    from src.shared.infrastructure.exceptions import register_exception_handlers

    app = FastAPI(title="My API")

    # Register all exception handlers
    register_exception_handlers(app)

    # Now define your routes
    @app.get("/")
    def root():
        return {"message": "Hello World"}
    ```

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(EntityNotFoundError, handle_entity_not_found)
    app.add_exception_handler(DuplicateEntityError, handle_duplicate_entity)
    app.add_exception_handler(ValidationError, handle_validation_error)
    app.add_exception_handler(UnauthorizedError, handle_unauthorized)
    app.add_exception_handler(ForbiddenError, handle_forbidden)
    app.add_exception_handler(BusinessRuleError, handle_business_rule)
    # Register catch-all handler last
    app.add_exception_handler(Exception, handle_generic_exception)
