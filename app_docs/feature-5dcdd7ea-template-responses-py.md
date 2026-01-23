# Template responses.py - Standardized Response Models

**ADW ID:** 5dcdd7ea
**Date:** 2026-01-23
**Specification:** specs/issue-126-adw-5dcdd7ea-sdlc_planner-template-responses.md

## Overview

This feature implements standardized Pydantic response models for consistent API responses across all TAC Bootstrap-generated projects. It provides generic pagination, success confirmations, and structured error handling with automatic OpenAPI schema generation.

## What Was Built

The implementation created a dual-template system following the TAC Bootstrap pattern:

- **Jinja2 Template** (`responses.py.j2`) - Used by CLI to generate responses.py for new projects
- **Rendered Reference** (`responses.py`) - Documentation example showing the template output
- **Generic PaginatedResponse[T]** - Type-safe pagination model with automatic page calculation
- **SuccessResponse** - Standard format for operation confirmations
- **ErrorResponse & ErrorDetail** - Structured error handling (complements exceptions.py)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/responses.py.j2`: Jinja2 template with {{ config.project.name }} variables for project generation
- `src/shared/infrastructure/responses.py`: Rendered reference implementation serving as documentation (not executed by CLI, since tac-bootstrap has framework="none")

### Key Changes

1. **Generic PaginatedResponse[T] Model**
   - Type parameter T for any item type (ProductResponse, UserResponse, etc.)
   - Fields: data: list[T], total: int, page: int, page_size: int, pages: int
   - Computed field `pages` using @computed_field decorator: `ceil(total / page_size)`
   - Validators: page >= 1 (1-indexed), 1 <= page_size <= 100, total >= 0
   - Graceful edge cases: pages=0 when total=0, empty data when page > pages

2. **SuccessResponse Model**
   - Fields: success: bool = True, message: str
   - Used for POST/PUT/DELETE confirmations
   - Explicit success indicator for programmatic API consumers

3. **ErrorDetail & ErrorResponse Models**
   - ErrorDetail fields: type: str, message: str, details: dict[str, Any] | None
   - ErrorResponse wraps ErrorDetail in standard envelope
   - Compatible with exception handlers from exceptions.py template
   - Common error types documented: EntityNotFoundError, DuplicateEntityError, validation_error, etc.

4. **IDK Documentation Format**
   - Module-level docstring with IDK tags (api-responses, pagination, error-handling)
   - Each model has comprehensive docstring with Responsibility, Fields, Usage Examples
   - Edge cases documented (page > pages, total=0, etc.)
   - Collaborators and Failure Modes sections included

5. **Template Variables**
   - Minimal Jinja2 logic: `{{ config.project.name }}` in header comment
   - Framework-agnostic design (no FastAPI imports, works with any Python web framework)

## How to Use

### Generate Project with Response Models

When using TAC Bootstrap CLI to generate a new project, the responses.py template will be rendered automatically:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap generate my-project
# responses.py will be generated in: my-project/src/shared/infrastructure/responses.py
```

### Using in API Routes

```python
from pydantic import BaseModel
from src.shared.infrastructure.responses import PaginatedResponse, SuccessResponse

# Define your item schema
class ProductResponse(BaseModel):
    id: str
    name: str
    price: float

# Use in paginated list endpoint
@router.get("/products", response_model=PaginatedResponse[ProductResponse])
def list_products(page: int = 1, page_size: int = 10):
    products = repository.find_all(page, page_size)
    total = repository.count()

    return PaginatedResponse(
        data=[ProductResponse.model_validate(p) for p in products],
        total=total,
        page=page,
        page_size=page_size
        # pages calculated automatically!
    )

# Use in DELETE operation
@router.delete("/products/{id}", response_model=SuccessResponse)
def delete_product(id: str):
    repository.delete(id)
    return SuccessResponse(message=f"Product {id} deleted successfully")
```

### Database Integration

Convert 1-indexed pagination to database OFFSET/LIMIT:

```python
# User provides page=2, page_size=10
offset = (page - 1) * page_size  # (2-1) * 10 = 10
limit = page_size  # 10
products = db.query(Product).offset(offset).limit(limit).all()
```

### Edge Cases Handled

- **Empty dataset**: total=0 → pages=0, data=[]
- **Page beyond range**: page=10 when pages=2 → returns data=[] gracefully (no error)
- **Exact boundary**: total=20, page_size=10 → pages=2
- **Partial last page**: total=11, page_size=10 → pages=2 (ceil division)

## Configuration

No configuration required. The template uses minimal Jinja2 variables:

- `{{ config.project.name }}` - Replaced with project name from config.yml during generation

## Testing

The implementation follows the dual creation pattern. Both template and rendered files exist at:

- Template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/responses.py.j2`
- Rendered: `src/shared/infrastructure/responses.py`

### Validation Commands

All validation commands pass with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short  # Tests pass
cd tac_bootstrap_cli && uv run ruff check .                  # No linting errors
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/           # No type errors
cd tac_bootstrap_cli && uv run tac-bootstrap --help          # CLI smoke test
```

### Edge Case Testing

When integrated into actual projects, test the following:

**PaginatedResponse:**
- Pagination calculation: total=0 → pages=0, total=11 page_size=10 → pages=2
- Validators: page=0 fails, page_size=0 fails, page_size=101 fails
- Generic type safety: PaginatedResponse[ProductResponse] provides type checking

**SuccessResponse:**
- success field always True
- message field required

**ErrorResponse:**
- ErrorDetail with None details vs populated details
- Integration with exception handlers from exceptions.py

## Notes

### Design Decisions

1. **Computed field for pages**: Cleaner API (users don't pass pages), immutable, type-safe, auto-documented in OpenAPI
2. **1-indexed pagination**: User-facing APIs standard (page 1, 2, 3), matches database OFFSET calculation
3. **page_size max of 100**: Prevents abuse, reasonable UI pagination limit, industry standard
4. **Graceful page > pages**: Returns empty data (no error), client detects via pages field, standard REST pattern
5. **Generic[T]**: Type safety, IDE autocomplete, Pydantic validation, OpenAPI schema generation
6. **SuccessResponse.success always True**: Explicit over implicit, consistent structure, conventional in REST APIs

### Integration Points

- **Routes**: Use `response_model=PaginatedResponse[ItemSchema]` in list endpoints
- **Services**: Return model instances instead of raw dicts
- **Exception handlers**: Already return ErrorResponse format (from exceptions.py template)
- **OpenAPI**: FastAPI auto-generates schema from response_model
- **Frontend**: Can generate TypeScript types from OpenAPI schema

### Security Considerations

- ErrorDetail.details should not contain sensitive data (passwords, tokens)
- total field could leak information (e.g., total users count) - consider permissions
- Error messages should be user-friendly but not reveal internal structure
- page_size limit prevents DoS via excessive pagination requests

### Related Templates

- `templates/shared/exceptions.py.j2` - Exception handling (ErrorResponse integrates with these)
- `templates/shared/base_schema.py.j2` - Base Pydantic model patterns
- `templates/capabilities/crud_basic/routes.py.j2` - Will use PaginatedResponse in future

### Future Enhancements

- Add next_page/prev_page URL fields to PaginatedResponse
- Add has_next/has_prev boolean helpers
- Add request_id to ErrorResponse for tracing
- Add CursorPaginatedResponse for cursor-based pagination
- Add internationalization support for error messages
