# Feature: Template health.py - FastAPI Health Check Endpoint

## Metadata
issue_number: `133`
adw_id: `8e6abce7`
issue_json: `{"number":133,"title":"Tarea 1.10: Template health.py","body":"/feature\n/adw_sdlc_zte_iso\n/adw_id feature_1.10\n\n**Tipo**: feature\n**Ganancia**: Endpoint /health listo para monitoreo. Verifica conexion a BD y reporta version de la app.\n\n**Instrucciones para el agente**:\n\n1. Crear template: tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2\n2. Crear renderizado en raiz: src/shared/api/health.py\n2. Contenido:\n   - Router FastAPI con prefix=\"\" o \"/health\"\n   - GET /health retorna:\n     {\n       \"status\": \"healthy\",\n       \"version\": \"{{ config.project.version | default('0.1.0') }}\",\n       \"database\": \"connected\" | \"disconnected\",\n       \"timestamp\": \"ISO8601\"\n     }\n   - Intenta hacer SELECT 1 a la BD para verificar conexion\n   - Si falla la BD, retorna status \"degraded\" pero HTTP 200\n\n**Criterios de aceptacion**:\n- Endpoint responde en <100ms\n- No expone informacion sensible\n- Reporta estado de la BD"}`

## Feature Description
Create a health check endpoint template for TAC Bootstrap CLI that generates health.py files for FastAPI projects. This module provides a production-ready /health endpoint for monitoring and observability systems. The endpoint performs lightweight checks on database connectivity and reports application version, enabling operations teams to monitor service health without exposing sensitive information.

The template uses async/await patterns with FastAPI dependency injection (get_db from database.py), performs a fast SELECT 1 database check, and returns HTTP 200 with a status field indicating 'healthy' or 'degraded'. It follows the Dual Creation Pattern, creating both a Jinja2 template for CLI generation and a rendered reference implementation in the project root.

## User Story
As a developer using TAC Bootstrap CLI
I want to generate health.py files with a production-ready /health endpoint
So that my projects have monitoring endpoints that verify database connectivity and report version information for observability platforms

## Problem Statement
Modern cloud-native applications require health check endpoints for:
- Load balancer health checks (AWS ALB, GCP Load Balancer, Kubernetes probes)
- Service mesh readiness checks (Istio, Linkerd)
- Monitoring and alerting systems (Datadog, New Relic, Prometheus)
- DevOps visibility into service availability and degradation
- Version tracking for deployment verification

Currently, developers must manually implement health endpoints, leading to:
- Inconsistent response formats across services
- Missing database connectivity checks
- Over-complicated health logic with excessive checks
- Security risks from exposing sensitive information
- Slow response times that trigger false positives in monitoring

## Solution Statement
Create a Jinja2 template (`health.py.j2`) that generates a health check API module. The template:
- Creates a FastAPI router with prefix='/health'
- Implements async GET /health endpoint that returns HTTP 200 always
- Performs SELECT 1 database check using get_db dependency from database.py
- Returns JSON with status ('healthy'/'degraded'), version from config, database state ('connected'/'disconnected'), and ISO8601 timestamp
- Uses async/await with AsyncSession pattern (or sync Session as fallback)
- Completes in <100ms typical case (SELECT 1 is ~1-10ms)
- Exposes no sensitive information (no hostnames, credentials, internal IPs)
- Includes IDK docstring with usage examples and monitoring integration patterns

Following the Dual Creation Pattern, also render a reference implementation in `src/shared/api/health.py` (note new directory structure) with explanatory comments indicating it's a reference example for a CLI generator project.

## Relevant Files
Files necessary for implementing the feature:

### Existing Files for Pattern Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - For understanding get_db dependency pattern and async/sync conditional rendering
- `src/shared/infrastructure/database.py` - To verify get_db function signature and understand session lifecycle
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2` - For understanding FastAPI Depends() patterns
- `config.yml` - Project configuration with values for rendering (project.name, project.version, paths.app_root)

### Existing Reference Implementations
- `src/shared/infrastructure/database.py` - Contains get_db function for dependency injection
- `src/shared/infrastructure/dependencies.py` - Shows FastAPI dependency patterns

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` - Jinja2 template for health check endpoint (PRIMARY)
- `src/shared/api/health.py` - Rendered reference implementation in project root (NEW DIRECTORY: src/shared/api/)

## Implementation Plan

### Phase 1: Research and Pattern Analysis
- Read database.py template to understand get_db dependency (sync vs async)
- Review dependencies.py template to understand FastAPI Depends() usage patterns
- Review config.yml to identify version field location and default values
- Verify FastAPI router patterns (prefix, tags, response_model)

### Phase 2: Create Template
- Create `health.py.j2` with:
  - IDK docstring following existing template format with monitoring integration examples
  - FastAPI router with prefix='/health' (users can mount at different path if needed)
  - Async GET /health endpoint using async def and AsyncSession (with sync fallback in comments)
  - Database check using `await session.execute(text("SELECT 1"))` pattern
  - JSON response with status, version (from config), database, timestamp fields
  - HTTP 200 always (status field indicates 'healthy'/'degraded')
  - Exception handling for database errors (catch all, set database='disconnected', status='degraded')
  - ISO8601 timestamp using datetime.utcnow().isoformat() + 'Z'
  - No timeouts (rely on database driver defaults, SELECT 1 is inherently fast)
  - Clear usage examples showing how to mount router in main.py
