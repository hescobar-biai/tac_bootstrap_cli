# Feature: Template exceptions.py - Typed Exceptions with FastAPI Handlers

## Metadata
issue_number: `123`
adw_id: `86bf2b0c`
issue_json: `{"number":123,"title":"Tarea 1.7: Template exceptions.py","body":"/feature\n**Ganancia**: Exceptions tipadas con HTTP handlers pre-registrados. Errores consistentes en toda la API sin repetir try/except en cada endpoint.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`\n2. Crear renderizado en raiz: `src/shared/infrastructure/exceptions.py`\n2. Clases de exception:\n   - `EntityNotFoundError(entity_type: str, entity_id: str)` → 404\n   - `DuplicateEntityError(entity_type: str, field: str, value: str)` → 409\n   - `ValidationError(message: str, details: dict)` → 422\n   - `UnauthorizedError(message: str)` → 401\n   - `ForbiddenError(message: str)` → 403\n   - `BusinessRuleError(message: str)` → 400\n3. FastAPI exception handlers:\n   - `register_exception_handlers(app: FastAPI)` que registra handler para cada exception\n   - Cada handler retorna JSON con `{\"error\": {\"type\": \"...\", \"message\": \"...\", \"details\": {...}}}`\n\n**Criterios de aceptacion**:\n- Cada exception mapea a un HTTP status code especifico\n- Los handlers retornan formato JSON consistente\n- `register_exception_handlers()` se puede llamar en main.py"}`

## Feature Description

Create a comprehensive exception handling system template for FastAPI applications. This system provides typed exceptions for common API error scenarios (404, 409, 422, 401, 403, 400) with automatic registration of FastAPI exception handlers that return consistent JSON error responses. The template implements the Dual Creation Pattern by creating both a Jinja2 template for CLI generation and a reference implementation in the project root.

## User Story

As a FastAPI developer using TAC Bootstrap
I want a pre-configured exception handling system with typed exceptions and handlers
So that I can have consistent error responses across all endpoints without repeating try/except blocks

## Problem Statement

FastAPI applications need consistent error handling across all endpoints. Without a centralized exception system, developers must:
- Manually handle exceptions in every endpoint with repetitive try/except blocks
- Risk inconsistent error response formats across different endpoints
- Duplicate error handling logic throughout the codebase
- Manually map domain exceptions to appropriate HTTP status codes

This leads to maintenance burden, inconsistent API behavior, and potential security issues from exposing internal error details.

## Solution Statement

Create an `exceptions.py` template that provides:
1. **AppError base class** - Foundation for all custom exceptions with common behavior
2. **6 typed exception classes** - Each mapping to a specific HTTP status code (404, 409, 422, 401, 403, 400)
3. **Consistent JSON error format** - `{"error": {"type": "...", "message": "...", "details": {...}}}`
4. **Automatic handler registration** - Single `register_exception_handlers(app)` call in main.py
5. **Security-focused design** - Catch-all handler for unexpected exceptions prevents stack trace leaks
6. **Comprehensive logging** - ERROR level for 5xx, WARNING for 4xx with structured logging
7. **Flexible validation details** - Support for field-level error structures

The template uses snake_case error types (e.g., "entity_not_found") for API-friendly, machine-readable error identification.

## Relevant Files

### Existing Files
- `/Volumes/MAc1/Celes/tac_bootstrap/trees/86bf2b0c/tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - Reference for template structure, IDK comments, and Jinja2 variable usage
- `/Volumes/MAc1/Celes/tac_bootstrap/trees/86bf2b0c/src/shared/infrastructure/database.py` - Reference for rendered output format with header comments
- `/Volumes/MAc1/Celes/tac_bootstrap/trees/86bf2b0c/config.yml` - Project configuration with values for template rendering

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2` - Jinja2 template for exception system
- `src/shared/infrastructure/exceptions.py` - Rendered reference implementation for this project

## Implementation Plan

### Phase 1: Template Creation
Create the Jinja2 template with proper structure:
- Set up IDK header comments following database.py.j2 pattern
- Define AppError base class with common exception behavior
- Create 6 typed exception classes with appropriate __init__ signatures
- Use minimal Jinja2 variables (only `{{ config.project.name }}` in header comments)

