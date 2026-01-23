# Database Template

Database connection and session management using SQLAlchemy. This file should be placed at `src/shared/infrastructure/database.py`.

## Template

```python
"""
IDK: database-connection, session-management, orm-setup

Module: database

Responsibility:
- Configure SQLAlchemy engine and session factory
- Provide declarative base for ORM models
- Manage database lifecycle (init, shutdown)
- Provide session dependency for FastAPI

Key Components:
- Base: SQLAlchemy declarative base
- engine: database connection engine
- SessionLocal: session factory
- get_db: FastAPI dependency for database sessions
- init_db: database initialization

Invariants:
- Single engine instance per application
- Sessions are scoped to request lifecycle
- Sessions auto-close after request
- All ORM models extend Base

Related Docs:
- docs/shared/infrastructure/database.md
"""

from typing import Generator
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import StaticPool
from core.config import settings

# Naming convention for constraints
# Ensures consistent constraint names across databases
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

# Declarative Base
# All ORM models must inherit from this
Base = declarative_base(metadata=metadata)


def create_db_engine():
    """
    IDK: engine-creation, connection-pool, database-setup

    Responsibility:
    - Create SQLAlchemy engine with appropriate settings
    - Configure connection pooling
    - Enable SQLite foreign keys if using SQLite

    Invariants:
    - Returns configured engine instance
    - Pool size and overflow from settings
    - Echo setting controls SQL logging

    Outputs:
    - Engine: configured SQLAlchemy engine

    Related Docs:
    - docs/shared/infrastructure/database-setup.md
    """
    # Get database URL from settings
    database_url = str(settings.database_url)

    # Special handling for SQLite (for testing/dev)
    if database_url.startswith("sqlite"):
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.database_echo,
        )

        # Enable foreign key constraints for SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    else:
        # PostgreSQL or other databases
        engine = create_engine(
            database_url,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            pool_pre_ping=True,  # Verify connections before using
            echo=settings.database_echo,
        )

    return engine


# Create engine instance
engine = create_db_engine()

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    IDK: dependency-injection, session-lifecycle, fastapi-dependency

    Responsibility:
    - Provide database session for FastAPI endpoints
    - Ensure session cleanup after request
    - Handle session lifecycle automatically

    Invariants:
    - Session created per request
    - Session closed after request completes
    - Session closed even if exception occurs

    Outputs:
    - Generator[Session]: database session

    Usage:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    Related Docs:
    - docs/shared/infrastructure/session-management.md
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    IDK: database-initialization, schema-creation, setup

    Responsibility:
    - Create all database tables from ORM models
    - Initialize database schema
    - Should be called on application startup

    Invariants:
    - Creates tables that don't exist
    - Does not drop existing tables
    - Idempotent (safe to call multiple times)

    Failure Modes:
    - OperationalError: database not accessible
    - ProgrammingError: invalid table definition

    Usage:
        # In main.py startup event
        @app.on_event("startup")
        def startup_event():
            init_db()

    Related Docs:
    - docs/shared/infrastructure/database-setup.md
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    IDK: database-teardown, schema-removal, cleanup

    Responsibility:
    - Drop all database tables
    - Clean up database schema
    - Use with caution (destructive operation)

    Invariants:
    - Drops all tables defined in metadata
    - Irreversible operation
    - Should only be used in development/testing

    Warning:
        This operation is DESTRUCTIVE and will delete all data!
        Never use in production.

    Usage:
        # In test teardown
        @pytest.fixture(scope="function")
        def db_session():
            init_db()
            yield
            drop_db()

    Related Docs:
    - docs/shared/infrastructure/testing.md
    """
    Base.metadata.drop_all(bind=engine)


def reset_db() -> None:
    """
    IDK: database-reset, test-setup, clean-slate

    Responsibility:
    - Drop and recreate all database tables
    - Reset database to clean state
    - Useful for testing

    Invariants:
    - Drops all tables first
    - Recreates all tables after
    - All data is lost

    Warning:
        This operation is DESTRUCTIVE and will delete all data!
        Only use in development/testing environments.

    Usage:
        # In test setup
        @pytest.fixture(scope="session")
        def setup_database():
            reset_db()
            yield
            drop_db()

    Related Docs:
    - docs/shared/infrastructure/testing.md
    """
    drop_db()
    init_db()


def get_db_context():
    """
    IDK: context-manager, session-management, standalone-usage

    Responsibility:
    - Provide context manager for standalone database operations
    - Useful for scripts, migrations, or background tasks
    - Automatic session cleanup

    Invariants:
    - Session created on enter
    - Session closed on exit
    - Session rolled back on exception

    Outputs:
    - Session: database session

    Usage:
        # In a standalone script
        from shared.infrastructure.database import get_db_context

        with get_db_context() as db:
            products = db.query(Product).all()
            print(f"Found {len(products)} products")

    Related Docs:
    - docs/shared/infrastructure/session-management.md
    """
    return SessionLocal()
```

