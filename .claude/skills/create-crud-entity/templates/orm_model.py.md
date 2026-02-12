# ORM Model Template

Template for creating SQLAlchemy ORM models for database persistence.

## Usage

Replace placeholders:
- `{{EntityName}}` - PascalCase entity name (e.g., `Product`, `Supplier`)
- `{{entity_name}}` - snake_case for table name (e.g., `product`, `supplier`)
- `{{entity_type}}` - lowercase entity type string (e.g., `"product"`, `"supplier"`)
- `{{fields}}` - Entity-specific column definitions

## Template

```python
"""
IDK: orm-model, persistence, {{entity_name}}-table

Module: models

Responsibility:
- Map {{EntityName}} domain model to database table
- Define column types and constraints
- Configure indexes for query performance
- Support CRUD operations via SQLAlchemy

Invariants:
- All Entity base fields present
- Primary key is 'id' (String, UUID)
- Table name follows snake_case convention
- Audit fields (created_at, updated_at) are non-nullable
- State field uses integer: 0=inactive, 1=active, 2=deleted

Related Docs:
- docs/{{capability}}/infrastructure/models.md
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, UTC

from shared.infrastructure.database import Base


class {{EntityName}}Model(Base):
    """
    IDK: orm-model, persistence, {{entity_name}}-table

    Responsibility:
    - Persist {{EntityName}} entities to database
    - Map domain fields to table columns
    - Enforce database-level constraints

    Invariants:
    - id is UUID primary key
    - code is unique per entity type
    - state values: 0 (inactive), 1 (active), 2 (deleted)
    - created_at and updated_at always populated
    - version increments on each update

    Table: {{entity_name}}

    Indexes:
    - ix_{{entity_name}}_code: for code lookups
    - ix_{{entity_name}}_state: for filtering by state
    - ix_{{entity_name}}_organization_id: for org filtering
    - ix_{{entity_name}}_owner: for ownership queries

    Related Docs:
    - docs/{{capability}}/infrastructure/persistence.md
    """

    __tablename__ = "{{entity_name}}"

    # ================================================
    # Base Entity Fields (from Entity base class)
    # ================================================

    # Primary identifier
    id = Column(String, primary_key=True, index=True)

    # Business identifiers
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    type = Column(String(50), nullable=False, default="{{entity_type}}")

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Audit trail
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    # State management
    state = Column(Integer, nullable=False, default=1, index=True)  # 0=inactive, 1=active, 2=deleted
    status = Column(String(50), nullable=True)
    version = Column(Integer, nullable=False, default=1)

    # Multi-tenancy / Organization
    organization_id = Column(String, nullable=True, index=True)
    project_id = Column(String, nullable=True)
    owner = Column(String, nullable=True, index=True)

    # Authorization fields (for authorized entities)
    group_path = Column(String, nullable=True, index=True)  # For hierarchical group access

    # ================================================
    # Entity-Specific Fields
    # ================================================

    {{fields}}

    # ================================================
    # Indexes for Performance
    # ================================================

    __table_args__ = (
        # Composite index for common queries
        Index('ix_{{entity_name}}_org_state', 'organization_id', 'state'),
        Index('ix_{{entity_name}}_owner_state', 'owner', 'state'),
        # Add custom indexes here
    )
```

## Example: Product ORM Model

