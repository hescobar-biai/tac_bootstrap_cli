# CRUD Authorized Templates with Multi-Tenant Support

**ADW ID:** feature_2_6
**Date:** 2026-01-23
**Specification:** specs/issue-150-adw-feature_2_6-sdlc_planner-crud-authorized-templates.md

## Overview

This feature adds a complete set of Jinja2 templates for generating CRUD entities with built-in multi-tenant authorization. The `--authorized` flag enables generation of entities with organization-level isolation, JWT authentication, and automatic security controls that prevent cross-tenant data access.

## What Was Built

- **6 New Templates** in `templates/capabilities/crud_authorized/`:
  - `domain_entity.py.j2` - Domain model with organization_id and created_by fields
  - `schemas.py.j2` - Pydantic schemas with authorization fields
  - `orm_model.py.j2` - SQLAlchemy model with indexed organization_id
  - `repository_authorized.py.j2` - Data access layer with automatic organization filtering
  - `service_authorized.py.j2` - Business logic that auto-sets ownership fields
  - `routes_authorized.py.j2` - FastAPI routes with JWT authentication

- **Enhanced Entity Generator Service**:
  - Template selection logic based on `entity_spec.authorized` flag
  - Automatic routing to authorized templates when `--authorized` flag is used
  - Support for combining `--authorized` with `--async-mode`

