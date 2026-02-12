# Entity Creation Workflow

Step-by-step process for creating a new CRUD entity with vertical slice architecture.

> **Documentation Standard**: All generated code must follow the IDK-first docstring format defined in [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md). Every class and function requires IDK keywords, Responsibility, and Invariants sections.

## Pre-flight Checklist

Before starting, gather this information:

```
Entity Information:
- [ ] Entity name (PascalCase): e.g., Product, Supplier, Order
- [ ] Business capability name (snake_case): e.g., product_catalog, supplier_management
- [ ] Entity-specific fields (name, type, constraints)
- [ ] Relationships to other entities (if any)
- [ ] Authorization required? (Yes/No)
```

## Authorization Decision

**Does this entity require access control?**

| Answer | Use Templates | Description |
|--------|---------------|-------------|
| **No** | Basic (`routes.py`, `service.py`, `repository.py`) | Public data, no restrictions |
| **Yes** | Authorized (`routes_authorized.py`, etc.) | Row/column/action level access |

### When to Use Authorized Templates

Use **authorized templates** if the entity needs:

- **Row-level access**: Users see only their own data, team data, or org data
- **Field-level access**: Sensitive fields hidden/masked based on role
- **Action permissions**: Different roles can create/read/update/delete
- **Audit trail**: Track who created/modified records
- **Multi-tenancy**: Data isolation between organizations

### Additional Info for Authorized Entities

```
Authorization Information:
- [ ] Resource type for permissions: e.g., "product", "purchase"
- [ ] Default access scope: OWNER (1), GROUP (2), or ORGANIZATION (3)
- [ ] Sensitive fields to protect? (for field-level permissions)
- [ ] Custom actions? (approve, sign, export, etc.)
```

## Step 1: Check Shared Infrastructure

First, verify if `<source-dir>/shared/` exists. If not, create it.

```bash
# Check if shared infrastructure exists (replace <source-dir> with your actual path)
ls <source-dir>/shared/domain/base_entity.py 2>/dev/null || echo "MISSING"
```

**If MISSING**, create the shared infrastructure:

1. Create directory structure:
```
<source-dir>/
├── shared/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── base_entity.py
│   │   └── events.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── base_schema.py
│   │   └── base_service.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── base_repository.py
│   │   └── base_repository_async.py
│   └── api/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── responses.py
│       └── health.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── dependencies.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
└── main.py
```

2. Use templates from [shared/](shared/) to create each file:
   - `base_entity.py` - Domain entity base class
   - `base_schema.py` - DTO base classes (BaseCreate, BaseUpdate, BaseResponse)
   - `base_service.py` - Service base class with CRUD operations
   - `base_repository.py` - Sync repository base class
   - `base_repository_async.py` - Async repository base class (optional)
   - `config.py` - Pydantic Settings configuration
   - `health.py` - Health check endpoints
   - `alembic.py` - Database migrations configuration

## Step 2: Create Entity Directory Structure

Create the vertical slice for your entity:

```bash
# Replace {capability} with your capability name (e.g., product_catalog)
mkdir -p <source-dir>/{capability}/domain
mkdir -p <source-dir>/{capability}/application
mkdir -p <source-dir>/{capability}/infrastructure
mkdir -p <source-dir>/{capability}/api
```

Create `__init__.py` files:
```bash
touch <source-dir>/{capability}/__init__.py
touch <source-dir>/{capability}/domain/__init__.py
touch <source-dir>/{capability}/application/__init__.py
touch <source-dir>/{capability}/infrastructure/__init__.py
touch <source-dir>/{capability}/api/__init__.py
```

## Step 3: Create Domain Model

**File**: `<source-dir>/{capability}/domain/{entity}.py`

Use template: [templates/domain_entity.py.md](templates/domain_entity.py.md)

**Checklist**:
- [ ] Extends `Entity` from `shared.domain.base_entity`
- [ ] Sets `type` field to entity type string
- [ ] Defines entity-specific fields with type hints
- [ ] Optional: Add domain methods for business logic
- [ ] **Docs**: IDK includes `domain-entity`, `aggregate-root`
- [ ] **Docs**: Invariants document state transitions

## Step 4: Create Application Layer

### 4a. Schemas (DTOs)

**File**: `<source-dir>/{capability}/application/schemas.py`

Use template: [templates/schemas.py.md](templates/schemas.py.md)

**Checklist**:
- [ ] `{Entity}Create` - Extends `BaseCreate`, add entity-specific required fields
- [ ] `{Entity}Update` - Extends `BaseUpdate`, add entity-specific optional fields
- [ ] `{Entity}Response` - Extends `BaseResponse`, add entity-specific fields
- [ ] **Docs**: IDK includes `dto`, `create-schema`, `input-validation`
- [ ] **Docs**: Fields section lists all schema fields

