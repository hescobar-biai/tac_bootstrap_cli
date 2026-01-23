# Feature: Template health.py - Health Endpoint with Database Check

## Metadata
issue_number: `131`
adw_id: `5e760945`
issue_json: `{"number":131,"title":"Tarea 1.10: Template health.py","body":"/feature\n/adw_sdlc_zte_iso\n**Tipo**: feature\n**Ganancia**: Endpoint /health listo para monitoreo. Verifica conexion a BD y reporta version de la app.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`\n2. Crear renderizado en raiz: `src/shared/api/health.py`\n2. Contenido:\n   - Router FastAPI con prefix=\"\" o \"/health\"\n   - `GET /health` retorna:\n     ```json\n     {\n       \"status\": \"healthy\",\n       \"version\": \"{{ config.project.version | default('0.1.0') }}\",\n       \"database\": \"connected\" | \"disconnected\",\n       \"timestamp\": \"ISO8601\"\n     }\n     ```\n   - Intenta hacer `SELECT 1` a la BD para verificar conexion\n   - Si falla la BD, retorna status \"degraded\" pero HTTP 200\n\n**Criterios de aceptacion**:\n- Endpoint responde en <100ms\n- No expone informacion sensible\n- Reporta estado de la BD\n\n## Estructura del Plan\n\n- **7 Fases**, **3 Iteraciones** de ejecucion\n- Cada tarea tiene: tipo (feature/chore/bug), descripcion, ganancia, instrucciones, criterios de aceptacion\n- Fases 1-5 (codigo) y Fases 6-7 (docs fractal) son independientes\n\n## REGLA CRITICA: Dual Creation Pattern\n\n**IMPORTANTE**: Este proyecto es TANTO el generador como un proyecto de referencia. Por lo tanto, cada tarea que cree un template DEBE crear DOS archivos:\n\n1. **Template Jinja2** en `tac_bootstrap_cli/tac_bootstrap/templates/` → usado por el CLI para generar en OTROS proyectos\n2. **Archivo renderizado** en la raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/`) → para que ESTE proyecto tambien lo tenga\n\n### Mapeo de rutas (template → archivo en raiz):\n\n| Template (tac_bootstrap_cli/tac_bootstrap/templates/) | Archivo en raiz (/Volumes/MAc1/Celes/tac_bootstrap/) |\n|---|---|\n| `shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |\n| `shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |\n| `shared/base_service.py.j2` | `src/shared/application/base_service.py` |\n| `shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |\n| `shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |\n| `shared/database.py.j2` | `src/shared/infrastructure/database.py` |\n| `shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |\n| `shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |\n| `shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |\n| `shared/health.py.j2` | `src/shared/api/health.py` |\n| `capabilities/crud_basic/domain_entity.py.j2` | *(se genera bajo demanda con `generate entity`)* |\n| `capabilities/crud_basic/schemas.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/service.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/repository.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/routes.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/orm_model.py.j2` | *(se genera bajo demanda)* |\n| `scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |\n| `scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |\n| `scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |\n| `claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |\n| `config/canonical_idk.yml.j2` | `canonical_idk.yml` |\n\n### Excepcion: Templates de capabilities (crud_basic, crud_authorized)\nLos templates de `capabilities/` NO se renderizan automaticamente en la raiz. Solo se generan cuando el usuario ejecuta `tac-bootstrap generate entity <name>`. Por eso no tienen archivo en raiz.\n\n### Contexto: config.yml de ESTE proyecto\n\nEl archivo `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` contiene la configuracion real de este proyecto. Los templates usan estas variables con la sintaxis `{{ config.project.name }}`, `{{ config.paths.app_root }}`, etc.\n\n**Valores actuales relevantes para renderizado:**\n```yaml\nproject:\n  name: \"tac-bootstrap\"\n  language: \"python\"\n  framework: \"none\"         # NOTA: no es FastAPI, pero architecture=ddd\n  architecture: \"ddd\"\n  package_manager: \"uv\"\n\npaths:\n  app_root: \"tac_bootstrap_cli\"   # Codigo del CLI vive aqui\n  scripts_dir: \"scripts\"\n  adws_dir: \"adws\"\n\ncommands:\n  test: \"uv run pytest\"\n  lint: \"uv run ruff check .\"\n```\n\n**IMPORTANTE - Consideracion de framework:**\n- Este proyecto tiene `framework: \"none\"` (no es una app FastAPI, es un CLI)\n- Las base classes (Fase 1) son templates para proyectos FastAPI que el CLI GENERA\n- Para la dual creation en la raiz: renderizar los templates como **ejemplo/referencia** usando los valores de config.yml, pero los imports de FastAPI/SQLAlchemy son de referencia (no se ejecutan en este proyecto)\n- Los scripts de Fase 6 SI son funcionales en este proyecto (Python, language=python)\n\n### Como implementar la dual creation:\n1. Crear el template `.j2` con variables Jinja2 (`{{ config.project.name }}`, etc.)\n2. Para renderizar el archivo en raiz, usar los valores de `config.yml`:\n   - `config.project.name` → `\"tac-bootstrap\"`\n   - `config.project.language` → `\"python\"`\n   - `config.paths.app_root` → `\"tac_bootstrap_cli\"`\n   - `config.commands.test` → `\"uv run pytest\"`\n3. Guardar el resultado en la ruta correspondiente de la raiz\n4. Verificar que AMBOS archivos existen y son consistentes\n\n### Ejemplo concreto de renderizado:\n\n**Template** (`templates/scripts/run_generators.sh.j2`):\n```bash\nREPO_ROOT=\"{{ config.paths.app_root | default('.') }}\"\n```\n\n**Renderizado en raiz** (`scripts/run_generators.sh`):\n```bash\nREPO_ROOT=\"tac_bootstrap_cli\"\n```\n\n**Template** (`templates/config/canonical_idk.yml.j2`):\n```yaml\n# Canonical IDK Vocabulary for {{ config.project.name }}\n{% if config.project.language == \"python\" %}\n  backend:\n    - api-gateway, routing, ...\n{% endif %}\n```\n\n**Renderizado en raiz** (`canonical_idk.yml`):\n```yaml\n# Canonical IDK Vocabulary for tac-bootstrap\n  backend:\n    - api-gateway, routing, ...\n```}"