```python
"""
IDK: orm-model, persistence, product-table

Module: models

Responsibility:
- Map Product domain model to database table
- Define column types and constraints for product data
- Configure indexes for product queries
- Support CRUD operations for products

Invariants:
- id is UUID primary key
- code and sku are unique
- state values: 0 (inactive), 1 (active), 2 (deleted)
- unit_price and stock_quantity are non-negative
- tags stored as JSON array

Table: product

Indexes:
- ix_product_code: for code lookups
- ix_product_sku: for SKU lookups
- ix_product_category: for category filtering
- ix_product_state: for filtering by state
- ix_product_org_state: composite for org queries

Related Docs:
- docs/product_catalog/infrastructure/persistence.md
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Index
from datetime import datetime, UTC

from shared.infrastructure.database import Base


class ProductModel(Base):
    """
    IDK: orm-model, persistence, product-table

    Responsibility:
    - Persist Product entities to database
    - Map product domain fields to table columns
    - Enforce database-level constraints for products

    Invariants:
    - id is UUID primary key
    - code is unique globally
    - sku is unique globally
    - state: 0=inactive, 1=active, 2=deleted
    - unit_price >= 0
    - stock_quantity >= 0
    - tags stored as JSON array (PostgreSQL) or TEXT (SQLite)

    Table: product

    Columns:
    - Base: id, code, name, description, type
    - Base: created_at, updated_at, created_by, updated_by
    - Base: state, status, version
    - Base: organization_id, project_id, owner, group_path
    - Product: sku, unit_price, category, brand, is_available, stock_quantity, tags

    Related Docs:
    - docs/product_catalog/domain/product.md
    - docs/product_catalog/infrastructure/persistence.md
    """

    __tablename__ = "product"

    # ================================================
    # Base Entity Fields
    # ================================================

    id = Column(String, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    type = Column(String(50), nullable=False, default="product")

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    state = Column(Integer, nullable=False, default=1, index=True)
    status = Column(String(50), nullable=True)
    version = Column(Integer, nullable=False, default=1)

    organization_id = Column(String, nullable=True, index=True)
    project_id = Column(String, nullable=True)
    owner = Column(String, nullable=True, index=True)
    group_path = Column(String, nullable=True, index=True)

    # ================================================
    # Product-Specific Fields
    # ================================================

    sku = Column(String(50), unique=True, nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    brand = Column(String(100), nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    tags = Column(JSON, nullable=True)  # Stored as JSON array

    # ================================================
    # Indexes
    # ================================================

    __table_args__ = (
        Index('ix_product_org_state', 'organization_id', 'state'),
        Index('ix_product_owner_state', 'owner', 'state'),
        Index('ix_product_category_state', 'category', 'state'),
        Index('ix_product_available', 'is_available', 'state'),
    )
```

## Field Type Reference

| Domain Type | SQLAlchemy Type | Database Type | Notes |
|-------------|----------------|---------------|-------|
| `str` | `String` | VARCHAR | Default length 255 |
| `str` (fixed) | `String(100)` | VARCHAR(100) | Specify max length |
| `int` | `Integer` | INTEGER | Whole numbers |
| `float` | `Float` | FLOAT/DOUBLE | Decimal numbers |
| `bool` | `Boolean` | BOOLEAN | True/false |
| `datetime` | `DateTime` | TIMESTAMP | Date and time |
| `list[str]` | `JSON` | JSON/JSONB | Arrays (use TEXT for SQLite) |
| `dict` | `JSON` | JSON/JSONB | Objects |
| `str` (UUID) | `String` or `UUID` | VARCHAR or UUID | Use PostgreSQL UUID type if available |

## Common Column Patterns

### Unique Constraints

```python
# Single column unique
code = Column(String(100), unique=True, nullable=False)

# Multiple column unique (composite)
__table_args__ = (
    UniqueConstraint('organization_id', 'code', name='uq_org_code'),
)
```

### Nullable vs Required

```python
# Required field
name = Column(String(255), nullable=False)

# Optional field
description = Column(String, nullable=True)

# Required with default
is_active = Column(Boolean, nullable=False, default=True)
```

### Indexes

```python
# Single column index
code = Column(String(100), index=True)

# Composite index (in __table_args__)
__table_args__ = (
    Index('ix_entity_org_state', 'organization_id', 'state'),
)
```

### Foreign Keys (Cross-Capability References)

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Foreign key to another entity
category_id = Column(String, ForeignKey('category.id'), nullable=True)

# Relationship (optional, for eager loading)
category = relationship("CategoryModel", lazy="joined")
```

### JSON Fields

```python
# For PostgreSQL (native JSON support)
from sqlalchemy.dialects.postgresql import JSONB

