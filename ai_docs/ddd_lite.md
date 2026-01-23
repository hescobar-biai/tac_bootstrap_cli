# DDD Lite - Vertical Slice Architecture Quick Reference

**IDK**: ddd-lite, vertical-slice, fastapi-crud, entity-patterns, screaming-architecture

A practical, actionable guide for implementing DDD patterns with FastAPI using vertical slice architecture. Ready-to-copy templates and patterns from the `create-crud-entity` skill.

---

## Screaming Architecture

> "Architecture should scream the use cases of the system." — Robert C. Martin

This codebase follows **Screaming Architecture**: folder names reflect **business domains**, not technical layers.

### Before vs After: Technical vs Domain-Focused

```text
# Technical Organization (Anti-Pattern)     # Business-Focused (This Codebase)
src/                                         src/
├── controllers/                             ├── prompt/          # Prompt management
├── models/                                  ├── provider/        # LLM provider integration
├── repositories/                            ├── execution/       # Prompt execution engine
├── services/                                ├── evaluation/      # Response comparison
└── utils/                                   └── shared/          # Cross-cutting concerns
```

### Why This Matters

| Aspect | Technical Organization | Business-Focused |
|--------|----------------------|------------------|
| **Onboarding** | "Where does user logic go?" | Navigate to `prompt/` or `provider/` |
| **Changes** | Features scattered across folders | All feature code in one place |
| **Team scaling** | Everyone touches everything | Teams own capabilities |
| **Cognitive load** | Must understand entire codebase | Focus on one business area |

### Business Capabilities in This Codebase

| Capability | Purpose | Domain Concepts |
|------------|---------|-----------------|
| `prompt/` | Prompt template management | Prompt, Version, Tag |
| `provider/` | LLM provider integration | Provider, Model, Config |
| `execution/` | Run prompts against LLMs | Execution, Request, Response |
| `evaluation/` | Compare and analyze responses | Comparison, Metrics |
| `shared/` | Cross-cutting infrastructure | Auth, Database, Logging |

---

## Quick Reference: Entity Creation Checklist

```text
[ ] 1. Gather entity info: name (PascalCase), capability (snake_case), fields
[ ] 2. Check if shared infrastructure exists (src/shared/)
[ ] 3. Decide authorization: Basic or Authorized templates?
[ ] 4. Create vertical slice structure (4 layers)
[ ] 5. Create domain aggregate (domain/aggregates/)
[ ] 6. Create DTOs (application/dtos/)
[ ] 7. Create command/query handlers (application/commands/, application/queries/)
[ ] 8. Create ORM model (infrastructure/persistence/)
[ ] 9. Create repository (infrastructure/persistence/)
[ ] 10. Create routes (presentation/api/router.py)
[ ] 11. Register router in main.py
[ ] 12. Add dependency factory in dependencies.py
[ ] 13. Generate database migration
[ ] 14. Run tests
```

---

## Vertical Slice Architecture

### Directory Structure

Each entity lives in its own **business capability** directory with **4 layers**:

```text
src/
├── {capability}/                    # e.g., prompt, provider, execution
│   ├── domain/                      # Pure business logic (no frameworks)
│   │   ├── aggregates/              # Aggregate roots (transaction boundaries)
│   │   │   └── {entity}.py
│   │   ├── entities/                # Domain entities (have identity)
│   │   ├── value_objects/           # Immutable types (defined by attributes)
│   │   ├── repositories/            # Repository interfaces (ports)
│   │   │   └── {entity}_repository.py
│   │   ├── services/                # Domain services (cross-entity logic)
│   │   ├── events/                  # Domain events
│   │   └── exceptions/              # Domain-specific exceptions
│   │
│   ├── application/                 # Use cases & orchestration
│   │   ├── commands/                # Write operations (CQRS)
│   │   │   ├── create_{entity}.py
│   │   │   ├── update_{entity}.py
│   │   │   └── delete_{entity}.py
│   │   ├── queries/                 # Read operations (CQRS)
│   │   │   ├── get_{entity}.py
│   │   │   └── list_{entities}.py
│   │   ├── use_cases/               # Complex multi-step workflows
│   │   └── dtos/                    # Data transfer objects
│   │       └── {entity}_dtos.py
│   │
│   ├── infrastructure/              # External concerns
│   │   ├── persistence/             # Database implementation
│   │   │   ├── models.py            # SQLAlchemy ORM models
│   │   │   └── repository.py        # Repository implementation
│   │   └── adapters/                # External service adapters
│   │
│   └── presentation/                # API layer
│       └── api/
│           ├── router.py            # FastAPI endpoints
│           └── dependencies.py      # Route-level DI
│
├── shared/                          # Cross-cutting concerns
│   ├── domain/
│   │   ├── value_objects/           # Shared value objects
│   │   ├── exceptions/              # Common exceptions
│   │   │   ├── base.py
│   │   │   └── common.py
│   │   └── events/                  # Event infrastructure
│   ├── infrastructure/
│   │   ├── database/                # DB connection & session
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── health.py
│   │   ├── config/                  # Application settings
│   │   │   └── settings.py
│   │   ├── auth/                    # Authentication
│   │   │   └── firebase.py
│   │   └── observability/           # Logging & metrics
│   │       └── logging.py
│   └── presentation/
│       └── middleware/              # HTTP middleware
│           ├── logging.py
│           └── error_handlers.py
│
└── main.py                          # App entry point
```

