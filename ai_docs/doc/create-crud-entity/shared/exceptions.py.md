# Exceptions Template

Custom exceptions and handlers. Place at `src/shared/api/exceptions.py`.

## Template

```python
"""
IDK: exception-handling, error-responses, http-errors

Module: exceptions

Responsibility:
- Define custom exception classes
- Provide FastAPI exception handlers
- Convert exceptions to HTTP responses
- Support structured error responses

Key Components:
- Custom exception classes for domain errors
- Exception handlers for FastAPI

Invariants:
- All exceptions have message attribute
- Handlers return JSON responses
- HTTP status codes match error types

Related Docs:
- docs/shared/api/error-handling.md
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse


# ===========================================
# Custom Exception Classes
# ===========================================

class EntityNotFoundError(Exception):
    """
    IDK: not-found-error, entity-retrieval, 404-error

    Responsibility:
    - Indicate entity doesn't exist
    - Provide error message
    - Trigger 404 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Entity not found"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """
    IDK: validation-error, input-validation, 400-error

    Responsibility:
    - Indicate validation failure
    - Provide error details
    - Trigger 400 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Validation failed", errors: list | None = None):
        self.message = message
        self.errors = errors or []
        super().__init__(self.message)


class DuplicateEntityError(Exception):
    """
    IDK: duplicate-error, uniqueness-violation, 409-error

    Responsibility:
    - Indicate duplicate entity
    - Provide error message
    - Trigger 409 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Entity already exists"):
        self.message = message
        super().__init__(self.message)


class ReferenceError(Exception):
    """
    IDK: reference-error, foreign-key, 400-error

    Responsibility:
    - Indicate referenced entity missing
    - Provide error message
    - Trigger 400 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Referenced entity not found"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """
    IDK: unauthorized-error, authentication, 401-error

    Responsibility:
    - Indicate missing authentication
    - Provide error message
    - Trigger 401 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    """
    IDK: forbidden-error, authorization, 403-error

    Responsibility:
    - Indicate insufficient permissions
    - Provide error message
    - Trigger 403 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Forbidden"):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    """
    IDK: conflict-error, optimistic-locking, 409-error

    Responsibility:
    - Indicate state conflict
    - Provide error message
    - Trigger 409 HTTP response

    Related Docs:
    - docs/shared/api/exceptions.md
    """

    def __init__(self, message: str = "Conflict"):
        self.message = message
        super().__init__(self.message)


# ===========================================
# Exception Handlers
# ===========================================

async def entity_not_found_handler(
    request: Request,
    exc: EntityNotFoundError
) -> JSONResponse:
    """
    IDK: exception-handler, not-found, http-response

    Responsibility:
    - Convert EntityNotFoundError to HTTP 404
    - Return structured error JSON
    - Include error message

    Outputs:
    - JSONResponse: 404 with error details
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "not_found",
            "message": exc.message,
            "detail": None
        }
    )


async def validation_error_handler(
    request: Request,
    exc: ValidationError
) -> JSONResponse:
    """Handle ValidationError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "validation_error",
            "message": exc.message,
            "detail": exc.errors
        }
    )


async def duplicate_entity_handler(
    request: Request,
    exc: DuplicateEntityError
) -> JSONResponse:
    """Handle DuplicateEntityError."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "duplicate",
            "message": exc.message,
            "detail": None
        }
    )


async def reference_error_handler(
    request: Request,
    exc: ReferenceError
) -> JSONResponse:
    """Handle ReferenceError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "reference_error",
            "message": exc.message,
            "detail": None
        }
    )


async def unauthorized_handler(
    request: Request,
    exc: UnauthorizedError
) -> JSONResponse:
    """Handle UnauthorizedError."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "unauthorized",
            "message": exc.message,
            "detail": None
        }
    )


async def forbidden_handler(
    request: Request,
    exc: ForbiddenError
) -> JSONResponse:
    """Handle ForbiddenError."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "forbidden",
            "message": exc.message,
            "detail": None
        }
    )


async def conflict_handler(
    request: Request,
    exc: ConflictError
) -> JSONResponse:
    """Handle ConflictError."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "conflict",
            "message": exc.message,
            "detail": None
        }
    )
```

## Register in main.py

```python
from fastapi import FastAPI
from shared.api.exceptions import (
    EntityNotFoundError,
    ValidationError,
    DuplicateEntityError,
    ReferenceError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    entity_not_found_handler,
    validation_error_handler,
    duplicate_entity_handler,
    reference_error_handler,
    unauthorized_handler,
    forbidden_handler,
    conflict_handler,
)

app = FastAPI()

# Register exception handlers
app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(DuplicateEntityError, duplicate_entity_handler)
app.add_exception_handler(ReferenceError, reference_error_handler)
app.add_exception_handler(UnauthorizedError, unauthorized_handler)
app.add_exception_handler(ForbiddenError, forbidden_handler)
app.add_exception_handler(ConflictError, conflict_handler)
```

## Directory Setup

```
src/
└── shared/
    └── api/
        ├── __init__.py
        ├── exceptions.py   # <-- This file
        └── responses.py
```

**`src/shared/api/__init__.py`**:
```python
"""Shared API components."""
from .exceptions import (
    EntityNotFoundError,
    ValidationError,
    DuplicateEntityError,
    ReferenceError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
)
from .responses import PaginatedResponse, SuccessResponse

__all__ = [
    "EntityNotFoundError",
    "ValidationError",
    "DuplicateEntityError",
    "ReferenceError",
    "UnauthorizedError",
    "ForbiddenError",
    "ConflictError",
    "PaginatedResponse",
    "SuccessResponse",
]
```

## Usage in Services

```python
from shared.api.exceptions import EntityNotFoundError, DuplicateEntityError

class ProductService:
    def get_by_id(self, product_id: str) -> ProductResponse:
        entity = self.repository.get_by_id(product_id)
        if not entity:
            raise EntityNotFoundError(f"Product with ID '{product_id}' not found")
        return ProductResponse.model_validate(entity)

    def create(self, data: ProductCreate) -> ProductResponse:
        existing = self.repository.get_by_code(data.code)
        if existing:
            raise DuplicateEntityError(f"Product with code '{data.code}' already exists")
        # ... create logic
```
