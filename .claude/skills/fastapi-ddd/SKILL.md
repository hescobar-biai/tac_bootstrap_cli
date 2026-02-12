---
name: fastapi-ddd
description: "Generates and maintains FastAPI services with DDD Lite vertical slice architecture. Use when creating new business capabilities, entities, CQRS commands/queries, Alembic migrations, or refactoring services following Screaming Architecture with domain aggregates, base Entity class, and multi-tenancy."
---

# FastAPI DDD Lite

Generate and maintain FastAPI services using **DDD Lite** with Screaming Architecture and vertical slice patterns. This skill implements the Celes conventions: Pydantic-based Entity, BaseRepository with SQLAlchemy, CQRS with commands/queries/use_cases, EntityState lifecycle, multi-tenancy, and IDK documentation.

## Instructions

### Prerequisites

- Python 3.10+
- FastAPI with sync or async support
- SQLAlchemy 2.0+ (sync `Session` for standard CRUD)
- Alembic for database migrations
- Pydantic v2 for entities and schemas

### Screaming Architecture

> "Architecture should scream the use cases of the system."

Folder names reflect **business domains**, not technical layers:

```
src/
+-- prompt/          # Prompt management capability
+-- provider/        # LLM provider integration
+-- execution/       # Prompt execution engine
+-- evaluation/      # Response comparison
+-- shared/          # Cross-cutting concerns
```

### Workflow: Scaffold a New Business Capability

When the user asks to create a new domain, entity, or feature:

1. **Identify the business capability** (e.g., `forecast`, `inventory`, `supplier`):
   - Determine the aggregate root entity name (PascalCase: `Forecast`, `Product`)
   - Identify fields beyond the base Entity (code, name, description are inherited)
   - Confirm if authorization scopes are needed

2. **Create the vertical slice structure** (4 layers):
   ```
   src/{capability}/
   +-- domain/
   |   +-- aggregates/
   |   |   +-- {entity}.py          # Aggregate root extending Entity
   |   +-- repositories/
   |   |   +-- {entity}_repository.py  # Repository interface (port)
   |   +-- value_objects/            # Immutable types (frozen dataclasses)
   |   +-- events/                   # Domain events
   |   +-- exceptions/               # Domain-specific errors
   +-- application/
   |   +-- commands/                 # Write operations (CQRS)
   |   |   +-- create_{entity}.py
   |   |   +-- update_{entity}.py
   |   |   +-- delete_{entity}.py
   |   +-- queries/                  # Read operations (CQRS)
   |   |   +-- get_{entity}.py
   |   |   +-- list_{entities}.py
   |   +-- use_cases/                # Complex multi-aggregate workflows
   |   +-- dtos/
   |       +-- {entity}_dtos.py      # Create, Update, Response schemas
   +-- infrastructure/
   |   +-- persistence/
   |       +-- models.py             # SQLAlchemy ORM model
   |       +-- repository.py         # Repository implementation
   +-- presentation/
       +-- api/
           +-- router.py             # FastAPI endpoints
           +-- dependencies.py       # Route-level DI
   ```

3. **Create the domain aggregate** using [templates/entity.py](templates/entity.py):
   - Extend the `Entity` base class (Pydantic BaseModel)
   - Inherit: id, code, name, description, created_at/by, updated_at/by, state, version, organization_id, project_id, owner
   - Add domain-specific fields and business rule methods
   - Use `EntityState` enum: INACTIVE(0), ACTIVE(1), DELETED(2)

4. **Create DTOs** using [templates/schemas.py](templates/schemas.py):
   - `{Entity}Create` extends `BaseCreate` (code, name, description + custom fields)
   - `{Entity}Update` extends `BaseUpdate` (all fields optional)
   - `{Entity}Response` extends `BaseResponse` (full entity + custom fields)
   - `PaginatedResponse[{Entity}Response]` for list endpoints

5. **Create CQRS handlers**:
   - `Create{Entity}Command` + `Create{Entity}Handler`
   - `Update{Entity}Command` + `Update{Entity}Handler`
   - `Delete{Entity}Command` + `Delete{Entity}Handler`
   - `Get{Entity}Query` + `Get{Entity}Handler`
   - `List{Entities}Query` + `List{Entities}Handler`
   - For complex workflows spanning multiple aggregates, use `use_cases/`

6. **Create ORM model and repository** using [templates/repository.py](templates/repository.py):
   - ORM model maps to database table
   - Repository extends `BaseRepository[T]` with generic CRUD
   - BaseRepository provides: create, get_by_id, get_by_code, get_all, update, delete, soft_delete, activate, deactivate