### Phase 2: Exception Handlers Implementation
Implement FastAPI exception handlers in the template:
- Create handler functions for each exception type returning consistent JSON format
- Implement catch-all handler for generic Exception to prevent stack trace leaks
- Add structured logging (ERROR for 5xx, WARNING for 4xx)
- Define `register_exception_handlers(app: FastAPI)` function

### Phase 3: Dual Creation Pattern
Follow the dual creation pattern requirement:
- Render the template using values from `config.yml` (project name = "tac-bootstrap")
- Create reference implementation at `src/shared/infrastructure/exceptions.py`
- Add header comment indicating it's a reference implementation
- Verify both files exist and are consistent

## Step by Step Tasks

### Task 1: Create exceptions.py.j2 Template with Base Class and Exceptions
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`
- Add IDK header comment with keywords: `exception-handling, error-responses, http-status-codes, fastapi-handlers`
- Document module responsibility, key components, invariants, usage examples, collaborators, failure modes
- Import required modules: `logging`, `FastAPI`, `Request`, `JSONResponse`
- Define `AppError` base class inheriting from `Exception` with:
  - `__init__(self, message: str, details: dict | None = None)`
  - Store message and details as instance attributes
- Define 6 typed exception classes inheriting from `AppError`:
  - `EntityNotFoundError(entity_type: str, entity_id: str)` - formats message as "Entity {type} with id {id} not found"
  - `DuplicateEntityError(entity_type: str, field: str, value: str)` - formats message as "Entity {type} with {field}={value} already exists"
  - `ValidationError(message: str, details: dict)` - accepts message and structured validation details
  - `UnauthorizedError(message: str)` - simple message-based exception
  - `ForbiddenError(message: str)` - simple message-based exception
  - `BusinessRuleError(message: str)` - simple message-based exception
- Use `{{ config.project.name }}` in module docstring header comment only

### Task 2: Implement Exception Handlers
- Create logger instance: `logger = logging.getLogger(__name__)`
- Define handler function for each exception type:
  - `def handle_entity_not_found(request: Request, exc: EntityNotFoundError) -> JSONResponse`
  - `def handle_duplicate_entity(request: Request, exc: DuplicateEntityError) -> JSONResponse`
  - `def handle_validation_error(request: Request, exc: ValidationError) -> JSONResponse`
  - `def handle_unauthorized(request: Request, exc: UnauthorizedError) -> JSONResponse`
  - `def handle_forbidden(request: Request, exc: ForbiddenError) -> JSONResponse`
  - `def handle_business_rule(request: Request, exc: BusinessRuleError) -> JSONResponse`
- Each handler should:
  - Log at WARNING level with message: `"Exception occurred: {exc.message}"`
  - Return JSONResponse with status code and error payload
  - Error payload format: `{"error": {"type": "<snake_case_name>", "message": "<message>", "details": <details_dict>}}`
- Map exceptions to HTTP status codes:
  - EntityNotFoundError → 404
  - DuplicateEntityError → 409
  - ValidationError → 422
  - UnauthorizedError → 401
  - ForbiddenError → 403
  - BusinessRuleError → 400
- Snake_case type names: "entity_not_found", "duplicate_entity", "validation_error", "unauthorized", "forbidden", "business_rule"

### Task 3: Implement Catch-All Handler and Registration Function
- Define catch-all exception handler:
  - `def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse`
  - Log at ERROR level with full exception details: `logger.error(f"Unexpected error: {exc}", exc_info=True)`
  - Return JSONResponse with status_code=500
  - Return sanitized error: `{"error": {"type": "internal_server_error", "message": "An internal error occurred", "details": {}}}`
  - Never expose stack traces or internal details in response
- Define registration function:
  - `def register_exception_handlers(app: FastAPI) -> None`
  - Register each custom exception handler using `app.add_exception_handler(ExceptionClass, handler_function)`
  - Register catch-all handler as last: `app.add_exception_handler(Exception, handle_generic_exception)`
  - Add docstring with IDK keywords: `exception-registration, fastapi-middleware, error-handling-setup`
  - Document usage example showing call in main.py after FastAPI app creation

### Task 4: Render Reference Implementation
- Read `config.yml` to extract project.name value ("tac-bootstrap")
- Render the template using Jinja2 with config values
- Create directory `src/shared/infrastructure/` if it doesn't exist
- Write rendered content to `src/shared/infrastructure/exceptions.py`
- Add header comment at top of rendered file:
  - `# Reference implementation - generated from exceptions.py.j2 template`
  - `# This file serves as documentation for the exceptions.py template output`
  - `# Not used by the CLI itself (tac-bootstrap has framework="none")`