---

## Module Anatomy

A visual overview of a single capability at a glance:

```text
                              ┌─────────────────────────────────────┐
                              │           presentation/             │
                              │  ┌───────────────────────────────┐  │
    HTTP Request ─────────────▶  │  api/router.py                │  │
                              │  │  - FastAPI endpoints          │  │
                              │  │  - Request validation         │  │
                              │  │  - Response serialization     │  │
                              │  └───────────────┬───────────────┘  │
                              └──────────────────│──────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────┐
                              │           application/              │
                              │  ┌─────────────┐ ┌─────────────┐    │
                              │  │  commands/  │ │  queries/   │    │
                              │  │  (writes)   │ │  (reads)    │    │
                              │  └──────┬──────┘ └──────┬──────┘    │
                              │         │              │            │
                              │  ┌──────▼──────────────▼──────┐     │
                              │  │        use_cases/          │     │
                              │  │  (complex workflows)       │     │
                              │  └─────────────┬──────────────┘     │
                              │                │                    │
                              │  ┌─────────────▼──────────────┐     │
                              │  │          dtos/             │     │
                              │  │  (data transfer objects)   │     │
                              │  └────────────────────────────┘     │
                              └──────────────────│──────────────────┘
                                                 │
                    ┌────────────────────────────┼───────────────────────────┐
                    │                            │                           │
                    ▼                            ▼                           ▼
┌─────────────────────────────────┐  ┌────────────────────┐  ┌─────────────────────────────────┐
│           domain/               │  │   <<interface>>    │  │        infrastructure/          │
│  ┌───────────────────────────┐  │  │   Repository       │  │  ┌───────────────────────────┐  │
│  │       aggregates/         │  │  │                    │  │  │     persistence/          │  │
│  │  - Business entities      │  │  │  get_by_id()       │◀─│──│  - ORM models             │  │
│  │  - Business rules         │  │  │  save()            │  │  │  - Repository impl        │  │
│  │  - Invariant validation   │  │  │  delete()          │  │  └───────────────────────────┘  │
│  └───────────────────────────┘  │  └────────────────────┘  │  ┌───────────────────────────┐  │
│  ┌───────────────────────────┐  │           ▲              │  │       adapters/           │  │
│  │      value_objects/       │  │           │              │  │  - External APIs          │  │
│  │  - Immutable types        │  │           │              │  │  - Message queues         │  │
│  └───────────────────────────┘  │           │              │  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │           │              └─────────────────────────────────┘
│  │       exceptions/         │  │           │
│  │  - Domain errors          │  │           │
│  └───────────────────────────┘  │           │
│  ┌───────────────────────────┐  │           │
│  │      repositories/        │──┼───────────┘
│  │  - Interface definitions  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘

              Dependency Rule: Outer layers depend on inner layers
              Domain has NO dependencies on other layers
```

---

## Layer Responsibilities

| Layer | Directory | Purpose | Contents | Depends On |
|-------|-----------|---------|----------|------------|
| **Domain** | `domain/` | Pure business logic | Aggregates, entities, value objects, repository interfaces, domain events, exceptions | Nothing (innermost) |
| **Application** | `application/` | Use cases & orchestration | Commands, queries, use cases, DTOs | `domain/` |
| **Infrastructure** | `infrastructure/` | External concerns | ORM models, repository implementations, external adapters | `domain/`, `application/` |
| **Presentation** | `presentation/` | HTTP interface | FastAPI routers, request/response handling | `application/` |

---

## CQRS Pattern

This codebase uses **Command Query Responsibility Segregation** in the application layer.

### Commands (Write Operations)

Located in `application/commands/`. Each command is a single write operation.

```python
# application/commands/create_prompt.py
"""
IDK: command, create-prompt, write-operation

Create a new prompt aggregate.
"""
from dataclasses import dataclass
from ..dtos.prompt_dtos import PromptCreate, PromptResponse


@dataclass
class CreatePromptCommand:
    """Command to create a new prompt."""
    data: PromptCreate
    user_id: str | None = None


class CreatePromptHandler:
    """Handler for CreatePromptCommand."""

    def __init__(self, repository: PromptRepository):
        self.repository = repository

    def execute(self, command: CreatePromptCommand) -> PromptResponse:
        # Validate business rules
        existing = self.repository.get_by_code(command.data.code)
        if existing:
            raise DuplicateEntityError(f"Prompt with code '{command.data.code}' exists")

        # Create domain aggregate
        prompt = Prompt(**command.data.model_dump())

        # Persist and return
        saved = self.repository.save(prompt)
        return PromptResponse.model_validate(saved)
```

### Queries (Read Operations)

Located in `application/queries/`. Each query is a single read operation.

