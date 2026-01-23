# Feature: Template database.py - Database Session Management

## Metadata
issue_number: `121`
adw_id: `a84f13cc`
issue_json: `{"number":121,"title":"Tarea 1.6: Template database.py","body":"/feature\n**Ganancia**: Session management centralizado. Un solo lugar para configurar la conexion a BD, crear sesiones, y manejar el lifecycle.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`\n2. Crear renderizado en raiz: `src/shared/infrastructure/database.py`\n2. Contenido:\n   - `engine` = create_engine con URL desde config/env\n   - `SessionLocal` = sessionmaker\n   - `Base` = declarative_base()\n   - `get_db()` generator para dependency injection en FastAPI\n   - Soporte condicional para async:\n     ```jinja2\n     {% if config.project.async_mode | default(false) %}\n     from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession\n     {% else %}\n     from sqlalchemy import create_engine\n     {% endif %}\n     ```\n3. Variable Jinja2: `{{ config.project.database_url | default(\"sqlite:///./app.db\") }}`\n\n**Criterios de aceptacion**:\n- get_db() es un generator que cierra session en finally\n- Soporta sqlite y postgresql via variable de entorno\n- Base es exportable para que modelos hereden de ella\n# PLAN: TAC Bootstrap v0.3 - Version Robusta\n\n## Objetivo\n\nEvolucionar `tac_bootstrap_cli` de un generador de estructura agentic a una herramienta completa que tambien genera codigo de aplicacion (entidades CRUD con DDD), documentacion fractal automatica, y validacion multi-capa. Basado en los patrones documentados en `ai_docs/doc/create-crud-entity/`.\n\n## Estructura del Plan\n\n- **7 Fases**, **3 Iteraciones** de ejecucion\n- Cada tarea tiene: tipo (feature/chore/bug), descripcion, ganancia, instrucciones, criterios de aceptacion\n- Fases 1-5 (codigo) y Fases 6-7 (docs fractal) son independientes\n\n## REGLA CRITICA: Dual Creation Pattern\n\n**IMPORTANTE**: Este proyecto es TANTO el generador como un proyecto de referencia. Por lo tanto, cada tarea que cree un template DEBE crear DOS archivos:\n\n1. **Template Jinja2** en `tac_bootstrap_cli/tac_bootstrap/templates/` → usado por el CLI para generar en OTROS proyectos\n2. **Archivo renderizado** en la raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/`) → para que ESTE proyecto tambien lo tenga\n\n### Mapeo de rutas (template → archivo en raiz):\n\n| Template (tac_bootstrap_cli/tac_bootstrap/templates/) | Archivo en raiz (/Volumes/MAc1/Celes/tac_bootstrap/) |\n|---|---|\n| `shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |\n| `shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |\n| `shared/base_service.py.j2` | `src/shared/application/base_service.py` |\n| `shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |\n| `shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |\n| `shared/database.py.j2` | `src/shared/infrastructure/database.py` |\n| `shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |\n| `shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |\n| `shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |\n| `shared/health.py.j2` | `src/shared/api/health.py` |\n| `capabilities/crud_basic/domain_entity.py.j2` | *(se genera bajo demanda con `generate entity`)* |\n| `capabilities/crud_basic/schemas.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/service.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/repository.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/routes.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/orm_model.py.j2` | *(se genera bajo demanda)* |\n| `scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |\n| `scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |\n| `scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |\n| `claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |\n| `config/canonical_idk.yml.j2` | `canonical_idk.yml` |\n\n### Excepcion: Templates de capabilities (crud_basic, crud_authorized)\nLos templates de `capabilities/` NO se renderizan automaticamente en la raiz. Solo se generan cuando el usuario ejecuta `tac-bootstrap generate entity <name>`. Por eso no tienen archivo en raiz.\n\n### Contexto: config.yml de ESTE proyecto\n\nEl archivo `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` contiene la configuracion real de este proyecto. Los templates usan estas variables con la sintaxis `{{ config.project.name }}`, `{{ config.paths.app_root }}`, etc.\n\n**Valores actuales relevantes para renderizado:**\n```yaml\nproject:\n  name: \"tac-bootstrap\"\n  language: \"python\"\n  framework: \"none\"         # NOTA: no es FastAPI, pero architecture=ddd\n  architecture: \"ddd\"\n  package_manager: \"uv\"\n\npaths:\n  app_root: \"tac_bootstrap_cli\"   # Codigo del CLI vive aqui\n  scripts_dir: \"scripts\"\n  adws_dir: \"adws\"\n\ncommands:\n  test: \"uv run pytest\"\n  lint: \"uv run ruff check .\"\n```\n\n**IMPORTANTE - Consideracion de framework:**\n- Este proyecto tiene `framework: \"none\"` (no es una app FastAPI, es un CLI)\n- Las base classes (Fase 1) son templates para proyectos FastAPI que el CLI GENERA\n- Para la dual creation en la raiz: renderizar los templates como **ejemplo/referencia** usando los valores de config.yml, pero los imports de FastAPI/SQLAlchemy son de referencia (no se ejecutan en este proyecto)\n- Los scripts de Fase 6 SI son funcionales en este proyecto (Python, language=python)\n\n### Como implementar la dual creation:\n1. Crear el template `.j2` con variables Jinja2 (`{{ config.project.name }}`, etc.)\n2. Para renderizar el archivo en raiz, usar los valores de `config.yml`:\n   - `config.project.name` → `\"tac-bootstrap\"`\n   - `config.project.language` → `\"python\"`\n   - `config.paths.app_root` → `\"tac_bootstrap_cli\"`\n   - `config.commands.test` → `\"uv run pytest\"`\n3. Guardar el resultado en la ruta correspondiente de la raiz\n4. Verificar que AMBOS archivos existen y son consistentes\n\n### Ejemplo concreto de renderizado:\n\n**Template** (`templates/scripts/run_generators.sh.j2`):\n```bash\nREPO_ROOT=\"{{ config.paths.app_root | default('.') }}\"\n```\n\n**Renderizado en raiz** (`scripts/run_generators.sh`):\n```bash\nREPO_ROOT=\"tac_bootstrap_cli\"\n```\n\n**Template** (`templates/config/canonical_idk.yml.j2`):\n```yaml\n# Canonical IDK Vocabulary for {{ config.project.name }}\n{% if config.project.language == \"python\" %}\n  backend:\n    - api-gateway, routing, ...\n{% endif %}\n```\n\n**Renderizado en raiz** (`canonical_idk.yml`):\n```yaml\n# Canonical IDK Vocabulary for tac-bootstrap\n  backend:\n    - api-gateway, routing, ..."} ## Auto-Resolved Clarifications\n\n**Summary:** Single template with async/sync conditionals. Environment-first config (DATABASE_URL → config.yml → sqlite default). Clean get_db() generator without error handling. Include connection pool config as commented examples. Render full reference implementation in root with explanatory comment. Keep focused on session management - no migration code.\n\n**Q:** Should the database.py template include async support by default, or should it generate two separate files?\n**A:** Single template with conditional async/sync blocks using {% if config.project.async_mode %}\n*Simpler maintenance - one template to update. The conditional blocks are clean and users see both patterns. Aligns with existing PLAN pattern showing conditional async imports.*\n\n**Q:** What should the default database URL be for projects that specify PostgreSQL vs SQLite?\n**A:** Single default: sqlite:///./app.db. PostgreSQL projects should set DATABASE_URL in .env\n*SQLite works out-of-box without setup, perfect for prototyping. PostgreSQL users are sophisticated enough to configure DATABASE_URL. Avoids complex database_type detection logic.*\n\n**Q:** Should get_db() include error handling for database connection failures?\n**A:** No explicit error handling in get_db(). Let exceptions propagate to FastAPI's exception handlers\n*Separation of concerns - get_db() is infrastructure, error handling is application layer. FastAPI handles DB exceptions gracefully. Keeps the generator simple and lets users add custom error handling if needed.*\n\n**Q:** Where should the database_url configuration come from?\n**A:** Environment variable (DATABASE_URL) with fallback to config.project.database_url, then hardcoded default\n*12-factor app pattern: env vars for deployment secrets. Config.yml for local dev convenience. Hardcoded default for instant prototyping. Priority: os.getenv('DATABASE_URL') || config.project.database_url || 'sqlite:///./app.db'*\n\n**Q:** For dual creation: should rendered database.py in root include SQLAlchemy imports as non-functional reference?\n**A:** Yes, include full SQLAlchemy imports as reference code with a comment header explaining it's a template reference\n*This project IS the reference implementation. Having the rendered file helps developers see the final output and serves as documentation. Add comment: '# Reference implementation - not used by CLI itself'*\n\n**Q:** Should the template include connection pooling configuration options?\n**A:** Yes, but as optional commented examples in the template\n*Production apps need pooling config, but sensible defaults work for 90% of cases. Include commented examples: # pool_size={{ config.database.pool_size | default(5) }} so users can uncomment and configure via config.yml*\n\n**Q:** Should the template include database migration initialization code?\n**A:** No, migrations are handled separately\n*Alembic setup is a separate concern with its own templates. Database.py focuses on runtime session management. Keep it focused and simple.*\n\n**Q:** What if default sqlite path exists - reuse or warn?\n**A:** Reuse silently - standard SQLite behavior\n*SQLite naturally handles existing files. No action needed. Users expect persistence. If they want fresh DB, they delete the file manually.*"}`