## Directory Setup

```
src/
└── shared/
    └── infrastructure/
        ├── __init__.py
        ├── database.py          # <-- This file
        ├── base_repository.py
        └── base_repository_async.py
```

**`src/shared/infrastructure/__init__.py`**:
```python
"""Shared infrastructure components."""
from .database import Base, engine, SessionLocal, get_db, init_db, drop_db, reset_db
from .base_repository import BaseRepository

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "drop_db",
    "reset_db",
    "BaseRepository",
]
```

## Usage in Application

### Main Application Setup

```python
# src/main.py
from fastapi import FastAPI
from shared.infrastructure.database import init_db
from core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

@app.on_event("startup")
def startup_event():
    """Initialize database on application startup."""
    init_db()
    print("Database initialized")

@app.on_event("shutdown")
def shutdown_event():
    """Clean shutdown."""
    print("Application shutting down")
```

### Using in Repository

```python
# src/product_catalog/infrastructure/repository.py
from sqlalchemy.orm import Session
from shared.infrastructure.base_repository import BaseRepository
from .models import ProductModel

class ProductRepository(BaseRepository[ProductModel]):
    """
    IDK: repository, product-persistence, data-access

    Responsibility:
    - CRUD operations for products
    - Product-specific queries
    """

    def __init__(self, db: Session):
        super().__init__(ProductModel, db)
```

### Using in Routes

```python
# src/product_catalog/api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.infrastructure.database import get_db
from ..application.service import ProductService
from ..infrastructure.repository import ProductRepository

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency factory for ProductService."""
    repository = ProductRepository(db)
    return ProductService(repository)

@router.get("/")
def list_products(
    service: ProductService = Depends(get_product_service)
):
    """List all products."""
    return service.get_all()
```

### Standalone Scripts

```python
# scripts/seed_data.py
from shared.infrastructure.database import get_db_context
from product_catalog.infrastructure.models import ProductModel

def seed_products():
    """Seed initial product data."""
    with get_db_context() as db:
        product = ProductModel(
            code="PROD001",
            name="Sample Product",
            description="A sample product",
        )
        db.add(product)
        db.commit()
        print(f"Created product: {product.name}")

if __name__ == "__main__":
    seed_products()
```

## Testing Setup

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.infrastructure.database import Base, get_db
from main import app

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
```

## Environment Configuration

The database connection is configured through settings. See [config.py.md](config.py.md) for full settings configuration.

**Required environment variables**:

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false
```

**Supported database URLs**:

| Database | URL Format |
|----------|------------|
| PostgreSQL | `postgresql://user:pass@host:port/db` |
| PostgreSQL (async) | `postgresql+asyncpg://user:pass@host:port/db` |
| SQLite | `sqlite:///path/to/database.db` |
| SQLite (memory) | `sqlite:///:memory:` |
| MySQL | `mysql+pymysql://user:pass@host:port/db` |

## Database Migration

For production, use Alembic for migrations instead of `init_db()`. See [alembic.py.md](alembic.py.md) for migration setup.

```bash
# Create migration
uv run alembic revision --autogenerate -m "initial schema"

# Run migration
uv run alembic upgrade head
```

## Advanced: Async Support

For async database operations, create a separate `database_async.py`:

```python
# src/shared/infrastructure/database_async.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

async_engine = create_async_engine(
    settings.database_url_async,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_db():
    """FastAPI dependency for async database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
```

## Health Check

```python
# In shared/api/health.py
from sqlalchemy import text
from shared.infrastructure.database import engine

def check_database_health() -> dict:
    """Check database connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
```
