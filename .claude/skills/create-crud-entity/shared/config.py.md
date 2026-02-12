# Configuration Template

Application settings using Pydantic Settings. This file should be placed at `src/core/config.py`.

## Template

```python
"""
IDK: configuration, settings, environment-variables

Module: config

Responsibility:
- Provide application configuration
- Load settings from environment variables
- Validate configuration with Pydantic
- Support environment-specific settings

Key Components:
- Settings: application settings class
- get_settings: cached settings factory

Invariants:
- Settings loaded from .env file
- All values validated with Pydantic
- Settings cached for performance
- Secrets use SecretStr type

Related Docs:
- docs/core/configuration.md
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    IDK: configuration, pydantic-settings, env-config

    Responsibility:
    - Define application configuration schema
    - Load and validate environment variables
    - Provide type-safe settings access
    - Support multiple environments

    Invariants:
    - All settings loaded from environment
    - Values validated by Pydantic
    - Secrets use SecretStr type
    - Defaults provided for development

    Collaborators:
    - Pydantic BaseSettings: validation engine
    - Environment variables: configuration source

    Related Docs:
    - docs/core/configuration.md
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="My API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment",
    )
    debug: bool = Field(default=False, description="Debug mode")

    # API
    api_v1_prefix: str = Field(default="/api/v1", description="API version prefix")
    allowed_hosts: list[str] = Field(
        default=["*"],
        description="Allowed hosts for CORS",
    )

    # Security
    secret_key: SecretStr = Field(
        default=SecretStr("change-me-in-production"),
        description="Secret key for JWT and encryption",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration in minutes",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration in days",
    )

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/app",
        description="PostgreSQL connection URL",
    )
    database_pool_size: int = Field(default=5, ge=1, le=100)
    database_max_overflow: int = Field(default=10, ge=0, le=100)
    database_echo: bool = Field(
        default=False,
        description="Echo SQL queries (debug)",
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["*"])
    cors_allow_headers: list[str] = Field(default=["*"])

    # Pagination
    default_page_size: int = Field(default=20, ge=1, le=100)
    max_page_size: int = Field(default=100, ge=1, le=1000)

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )

    # Optional integrations
    redis_url: str | None = Field(
        default=None,
        description="Redis URL for caching",
    )
    sentry_dsn: str | None = Field(
        default=None,
        description="Sentry DSN for error tracking",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("allowed_hosts", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        """Parse allowed hosts from comma-separated string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def database_url_sync(self) -> str:
        """Get sync database URL (for Alembic)."""
        return str(self.database_url)

    @property
    def database_url_async(self) -> str:
        """Get async database URL (for async SQLAlchemy)."""
        url = str(self.database_url)
        return url.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache
def get_settings() -> Settings:
    """
    IDK: settings-factory, caching, singleton

    Responsibility:
    - Provide cached settings instance
    - Ensure single settings object
    - Load from environment on first call

    Invariants:
    - Returns same instance (cached)
    - Settings loaded once
    - Thread-safe via lru_cache

    Outputs:
    - Settings: application settings

    Related Docs:
    - docs/core/configuration.md
    """
    return Settings()


# Convenience alias
settings = get_settings()
```

## Directory Setup

```
src/
└── core/
    ├── __init__.py
    ├── config.py        # <-- This file
    └── dependencies.py
```

**`src/core/__init__.py`**:
```python
"""Core application configuration and dependencies."""
from .config import Settings, get_settings, settings

__all__ = ["Settings", "get_settings", "settings"]
```

## Environment File

Create `.env` file in project root:

```bash
# .env

# Application
APP_NAME=My API
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

# API
API_V1_PREFIX=/api/v1

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO

# Optional
# REDIS_URL=redis://localhost:6379/0
# SENTRY_DSN=https://xxx@sentry.io/xxx
```

Create `.env.example` (commit to git):

```bash
# .env.example

# Application
APP_NAME=My API
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=false

# API
API_V1_PREFIX=/api/v1

# Security
SECRET_KEY=change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false

# CORS
CORS_ORIGINS=http://localhost:3000

# Logging
LOG_LEVEL=INFO

# Optional
# REDIS_URL=redis://localhost:6379/0
# SENTRY_DSN=
```

## Usage in Application

### Main Application

```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)
```

### Database Connection

```python
# src/shared/infrastructure/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    settings.database_url_sync,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Async Database Connection

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
```

### Dependency Injection

```python
# src/core/dependencies.py
from core.config import get_settings, Settings

def get_config() -> Settings:
    """Dependency for injecting settings."""
    return get_settings()
```

## Environment-Specific Configuration

```python
# For environment-specific behavior
from core.config import settings

if settings.is_production:
    # Production-only configuration
    pass
elif settings.is_development:
    # Development-only configuration
    pass
```