## Feature Description
Create a centralized database session management template for TAC Bootstrap CLI that generates database.py files for projects. This template provides a single source of truth for database connection configuration, session creation, and lifecycle management. The template supports both synchronous and asynchronous SQLAlchemy patterns through conditional rendering, allowing projects to use either based on their `async_mode` configuration.

The template follows the Dual Creation Pattern, creating both a Jinja2 template for CLI generation and a rendered reference implementation in the project root.

## User Story
As a developer using TAC Bootstrap CLI
I want to generate database.py files with proper session management
So that my FastAPI projects have centralized, production-ready database configuration with support for both sync and async patterns

## Problem Statement
FastAPI projects require proper SQLAlchemy session management with:
- Database connection configuration from environment variables
- SessionLocal factory for dependency injection
- Declarative Base for ORM models
- get_db() generator that properly handles session lifecycle
- Support for both synchronous and asynchronous patterns
- Connection pooling configuration options

Currently, developers must manually create this boilerplate or copy-paste from examples, leading to inconsistencies and potential bugs in session management.

## Solution Statement
Create a Jinja2 template (`database.py.j2`) that generates production-ready database configuration. The template:
- Uses environment variable DATABASE_URL with fallback to config.project.database_url, then hardcoded sqlite default
- Conditionally imports sync/async SQLAlchemy based on config.project.async_mode
- Creates engine with optional connection pool settings (as commented examples)
- Provides SessionLocal sessionmaker
- Exports declarative_base() for model inheritance
- Implements get_db() generator for FastAPI dependency injection with proper cleanup