metadata = Column(JSONB, nullable=True)
tags = Column(JSONB, nullable=True)

# For SQLite compatibility (store as TEXT)
from sqlalchemy import JSON

metadata = Column(JSON, nullable=True)  # SQLAlchemy handles serialization
```

### Enum Fields

```python
from sqlalchemy import Enum
import enum

class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DISCONTINUED = "discontinued"

status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.DRAFT)
```

### Timestamps with Timezone

```python
from datetime import datetime, UTC

# Auto-set on create
created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

# Auto-update on modify
updated_at = Column(
    DateTime,
    nullable=False,
    default=lambda: datetime.now(UTC),
    onupdate=lambda: datetime.now(UTC)
)
```

## Naming Conventions

Follow these naming conventions for consistency:

| Element | Convention | Example |
|---------|-----------|---------|
| Class name | `{Entity}Model` | `ProductModel` |
| Table name | `snake_case` | `product` |
| Column names | `snake_case` | `unit_price` |
| Index names | `ix_{table}_{column}` | `ix_product_code` |
| Constraint names | `uq_{table}_{column}` | `uq_product_sku` |
| Foreign keys | `fk_{table}_{column}_{ref_table}` | `fk_product_category_id_category` |

## Best Practices

1. **Always define __tablename__**: Explicit is better than implicit
2. **Use indexes on filter columns**: Columns used in WHERE clauses
3. **Set nullable explicitly**: Don't rely on defaults
4. **Validate in domain layer**: Database constraints are safety net
5. **Use UTC for timestamps**: Avoid timezone issues
6. **Keep JSON fields simple**: Complex queries on JSON are slow
7. **Add composite indexes**: For common multi-column queries
8. **Document constraints in docstrings**: Help future developers

## Anti-Patterns to Avoid

**Don't use ORM relationships for vertical slices:**
```python
# BAD: Creates tight coupling between slices
orders = relationship("OrderModel", back_populates="product")

# GOOD: Use IDs and repository queries
# product_id is enough, query via repository when needed
```

**Don't put business logic in models:**
```python
# BAD: Business logic in ORM model
def calculate_total(self):
    return self.unit_price * self.quantity

# GOOD: Business logic in domain entity or service
```

**Don't use database defaults for complex logic:**
```python
# BAD: Complex default in database
code = Column(String, default=lambda: generate_complex_code())

# GOOD: Set in service layer before saving
```

## Testing ORM Models

```python
# tests/unit/product_catalog/test_models.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.infrastructure.database import Base
from product_catalog.infrastructure.models import ProductModel


@pytest.fixture
def db_session():
    """Create in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_product(db_session):
    """Test creating a product model."""
    product = ProductModel(
        id="test-id",
        code="PROD-001",
        name="Test Product",
        sku="SKU-001",
        unit_price=99.99,
        state=1,
    )
    db_session.add(product)
    db_session.commit()

    retrieved = db_session.query(ProductModel).filter_by(code="PROD-001").first()
    assert retrieved is not None
    assert retrieved.name == "Test Product"
    assert retrieved.unit_price == 99.99


def test_unique_code_constraint(db_session):
    """Test code uniqueness constraint."""
    from sqlalchemy.exc import IntegrityError

    product1 = ProductModel(id="id1", code="PROD-001", name="Product 1", sku="SKU1", unit_price=10)
    product2 = ProductModel(id="id2", code="PROD-001", name="Product 2", sku="SKU2", unit_price=20)

    db_session.add(product1)
    db_session.commit()

    db_session.add(product2)
    with pytest.raises(IntegrityError):
        db_session.commit()
```

## Migration Generation

After creating the ORM model, generate a database migration:

```bash
# Generate migration
uv run alembic revision --autogenerate -m "add_{{entity_name}}_table"

# Review the generated migration file in alembic/versions/

# Apply migration
uv run alembic upgrade head
```

See [alembic.py.md](../shared/alembic.py.md) for migration setup.
