# Database Session Management Template

**ADW ID:** a84f13cc
**Date:** 2026-01-23
**Specification:** specs/issue-121-adw-a84f13cc-sdlc_planner-template-database-py.md

## Overview

This feature adds a centralized database session management template for TAC Bootstrap CLI that generates production-ready database.py files for FastAPI projects. The template supports both synchronous and asynchronous SQLAlchemy patterns through conditional rendering, providing a single source of truth for database connection configuration, session creation, and lifecycle management following the 12-factor app pattern.

## What Was Built

Following the Dual Creation Pattern, two files were created:

- **Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - Jinja2 template for CLI generation
- **Reference Implementation**: `src/shared/infrastructure/database.py` - Rendered reference showing final output

The template provides:
- Environment-first database URL configuration with fallback chain
- Conditional sync/async SQLAlchemy engine creation
- SessionLocal factory for creating database sessions
- Declarative Base for ORM model inheritance
- get_db() generator for FastAPI dependency injection with proper cleanup
- Optional connection pool configuration as commented examples

## Technical Implementation

### Files Created

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`: Jinja2 template with 238 lines including:
  - Comprehensive IDK docstring with usage examples
  - Conditional imports for sync/async SQLAlchemy
  - Environment variable priority chain for DATABASE_URL
  - Sync and async engine creation with pool config examples
  - Sync and async get_db() generator implementations

- `src/shared/infrastructure/database.py`: Reference implementation with 168 lines:
  - Synchronous version (async_mode=false, the default)
  - Full SQLAlchemy imports and setup
  - Header comment explaining it's a template reference
  - Complete working example for FastAPI projects

### Key Implementation Details

**1. Environment-First Configuration**
```python
DATABASE_URL = os.getenv("DATABASE_URL") or "{{ config.project.database_url | default('sqlite:///./app.db') }}"
```
Priority chain: `DATABASE_URL` env var → `config.project.database_url` → hardcoded sqlite default

**2. Conditional Async/Sync Support**
```jinja2
{% if config.project.async_mode | default(false) %}
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
{% else %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
{% endif %}
```

**3. Connection Pool Configuration**
Both sync and async engines include commented examples:
```python
# pool_size={{ config.database.pool_size | default(5) }},
# max_overflow={{ config.database.max_overflow | default(10) }},
# pool_pre_ping=True,  # Enable connection health checks
# pool_recycle=3600,   # Recycle connections after 1 hour
```

**4. get_db() Generator with Proper Cleanup**

Synchronous version:
```python
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Asynchronous version:
```python
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

**5. IDK Documentation Pattern**
The template follows existing IDK docstring format with:
- Module-level docstring with IDK tags, responsibilities, key components, invariants
- Function-level docstrings for get_db() with usage examples
- Complete usage examples showing FastAPI integration
- Failure modes documentation
- Collaborators and related docs references

## How to Use

### For CLI Users (Generating Projects)

When TAC Bootstrap generates a project with async mode disabled (default):

```bash
tac-bootstrap init my-project
# Creates src/shared/infrastructure/database.py with sync SQLAlchemy
```

When generating with async mode:

```yaml
# config.yml
project:
  async_mode: true
```

```bash
tac-bootstrap init my-async-project
# Creates src/shared/infrastructure/database.py with async SQLAlchemy
```

### For Generated Projects

The generated database.py provides:

1. **Import database components in your models**:
```python
from src.shared.infrastructure.database import Base

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
```

2. **Use get_db() in FastAPI routes**:
```python
from src.shared.infrastructure.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()
```

3. **Create database tables on startup**:
```python
from src.shared.infrastructure.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)
```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (highest priority)
  - Example: `postgresql://user:pass@localhost/dbname`
  - Example: `sqlite:///./app.db`
  - If not set, falls back to config.yml or hardcoded default

### config.yml Variables

```yaml
project:
  async_mode: false  # Set to true for async SQLAlchemy
  database_url: "sqlite:///./app.db"  # Fallback if DATABASE_URL not set

database:
  pool_size: 5  # Uncomment in generated code to use
  max_overflow: 10  # Uncomment in generated code to use
```

### Connection Pool Configuration

The template includes commented examples for production configuration. Uncomment in the generated database.py to use:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Number of permanent connections
    max_overflow=10,  # Max overflow connections
    pool_pre_ping=True,  # Health check before checkout
    pool_recycle=3600,  # Recycle after 1 hour
    echo=False,  # Set True for SQL query logging
)
```

## Testing

The template follows the Dual Creation Pattern, so the reference implementation can be validated:

```bash
# Verify template exists
ls tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2

# Verify reference implementation exists
ls src/shared/infrastructure/database.py

# Run all tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# CLI smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Design Decisions

### Auto-Resolved Clarifications

The following design decisions were made based on analysis during planning:

1. **Single template with conditionals**: Instead of separate sync/async templates, use conditional blocks (`{% if config.project.async_mode %}`). This simplifies maintenance and allows users to see both patterns.

2. **SQLite default**: Default to `sqlite:///./app.db` for instant prototyping without PostgreSQL setup. PostgreSQL projects set `DATABASE_URL` in environment.

3. **No explicit error handling in get_db()**: Let exceptions propagate to FastAPI's exception handlers. Follows separation of concerns - get_db() is infrastructure layer, error handling is application layer.

4. **Environment-first config**: Follow 12-factor app pattern using environment variables for deployment secrets, config.yml for local dev convenience, hardcoded default for instant prototyping.

5. **Reference implementation included**: The rendered file in project root serves as documentation and reference, with header comment explaining it's not used by the CLI itself (framework="none").

6. **Commented pool configuration**: Include pool config as optional commented examples so production apps can uncomment and configure via config.yml. Sensible defaults work for 90% of cases.

7. **No migration code**: Database migrations are a separate concern handled by Alembic in other templates. database.py focuses solely on runtime session management.

## Notes

### Related Templates

This template works with other shared infrastructure templates:

- `base_repository.py.j2`: Uses Session from database.py
- `base_repository_async.py.j2`: Uses AsyncSession from database.py
- `base_entity.py.j2`: Domain entities that ORM models inherit from
- `base_service.py.j2`: Services that use repositories with sessions

### SQLAlchemy Patterns

**Synchronous** (default):
- Uses `create_engine()` and `sessionmaker()`
- Returns `Session` from get_db()
- Compatible with sync FastAPI route handlers

**Asynchronous** (when async_mode=true):
- Uses `create_async_engine()` and `async_sessionmaker()`
- Returns `AsyncSession` from get_db()
- Requires async route handlers with `await`

### Future Enhancements

Potential improvements for future versions:

- Add Alembic migration initialization in separate template
- Add read replica configuration examples
- Add connection retry logic examples
- Create health check endpoint template that tests database connection
- Add support for multiple database connections (multi-tenant scenarios)
- Add example of transaction context managers

### Context from PLAN_TAC_BOOTSTRAP.md

This task is part of **Phase 1: Templates Base Classes (Fase 1)**, specifically **Task 1.6: Template database.py**. It completes the shared infrastructure templates needed for DDD-based FastAPI projects generated by TAC Bootstrap CLI.

The template follows all architectural patterns established in the project:
- Dual Creation Pattern (template + rendered reference)
- IDK documentation format
- Environment-first configuration
- 12-factor app principles
- Separation of concerns (infrastructure vs application layer)
