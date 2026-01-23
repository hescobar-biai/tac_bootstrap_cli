# Health Endpoint Template

**ADW ID:** 8e6abce7
**Date:** 2026-01-23
**Specification:** specs/issue-133-adw-8e6abce7-sdlc_planner-template-health.md

## Overview

This feature adds a production-ready health check endpoint template for TAC Bootstrap CLI. The template generates health.py files that provide /health endpoints for FastAPI projects, enabling monitoring systems, load balancers, and observability platforms to verify service health and database connectivity.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`
  - Dual-mode template supporting both async and sync SQLAlchemy patterns
  - Configurable via `config.project.async_mode` flag
  - Database connectivity check using lightweight SELECT 1 query
  - Standardized JSON response format (status, version, database, timestamp)

- **Reference Implementation**: `src/shared/api/health.py`
  - Rendered example showing sync mode implementation
  - Comprehensive IDK docstring with monitoring integration examples
  - Demonstrates proper FastAPI router patterns and dependency injection

- **New Directory Structure**: `src/shared/api/`
  - Created to separate API layer from infrastructure layer
  - Follows clean architecture principles (API vs Infrastructure)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`: Jinja2 template with conditional async/sync rendering
- `src/shared/api/health.py`: Rendered reference implementation (sync mode)
- `src/shared/api/__init__.py`: Created for proper Python package structure

### Key Changes

1. **Dual-Mode Template**: Supports both async (AsyncSession) and sync (Session) SQLAlchemy patterns using Jinja2 conditionals (`{% if config.project.async_mode %}`). This allows the template to work with different project configurations.

2. **Database Health Check**: Implements lightweight SELECT 1 query for database connectivity verification (~1-10ms typical). Gracefully handles database failures by returning status='degraded' while maintaining HTTP 200 response.

3. **Standardized Response Format**: Returns JSON with four fields:
   - `status`: 'healthy' or 'degraded'
   - `version`: from `config.project.version` (default: '0.1.0')
   - `database`: 'connected' or 'disconnected'
   - `timestamp`: UTC ISO8601 format with 'Z' suffix

4. **Comprehensive Documentation**: IDK docstring includes usage examples for mounting the router, monitoring integration patterns (Kubernetes probes, AWS ALB, Docker Compose, Datadog), and detailed failure mode documentation.

5. **Security Considerations**: No sensitive information exposed (no DATABASE_URL, hostnames, credentials). Always returns HTTP 200 to prevent information leakage about service state to unauthorized parties.

## How to Use

### For CLI Users (Generating Projects)

When running TAC Bootstrap CLI to generate a new project, the health.py template will be rendered based on your configuration:

```bash
# Generated projects will automatically include health endpoint
# Location: src/shared/api/health.py (or configured path)
```

### Mounting the Health Router

In your generated project's main.py or app factory:

```python
from fastapi import FastAPI
from src.shared.api.health import router as health_router

app = FastAPI()

# Option 1: Mount with prefix (endpoint at /health/health)
app.include_router(health_router)

# Option 2: Mount without prefix (endpoint at /health)
app.include_router(health_router, prefix="")

# Option 3: Custom prefix (endpoint at /api/v1/health)
app.include_router(health_router, prefix="/api/v1")
```

### Testing the Endpoint

```bash
# Test locally
curl http://localhost:8000/health

# Example response (healthy)
{
  "status": "healthy",
  "version": "0.1.0",
  "database": "connected",
  "timestamp": "2026-01-23T10:30:45.123456Z"
}

# Example response (degraded - database down)
{
  "status": "degraded",
  "version": "0.1.0",
  "database": "disconnected",
  "timestamp": "2026-01-23T10:30:47.987654Z"
}
```

## Configuration

### Template Configuration

The template uses these configuration variables from `config.yml`:

```yaml
project:
  name: "your-project-name"
  version: "1.0.0"  # Optional, defaults to "0.1.0"
  async_mode: true  # Optional, defaults to false (sync mode)
```

### Async vs Sync Mode

- **async_mode: true** → Generates async endpoint with `AsyncSession` and `await db.execute()`
- **async_mode: false** → Generates sync endpoint with `Session` and `db.execute()`

The template automatically adapts imports and function signatures based on this setting.

## Monitoring Integration

### Kubernetes Probes

```yaml
# Liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# Readiness probe
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 2
  failureThreshold: 2
```

### AWS Application Load Balancer

```
Target: HTTP:8000/health
Healthy threshold: 2
Unhealthy threshold: 3
Timeout: 5 seconds
Interval: 30 seconds
Success codes: 200
```

### Docker Compose

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Testing

The template follows TAC Bootstrap's testing conventions:

```bash
# Run tests from CLI directory
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "health"

# Verify template is valid Jinja2
cd tac_bootstrap_cli && uv run python -c "from jinja2 import Template; Template(open('tac_bootstrap/templates/shared/health.py.j2').read())"

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking (may have partial coverage)
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

1. **Always HTTP 200**: The endpoint returns HTTP 200 even in degraded state. The `status` field indicates actual health. This design:
   - Prevents false positive alerts in monitoring systems
   - Follows industry best practices for health endpoints
   - Allows load balancers to distinguish between service down vs. degraded

2. **Minimal Checks**: Only database connectivity is checked via SELECT 1. Additional checks (Redis, external APIs) are intentionally excluded to:
   - Keep response time <100ms
   - Avoid cascading failures
   - Simplify debugging

3. **No Timeouts**: Relies on database driver defaults. SELECT 1 is inherently fast (~1-10ms), explicit timeouts add complexity without benefit.

4. **Dual Creation Pattern**: Both template and reference implementation are maintained. The reference implementation (`src/shared/api/health.py`) serves as documentation for template users.

### Architecture Notes

- **New API Layer**: Introduced `src/shared/api/` directory to separate API concerns from infrastructure (`src/shared/infrastructure/`). This follows clean architecture principles.

- **Template Location**: Template stored in `tac_bootstrap_cli/tac_bootstrap/templates/shared/` alongside other shared templates (database.py.j2, dependencies.py.j2).

### Limitations

- The reference implementation uses sync mode (Session) since tac-bootstrap itself has `framework="none"` and doesn't run as a FastAPI service
- Template assumes database.py exists with get_db() function (dependency on prior templates)
- No additional health checks (cache, message queue, external APIs) - these can be added by users if needed

### Future Enhancements

Potential improvements for future iterations:
- Add optional Redis connectivity check
- Include custom health check callbacks
- Add response caching (short TTL)
- Provide configurable timeout values
- Add detailed metrics endpoint (/health/detailed)