Following the Dual Creation Pattern, also render a reference implementation in `src/shared/infrastructure/database.py` with a header comment explaining it's a template reference.

## Relevant Files
Files necessary for implementing the feature:

### Existing Template Examples
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` - Example of existing shared template structure, IDK docstring format, and conditional patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2` - Example of async SQLAlchemy patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2` - Example of domain layer template
- `config.yml` - Project configuration with values for rendering (project.name, paths.app_root, etc.)

### Existing Reference Implementations
- `src/shared/infrastructure/base_repository.py` - Reference for understanding database session usage patterns
- `src/shared/infrastructure/base_repository_async.py` - Reference for async session patterns

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - Jinja2 template for database configuration (PRIMARY)
- `src/shared/infrastructure/database.py` - Rendered reference implementation in project root

## Implementation Plan

### Phase 1: Research and Pattern Analysis
- Read existing templates to understand Jinja2 variable usage, IDK docstring format, and conditional rendering patterns
- Read existing base_repository files to understand how database sessions are used
- Review config.yml to identify all relevant configuration variables

### Phase 2: Create Template
- Create `database.py.j2` with:
  - IDK docstring following existing template format
  - Conditional imports for sync/async SQLAlchemy
  - Environment variable reading with fallback chain (DATABASE_URL → config → default)
  - Engine creation with commented pool configuration examples
  - SessionLocal sessionmaker (sync or async based on mode)
  - declarative_base() export
  - get_db() generator with proper try/finally cleanup
- Use Jinja2 variables: `{{ config.project.async_mode }}`, `{{ config.project.database_url }}`, `{{ config.database.pool_size }}`

### Phase 3: Render Reference Implementation
- Render the template using values from config.yml:
  - `config.project.name` → "tac-bootstrap"
  - `config.project.async_mode` → undefined (defaults to false, sync mode)
  - `config.project.database_url` → undefined (uses hardcoded sqlite default)
- Add header comment: "# Reference implementation - generated from database.py.j2 template"
- Save to `src/shared/infrastructure/database.py`
- Ensure directory exists (create if needed)

### Phase 4: Validation
- Verify template file exists and is valid Jinja2
- Verify rendered file exists with correct content
- Check that both files follow existing code patterns
- Validate IDK docstring format matches other templates

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Research Existing Patterns
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` to understand:
  - IDK docstring format and structure
  - Jinja2 variable syntax and defaults
  - Import organization
  - Module-level variable definitions
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2` to understand async SQLAlchemy import patterns
- Read `config.yml` to identify configuration structure and available variables

### Task 2: Create database.py.j2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`
- Write IDK docstring with:
  - IDK tags: database-session, connection-management, orm-configuration
  - Module name: database
  - Responsibility: Centralized database session management and configuration
  - Key Components: engine, SessionLocal, Base, get_db()
  - Invariants: Session cleanup in finally block, environment variable priority
  - Usage examples showing how to use get_db() in FastAPI routes