## Auto-Resolved Clarifications

**Summary:** Create health.py.j2 template with FastAPI router at prefix='', endpoint GET /health returning JSON with status/version/database/timestamp. Use get_db dependency for SELECT 1 check, catch all exceptions to return 'degraded' status with HTTP 200. Render to src/shared/api/health.py as reference code for this CLI project.

**Q:** Should the health endpoint be registered automatically in the main FastAPI app, or is that a separate task?
**A:** Leave registration as a separate concern. The template creates a router that can be included in main.py via `app.include_router(health_router)`.
*The task only asks to create the health.py file with a router. App registration is typically done in main.py and isn't mentioned in acceptance criteria. Keep it simple - just create the router.*

**Q:** What database connection method should be used for the SELECT 1 check?
**A:** Use the get_db dependency from database.py (Tarea 1.6) with Depends() in a sub-function, then call session.execute(text('SELECT 1')).
*Reuses existing infrastructure. The database.py template provides get_db which returns a Session. This is the standard FastAPI pattern and avoids duplicate connection logic.*

**Q:** Should the health check timeout the database query?
**A:** No explicit timeout. Rely on default database connection timeout settings.
*The <100ms requirement is aspirational for healthy systems. Adding timeout logic adds complexity. If DB is slow/down, the default timeout will trigger and we'll catch the exception to return 'disconnected'.*

**Q:** What should happen if the database dependency itself isn't configured?
**A:** Catch all exceptions (generic Exception) in the database check and return database='disconnected' with status='degraded'.
*Simple and robust. Whether it's missing DATABASE_URL, connection failure, or any other DB issue, the health check should never crash. Return degraded state with HTTP 200 as specified.*

**Q:** The prefix is specified as '' or '/health' - which one should be used?
**A:** Use prefix='' (empty string) so the endpoint is accessible at /health.
*Standard convention is /health as the endpoint path. Using prefix='' with @router.get('/health') gives /health. Using prefix='/health' would require @router.get('') which is less intuitive.*

**Q:** Should the version come from config.project.version, or should it read from package metadata?
**A:** Use {{ config.project.version | default('0.1.0') }} in the template as specified in the task instructions.
*The task explicitly shows this approach. It's simple and matches the dual-creation pattern where templates use config variables.*

