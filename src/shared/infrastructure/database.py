# Reference implementation - generated from database.py.j2 template
# This file serves as documentation for the database.py template output
# Not used by the CLI itself (tac-bootstrap has framework="none")

"""
IDK: database-session, connection-management, orm-configuration

Module: database

Responsibility:
- Centralized database session management and configuration
- Provide database engine with connection pooling
- Export declarative Base for ORM model inheritance
- Provide get_db() generator for FastAPI dependency injection
- Handle session lifecycle with proper cleanup
- Support both synchronous and asynchronous SQLAlchemy patterns

Key Components:
- DATABASE_URL: Connection string from environment with fallback chain
- engine: SQLAlchemy engine with optional connection pool configuration
- SessionLocal: Session factory for creating database sessions
- Base: Declarative base class for ORM models
- get_db(): Generator function for dependency injection with cleanup

Invariants:
- DATABASE_URL priority: os.getenv('DATABASE_URL') → config.project.database_url → 'sqlite:///./app.db'
- Session cleanup happens in finally block (guaranteed)
- get_db() yields session, ensures cleanup even on exception
- Connection pool settings available as commented examples
- Async mode uses AsyncSession and async_sessionmaker
- Sync mode uses Session and sessionmaker

Usage Examples:

```python
# Import database components
from src.shared.infrastructure.database import Base, get_db, engine
from sqlalchemy.orm import Session
from fastapi import Depends

# Define ORM model using Base
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

# Use get_db() in FastAPI routes with dependency injection
@router.get("/products/{product_id}")
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

# Create database tables (typically in main.py or startup script)
from src.shared.infrastructure.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)

# Use in repository layer
class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: str) -> ProductModel | None:
        return self.session.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
```

Collaborators:
- SQLAlchemy Engine: Database connection management
- SQLAlchemy Session: Transaction and query execution
- ORM Models: Entities that inherit from Base
- FastAPI: Dependency injection system uses get_db()

Failure Modes:
- ConnectionError: Database URL invalid or database unreachable
- OperationalError: Database connection timeout or pool exhausted
- ProgrammingError: SQL syntax errors in queries
- All exceptions propagate to FastAPI's exception handlers

Related Docs:
- docs/shared/infrastructure/database-setup.md
- docs/shared/infrastructure/session-management.md
- ai_docs/doc/create-crud-entity/
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Database URL with environment variable priority chain
# Priority: DATABASE_URL env var → config.project.database_url → hardcoded sqlite default
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./app.db"

# Create SQLAlchemy engine with optional connection pool settings
engine = create_engine(
    DATABASE_URL,
    # Uncomment for custom connection pool configuration:
    # pool_size=5,
    # max_overflow=10,
    # pool_pre_ping=True,  # Enable connection health checks
    # pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False,  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Declarative Base for ORM models
# All models should inherit from this Base class
Base = declarative_base()

def get_db() -> Session:
    """
    IDK: dependency-injection, session-management, cleanup

    Responsibility:
    - Provide database session for FastAPI dependency injection
    - Ensure session cleanup in finally block
    - Yield session for use in route handlers
    - Handle session lifecycle automatically

    Invariants:
    - Session is always closed, even on exception
    - Each request gets its own session
    - Finally block guarantees cleanup

    Usage Pattern:
    - Used with FastAPI Depends() for automatic injection
    - Session is closed after request completes
    - Supports sync route handlers

    Example:

    ```python
    from fastapi import Depends
    from sqlalchemy.orm import Session

    @router.get("/products")
    def list_products(db: Session = Depends(get_db)):
        products = db.query(ProductModel).all()
        return products
    ```

    Yields:
    - Session: Database session for synchronous operations

    Related Docs:
    - docs/shared/infrastructure/dependency-injection.md
    - docs/shared/infrastructure/session-management.md
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