- **Comprehensive Test Suite**:
  - 789 lines of tests in `tests/test_authorized_templates.py`
  - Template rendering validation
  - Authorization logic verification
  - Edge case coverage

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py`: Added template selection logic that chooses between `crud_basic/` and `crud_authorized/` template sets based on the `authorized` flag
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Enhanced CLI help text for `--authorized` flag

### New Files Created

**Template Files:**
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/domain_entity.py.j2` (145 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/schemas.py.j2` (147 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/orm_model.py.j2` (121 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/repository_authorized.py.j2` (245 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/service_authorized.py.j2` (211 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/routes_authorized.py.j2` (348 lines)

**Test Files:**
- `tac_bootstrap_cli/tests/test_authorized_templates.py` (789 lines)

### Key Changes

**1. Multi-Tenant Security Architecture:**
- All repository queries automatically filter by `organization_id` to enforce tenant isolation
- Service layer auto-injects `organization_id` and `created_by` on entity creation (never trusts client input)
- Routes return 404 instead of 403 for cross-tenant access attempts to prevent information leakage
- JWT authentication dependency (`get_current_user`) extracts user context from bearer tokens

**2. Template Selection Logic:**
The `EntityGeneratorService.build_generation_plan()` method now selects templates based on authorization requirements:
```python
if entity_spec.authorized:
    template_prefix = "capabilities/crud_authorized"
    routes_template = f"{template_prefix}/routes_authorized.py.j2"
    service_template = f"{template_prefix}/service_authorized.py.j2"
    repo_template = f"{template_prefix}/repository_authorized.py.j2"
    # ...
else:
    template_prefix = "capabilities/crud_basic"
    # Use basic templates
```

**3. Authorization Flow:**
- **Routes Layer**: `get_current_user()` dependency extracts `user_id` and `organization_id` from JWT
- **Service Layer**: Receives user context, sets ownership fields on CREATE, passes org ID to repository
- **Repository Layer**: Applies `.filter(Model.organization_id == organization_id)` to ALL queries

**4. Automatic Field Injection:**
- Domain and ORM templates automatically include `organization_id: str` (indexed, required)
- Domain and ORM templates automatically include `created_by: str` (optional)
- These fields are injected by templates, not specified by users

## How to Use

### Generate an Authorized Entity

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap generate entity Product --authorized --no-interactive \
  --fields "name:str:required,price:float:required,description:str:optional"
```

This generates 6 files with multi-tenant authorization built-in:
```
infrastructure/products/entities/product.py          # Domain entity
infrastructure/products/schemas/product_schemas.py   # Pydantic schemas
infrastructure/products/models/product_model.py      # ORM model with organization_id
infrastructure/products/repositories/product_repository.py  # Filtered queries
application/products/services/product_service.py     # Auto-sets ownership
interfaces/api/products/product_routes.py            # JWT authentication
```

### Generated Code Features

**Repository (Automatic Tenant Filtering):**
```python
def get_by_id(self, id: str, organization_id: str) -> Optional[ProductModel]:
    return self.session.query(ProductModel).filter(
        ProductModel.id == id,
        ProductModel.organization_id == organization_id,
        ProductModel.state != 2
    ).first()
```

**Service (Auto-Inject Ownership):**
```python
def create(self, data: ProductCreate, user_id: str, organization_id: str) -> Product:
    # Auto-set organization_id (never trust client)
    data.organization_id = organization_id
    data.created_by = user_id
    return self.repository.create(data)
```

**Routes (JWT Authentication):**
```python
@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    product = service.create(
        data,
        current_user.user_id,
        current_user.organization_id
    )
    return product
```

### Combining with Async Mode

```bash
uv run tac-bootstrap generate entity Product --authorized --async-mode \
  --no-interactive --fields "name:str:required"
```

Generates async repository with organization filtering.

## Configuration

### JWT Token Requirements

The generated `get_current_user()` dependency expects JWT tokens with these claims:
```json
{
  "user_id": "user-uuid",
  "organization_id": "org-uuid"
}
```

### TODO: Production Implementation

The generated templates include mock JWT validation with TODO comments:
```python
# TODO: Replace mock JWT validation with your actual auth system
# TODO: Use proper JWT secret from environment variables
# TODO: Validate token signature, expiration, and issuer
# TODO: Handle token refresh logic
```

You must implement:
1. Real JWT signature validation with your secret key
2. Token expiration checking
3. Issuer and audience validation
4. Integration with your authentication system

### Database Schema

Generated ORM models include:
- `organization_id: str` (indexed, required) - for tenant isolation
- `created_by: str` (optional) - tracks entity creator

Ensure your database migrations include these columns.

## Testing

### Run Template Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_authorized_templates.py -v
```

### Run All Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Test Coverage

The test suite validates:
- Template rendering produces valid Python code
- Organization ID filtering in all repository queries
- JWT authentication dependency in all route endpoints
- Automatic setting of `organization_id` and `created_by` in CREATE operations
- 404 responses for cross-tenant access attempts
- Integration with `--async-mode` flag

## Notes

### Design Decisions

**Standalone Templates vs Inheritance:**
The authorized templates are complete, standalone files rather than extending basic templates via Jinja2 inheritance. This duplicates some code but maintains clarity and makes templates easier to customize.

**404 vs 403 for Authorization Failures:**
Routes return 404 when a resource doesn't exist OR belongs to a different organization. This prevents information leakage about which IDs exist in other tenants' data.

**Auto-Injection of organization_id:**
The service layer always sets `organization_id` from the JWT token, never from client input. This prevents privilege escalation attacks where clients try to create entities in other organizations.

**No Role-Based Access Control:**
These templates implement organization-level isolation only. They do NOT include role-based permissions (admin, user, viewer). Add RBAC manually if needed.

### Security Considerations

1. **All Queries Must Filter:** The repository templates apply `organization_id` filtering to ALL queries. Never bypass this filter.
2. **Never Trust Client Input:** The service layer overwrites any `organization_id` value from the client with the authenticated user's org ID.
3. **Audit Logging:** Templates include TODO comments for adding audit logs when authorization checks fail.
4. **Token Validation:** Replace mock JWT validation with production-grade validation before deploying.

### Limitations

- No support for users belonging to multiple organizations
- No role-based permissions within organizations
- No public resources (all entities require organization membership)
- JWT validation is mocked and requires production implementation

### Future Enhancements (Not Implemented)

- Templates with role-based access control (RBAC)
- Audit logging of authorization failures
- Support for multi-organization users
- Templates for public resources (no organization required)
- Token refresh and rotation handling

### Related Features

- **Prerequisite:** `crud_basic/` templates (Tarea 2.2 - issue 142)
- **Prerequisite:** EntitySpec with `authorized` field (Tarea 2.1 - issue 140)
- **Prerequisite:** CLI with `--authorized` flag (Tarea 2.4 - issue 146)