**Note**: Base classes (`BaseCreate`, `BaseUpdate`, `BaseResponse`) are imported from `shared.application.base_schema` and provide common fields automatically.

### 4b. Service

**File**: `<source-dir>/{capability}/application/service.py`

Use template:
- **Basic**: [templates/service.py.md](templates/service.py.md)
- **Authorized**: [templates/service_authorized.py.md](templates/service_authorized.py.md)

**Checklist (Basic with BaseService)**:
- [ ] Extends `BaseService[TCreate, TUpdate, TResponse, TModel, TDomain]`
- [ ] Constructor calls `super().__init__()` with repository, response_class, domain_class, entity_name
- [ ] Inherits: create, get_by_id, get_by_code, get_all, update, delete, hard_delete, activate, deactivate, restore
- [ ] Add custom business methods as needed
- [ ] **Docs**: IDK includes `use-case`, `orchestration`, `{entity}-management`
- [ ] **Docs**: Invariants document mutation rules, Failure Modes list exceptions

**Checklist (Authorized)**:
- [ ] Constructor accepts repository AND auth_service
- [ ] Set `RESOURCE_TYPE` and `DEFAULT_ACCESS_SCOPE`
- [ ] All methods accept `AuthorizationContext`
- [ ] Uses `get_by_id_authorized()` and `get_all_authorized()`
- [ ] Applies field filtering with `filter_response_fields()`
- [ ] Sets `owner`, `organization_id`, `created_by`, `updated_by`

**Note**: BaseService provides soft delete by default. Use `hard_delete()` for permanent deletion.

## Step 5: Create Infrastructure Layer

### 5a. ORM Model

**File**: `<source-dir>/{capability}/infrastructure/models.py`

Use template: [templates/orm_model.py.md](templates/orm_model.py.md)

**Checklist**:
- [ ] Extends `Base` from `shared.infrastructure.database`
- [ ] Sets `__tablename__`
- [ ] All Entity base fields defined
- [ ] Entity-specific fields defined
- [ ] Appropriate column types (String, Integer, Float, Boolean, JSON)
- [ ] Indexes on frequently queried fields
- [ ] **Docs**: IDK includes `orm-model`, `persistence`, `{entity}-table`
- [ ] **Docs**: Invariants document column constraints

### 5b. Repository

**File**: `<source-dir>/{capability}/infrastructure/repository.py`

Use template:
- **Basic**: [templates/repository.py.md](templates/repository.py.md)
- **Authorized**: [templates/repository_authorized.py.md](templates/repository_authorized.py.md)

**Checklist (Basic)**:
- [ ] Extends `BaseRepository`
- [ ] Constructor sets model class
- [ ] Optional: Custom query methods
- [ ] **Docs**: IDK includes `repository`, `data-access`, `{entity}-persistence`
- [ ] **Docs**: Invariants document query filtering rules

**Checklist (Authorized)**:
- [ ] Extends `AuthorizedRepository`
- [ ] Inherits `get_all_authorized()`, `get_by_id_authorized()`, etc.
- [ ] Model has `owner`, `organization_id`, `group_path` fields
- [ ] **Docs**: IDK adds `row-level-security`, `rbac`

## Step 6: Create API Layer

**File**: `<source-dir>/{capability}/api/routes.py`

Use template:
- **Basic**: [templates/routes.py.md](templates/routes.py.md)
- **Authorized**: [templates/routes_authorized.py.md](templates/routes_authorized.py.md)

**Checklist (Basic)**:
- [ ] Router with prefix and tags
- [ ] POST endpoint for create
- [ ] GET endpoint for single entity
- [ ] GET endpoint for list (with pagination, filters, sorting)
- [ ] PUT endpoint for update
- [ ] DELETE endpoint for delete
- [ ] **Docs**: IDK includes `http-endpoint`, `{action}-operation`, `{entity}-api`
- [ ] **Docs**: Failure Modes list HTTP status codes (400, 404, 409, 500)

**Checklist (Authorized)**:
- [ ] Import `require_permission`, `require_resource_permission`
- [ ] All endpoints require `AuthorizationContext`
- [ ] Use `require_permission("{resource}", "{action}")` for action-level
- [ ] Use `require_resource_permission("{resource}", "{action}")` for resource-level
- [ ] Pass `context` to service methods
- [ ] **Docs**: IDK adds `permission-check`, `auth-filter`

## Step 7: Register Router in main.py

Add the new router to `<source-dir>/main.py`:

```python
# Import the router
from {capability}.api.routes import router as {entity}_router

# Register with app
app.include_router({entity}_router, prefix=settings.api_v1_prefix)
```

## Step 8: Update Dependencies

Add factory function to `<source-dir>/core/dependencies.py`:

**Basic:**
```python
from {capability}.infrastructure.repository import {Entity}Repository
from {capability}.application.service import {Entity}Service

def get_{entity}_service() -> {Entity}Service:
    db = get_db()
    repository = {Entity}Repository(db)
    return {Entity}Service(repository)
```