```python
# application/queries/get_prompt.py
"""
IDK: query, get-prompt, read-operation

Retrieve a prompt by ID.
"""
from dataclasses import dataclass
from ..dtos.prompt_dtos import PromptResponse


@dataclass
class GetPromptQuery:
    """Query to get a prompt by ID."""
    prompt_id: str


class GetPromptHandler:
    """Handler for GetPromptQuery."""

    def __init__(self, repository: PromptRepository):
        self.repository = repository

    def execute(self, query: GetPromptQuery) -> PromptResponse:
        prompt = self.repository.get_by_id(query.prompt_id)
        if not prompt:
            raise EntityNotFoundError(f"Prompt '{query.prompt_id}' not found")
        return PromptResponse.model_validate(prompt)
```

### When to Use `use_cases/`

Use the `use_cases/` directory for **complex workflows** that:
- Involve multiple aggregates
- Require transaction coordination
- Have complex business logic spanning multiple steps

```python
# application/use_cases/execute_prompt.py
"""
IDK: use-case, execute-prompt, workflow

Complex workflow: render prompt, call LLM, validate output, store result.
"""

class ExecutePromptUseCase:
    """Orchestrates prompt execution across multiple aggregates."""

    def __init__(
        self,
        prompt_repo: PromptRepository,
        provider_repo: ProviderRepository,
        execution_repo: ExecutionRepository,
    ):
        self.prompt_repo = prompt_repo
        self.provider_repo = provider_repo
        self.execution_repo = execution_repo

    def execute(self, request: ExecutePromptRequest) -> ExecutionResponse:
        # 1. Load prompt template
        prompt = self.prompt_repo.get_by_id(request.prompt_id)

        # 2. Load provider configuration
        provider = self.provider_repo.get_by_id(request.provider_id)

        # 3. Render prompt with variables
        rendered = prompt.render(request.variables)

        # 4. Call LLM
        llm_response = provider.call(rendered)

        # 5. Create and save execution record
        execution = Execution(prompt_id=prompt.id, response=llm_response)
        return self.execution_repo.save(execution)
```

### CQRS Decision Guide

| Scenario | Use |
|----------|-----|
| Simple CRUD create | `commands/create_{entity}.py` |
| Simple CRUD read | `queries/get_{entity}.py` |
| Simple CRUD update | `commands/update_{entity}.py` |
| Simple CRUD delete | `commands/delete_{entity}.py` |
| List with pagination | `queries/list_{entities}.py` |
| Multi-aggregate workflow | `use_cases/{workflow_name}.py` |
| Transaction spanning entities | `use_cases/{workflow_name}.py` |

---

## Reading the Architecture

A guide for developers onboarding to this codebase:

### Step 1: Identify the Business Capability

Look at folder names in `src/` to find the domain you need:

```text
src/
├── prompt/      ← Managing prompt templates? Start here
├── provider/    ← LLM configuration? Start here
├── execution/   ← Running prompts? Start here
├── evaluation/  ← Comparing responses? Start here
└── shared/      ← Cross-cutting infrastructure
```

### Step 2: Navigate by Layer

Once in a capability, navigate by what you need:

| You Need | Navigate To |
|----------|-------------|
| Business rules, domain logic | `domain/aggregates/` |
| Immutable types, value semantics | `domain/value_objects/` |
| Repository interface | `domain/repositories/` |
| API request handling | `presentation/api/router.py` |
| Write operation logic | `application/commands/` |
| Read operation logic | `application/queries/` |
| Complex workflows | `application/use_cases/` |
| DTOs for API | `application/dtos/` |
| Database models | `infrastructure/persistence/models.py` |
| Repository implementation | `infrastructure/persistence/repository.py` |
| External service calls | `infrastructure/adapters/` |

### Step 3: Follow Request Flow

For any API endpoint, trace the flow:

```text
1. presentation/api/router.py     → HTTP handler
2. application/commands/*.py      → Business orchestration (write)
   OR application/queries/*.py    → Business orchestration (read)
3. domain/aggregates/*.py         → Business rules & validation
4. domain/repositories/*.py       → Repository interface
5. infrastructure/persistence/    → Actual database operations
```

### Step 4: Find Cross-Cutting Concerns

Shared infrastructure lives in `src/shared/`:

| Concern | Location |
|---------|----------|
| Database session | `shared/infrastructure/database/session.py` |
| Configuration | `shared/infrastructure/config/settings.py` |
| Authentication | `shared/infrastructure/auth/firebase.py` |
| Logging | `shared/infrastructure/observability/logging.py` |
| Error handling | `shared/presentation/middleware/error_handlers.py` |
| Common exceptions | `shared/domain/exceptions/common.py` |

---

## Base Classes

### Entity Base Class (`shared/domain/base_entity.py`)

