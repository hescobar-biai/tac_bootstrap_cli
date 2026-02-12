---
name: create-crud-entity
description: Generate complete CRUD entities following vertical slice architecture. Use when creating new business entities, domain models, or API endpoints. Triggers on requests like "create entity", "add CRUD for", "new domain model", or "generate API for".
---

# Create CRUD Entity

Generate complete CRUD entities following **vertical slice architecture** with typed models, service layer, and API endpoints.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `source_dir` | Root source directory | `src/` |
| `capability` | Business capability name | `product_catalog` |
| `entity` | Entity name (snake_case) | `product` |
| `framework` | Backend framework (from ADRs) | `FastAPI` |
| `orm` | ORM/data layer (from ADRs) | `SQLAlchemy` |

If no spec is provided, ask the user for entity name, capability, and fields.

## Quick Start

1. **Check shared infrastructure**: If `<source-dir>/shared/` doesn't exist, create it first using templates in [shared/](shared/)
2. **Gather entity info**: Name, fields, business capability name
3. **Decide authorization**: Does entity need access control? (See [WORKFLOW.md](WORKFLOW.md))
4. **Generate vertical slice**: Create all files using templates in [templates/](templates/)
5. **Register router**: Add to `<source-dir>/main.py`

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).

## Template Variants

| Variant | Use Case |
|---------|----------|
| **Basic** | Public data, no restrictions |
| **Authorized** | Row/column/action level access control |
| **Async** | High concurrency, async/await patterns |

## Architecture Overview

Each entity lives in its own **business capability** directory:

```
<source-dir>/
├── {capability_name}/           # e.g., product_catalog, user_management
│   ├── domain/
│   │   ├── {entity}.py         # Domain model (extends Entity)
│   │   ├── value_objects.py    # Immutable value types
│   │   └── events.py           # Domain events
│   ├── application/
│   │   ├── schemas.py          # DTOs: Create, Update, Response
│   │   ├── service.py          # Business logic orchestration
│   │   └── event_handlers.py   # Domain event handlers
│   ├── infrastructure/
│   │   ├── models.py           # ORM model
│   │   └── repository.py       # Data access layer
│   └── api/
│       └── routes.py           # CRUD endpoints
├── shared/                      # Common infrastructure
├── core/                        # App configuration
└── main.py                      # App entry point
```

## Entity Base Class

All domain models extend `Entity` from `<source-dir>/shared/domain/base_entity.py`:

```python
from shared.domain.base_entity import Entity

class Product(Entity):
    type: str = "product"

    # Entity-specific fields
    sku: str
    unit_price: float
    category: str
```

**Inherited fields** from Entity:
- `id`, `code`, `name`, `description`, `type`
- `created_at`, `created_by`, `updated_at`, `updated_by`
- `state` (per project conventions, e.g., 0=inactive, 1=active, 2=deleted)
- `status`, `version`, `organization_id`, `project_id`, `owner`

## Layer Responsibilities

| Layer | Purpose | Depends On |
|-------|---------|------------|
| **domain/** | Pure business logic, framework-agnostic | Nothing |
| **application/** | Use cases, orchestration, DTOs | domain/ |
| **infrastructure/** | Database, external APIs | domain/, application/ |
| **api/** | HTTP endpoints, request handling | application/ |

## CRUD Endpoints Generated

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/{entities}/` | Create new entity |
| GET | `/{entities}/{id}` | Get by ID |
| GET | `/{entities}/` | List with pagination, filters, sorting |
| PUT | `/{entities}/{id}` | Update entity |
| DELETE | `/{entities}/{id}` | Soft delete entity |

## Templates Reference

### Entity Templates (Basic)
- [domain_entity.py.md](templates/domain_entity.py.md) - Domain model
- [schemas.py.md](templates/schemas.py.md) - Request/response DTOs (uses BaseSchema)
- [service.py.md](templates/service.py.md) - Application service (uses BaseService)
- [orm_model.py.md](templates/orm_model.py.md) - ORM model
- [repository.py.md](templates/repository.py.md) - Data access
- [routes.py.md](templates/routes.py.md) - API endpoints

### Entity Templates (Authorized)
- [routes_authorized.py.md](templates/routes_authorized.py.md) - Routes with `require_permission`
- [service_authorized.py.md](templates/service_authorized.py.md) - Service with `AuthorizationContext`
- [repository_authorized.py.md](templates/repository_authorized.py.md) - Extends `AuthorizedRepository`

### Advanced Templates
- [domain_events.py.md](templates/domain_events.py.md) - Domain event patterns
- [value_objects.py.md](templates/value_objects.py.md) - Immutable value types
- [tests.py.md](templates/tests.py.md) - Unit & integration tests

### Shared Infrastructure
| Template | Purpose |
|----------|---------|
| [base_entity.py.md](shared/base_entity.py.md) | Entity base class with audit fields |
| [base_schema.py.md](shared/base_schema.py.md) | Schema base classes (BaseCreate, BaseUpdate, BaseResponse) |
| [base_service.py.md](shared/base_service.py.md) | Service base class with CRUD operations |
| [base_repository.py.md](shared/base_repository.py.md) | Generic sync CRUD repository |
| [base_repository_async.py.md](shared/base_repository_async.py.md) | Generic async CRUD repository |
| [database.py.md](shared/database.py.md) | Database connection & session |
| [config.py.md](shared/config.py.md) | Settings configuration |
| [exceptions.py.md](shared/exceptions.py.md) | Custom exception classes |
| [responses.py.md](shared/responses.py.md) | Common response models |
| [dependencies.py.md](shared/dependencies.py.md) | Dependency injection |
| [health.py.md](shared/health.py.md) | Health check endpoints |
| [alembic.py.md](shared/alembic.py.md) | Database migrations setup |

## Delete Behavior

By default, entities use **soft delete**:

| Method | Behavior | Use Case |
|--------|----------|----------|
| `delete()` | Sets state to deleted | Default, preserves data |
| `hard_delete()` | Removes from DB | GDPR, cleanup |
| `deactivate()` | Sets state to inactive | Temporary disable |
| `restore()` | Sets state to active | Undo soft delete |

## Best Practices

1. **Naming**: Use business language for capability names (e.g., `product_catalog`, not `products`)
2. **Fields**: Keep domain models focused; split large entities into value objects
3. **Validation**: Put business rules in domain layer, input validation in schemas
4. **Cross-capability**: Use repository interfaces for cross-slice references
5. **State management**: Use `state` field for soft deletes per project conventions
6. **Audit trail**: Always pass `user_id` to service methods for tracking
7. **Testing**: Create tests alongside each capability
8. **Events**: Use domain events for loose coupling between capabilities
