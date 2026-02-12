# Alembic Configuration Template

Templates for database migrations using Alembic.

## Directory Structure

```
backend/
├── alembic/
│   ├── versions/           # Migration files
│   │   └── .gitkeep
│   ├── env.py              # Alembic environment
│   ├── script.py.mako      # Migration template
│   └── README
├── alembic.ini             # Alembic configuration
└── src/
```

## Setup Commands

```bash
# Initialize Alembic (run once)
uv run alembic init alembic

# Create migration
uv run alembic revision --autogenerate -m "description"

# Run migrations
uv run alembic upgrade head

# Rollback one version
uv run alembic downgrade -1

# Show current version
uv run alembic current

# Show migration history
uv run alembic history
```

---

## alembic.ini

**File**: `alembic.ini`

```ini
[alembic]
# Path to migration scripts
script_location = alembic

# Template for new migrations
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Prepend datetime to migration file
prepend_sys_path = .

# Timezone for timestamps
timezone = UTC

# Truncate long migration names
truncate_slug_length = 40

# Set to 'true' to run offline mode
# sqlalchemy.url will be overridden by env.py
sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]
# Format migrations with ruff
hooks = ruff
ruff.type = exec
ruff.executable = ruff
ruff.options = format REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

---

## env.py (Synchronous)

**File**: `alembic/env.py`

```python
"""
IDK: database-migration, alembic-config, schema-versioning

Module: env (Alembic environment)

Responsibility:
- Configure Alembic migration environment
- Register all ORM models for autogeneration
- Provide offline and online migration modes
- Connect to database for schema changes

Key Components:
- run_migrations_offline: generate SQL without database
- run_migrations_online: execute migrations with database

Invariants:
- All models imported and registered
- Database URL from settings
- Metadata from Base class

Related Docs:
- docs/infrastructure/database-migrations.md
"""

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config

from alembic import context

# Import your models' Base
from src.shared.infrastructure.database import Base

# Import all models to register them with Base.metadata
# This is important for autogenerate to detect changes
from src.product_catalog.infrastructure.models import ProductModel
from src.user_management.infrastructure.models import UserModel
# Add other model imports here...

# Import settings for database URL
from src.core.config import settings

# Alembic Config object
config = context.config

# Override sqlalchemy.url with settings
config.set_main_option("sqlalchemy.url", settings.database_url_sync)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    IDK: offline-migration, sql-generation, alembic-offline

    Responsibility:
    - Generate SQL migration script
    - No database connection required
    - Output migration commands

    Invariants:
    - Generates SQL only
    - No database execution
    - Uses URL from config

    Related Docs:
    - docs/infrastructure/migrations.md
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    IDK: online-migration, schema-update, alembic-online

    Responsibility:
    - Execute migrations against database
    - Create database connection
    - Apply schema changes

    Invariants:
    - Connects to database
    - Executes migrations in transaction
    - Uses connection pool

    Related Docs:
    - docs/infrastructure/migrations.md
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## env.py (Async)

**File**: `alembic/env.py` (async version)

```python
"""Alembic async environment configuration."""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import your models' Base
from src.shared.infrastructure.database import Base

# Import all models to register them
from src.product_catalog.infrastructure.models import ProductModel
from src.user_management.infrastructure.models import UserModel
# Add other model imports...

# Import settings
from src.core.config import settings

config = context.config

# Use async database URL
config.set_main_option("sqlalchemy.url", settings.database_url_async)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Execute migrations with connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async online mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## script.py.mako

**File**: `alembic/script.py.mako`

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade database schema."""
    ${downgrades if downgrades else "pass"}
```

---

## Example Migration

**File**: `alembic/versions/20240115_1200_abc123_create_products_table.py`

```python
"""Create products table

Revision ID: abc123def456
Revises:
Create Date: 2024-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "abc123def456"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create products table."""
    op.create_table(
        "products",
        # Identity
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(100), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("type", sa.String(50), nullable=True),

        # Audit
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(255), nullable=True),

        # State
        sa.Column("state", sa.Integer, nullable=False, default=1),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("version", sa.Integer, nullable=False, default=1),

        # Multi-tenancy
        sa.Column("organization_id", sa.String(100), nullable=True),
        sa.Column("project_id", sa.String(100), nullable=True),
        sa.Column("owner", sa.String(255), nullable=True),

        # Product-specific
        sa.Column("sku", sa.String(50), nullable=False, unique=True),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("brand", sa.String(100), nullable=True),
        sa.Column("is_available", sa.Boolean, nullable=False, default=True),
        sa.Column("stock_quantity", sa.Integer, nullable=False, default=0),
        sa.Column("tags", sa.JSON, nullable=True),
    )

    # Create indexes
    op.create_index("ix_products_code", "products", ["code"])
    op.create_index("ix_products_sku", "products", ["sku"])
    op.create_index("ix_products_category", "products", ["category"])
    op.create_index("ix_products_state", "products", ["state"])
    op.create_index("ix_products_organization_id", "products", ["organization_id"])


def downgrade() -> None:
    """Drop products table."""
    op.drop_index("ix_products_organization_id", table_name="products")
    op.drop_index("ix_products_state", table_name="products")
    op.drop_index("ix_products_category", table_name="products")
    op.drop_index("ix_products_sku", table_name="products")
    op.drop_index("ix_products_code", table_name="products")
    op.drop_table("products")
```

---

## pyproject.toml Scripts

Add to `pyproject.toml`:

```toml
[tool.uv.scripts]
migrate = "alembic upgrade head"
migrate-create = "alembic revision --autogenerate -m"
migrate-down = "alembic downgrade -1"
migrate-history = "alembic history"
migrate-current = "alembic current"
```

Usage:

```bash
# Run all pending migrations
uv run migrate

# Create new migration
uv run migrate-create "add_users_table"

# Rollback last migration
uv run migrate-down

# Show history
uv run migrate-history
```

---

## Best Practices

1. **Always review autogenerated migrations** before running
2. **Name migrations descriptively**: `add_users_table`, `add_index_on_email`
3. **Keep migrations small and focused**
4. **Test migrations on a copy of production data**
5. **Include both upgrade() and downgrade()** for rollback capability
6. **Don't modify migrations after they've been applied** to other environments