```python
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4
from datetime import datetime, UTC
from enum import IntEnum


class EntityState(IntEnum):
    """Entity lifecycle states."""
    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2


class Entity(BaseModel):
    """Base class for all domain entities."""

    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        use_enum_values=True,
    )

    # Core Identity
    id: str = Field(default_factory=lambda: str(uuid4()))
    code: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    type: str | None = Field(default=None, max_length=50)

    # Audit Trail
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_by: str | None = Field(default=None)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_by: str | None = Field(default=None)

    # State Management
    state: int = Field(default=EntityState.ACTIVE, ge=0, le=2)
    status: str | None = Field(default=None, max_length=50)
    version: int = Field(default=1, ge=1)

    # Multi-tenancy
    organization_id: str | None = Field(default=None)
    project_id: str | None = Field(default=None)
    owner: str | None = Field(default=None)

    def mark_updated(self, user_id: str | None = None) -> None:
        """Update audit trail on modification."""
        self.updated_at = datetime.now(UTC)
        if user_id:
            self.updated_by = user_id
        self.version += 1

    def deactivate(self, user_id: str | None = None) -> None:
        """Transition to INACTIVE state."""
        self.state = EntityState.INACTIVE
        self.mark_updated(user_id)

    def activate(self, user_id: str | None = None) -> None:
        """Transition to ACTIVE state."""
        self.state = EntityState.ACTIVE
        self.mark_updated(user_id)

    def delete(self, user_id: str | None = None) -> None:
        """Soft delete (state = DELETED)."""
        self.state = EntityState.DELETED
        self.mark_updated(user_id)

    def is_active(self) -> bool:
        return self.state == EntityState.ACTIVE

    def is_deleted(self) -> bool:
        return self.state == EntityState.DELETED

    def is_inactive(self) -> bool:
        return self.state == EntityState.INACTIVE
```

### Schema Base Classes (`shared/application/base_schema.py`)

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseCreate(BaseModel):
    """Base schema for entity creation."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class BaseUpdate(BaseModel):
    """Base schema for entity updates (all fields optional)."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class BaseResponse(BaseModel):
    """Base schema for API responses."""
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    code: str
    name: str
    description: str | None
    type: str | None
    created_at: datetime
    created_by: str | None
    updated_at: datetime
    updated_by: str | None
    state: int
    status: str | None
    version: int
    organization_id: str | None
    project_id: str | None
    owner: str | None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response wrapper."""
    model_config = ConfigDict(from_attributes=True)

    data: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    pages: int = Field(ge=0)

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True
```

### Repository Base Class (`shared/infrastructure/base_repository.py`)

```python
from typing import TypeVar, Generic, Type, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import datetime, UTC

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Generic CRUD repository."""

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, entity_id: str) -> T | None:
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def get_by_code(self, code: str) -> T | None:
        return self.db.query(self.model).filter(self.model.code == code).first()

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> Tuple[list[T], int]:
        query = self.db.query(self.model)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        total = query.count()

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            query = query.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))

        # Apply pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    def update(self, entity_id: str, data: dict) -> T | None:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None

        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        entity.updated_at = datetime.now(UTC)
        entity.version = entity.version + 1

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: str) -> bool:
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True

    def soft_delete(self, entity_id: str) -> T | None:
        return self.update(entity_id, {"state": 2})

    def exists(self, entity_id: str) -> bool:
        return self.db.query(self.model).filter(self.model.id == entity_id).count() > 0

    def count(self, filters: dict | None = None) -> int:
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        return query.count()
```

### Service Base Class (`shared/application/base_service.py`)

```python
from typing import TypeVar, Generic, Type
from datetime import datetime, UTC

from shared.infrastructure.base_repository import BaseRepository
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse, PaginatedResponse
from shared.domain.exceptions.common import EntityNotFoundError, DuplicateEntityError

TCreate = TypeVar("TCreate", bound=BaseCreate)
TUpdate = TypeVar("TUpdate", bound=BaseUpdate)
TResponse = TypeVar("TResponse", bound=BaseResponse)
TModel = TypeVar("TModel")
TDomain = TypeVar("TDomain")