- Verify the rendered file has correct project name in docstring

### Task 5: Validation and Testing
- Verify both files exist:
  - Template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`
  - Rendered: `src/shared/infrastructure/exceptions.py`
- Verify template contains Jinja2 variable syntax: `{{ config.project.name }}`
- Verify rendered file has "tac-bootstrap" in docstring (not template syntax)
- Check all 6 exception classes are defined with correct signatures
- Check all handlers return correct HTTP status codes
- Check `register_exception_handlers()` function exists and registers all handlers
- Check catch-all handler is registered last for Exception type
- Run validation commands (listed below)

## Testing Strategy

### Unit Tests
This template generates infrastructure code that will be tested in the projects that use it. For this task, validation focuses on:
- Template syntax correctness (Jinja2 renders without errors)
- Rendered file matches expected structure
- All exception classes are present with correct HTTP status code mappings
- All handlers follow consistent JSON response format
- Registration function includes all handlers plus catch-all

### Edge Cases
- Empty details dict in ValidationError → should still return valid JSON with empty details
- None details in AppError → should convert to empty dict in JSON response
- Exception raised with special characters in message → should be JSON-safe
- Nested validation errors in details dict → should serialize correctly to JSON
- Catch-all handler receives non-AppError exception → should log and return generic 500

## Acceptance Criteria

- [x] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`
- [x] Template contains AppError base class with message and details attributes
- [x] Template defines all 6 exception classes with correct signatures:
  - EntityNotFoundError(entity_type, entity_id) → 404
  - DuplicateEntityError(entity_type, field, value) → 409
  - ValidationError(message, details) → 422
  - UnauthorizedError(message) → 401
  - ForbiddenError(message) → 403
  - BusinessRuleError(message) → 400
- [x] Each exception handler returns consistent JSON format: `{"error": {"type": "...", "message": "...", "details": {...}}}`
- [x] Exception handlers use snake_case type names (e.g., "entity_not_found")
- [x] Exception handlers log at WARNING level for 4xx errors
- [x] Catch-all handler logs at ERROR level and returns sanitized 500 response without exposing internals
- [x] `register_exception_handlers(app: FastAPI)` function registers all handlers including catch-all
- [x] Rendered reference file created at `src/shared/infrastructure/exceptions.py` with header comment
- [x] Template uses only `{{ config.project.name }}` in docstring header
- [x] Rendered file contains "tac-bootstrap" (not template syntax)
- [x] IDK header comments follow database.py.j2 pattern with comprehensive documentation

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Verify files exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2
ls -la src/shared/infrastructure/exceptions.py

# Verify Python syntax (both files should be valid Python)
python -m py_compile tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2 || echo "Template has Jinja2 syntax (expected)"
python -m py_compile src/shared/infrastructure/exceptions.py

# Run standard validation commands
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions
1. **AppError base class**: Provides single point for registering all custom exceptions and common behavior
2. **Snake_case error types**: More API-friendly than PascalCase, machine-readable for clients
3. **Catch-all handler**: Security best practice to prevent stack trace leaks in production
4. **Logging levels**: ERROR for server issues (500s), WARNING for client errors (4xx) follows standard severity practices
5. **Flexible validation details**: Dict structure with optional 'fields' key supports various validation scenarios

### Security Considerations
- Catch-all handler sanitizes unexpected exceptions to prevent information disclosure
- No stack traces exposed in API responses
- Internal errors logged server-side but generic message returned to client

### Future Enhancements (Not in Scope)
- i18n support for error messages
- Custom HTTP response headers (WWW-Authenticate, Retry-After)
- Error codes in addition to error types
- Exception telemetry/metrics integration
- Structured logging with correlation IDs

### Dependencies
No new dependencies required - uses standard library (logging) and FastAPI built-ins.
