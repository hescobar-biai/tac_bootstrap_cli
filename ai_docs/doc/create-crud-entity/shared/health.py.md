# Health Check Template

Templates for health and readiness endpoints.

## Overview

Health checks enable:
- **Liveness**: Is the application running?
- **Readiness**: Is the application ready to serve traffic?
- **Dependencies**: Are external services available?

## Directory Structure

```
src/
├── shared/
│   └── api/
│       └── health.py       # Health check router
└── main.py                 # Register health router
```

---

## Health Router

**File**: `src/shared/api/health.py`

```python
"""
IDK: health-check, monitoring, liveness-probe

Module: health

Responsibility:
- Provide health check endpoints
- Monitor service dependencies
- Support liveness and readiness probes
- Return service status

Key Components:
- health_check: full health check with dependencies
- liveness: simple liveness probe
- readiness: readiness probe for load balancers

Invariants:
- Health checks return HTTP 200 when healthy
- Dependency status included in response
- Probes suitable for Kubernetes/Docker

Related Docs:
- docs/shared/api/health-checks.md
"""

from datetime import datetime, UTC
from enum import Enum

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config import settings
from shared.infrastructure.database import get_db

router = APIRouter(tags=["Health"])


class HealthStatus(str, Enum):
    """Health status values."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class DependencyHealth(BaseModel):
    """Health status of a dependency."""

    name: str
    status: HealthStatus
    latency_ms: float | None = None
    message: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: HealthStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    version: str = Field(default=settings.app_version)
    environment: str = Field(default=settings.environment)
    dependencies: list[DependencyHealth] = Field(default_factory=list)


class ReadinessResponse(BaseModel):
    """Readiness check response."""

    ready: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    checks: dict[str, bool] = Field(default_factory=dict)


async def check_database(db: Session) -> DependencyHealth:
    """Check database connectivity."""
    import time

    start = time.perf_counter()
    try:
        db.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="database",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2),
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            latency_ms=round(latency, 2),
            message=str(e),
        )


async def check_redis() -> DependencyHealth:
    """Check Redis connectivity (if configured)."""
    import time

    if not settings.redis_url:
        return DependencyHealth(
            name="redis",
            status=HealthStatus.HEALTHY,
            message="Not configured",
        )

    start = time.perf_counter()
    try:
        import redis

        r = redis.from_url(settings.redis_url)
        r.ping()
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="redis",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2),
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            latency_ms=round(latency, 2),
            message=str(e),
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check application health and dependencies",
)
async def health_check(
    db: Session = Depends(get_db),
) -> HealthResponse:
    """
    Health check endpoint.

    Returns:
    - **status**: Overall health status
    - **version**: Application version
    - **environment**: Deployment environment
    - **dependencies**: Status of external dependencies
    """
    dependencies = []

    # Check database
    db_health = await check_database(db)
    dependencies.append(db_health)

    # Check Redis (if configured)
    redis_health = await check_redis()
    if redis_health.message != "Not configured":
        dependencies.append(redis_health)

    # Determine overall status
    unhealthy = any(d.status == HealthStatus.UNHEALTHY for d in dependencies)
    degraded = any(d.status == HealthStatus.DEGRADED for d in dependencies)

    if unhealthy:
        overall_status = HealthStatus.UNHEALTHY
    elif degraded:
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY

    return HealthResponse(
        status=overall_status,
        dependencies=dependencies,
    )


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    description="Simple liveness check for container orchestration",
)
async def liveness() -> dict[str, str]:
    """
    Liveness probe for Kubernetes/Docker.

    Returns 200 if application is running.
    Used by container orchestrators to determine if container should be restarted.
    """
    return {"status": "alive"}


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    summary="Readiness probe",
    description="Check if application is ready to serve traffic",
)
async def readiness(
    db: Session = Depends(get_db),
) -> ReadinessResponse:
    """
    Readiness probe for Kubernetes/Docker.

    Returns ready=true only if all critical dependencies are available.
    Used by load balancers to determine if traffic should be sent to this instance.
    """
    checks = {}

    # Database check
    db_health = await check_database(db)
    checks["database"] = db_health.status == HealthStatus.HEALTHY

    # Add more critical dependency checks here
    # checks["cache"] = await check_cache_ready()
    # checks["queue"] = await check_queue_ready()

    ready = all(checks.values())

    return ReadinessResponse(
        ready=ready,
        checks=checks,
    )


@router.get(
    "/health/info",
    summary="Application info",
    description="Get application metadata",
)
async def info() -> dict:
    """
    Application information endpoint.

    Returns metadata about the running application.
    """
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "python_version": "3.12",
        "api_prefix": settings.api_v1_prefix,
    }
```

---

## Async Version

**File**: `src/shared/api/health_async.py`

```python
"""Async health check endpoints."""

from datetime import datetime, UTC

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from shared.infrastructure.database_async import get_async_db

router = APIRouter(tags=["Health"])


async def check_database_async(db: AsyncSession) -> dict:
    """Check database connectivity asynchronously."""
    import time

    start = time.perf_counter()
    try:
        await db.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        return {
            "name": "database",
            "status": "healthy",
            "latency_ms": round(latency, 2),
        }
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return {
            "name": "database",
            "status": "unhealthy",
            "latency_ms": round(latency, 2),
            "message": str(e),
        }


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_async_db),
) -> dict:
    """Async health check."""
    db_health = await check_database_async(db)

    status = "healthy" if db_health["status"] == "healthy" else "unhealthy"

    return {
        "status": status,
        "timestamp": datetime.now(UTC).isoformat(),
        "version": settings.app_version,
        "environment": settings.environment,
        "dependencies": [db_health],
    }


@router.get("/health/live")
async def liveness() -> dict:
    """Liveness probe."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(
    db: AsyncSession = Depends(get_async_db),
) -> dict:
    """Readiness probe."""
    db_health = await check_database_async(db)
    ready = db_health["status"] == "healthy"

    return {
        "ready": ready,
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": {"database": ready},
    }
```

---

## Register in Main

**File**: `src/main.py` (updated)

```python
"""Application entry point."""

from fastapi import FastAPI

from core.config import settings
from shared.api.health import router as health_router

# Import capability routers
from product_catalog.api.routes import router as product_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Health endpoints (no prefix)
app.include_router(health_router)

# API routes
app.include_router(product_router, prefix=settings.api_v1_prefix)
```

---

## Kubernetes Configuration

**File**: `k8s/deployment.yaml` (example)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: my-api:latest
          ports:
            - containerPort: 8000

          # Liveness probe - restart if fails
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3

          # Readiness probe - remove from load balancer if fails
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 3

          # Startup probe - for slow starting containers
          startupProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 0
            periodSeconds: 5
            failureThreshold: 30
```

---

## Docker Compose Health Check

**File**: `docker-compose.yml` (example)

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Response Examples

### Health Check Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "version": "1.0.0",
  "environment": "production",
  "dependencies": [
    {
      "name": "database",
      "status": "healthy",
      "latency_ms": 2.34
    },
    {
      "name": "redis",
      "status": "healthy",
      "latency_ms": 0.89
    }
  ]
}
```

### Readiness Response

```json
{
  "ready": true,
  "timestamp": "2024-01-15T12:00:00Z",
  "checks": {
    "database": true
  }
}
```

### Unhealthy Response

```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "version": "1.0.0",
  "environment": "production",
  "dependencies": [
    {
      "name": "database",
      "status": "unhealthy",
      "latency_ms": 5000.00,
      "message": "Connection timeout"
    }
  ]
}
```