class BaseService(Generic[TCreate, TUpdate, TResponse, TModel, TDomain]):
    """Generic service with CRUD operations."""

    def __init__(
        self,
        repository: BaseRepository[TModel],
        response_class: Type[TResponse],
        domain_class: Type[TDomain],
        entity_name: str,
        model_class: Type[TModel] | None = None,
    ):
        self.repository = repository
        self.response_class = response_class
        self.domain_class = domain_class
        self.entity_name = entity_name
        self.model_class = model_class or repository.model

    def create(self, data: TCreate, user_id: str | None = None) -> TResponse:
        # Check duplicate
        existing = self.repository.get_by_code(data.code)
        if existing:
            raise DuplicateEntityError(f"{self.entity_name} with code '{data.code}' already exists")

        # Create domain entity
        now = datetime.now(UTC)
        entity_data = data.model_dump()
        entity_data.update({
            "created_at": now,
            "updated_at": now,
            "created_by": user_id,
            "updated_by": user_id,
        })
        domain_entity = self.domain_class(**entity_data)

        # Save
        db_model = self.model_class(**domain_entity.model_dump())
        saved = self.repository.create(db_model)
        return self.response_class.model_validate(saved)

    def get_by_id(self, entity_id: str) -> TResponse:
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFoundError(f"{self.entity_name} with ID '{entity_id}' not found")
        return self.response_class.model_validate(entity)

    def get_by_code(self, code: str) -> TResponse:
        entity = self.repository.get_by_code(code)
        if not entity:
            raise EntityNotFoundError(f"{self.entity_name} with code '{code}' not found")
        return self.response_class.model_validate(entity)

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        include_deleted: bool = False,
    ) -> PaginatedResponse[TResponse]:
        effective_filters = filters.copy() if filters else {}
        if not include_deleted and "state" not in effective_filters:
            effective_filters["state"] = 1

        items, total = self.repository.get_all(
            page=page, page_size=page_size, filters=effective_filters,
            sort_by=sort_by, sort_order=sort_order
        )
        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return PaginatedResponse(
            data=[self.response_class.model_validate(item) for item in items],
            total=total, page=page, page_size=page_size, pages=pages
        )

    def update(self, entity_id: str, data: TUpdate, user_id: str | None = None) -> TResponse:
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(f"{self.entity_name} with ID '{entity_id}' not found")

        update_data = data.model_dump(exclude_unset=True)
        if user_id:
            update_data["updated_by"] = user_id

        updated = self.repository.update(entity_id, update_data)
        return self.response_class.model_validate(updated)

    def delete(self, entity_id: str, user_id: str | None = None) -> bool:
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(f"{self.entity_name} with ID '{entity_id}' not found")

        update_data = {"state": 2}
        if user_id:
            update_data["updated_by"] = user_id
        self.repository.update(entity_id, update_data)
        return True

    def hard_delete(self, entity_id: str) -> bool:
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(f"{self.entity_name} with ID '{entity_id}' not found")
        return self.repository.delete(entity_id)

    def activate(self, entity_id: str, user_id: str | None = None) -> TResponse:
        return self._change_state(entity_id, 1, user_id)

    def deactivate(self, entity_id: str, user_id: str | None = None) -> TResponse:
        return self._change_state(entity_id, 0, user_id)

    def restore(self, entity_id: str, user_id: str | None = None) -> TResponse:
        return self._change_state(entity_id, 1, user_id)

    def _change_state(self, entity_id: str, state: int, user_id: str | None) -> TResponse:
        existing = self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(f"{self.entity_name} with ID '{entity_id}' not found")
        update_data = {"state": state}
        if user_id:
            update_data["updated_by"] = user_id
        updated = self.repository.update(entity_id, update_data)
        return self.response_class.model_validate(updated)
```

---

## Entity State Management

### EntityState Enum

| State | Value | Meaning | Use Case |
|-------|-------|---------|----------|
| `INACTIVE` | 0 | Deactivated | Temporarily disabled |
| `ACTIVE` | 1 | Operational | Normal state (default) |
| `DELETED` | 2 | Soft-deleted | Archived, recoverable |

### State Transitions

```text
        deactivate()          delete()
INACTIVE <────────── ACTIVE ──────────> DELETED
    │                  ^                   │
    │    activate()    │    restore()      │
    └──────────────────┴───────────────────┘
```

### Delete Behavior

| Method | Behavior | Use Case |
|--------|----------|----------|
| `delete()` | Sets state=2 | Default, preserves data |
| `hard_delete()` | Removes from DB | GDPR, cleanup |
| `deactivate()` | Sets state=0 | Temporary disable |
| `restore()` | Sets state=1 | Undo soft delete |

---

## Template: Domain Aggregate

**Path**: `{capability}/domain/aggregates/{entity}.py`

```python
"""
IDK: domain-entity, {entity_type}, aggregate-root

Module: {entity_name}

Responsibility:
- Represent {EntityName} domain concept
- Encapsulate business rules
- Validate entity invariants
"""

from shared.domain.base_entity import Entity


class {EntityName}(Entity):
    """
    Domain aggregate for {EntityName}.

    Inherited Fields: id, code, name, description, type, created_at,
    created_by, updated_at, updated_by, state, status, version,
    organization_id, project_id, owner
    """

    type: str = "{entity_type}"

    # Entity-specific fields
    sku: str
    unit_price: float
    category: str | None = None
    is_available: bool = True
    stock_quantity: int = 0
    tags: list[str] = []

    # Domain methods
    def apply_discount(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.unit_price = self.unit_price * (1 - percentage / 100)
        self.mark_updated()

    def is_low_stock(self, threshold: int = 10) -> bool:
        return self.stock_quantity < threshold
```

---

## Template: DTOs

**Path**: `{capability}/application/dtos/{entity}_dtos.py`

```python
"""
IDK: dto, {entity_name}, data-transfer-object

Application DTOs for {EntityName}.
"""

from pydantic import Field
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse


class {EntityName}Create(BaseCreate):
    """Schema for creating {EntityName}."""
    sku: str = Field(..., min_length=1, max_length=50)
    unit_price: float = Field(..., ge=0)
    category: str | None = Field(default=None, max_length=100)
    is_available: bool = Field(default=True)
    stock_quantity: int = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list)


class {EntityName}Update(BaseUpdate):
    """Schema for updating {EntityName} (all fields optional)."""
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    unit_price: float | None = Field(default=None, ge=0)
    category: str | None = None
    is_available: bool | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    tags: list[str] | None = None


class {EntityName}Response(BaseResponse):
    """Schema for {EntityName} API response."""
    sku: str
    unit_price: float
    category: str | None
    is_available: bool
    stock_quantity: int
    tags: list[str]