**Q:** Should the template include logging of health check failures?
**A:** No logging. Keep it minimal.
*Not mentioned in requirements. Health endpoints are hit frequently by monitoring tools. Logging every failure could spam logs. The status response provides sufficient observability.*

**Q:** Given that this project has framework='none', should the rendered file in src/shared/api/health.py be treated purely as reference code?
**A:** Yes, render it as reference/example code. It won't execute in this CLI project but serves as documentation and testing of the template.
*Per the dual-creation pattern instructions, rendered files in the root are examples/references when framework='none'. The real use case is when CLI generates this for FastAPI projects.*

## Feature Description

This task implements a health check endpoint template (`health.py.j2`) for FastAPI applications. The endpoint provides monitoring capabilities by checking database connectivity and reporting application version. It follows the dual-creation pattern, generating both a Jinja2 template for the CLI and a reference implementation in the root project.

The health endpoint returns JSON responses with status (healthy/degraded), version from config, database connectivity status, and ISO8601 timestamp. It performs a lightweight `SELECT 1` database check and gracefully handles failures by returning HTTP 200 with status="degraded" to avoid triggering monitoring alerts for transient issues.

## User Story

As a DevOps engineer deploying FastAPI applications generated by TAC Bootstrap
I want a standardized /health endpoint with database connectivity checking
So that I can monitor application health and database status without exposing sensitive information

## Problem Statement

FastAPI applications need standardized health check endpoints for:
- Load balancers and orchestration systems (Kubernetes liveness/readiness probes)
- Monitoring and alerting systems to detect service degradation
- Database connectivity verification without exposing connection details
- Version tracking for deployment verification

Currently, there's no template for generating this common pattern, forcing developers to manually implement health endpoints with inconsistent approaches to database checking and error handling.

## Solution Statement

Create a `health.py.j2` template that generates a FastAPI router with:
- Simple `/health` endpoint accessible without authentication
- Fast database connectivity check using `SELECT 1` query
- Graceful degradation (HTTP 200 with status="degraded" on DB failure)
- Version information from TACConfig
- ISO8601 timestamps for response validation
- No sensitive information exposure (no connection strings, no stack traces)

The template uses the existing `get_db()` dependency from `database.py.j2` for database session management, ensuring consistency with the rest of the application's data layer.

## Relevant Files

Archivos necesarios para implementar la feature:

### Existing Templates
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - Provides `get_db()` dependency for database session management (already exists, read for reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2` - Optional reference for FastAPI dependency patterns (already exists, not modified)

### Existing Reference Implementations
- `src/shared/infrastructure/database.py` - Reference implementation of database.py template, provides context on get_db() usage

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` - New Jinja2 template for health endpoint router
- `src/shared/api/health.py` - Reference implementation rendered from template (for documentation and dual-creation pattern)

### Configuration
- `config.yml` - Contains project configuration values used for rendering (project.version, project.name, etc.)

## Implementation Plan

### Phase 1: Foundation
1. Review existing `database.py.j2` template to understand `get_db()` dependency pattern
2. Review existing reference implementations to understand IDK documentation style
3. Identify the correct directory structure for the new template (`tac_bootstrap_cli/tac_bootstrap/templates/shared/`)
4. Identify the correct directory for reference implementation (`src/shared/api/`)

### Phase 2: Core Implementation
1. Create the Jinja2 template `health.py.j2` with:
   - IDK documentation following the pattern from other templates
   - FastAPI router with prefix="" (empty string)
   - GET /health endpoint function
   - Database connectivity check helper function
   - Proper imports (FastAPI, SQLAlchemy, datetime, typing)
   - Jinja2 variables for config values (version)
   - Conditional rendering for async mode (config.project.async_mode)
2. Implement the health check logic:
   - Main endpoint function returning JSON response
   - Database check sub-function using get_db() dependency
   - Exception handling for database failures (catch all exceptions)
   - Status determination logic (healthy vs degraded)
   - ISO8601 timestamp generation
3. Follow the established template patterns:
   - Use IDK documentation header
   - Include usage examples in docstrings
   - Match style of other shared templates (database.py.j2, dependencies.py.j2)

### Phase 3: Integration
1. Render the template to `src/shared/api/health.py` as reference implementation:
   - Create `src/shared/api/` directory if it doesn't exist
   - Use config.yml values for rendering (project.name="tac-bootstrap", project.version, async_mode=false)
   - Add reference implementation header comment
   - Ensure consistent IDK documentation style
2. Verify both files exist and are consistent
3. Validate that the template uses correct Jinja2 syntax and config variables

## Step by Step Tasks

### Task 1: Review existing templates and patterns
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` to understand get_db() pattern
- Read `src/shared/infrastructure/database.py` reference implementation
- Review IDK documentation style from existing templates
- Understand conditional rendering patterns for async_mode

### Task 2: Create template directory structure
- Verify `tac_bootstrap_cli/tac_bootstrap/templates/shared/` exists (should exist from previous tasks)
- Create `src/shared/api/` directory if it doesn't exist

### Task 3: Create health.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`
- Add IDK documentation header describing the module's responsibility
- Define FastAPI router with prefix=""
- Implement GET /health endpoint with proper type annotations
- Implement database check helper function using get_db() dependency
- Add exception handling for database connectivity failures
- Use `{{ config.project.version | default('0.1.0') }}` for version field
- Include conditional rendering for sync vs async mode based on `config.project.async_mode`
- Add comprehensive docstrings with usage examples
- Follow the style and structure of existing templates

### Task 4: Render reference implementation
- Load config.yml to get rendering values
- Render template with config values (name="tac-bootstrap", async_mode=false)
- Write rendered output to `src/shared/api/health.py`
- Add header comment indicating it's a reference implementation
- Verify the rendered file is valid Python syntax

### Task 5: Validation and verification
- Execute Validation Commands (see below)
- Verify both files exist:
  - `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`
  - `src/shared/api/health.py`
- Verify health.py.j2 uses correct Jinja2 syntax
- Verify reference implementation has consistent formatting
- Verify no sensitive information is exposed in health responses
- Verify database check uses get_db() dependency correctly
- Verify HTTP 200 returned even on database failure

## Testing Strategy

### Unit Tests
- No unit tests required for this task (templates are tested through integration)
- Reference implementation is non-executable (framework="none" project)
- Template validation happens through Validation Commands

### Edge Cases
- Database connection not configured (DATABASE_URL missing) → returns degraded
- Database connection fails (DB unreachable) → returns degraded with HTTP 200
- Database query timeout → returns degraded with HTTP 200
- Missing config.project.version → defaults to "0.1.0"
- Async mode enabled → uses async get_db() and async/await patterns
- Sync mode (default) → uses sync get_db() generator

## Acceptance Criteria

1. Template file `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2` exists and is valid Jinja2
2. Reference file `src/shared/api/health.py` exists and is valid Python
3. Health endpoint uses FastAPI router with prefix="" (accessible at /health)
4. Response includes: status (healthy/degraded), version, database (connected/disconnected), timestamp (ISO8601)
5. Database check uses get_db() dependency from database.py
6. Database failures return HTTP 200 with status="degraded" (not HTTP 500)
7. No sensitive information exposed (no connection strings, no stack traces)
8. Template includes IDK documentation following existing patterns
9. Template supports both sync and async modes via conditional rendering
10. Validation Commands pass with zero errors

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

```bash
# Verify template exists and uses valid Jinja2 syntax
cd tac_bootstrap_cli && uv run python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap/templates')); env.get_template('shared/health.py.j2')"

# Verify reference implementation exists and is valid Python
python -m py_compile src/shared/api/health.py

# Run full test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This template is part of FASE 1 (Base Classes y Database) in PLAN_TAC_BOOTSTRAP.md (Tarea 1.10)
- The health endpoint is designed to be lightweight (<100ms response time) for frequent polling
- Uses HTTP 200 for degraded state to avoid triggering load balancer circuit breakers on transient DB issues
- The template follows the dual-creation pattern: one .j2 template + one reference implementation
- Reference implementation serves as documentation and template validation
- Health endpoint should NOT require authentication (monitoring tools need unauthenticated access)
- Router can be included in main.py with: `app.include_router(health_router)` (registration is separate task)
- Database check uses `SELECT 1` which is a lightweight, portable query supported by all major databases
- Follows established IDK documentation style from other shared templates
- Supports both sync and async SQLAlchemy patterns via conditional Jinja2 rendering