7. **Create API routes** using [templates/routes.py](templates/routes.py):
   - CRUD endpoints: POST, GET, GET/{id}, PUT/{id}, DELETE/{id}
   - Use dependency injection for repository and services
   - Return proper HTTP status codes (201 for create, 204 for delete)

8. **Register in main.py**:
   ```python
   from src.{capability}.presentation.api.router import router as {capability}_router
   app.include_router({capability}_router, prefix="/api/v1/{capability}")
   ```

9. **Generate Alembic migration**:
   ```bash
   alembic revision --autogenerate -m "add {entity} table"
   alembic upgrade head
   ```

### Entity Base Class

All entities inherit from the `Entity` base class (Pydantic):

```python
class EntityState(IntEnum):
    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    code: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    type: str | None = None
    created_at: datetime
    created_by: str | None = None
    updated_at: datetime
    updated_by: str | None = None
    state: int = EntityState.ACTIVE
    version: int = 1
    organization_id: str | None = None
    project_id: str | None = None
    owner: str | None = None
```

Methods: `mark_updated()`, `activate()`, `deactivate()`, `delete()` (soft), `is_active()`, `is_deleted()`

### CQRS Decision Guide

| Scenario | Location |
|----------|----------|
| Simple CRUD create | `commands/create_{entity}.py` |
| Simple CRUD read | `queries/get_{entity}.py` |
| Simple CRUD update | `commands/update_{entity}.py` |
| Simple CRUD delete | `commands/delete_{entity}.py` |
| List with pagination | `queries/list_{entities}.py` |
| Multi-aggregate workflow | `use_cases/{workflow_name}.py` |

### IDK Documentation Standard

Every Python file includes an IDK (I Don't Know) tag for searchability:

```python
"""
IDK: command, create-prompt, write-operation

Create a new prompt aggregate.
"""
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Aggregate | PascalCase noun | `Prompt`, `Provider` |
| ORM Model | `{Entity}Model` | `PromptModel` |
| Repository Interface | `{Entity}Repository` | `PromptRepository` |
| Repository Impl | `{Entity}RepositoryImpl` | `PromptRepositoryImpl` |
| Service | `{Entity}Service` | `PromptService` |
| Create DTO | `{Entity}Create` | `PromptCreate` |
| Update DTO | `{Entity}Update` | `PromptUpdate` |
| Response DTO | `{Entity}Response` | `PromptResponse` |
| Files | snake_case | `prompt_repository.py` |
| Tables | snake_case plural | `prompts` |

See [reference.md](reference.md) for the complete DDD Lite reference including authorization scopes, value objects, domain events, and testing patterns.

## Examples

### Example 1: Create a "Forecast" Business Capability

User request:
```
Create a Forecast entity with horizon_days, frequency, and model_type fields.
Include full CRUD endpoints.
```

You would:
1. Create directory structure under `src/forecast/`
2. Create `domain/aggregates/forecast.py` extending Entity with:
   - `horizon_days: int = Field(ge=1, le=365)`
   - `frequency: str = Field(default="daily")` (daily, weekly, monthly)
   - `model_type: str = Field(default="lightgbm")` (lightgbm, prophet, ensemble)
3. Create `application/dtos/forecast_dtos.py` with ForecastCreate, ForecastUpdate, ForecastResponse
4. Create CQRS handlers in `application/commands/` and `application/queries/`
5. Create `infrastructure/persistence/models.py` with ForecastModel
6. Create `infrastructure/persistence/repository.py` extending BaseRepository
7. Create `presentation/api/router.py` with CRUD endpoints
8. Register router in main.py: `app.include_router(forecast_router, prefix="/api/v1/forecast")`
9. Generate migration: `alembic revision --autogenerate -m "add forecasts table"`

### Example 2: Add a Complex Use Case

User request:
```
Create an "execute forecast" use case that loads config, selects a model,
runs prediction, and stores results.
```

You would:
1. Create `application/use_cases/execute_forecast.py`
2. Define `ExecuteForecastUseCase` with multiple repository dependencies
3. Implement multi-step workflow: load config -> select model -> execute -> store
4. Add to router as POST `/api/v1/forecast/execute`

### Example 3: Add Authorization Scopes

User request:
```
Add OWNER-level authorization so users can only see their own forecasts.
```

You would:
1. Import AccessScope enum: OWNER(1), GROUP(2), ORGANIZATION(3), SUPERUSER(4)
2. Add `_apply_access_filter()` to the repository query methods
3. Filter by `owner == current_user_id` for OWNER scope
4. Filter by `organization_id` for ORGANIZATION scope