```

---

## Template: Service

**Path**: `{capability}/application/service.py` (or within commands/queries)

```python
"""
IDK: service, {entity_name}, business-logic

Service for {EntityName} business logic.
"""

from shared.application.base_service import BaseService
from ..domain.aggregates.{entity_name} import {EntityName}
from ..infrastructure.persistence.repository import {EntityName}Repository
from ..infrastructure.persistence.models import {EntityName}Model
from .dtos.{entity_name}_dtos import {EntityName}Create, {EntityName}Update, {EntityName}Response


class {EntityName}Service(BaseService[
    {EntityName}Create,
    {EntityName}Update,
    {EntityName}Response,
    {EntityName}Model,
    {EntityName}
]):
    """Service for {EntityName} business logic."""

    def __init__(self, repository: {EntityName}Repository):
        super().__init__(
            repository=repository,
            response_class={EntityName}Response,
            domain_class={EntityName},
            entity_name="{EntityName}",
            model_class={EntityName}Model,
        )

    # Custom business methods
    def get_available(self) -> list[{EntityName}Response]:
        items = self.repository.get_available()
        return [{EntityName}Response.model_validate(item) for item in items]

    def get_by_category(self, category: str) -> list[{EntityName}Response]:
        items = self.repository.get_by_category(category)
        return [{EntityName}Response.model_validate(item) for item in items]
```

---

## Template: ORM Model

**Path**: `{capability}/infrastructure/persistence/models.py`

```python
"""
IDK: orm-model, {entity_name}, persistence

SQLAlchemy ORM model for {EntityName}.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Index
from datetime import datetime, UTC
from shared.infrastructure.database.base import Base


class {EntityName}Model(Base):
    """ORM model for {entity_name} table."""

    __tablename__ = "{entity_name}"

    # Base Entity Fields
    id = Column(String, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    type = Column(String(50), nullable=False, default="{entity_type}")

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC),
                        onupdate=lambda: datetime.now(UTC))
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    state = Column(Integer, nullable=False, default=1, index=True)
    status = Column(String(50), nullable=True)
    version = Column(Integer, nullable=False, default=1)

    organization_id = Column(String, nullable=True, index=True)
    project_id = Column(String, nullable=True)
    owner = Column(String, nullable=True, index=True)
    group_path = Column(String, nullable=True, index=True)

    # Entity-Specific Fields
    sku = Column(String(50), unique=True, nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    is_available = Column(Boolean, nullable=False, default=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    tags = Column(JSON, nullable=True)

    # Indexes
    __table_args__ = (
        Index('ix_{entity_name}_org_state', 'organization_id', 'state'),
        Index('ix_{entity_name}_owner_state', 'owner', 'state'),
    )
```

---

## Template: Repository

**Path**: `{capability}/infrastructure/persistence/repository.py`

```python
"""
IDK: repository, {entity_name}, data-access

Repository for {EntityName} data access.
"""

from sqlalchemy.orm import Session
from shared.infrastructure.base_repository import BaseRepository
from .models import {EntityName}Model


class {EntityName}Repository(BaseRepository[{EntityName}Model]):
    """Repository for {EntityName} CRUD operations."""

    def __init__(self, db: Session):
        super().__init__({EntityName}Model, db)

    # Custom query methods
    def get_available(self) -> list[{EntityName}Model]:
        return (
            self.db.query(self.model)
            .filter(self.model.is_available == True)
            .filter(self.model.state == 1)
            .all()
        )

    def get_by_category(self, category: str) -> list[{EntityName}Model]:
        return (
            self.db.query(self.model)
            .filter(self.model.category == category)
            .filter(self.model.state == 1)
            .all()
        )

    def get_low_stock(self, threshold: int = 10) -> list[{EntityName}Model]:
        return (
            self.db.query(self.model)
            .filter(self.model.stock_quantity < threshold)
            .filter(self.model.is_available == True)
            .filter(self.model.state == 1)
            .all()
        )
```

---

## Template: Routes

**Path**: `{capability}/presentation/api/router.py`

```python
"""
IDK: http-endpoint, {entity_name}, fastapi-router

