---
name: scaffold-backend-service
description: Scaffold a backend service with config, data client, models, service layer, and API endpoints following project conventions. Use when creating a new backend domain, adding API endpoints, building a data client, or extending the service layer. Triggers on requests like "create a backend service", "add an API endpoint", "scaffold backend", "new data client", or "add a service".
---

# Scaffold Backend Service

Generate backend components following project ADRs and conventions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `backend_dir` | Root directory for backend code | `backend/app/` |
| `framework` | Backend framework (from ADRs) | `FastAPI`, `Flask`, `Express` |
| `data_source` | Data source type (from ADRs) | `PostgreSQL`, `MongoDB`, `REST API` |
| `di_pattern` | Dependency injection pattern | `singleton`, `factory`, `container` |
| `file` | Target file(s) from the spec | `backend/app/services/orders.py` |

If no spec is provided, detect the backend framework from project ADRs or existing code.

## Decision Tree

1. **New domain?** (e.g., new data source, new feature area)
   - Yes: Follow all 6 steps below
   - No, extending existing domain: Skip to the relevant step

2. **New data source?** (e.g., new external API, new database)
   - Yes: Steps 1-2 (config + client)
   - No: Skip to Step 3

## Step 1: Config Additions

Add settings to `<backend-dir>/core/config.py` (or equivalent config module):

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # ... existing settings ...

    # New domain settings
    NEW_SERVICE_URL: str
    NEW_SERVICE_API_KEY: Optional[str] = None
    NEW_SERVICE_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

Pattern: uppercase with underscores, type-annotated, defaults where sensible, loaded from `.env`.

## Step 2: Data Client (per project DI pattern)

Create `<backend-dir>/core/<client_name>.py`:

```python
"""Client wrapper for <service>."""
from typing import Any, Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)


class MyClient:
    """Wrapper around <service> client."""

    def __init__(self):
        self._client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        try:
            # Initialize the underlying client
            self._client = SomeLibrary(url=settings.NEW_SERVICE_URL)
            logger.info("Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise

    @property
    def client(self):
        if self._client is None:
            self._initialize_client()
        return self._client

    async def execute_query(self, query: str, params: Optional[dict] = None) -> list[dict[str, Any]]:
        try:
            # Execute and return results
            ...
        except Exception as e:
            logger.error(f"Query error: {e}")
            raise


# Singleton instance (per project DI pattern)
_client: Optional[MyClient] = None

def get_my_client() -> MyClient:
    """Get or create the client singleton."""
    global _client
    if _client is None:
        _client = MyClient()
    return _client
```

## Step 3: Response Models

Add models to `<backend-dir>/models/schemas.py` (or equivalent):

```python
from pydantic import BaseModel
from typing import Optional

class MyItemResponse(BaseModel):
    id: str
    name: str
    value: float
    metadata: Optional[dict] = None

class MyListResponse(BaseModel):
    items: list[MyItemResponse]
    total_count: int
```

Pattern: `*Response` suffix, BaseModel, explicit types, Optional with defaults.

## Step 4: Service Layer

Create `<backend-dir>/services/<domain>_service.py`:

```python
"""Service layer for <domain> operations."""
from typing import Any, Optional, List
from datetime import date
import logging

from ..core.<client_module> import get_my_client
from ..core.config import settings

logger = logging.getLogger(__name__)


class MyDomainService:
    """Service for <domain> operations."""

    def __init__(self):
        self.client = get_my_client()

    async def get_items(self, start_date: date, end_date: date, ...) -> list[dict[str, Any]]:
        try:
            results = await self.client.execute_query(...)
            return results
        except Exception as e:
            logger.error(f"Error fetching items: {e}")
            raise


# Singleton factory for dependency injection
_service: Optional[MyDomainService] = None

def get_my_service() -> MyDomainService:
    global _service
    if _service is None:
        _service = MyDomainService()
    return _service
```

## Step 5: API Endpoints

Create `<backend-dir>/api/v1/endpoints/<domain>.py` (or equivalent route module):

```python
"""API endpoints for <domain>."""
from fastapi import APIRouter, Query, HTTPException, Depends
from datetime import date
from typing import List, Optional
import logging

from ....models.schemas import MyItemResponse
from ....services.<domain>_service import get_my_service, MyDomainService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/<domain>", tags=["<domain>"])


@router.get("/items", response_model=List[MyItemResponse])
async def get_items(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    service: MyDomainService = Depends(get_my_service)
):
    """Get items within the specified time period."""
    try:
        if end_date < start_date:
            raise HTTPException(status_code=400, detail="end_date must be after start_date")
        results = await service.get_items(start_date, end_date)
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in items endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

Endpoint pattern: `Query(...)` for required params, `Query(default, ...)` for optional, `Depends()` for service injection, try/except with re-raise for HTTPException.

## Step 6: Register in App Entrypoint

Add the router to the app factory (e.g., `<backend-dir>/main.py`):

```python
from .api.v1.endpoints import health, my_domain

# In create_application():
app.include_router(my_domain.router, prefix=settings.API_PREFIX)
```

## Detailed Patterns

For annotated code examples showing the singleton client, config, service layer, and endpoint patterns, see [references/patterns.md](references/patterns.md).

## Checklist

1. Config in config module — settings class, env vars
2. Client in core/ — per project DI pattern, lazy init
3. Models in models module — typed fields, response suffixes
4. Service in services/ — async methods, singleton factory
5. Endpoints in API module — router, dependency injection, response_model
6. Router registered in app entrypoint with API prefix