- Focus on async patterns with commented sync alternative
- Keep simple: no extra checks, no configuration complexity

### Phase 3: Render Reference Implementation
- Create directory `src/shared/api/` if it doesn't exist
- Render the template using values from config.yml:
  - `config.project.name` → "tac-bootstrap"
  - `config.project.version` → default "0.1.0" (likely no version in config.yml)
  - Async mode preference (based on database.py async mode setting)
- Add header comment: "# Reference implementation - generated from health.py.j2 template"
- Add clarifying comment: "# This file serves as documentation for the health.py template output"
- Add clarifying comment: "# Not used by the CLI itself (tac-bootstrap has framework='none')"
- Save to `src/shared/api/health.py`

### Phase 4: Validation
- Verify template file exists and is valid Jinja2
- Verify rendered file exists with correct content
- Check that both files follow existing code patterns (IDK docstring, import organization)
- Verify database dependency injection is correct
- Verify response format matches specification (status, version, database, timestamp)
- Validate HTTP 200 behavior for both healthy and degraded states
- Confirm no sensitive information is exposed
- Verify async patterns are correct (async def, await, AsyncSession)

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Research Existing Patterns
- Read `src/shared/infrastructure/database.py` to understand:
  - get_db function signature (async generator returning AsyncSession or sync Session)
  - Import path for dependency injection
  - Whether async or sync mode is used
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` to understand:
  - How async mode is conditionally rendered with `{% if config.project.async_mode %}`
  - IDK docstring format and structure
  - Session lifecycle patterns (try/finally, context manager)
- Read `config.yml` to understand:
  - Project configuration structure
  - Whether project.version field exists
  - Default values for version

### Task 2: Create Jinja2 Template
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/shared/` if it doesn't exist (it should already exist from prior tasks)
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` with:
  - Comprehensive IDK docstring explaining:
    - Module purpose: production-ready health check endpoint
    - Key components: router, GET /health endpoint, database check, response format
    - Responsibility: verify service health, database connectivity, report version
    - Invariants: always HTTP 200, status field indicates health, completes <100ms typical
    - Usage examples showing how to mount router in FastAPI app
    - Monitoring integration patterns (load balancer, Kubernetes probes, Datadog)
    - Collaborators: FastAPI router, database.py get_db, SQLAlchemy session
    - Failure modes: database unreachable → status='degraded', still HTTP 200
  - Imports:
    ```python
    from datetime import datetime
    from fastapi import APIRouter, Depends
    from sqlalchemy import text
    {% if config.project.async_mode | default(false) %}
    from sqlalchemy.ext.asyncio import AsyncSession
    {% else %}
    from sqlalchemy.orm import Session
    {% endif %}
    from src.shared.infrastructure.database import get_db
    ```
  - Create router:
    ```python
    router = APIRouter(
        prefix="/health",
        tags=["health"],
    )
    ```
  - Define response model (inline dict, no Pydantic needed for simplicity)
  - Implement GET /health endpoint:
    - Use `{% if config.project.async_mode | default(false) %}` for async/sync branching
    - Async version:
      ```python
      @router.get("/health")
      async def health_check(db: AsyncSession = Depends(get_db)):
          """Health check endpoint..."""
          status = "healthy"
          database_status = "connected"

          try:
              await db.execute(text("SELECT 1"))
          except Exception:
              database_status = "disconnected"
              status = "degraded"

          return {
              "status": status,
              "version": "{{ config.project.version | default('0.1.0') }}",
              "database": database_status,
              "timestamp": datetime.utcnow().isoformat() + "Z"
          }
      ```
    - Sync version (in else block):
      ```python
      @router.get("/health")
      def health_check(db: Session = Depends(get_db)):
          """Health check endpoint..."""
          status = "healthy"
          database_status = "connected"

          try:
              db.execute(text("SELECT 1"))
          except Exception:
              database_status = "disconnected"
              status = "degraded"

          return {
              "status": status,
              "version": "{{ config.project.version | default('0.1.0') }}",
              "database": database_status,
              "timestamp": datetime.utcnow().isoformat() + "Z"
          }
      ```
  - Add usage example in docstring:
    ```python
    # In your main.py or app factory:
    from src.shared.api.health import router as health_router
    app.include_router(health_router)

    # The endpoint will be available at /health/health
    # To mount at /health directly:
    app.include_router(health_router, prefix="")
    ```
  - Add monitoring integration examples in docstring:
    ```
    # Kubernetes liveness probe:
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 30
      periodSeconds: 10

    # AWS ALB health check:
    Target: HTTP:8000/health
    Healthy threshold: 2
    Unhealthy threshold: 3
    Timeout: 5
    Interval: 30
    ```

### Task 3: Render Reference Implementation
- Check if directory `src/shared/api/` exists
  - If not, create it with `mkdir -p src/shared/api`
  - Create `__init__.py` in `src/shared/api/` if needed
- Render the template to `src/shared/api/health.py` using config.yml values:
  - `config.project.name` → "tac-bootstrap"
  - `config.project.version` → "0.1.0" (use default since likely not in config.yml)
  - `config.project.async_mode` → false (not set in config.yml, so default to sync)
- Add header comments:
  ```python
  # Reference implementation - generated from health.py.j2 template
  # This file serves as documentation for the health.py template output
  # Not used by the CLI itself (tac-bootstrap has framework="none")
  ```
- Save the file
- Create `src/shared/__init__.py` if it doesn't exist (for proper Python package structure)

### Task 4: Verify Template and Rendered Files
- Verify `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` exists
- Verify `src/shared/api/health.py` exists
- Check that both files have:
  - Proper IDK docstring format
  - Correct imports (FastAPI, SQLAlchemy, datetime)
  - Database dependency injection using get_db
  - SELECT 1 database check
  - Response format with status, version, database, timestamp
  - HTTP 200 always (no status code variation)
  - Exception handling for database errors
  - No sensitive information exposed
  - Clear usage examples

### Task 5: Validate Correctness
- Verify response format matches specification:
  - `status`: "healthy" or "degraded"
  - `version`: from config or default "0.1.0"
  - `database`: "connected" or "disconnected"
  - `timestamp`: ISO8601 format with 'Z' suffix
- Verify database check pattern:
  - Uses `text("SELECT 1")` from SQLAlchemy
  - Catches all exceptions (bare except or Exception)
  - Sets database='disconnected' and status='degraded' on error
- Verify no sensitive information:
  - No DATABASE_URL
  - No hostnames or IPs
  - No internal service names
  - No credentials or tokens
- Verify async patterns (if async mode):
  - `async def health_check`
  - `await db.execute(...)`
  - `AsyncSession` type hint
- Verify sync patterns (if sync mode):
  - `def health_check` (no async)
  - `db.execute(...)` (no await)
  - `Session` type hint

### Task 6: Run Validation Commands
Execute all validation commands to ensure zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check (may have errors if types not fully annotated, acceptable)
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI still works

## Testing Strategy

### Unit Tests
No dedicated unit tests needed for this template (it's a Jinja2 template, not executable code in the CLI). However:
- Template rendering could be tested in integration tests (future work)
- Verify template file exists and is valid Jinja2 syntax
- Verify rendered file exists and has expected structure

### Edge Cases
Consider these scenarios in the template design:
- Database completely unavailable → status='degraded', database='disconnected', HTTP 200
- Database connection timeout → same as above (caught by exception handler)
- Database responds slowly → no explicit timeout, rely on driver defaults
- config.project.version missing → use default '0.1.0' via Jinja2 filter
- Async vs sync mode → template supports both with conditional rendering

## Acceptance Criteria
- [ ] Template file `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` exists and is valid Jinja2
- [ ] Rendered file `src/shared/api/health.py` exists with correct content
- [ ] Both files have IDK docstring format with comprehensive examples
- [ ] Endpoint uses FastAPI router with prefix='/health'
- [ ] GET /health endpoint is async (or sync if async_mode=false)
- [ ] Database check uses get_db dependency from database.py
- [ ] Database check performs SELECT 1 for connectivity verification
- [ ] Response format matches specification: status, version, database, timestamp
- [ ] HTTP 200 always returned (status field indicates healthy/degraded)
- [ ] Exception handling catches database errors and sets degraded state
- [ ] Timestamp is ISO8601 format with 'Z' suffix (UTC)
- [ ] No sensitive information exposed (no URLs, credentials, hostnames)
- [ ] Usage examples show how to mount router in main.py
- [ ] Monitoring integration examples included (Kubernetes, ALB)
- [ ] Template supports both async and sync modes with conditional rendering
- [ ] Rendered file has header comments indicating it's a reference example
- [ ] Directory `src/shared/api/` created with proper `__init__.py`
- [ ] All validation commands pass (pytest, ruff, mypy, CLI smoke test)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is Task 1.10 in the TAC Bootstrap implementation plan (Fase 1: Base Classes and Infrastructure)
- The /health endpoint is a critical production requirement for observability
- The template follows the Dual Creation Pattern (template + rendered reference)
- The rendered file in src/shared/api/health.py is a reference example only (this project is a CLI, not a FastAPI app)
- The database check (SELECT 1) is intentionally simple and fast (<10ms typical)
- No explicit timeout on database check - rely on database driver defaults
- Always HTTP 200 (even on degraded) - many monitoring tools prefer this pattern with status field
- The prefix='/health' means the endpoint will be at /health/health if mounted normally, or /health if mounted with prefix=""
- Users can override router prefix when mounting in their app
- No Pydantic response model needed - simple dict return is clearer for this use case
- Template supports both async and sync modes to accommodate different project configurations
- Future work: Add additional health checks (Redis, external APIs) as commented examples