FastAPI routes for {EntityName} CRUD.
"""

from fastapi import APIRouter, Depends, Query, status
from shared.application.base_schema import PaginatedResponse, MessageResponse
from core.dependencies import get_{entity_name}_service
from ...application.dtos.{entity_name}_dtos import {EntityName}Create, {EntityName}Update, {EntityName}Response
from ...application.service import {EntityName}Service

router = APIRouter(prefix="/{entities}", tags=["{Tag}"])


@router.post("/", response_model={EntityName}Response, status_code=status.HTTP_201_CREATED)
async def create_{entity_name}(
    data: {EntityName}Create,
    service: {EntityName}Service = Depends(get_{entity_name}_service)
) -> {EntityName}Response:
    """Create a new {EntityName}."""
    return service.create(data)


@router.get("/{{{entity_name}_id}}", response_model={EntityName}Response)
async def get_{entity_name}(
    {entity_name}_id: str,
    service: {EntityName}Service = Depends(get_{entity_name}_service)
) -> {EntityName}Response:
    """Get {EntityName} by ID."""
    return service.get_by_id({entity_name}_id)


@router.get("/", response_model=PaginatedResponse[{EntityName}Response])
async def list_{entity_name}s(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str | None = Query(None),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    service: {EntityName}Service = Depends(get_{entity_name}_service)
) -> PaginatedResponse[{EntityName}Response]:
    """List {EntityName}s with pagination."""
    return service.get_all(page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order)


@router.put("/{{{entity_name}_id}}", response_model={EntityName}Response)
async def update_{entity_name}(
    {entity_name}_id: str,
    data: {EntityName}Update,
    service: {EntityName}Service = Depends(get_{entity_name}_service)
) -> {EntityName}Response:
    """Update {EntityName}."""
    return service.update({entity_name}_id, data)


@router.delete("/{{{entity_name}_id}}", response_model=MessageResponse)
async def delete_{entity_name}(
    {entity_name}_id: str,
    service: {EntityName}Service = Depends(get_{entity_name}_service)
) -> MessageResponse:
    """Soft delete {EntityName}."""
    service.delete({entity_name}_id)
    return MessageResponse(message=f"{EntityName} {entity_name}_id deleted successfully")
```

---

## Path Reference Table

Quick reference for where files live:

| Component | Old Path (Deprecated) | New Path (Current) |
|-----------|----------------------|-------------------|
| Domain entity | `domain/{entity}.py` | `domain/aggregates/{entity}.py` |
| Value objects | `domain/value_objects.py` | `domain/value_objects/{name}.py` |
| Repository interface | - | `domain/repositories/{entity}_repository.py` |
| Domain events | `domain/events.py` | `domain/events/{event}.py` |
| Domain exceptions | - | `domain/exceptions/{name}.py` |
| Schemas/DTOs | `application/schemas.py` | `application/dtos/{entity}_dtos.py` |
| Service | `application/service.py` | `application/service.py` or `commands/`/`queries/` |
| Commands | - | `application/commands/{action}_{entity}.py` |
| Queries | - | `application/queries/{action}_{entity}.py` |
| Use cases | - | `application/use_cases/{workflow}.py` |
| ORM model | `infrastructure/models.py` | `infrastructure/persistence/models.py` |
| Repository impl | `infrastructure/repository.py` | `infrastructure/persistence/repository.py` |
| External adapters | - | `infrastructure/adapters/{name}.py` |
| Routes | `api/routes.py` | `presentation/api/router.py` |
| Route dependencies | - | `presentation/api/dependencies.py` |

---

## Authorization Patterns

### Authorization Template Types

| Template | Use Case |
|----------|----------|
| **Basic** | Public data, no restrictions |
| **Authorized** | Row/column/action level access control |

### Access Scopes

| Scope | Value | User Sees |
|-------|-------|-----------|
| **OWNER** | 1 | Only own entities (`owner == user_id`) |
| **GROUP** | 2 | Own + group entities |
| **ORGANIZATION** | 3 | All org entities |
| **SUPERUSER** | - | All entities (no filtering) |

### Authorized Repository Pattern

```python
def get_by_id_authorized(
    self,
    entity_id: str,
    user_id: str,
    organization_id: str,
    group_paths: list[str],
    access_scope: AccessScope,
    is_superuser: bool = False,
) -> Model | None:
    query = self.db.query(self.model).filter(self.model.id == entity_id)

    if not is_superuser:
        query = self._apply_access_filter(query, user_id, organization_id, group_paths, access_scope)

    return query.first()

def _apply_access_filter(self, query, user_id, organization_id, group_paths, access_scope):
    # Always filter by organization
    query = query.filter(self.model.organization_id == organization_id)

    if access_scope == AccessScope.OWNER:
        query = query.filter(self.model.owner == user_id)
    elif access_scope == AccessScope.GROUP:
        group_conditions = [self.model.group_path.like(f"{path}%") for path in group_paths]
        query = query.filter(or_(self.model.owner == user_id, *group_conditions))

    return query
```

---

## Naming Conventions

### Classes & Files

| Element | Convention | Example |
|---------|------------|---------|
| Domain Aggregate | `PascalCase` | `Prompt`, `Provider` |
| ORM Model | `{Entity}Model` | `PromptModel` |
| Repository | `{Entity}Repository` | `PromptRepository` |
| Service | `{Entity}Service` | `PromptService` |
| DTOs | `{Entity}Create/Update/Response` | `PromptCreate` |
| Command | `{Action}{Entity}Command` | `CreatePromptCommand` |
| Query | `{Action}{Entity}Query` | `GetPromptQuery` |
| File names | `snake_case.py` | `prompt.py`, `create_prompt.py` |

### Database

| Element | Convention | Example |
|---------|------------|---------|
| Table name | `snake_case` | `prompt`, `provider` |
| Column names | `snake_case` | `unit_price`, `created_at` |
| Index names | `ix_{table}_{column}` | `ix_prompt_code` |
| Constraint names | `uq_{table}_{column}` | `uq_prompt_sku` |

### URLs

| Convention | Example |
|------------|---------|
| Plural nouns | `/prompts/`, `/providers/` |
| Lowercase | `/prompt-versions/` |
| Hyphens for multi-word | `/execution-results/` |

---

## IDK Documentation Standard

All generated code follows the **IDK-first docstring format**:

```python
"""
IDK: keyword-1, keyword-2, keyword-3