- Add conditional async/sync imports:
  ```jinja2
  {% if config.project.async_mode | default(false) %}
  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
  {% else %}
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker, Session
  {% endif %}
  ```
- Add common imports (declarative_base, os)
- Create DATABASE_URL with priority chain:
  ```python
  DATABASE_URL = os.getenv("DATABASE_URL") or "{{ config.project.database_url | default('sqlite:///./app.db') }}"
  ```
- Create engine with commented pool config examples:
  ```jinja2
  {% if config.project.async_mode | default(false) %}
  engine = create_async_engine(
      DATABASE_URL,
      # Uncomment for custom connection pool:
      # pool_size={{ config.database.pool_size | default(5) }},
      # max_overflow={{ config.database.max_overflow | default(10) }},
      # pool_pre_ping=True,
  )
  {% else %}
  engine = create_engine(
      DATABASE_URL,
      # Uncomment for custom connection pool:
      # pool_size={{ config.database.pool_size | default(5) }},
      # max_overflow={{ config.database.max_overflow | default(10) }},
      # pool_pre_ping=True,
  )
  {% endif %}
  ```
- Create SessionLocal sessionmaker (async_sessionmaker for async mode)
- Export Base = declarative_base()
- Implement get_db() generator:
  ```jinja2
  {% if config.project.async_mode | default(false) %}
  async def get_db() -> AsyncSession:
      """Dependency injection for async database sessions."""
      async with SessionLocal() as session:
          try:
              yield session
          finally:
              await session.close()
  {% else %}
  def get_db() -> Session:
      """Dependency injection for database sessions."""
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  {% endif %}
  ```

### Task 3: Render Reference Implementation
- Create directory `src/shared/infrastructure/` if it doesn't exist
- Read config.yml to get rendering values
- Render template with:
  - `config.project.async_mode` = undefined (default to false)
  - `config.project.database_url` = undefined (use hardcoded default)
  - `config.database.pool_size` = undefined (use default 5)
- Add header comment to rendered file:
  ```python
  # Reference implementation - generated from database.py.j2 template
  # This file serves as documentation for the database.py template output
  # Not used by the CLI itself (tac-bootstrap has framework="none")
  ```
- Save to `src/shared/infrastructure/database.py`

### Task 4: Validation and Testing
- Verify template file exists at correct path
- Verify rendered file exists at correct path
- Read both files to check consistency
- Validate IDK docstring format matches other templates
- Check that get_db() uses try/finally pattern
- Verify environment variable fallback chain is correct
- Execute Validation Commands

## Testing Strategy

### Unit Tests
No automated tests needed for this task (template creation). Manual validation through file inspection.

### Manual Validation
- Template file exists and is valid Jinja2
- Rendered file exists with sync mode (async_mode=false)
- get_db() generator has proper try/finally cleanup
- DATABASE_URL uses environment variable priority chain
- Pool configuration examples are commented
- IDK docstring follows existing template format
- Both files are consistent in structure

### Edge Cases
- Missing config variables (should use defaults)
- async_mode=true (should generate async version)
- async_mode=false or undefined (should generate sync version)
- DATABASE_URL environment variable set (should override config)

## Acceptance Criteria
- Template file created: `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`
- Reference file created: `src/shared/infrastructure/database.py`
- get_db() is a generator that closes session in finally block
- Supports sqlite and postgresql via DATABASE_URL environment variable
- Base is exported for model inheritance (Base = declarative_base())
- Template includes conditional async/sync support via config.project.async_mode
- Pool configuration included as commented examples
- IDK docstring follows existing template format
- Environment variable priority: DATABASE_URL env var → config.project.database_url → hardcoded sqlite default
- Rendered reference includes header comment explaining it's a template reference
- All Validation Commands pass

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions from Auto-Resolved Clarifications
1. **Single template approach**: Using conditional blocks instead of separate sync/async templates for easier maintenance
2. **SQLite default**: Provides instant prototyping without PostgreSQL setup
3. **No explicit error handling**: Let FastAPI handle database exceptions at application layer
4. **Environment-first config**: Following 12-factor app pattern for deployment
5. **Reference implementation**: Full rendered file in root serves as documentation
6. **Commented pool config**: Production options available but not forced on users
7. **No migration code**: Alembic setup is separate concern

### Future Enhancements
- Add Alembic migration initialization in separate template
- Add read replica configuration examples
- Add connection retry logic examples
- Create health check endpoint that tests database connection

### Related Tasks
- Task 1.1-1.5: Base classes (entity, schema, service, repository) - already completed
- Task 1.7: Template exceptions.py - next task, uses database sessions for error context
- Task 1.8-1.10: Additional infrastructure templates (responses, dependencies, health)
