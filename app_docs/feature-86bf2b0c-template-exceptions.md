# Template exceptions.py - Typed Exceptions with FastAPI Handlers

**ADW ID:** 86bf2b0c
**Date:** 2026-01-23
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/86bf2b0c/specs/issue-123-adw-86bf2b0c-sdlc_planner-template-exceptions.md

## Overview

A comprehensive exception handling system template for FastAPI applications that provides typed exceptions for common API error scenarios with automatic FastAPI handler registration. This template implements the Dual Creation Pattern by generating both a Jinja2 template for CLI generation and a reference implementation in the project root.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2` - Template for generating exception systems in generated projects
- **Reference Implementation**: `src/shared/infrastructure/exceptions.py` - Rendered example implementation for tac-bootstrap project
- **AppError Base Class**: Foundation for all custom exceptions with message and details attributes
- **6 Typed Exception Classes**: Each mapping to specific HTTP status codes (404, 409, 422, 401, 403, 400)
- **FastAPI Exception Handlers**: Automatic conversion of exceptions to consistent JSON responses
- **Registration Function**: Single `register_exception_handlers(app)` call for setup
- **Security-Focused Design**: Catch-all handler prevents stack trace leaks
- **Structured Logging**: ERROR level for 5xx, WARNING level for 4xx errors

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`: Jinja2 template with IDK header documentation, 6 typed exception classes, FastAPI handlers, and registration function
- `src/shared/infrastructure/exceptions.py`: Rendered reference implementation showing expected output with "tac-bootstrap" project name

### Key Changes

1. **Exception Class Hierarchy**: All custom exceptions inherit from `AppError` base class, which provides consistent message and details attributes
2. **HTTP Status Code Mapping**: Each exception type automatically maps to appropriate HTTP status code (404, 409, 422, 401, 403, 400)
3. **Consistent JSON Format**: All error responses follow `{"error": {"type": "...", "message": "...", "details": {...}}}` structure with snake_case type names
4. **Centralized Handler Registration**: Single function registers all handlers including catch-all for unexpected exceptions
5. **Security Safeguards**: Generic Exception handler logs full stack trace but returns sanitized 500 response to prevent information disclosure
6. **Comprehensive IDK Documentation**: Module includes responsibility, key components, invariants, usage examples, collaborators, and failure modes following database.py.j2 pattern

## How to Use

### In Generated Projects

1. **Generate Exception System**: When TAC Bootstrap CLI generates a new FastAPI project, the exceptions.py template will be rendered with the project's configuration

2. **Register Handlers in main.py**:
```python
from fastapi import FastAPI
from src.shared.infrastructure.exceptions import register_exception_handlers

app = FastAPI(title="My Project")

# Register all exception handlers at startup
register_exception_handlers(app)
```

3. **Raise Typed Exceptions in Domain/Application Layers**:
```python
from src.shared.infrastructure.exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
    ValidationError,
    BusinessRuleError,
)

# In repository layer
class ProductRepository:
    def get_by_id(self, product_id: str) -> Product:
        result = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not result:
            raise EntityNotFoundError("Product", product_id)
        return Product.from_model(result)

# In application service
class CreateProductService:
    def execute(self, data: dict) -> Product:
        errors = {}
        if not data.get("name"):
            errors["name"] = "Name is required"
        if errors:
            raise ValidationError("Validation failed", {"fields": errors})
        # Continue with creation...
```

4. **Automatic Error Handling**: FastAPI automatically catches exceptions and returns appropriate JSON responses without try/except blocks in endpoints

### Available Exception Types

- **EntityNotFoundError(entity_type, entity_id)** → HTTP 404 - Entity not found in database
- **DuplicateEntityError(entity_type, field, value)** → HTTP 409 - Duplicate unique field value
- **ValidationError(message, details)** → HTTP 422 - Input validation failed
- **UnauthorizedError(message)** → HTTP 401 - Authentication required or failed
- **ForbiddenError(message)** → HTTP 403 - Authenticated but lacks permission
- **BusinessRuleError(message)** → HTTP 400 - Business rule violation

### Error Response Format

All exceptions return consistent JSON structure:
```json
{
  "error": {
    "type": "entity_not_found",
    "message": "Entity Product with id 123 not found",
    "details": {}
  }
}
```

## Configuration

The template uses minimal Jinja2 variables:
- `{{ config.project.name }}`: Rendered in module docstring header comment only

Example config.yml:
```yaml
project:
  name: "my-api-project"
```

## Testing

The exception system is infrastructure code that will be tested in generated projects. For TAC Bootstrap development:

```bash
# Verify template syntax
python -m py_compile tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2 || echo "Template has Jinja2 syntax (expected)"

# Verify rendered implementation
python -m py_compile src/shared/infrastructure/exceptions.py

# Run full test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Verify CLI functionality
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

1. **AppError Base Class**: Provides single point for registering all custom exceptions and ensures consistent behavior across exception types
2. **Snake_case Error Types**: API-friendly, machine-readable format (e.g., "entity_not_found" vs "EntityNotFoundError") for client-side error handling
3. **Catch-all Handler**: Security best practice to prevent stack trace leaks in production while logging full details server-side
4. **Logging Levels**: ERROR for server issues (500s), WARNING for client errors (4xx) follows standard severity practices
5. **Flexible Validation Details**: Dict structure supports various validation scenarios including field-level errors

### Security Considerations

- Catch-all handler sanitizes unexpected exceptions preventing information disclosure
- No stack traces exposed in API responses (logged server-side only)
- Internal errors return generic message to clients while logging full context

### Dual Creation Pattern

This feature follows the Dual Creation Pattern requirement:
- **Template**: `templates/shared/exceptions.py.j2` - For CLI generation
- **Reference**: `src/shared/infrastructure/exceptions.py` - Rendered with config.yml values for documentation

The reference implementation shows exactly what will be generated in target projects.

### Related Templates

- `templates/shared/database.py.j2` - Reference for template structure and IDK documentation pattern
- Future templates may integrate with this exception system (e.g., repository templates using EntityNotFoundError)