Responsibility:
- What this symbol is responsible for

Invariants:
- Rules that must never be violated

Inputs:
- param_name (type): description

Outputs:
- Return type and meaning

Failure Modes:
- Exception/error conditions
"""
```

### IDK Keywords by Layer

| Layer | IDK Examples |
|-------|--------------|
| Domain | `domain-entity`, `value-object`, `aggregate-root`, `business-rule` |
| Application | `command`, `query`, `use-case`, `dto`, `orchestration` |
| Infrastructure | `repository`, `orm-mapping`, `data-access`, `persistence`, `adapter` |
| Presentation | `http-endpoint`, `fastapi-router`, `request-handler`, `pagination` |

---

## Value Objects

Immutable objects defined by their attributes, not identity.

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable money value object."""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter ISO code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)


@dataclass(frozen=True, slots=True)
class Email:
    """Immutable email value object."""
    address: str

    def __post_init__(self) -> None:
        import re
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.address):
            raise ValueError(f"Invalid email: {self.address}")

    @property
    def domain(self) -> str:
        return self.address.split("@")[1]
```

---

## Domain Events

Events for loose coupling between capabilities.

```python
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    """Base class for domain events."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class PromptCreated(DomainEvent):
    """Event raised when a Prompt is created."""
    entity_id: str
    code: str
    name: str
    created_by: str | None = None

    @property
    def event_type(self) -> str:
        return "prompt.created"


# Publishing events from service
class PromptService(BaseService):
    def create(self, data: PromptCreate, user_id: str | None = None) -> PromptResponse:
        result = super().create(data, user_id)
        event_bus.publish(PromptCreated(
            entity_id=result.id, code=result.code, name=result.name, created_by=user_id
        ))
        return result
```

---

## Testing Patterns

### Service Unit Test

```python
import pytest
from unittest.mock import MagicMock
from shared.domain.exceptions.common import EntityNotFoundError, DuplicateEntityError


class TestPromptService:
    @pytest.fixture
    def mock_repository(self):
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        return PromptService(repository=mock_repository)

    def test_create_success(self, service, mock_repository, sample_model):
        mock_repository.get_by_code.return_value = None
        mock_repository.create.return_value = sample_model

        result = service.create(PromptCreate(code="P1", name="Prompt"))

        assert result.code == "P1"
        mock_repository.create.assert_called_once()

    def test_create_duplicate_raises_error(self, service, mock_repository, sample_model):
        mock_repository.get_by_code.return_value = sample_model

        with pytest.raises(DuplicateEntityError):
            service.create(PromptCreate(code="P1", name="Prompt"))
```

### Routes Integration Test

```python
from fastapi import status


class TestPromptRoutes:
    API_PREFIX = "/api/v1/prompts"

    def test_create_entity(self, client):
        response = client.post(f"{self.API_PREFIX}/", json={"code": "P1", "name": "Prompt"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["code"] == "P1"

    def test_get_entity_not_found(self, client):
        response = client.get(f"{self.API_PREFIX}/non-existent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
```

---

## HTTP Status Codes

| Code | Method | Use Case |
|------|--------|----------|
| `201 Created` | POST | Successful creation |
| `200 OK` | GET, PUT, DELETE | Successful operation |
| `400 Bad Request` | All | Validation errors |
| `404 Not Found` | GET, PUT, DELETE | Entity doesn't exist |
| `409 Conflict` | POST, PUT | Duplicate code |
| `422 Unprocessable Entity` | POST, PUT | Schema validation error |
| `500 Internal Error` | All | Server error |

---

## UV Commands Reference

```bash
# Development
uv run dev                    # Start dev server

# Testing
uv run pytest                 # Run tests
uv run pytest --cov=src       # Run with coverage

# Code Quality
uv run ruff check .           # Run linter
uv run ruff format .          # Format code

# Database
uv run alembic revision --autogenerate -m "add_table"  # Create migration
uv run alembic upgrade head   # Apply migration
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Business logic in routes | Violates separation | Move to commands/services |
| Business logic in ORM model | Mixes concerns | Keep in domain aggregate |
| Database queries in domain | Framework dependency | Use repository pattern |
| Skip `mark_updated()` | Audit trail broken | Always call after mutations |
| Use ORM relationships across slices | Tight coupling | Use IDs and repository queries |
| Mutate value objects | Breaks immutability | Create new instances |
| Mix commands and queries | CQRS violation | Separate read/write operations |
| Domain depends on infrastructure | Inverts dependencies | Domain defines interfaces |

---

## Related Documentation

- `ai_docs/ddd.md` - DDD + Hexagonal Architecture theory
- `ai_docs/solid.md` - SOLID principles
- `ai_docs/design_patterns.md` - Design patterns reference
- `.claude/skills/create-crud-entity/` - Full skill templates