**Authorized:**
```python
from {capability}.infrastructure.repository import {Entity}Repository
from {capability}.application.service import {Entity}Service

def get_{entity}_service() -> {Entity}Service:
    db = get_db()
    repository = {Entity}Repository(db)
    auth_service = get_authorization_service()  # Include auth service
    return {Entity}Service(repository, auth_service)
```

## Step 9: Create Permissions (Authorized Only)

If using authorized templates, create the permissions for your entity:

```bash
# Create permissions via API
curl -X POST /api/v1/auth/permissions \
  -H "Content-Type: application/json" \
  -H "X-User-ID: admin" \
  -d '{
    "code": "{entity}_create",
    "name": "Create {Entity}",
    "resource_type": "{entity}",
    "action": "create",
    "access_scope": 3,
    "effect": "allow"
  }'

# Repeat for: read, update, delete, and any custom actions
```

**Standard permissions to create:**

| Permission Code | Action | Description |
|-----------------|--------|-------------|
| `{entity}_create` | create | Create new records |
| `{entity}_read` | read | View records |
| `{entity}_update` | update | Modify records |
| `{entity}_delete` | delete | Delete records |

**Then assign to roles:**
```bash
curl -X POST /api/v1/auth/roles/{role_id}/permissions \
  -H "Content-Type: application/json" \
  -H "X-User-ID: admin" \
  -d '{"permission_id": "{permission_id}"}'
```

## Step 10: Validation

Run these checks:

```bash
# Check imports work
python -c "from src.{capability}.api.routes import router"

# Run type checker
pyright <source-dir>/{capability}/

# Start server and test
uvicorn src.main:app --reload
```

**Test endpoints**:
- `POST /api/v1/{entities}/` - Create
- `GET /api/v1/{entities}/{id}` - Read
- `GET /api/v1/{entities}/` - List
- `PUT /api/v1/{entities}/{id}` - Update
- `DELETE /api/v1/{entities}/{id}` - Delete

## Common Issues

### Import Errors

If you get `ModuleNotFoundError`:
1. Ensure all `__init__.py` files exist
2. Check relative import paths
3. Verify `src/` is in Python path

### Database Errors

If tables don't create:
1. Import model in `database/__init__.py`
2. Call `Base.metadata.create_all()` on startup
3. Check SQLAlchemy connection string

### Validation Errors

If Pydantic validation fails:
1. Check field types match between domain model and schemas
2. Verify required vs optional fields
3. Check `model_config = {"from_attributes": True}` in Response schemas

---

## Optional Steps

### Step 11: Create Database Migration

Use Alembic to create a migration for the new entity:

```bash
# Create migration
uv run alembic revision --autogenerate -m "add_{entity}_table"

# Review generated migration in alembic/versions/

# Apply migration
uv run alembic upgrade head
```

See [shared/alembic.py.md](shared/alembic.py.md) for configuration details.

### Step 12: Create Tests

**Directory**: `tests/unit/{capability}/` and `tests/integration/{capability}/`

Use template: [templates/tests.py.md](templates/tests.py.md)

**Create test files**:
```bash
mkdir -p tests/unit/{capability}
mkdir -p tests/integration/{capability}
touch tests/unit/{capability}/__init__.py
touch tests/unit/{capability}/test_service.py
touch tests/unit/{capability}/test_domain.py
touch tests/integration/{capability}/__init__.py
touch tests/integration/{capability}/test_routes.py
```

**Run tests**:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific capability tests
uv run pytest tests/unit/{capability}/
```

### Step 13: Add Domain Events (Optional)

For loose coupling between capabilities:

**File**: `<source-dir>/{capability}/domain/events.py`

Use template: [templates/domain_events.py.md](templates/domain_events.py.md)

**Checklist**:
- [ ] Create event classes: `{Entity}Created`, `{Entity}Updated`, `{Entity}Deleted`
- [ ] Publish events from service methods
- [ ] Create event handlers in `application/event_handlers.py`
- [ ] Import handlers in `main.py` to register them

### Step 14: Add Value Objects (Optional)

For complex domain concepts:

**File**: `<source-dir>/{capability}/domain/value_objects.py`

Use template: [templates/value_objects.py.md](templates/value_objects.py.md)

**Checklist**:
- [ ] Add validation via `model_validator`
- [ ] Use in domain entities instead of primitive types

---

## Quick Reference: UV Commands

```bash
# Development
uv run dev                    # Start dev server

# Testing
uv run test                   # Run tests
uv run test-cov               # Run with coverage

# Code Quality
uv run lint                   # Run linter
uv run format                 # Format code
uv run typecheck              # Type checking

# Database
uv run migrate                # Run migrations
uv run migrate-create "msg"   # Create migration
```
