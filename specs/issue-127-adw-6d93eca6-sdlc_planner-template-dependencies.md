# Feature: Template dependencies.py - FastAPI Dependency Injection Factories

## Metadata
issue_number: `127`
adw_id: `6d93eca6`
issue_json: `{"number":127,"title":"Tarea 1.9: Template dependencies.py","body":"/feature\n/adw_sdlc_zte_iso\n**Tipo**: feature\n**Ganancia**: Factory functions para dependency injection en FastAPI. Patron consistente para obtener servicios y repositorios en endpoints.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2`\n2. Crear renderizado en raiz: `src/shared/infrastructure/dependencies.py`\n2. Contenido:\n   - `get_db` reimportado de database.py (convenience)\n   - Pattern para crear service factories:\n     ```python\n     def get_service(db: Session = Depends(get_db)):\n         repository = Repository(db)\n         return Service(repository)\n     ```\n   - Ejemplo comentado de como agregar auth dependency\n3. El template debe ser extensible (los usuarios agregan sus propias factories)\n\n**Criterios de aceptacion**:\n- Patron Depends() de FastAPI usado correctamente\n- Ejemplo funcional incluido en comentarios\n# PLAN: TAC Bootstrap v0.3 - Version Robusta\n\n## Objetivo\n\nEvolucionar `tac_bootstrap_cli` de un generador de estructura agentic a una herramienta completa que tambien genera codigo de aplicacion (entidades CRUD con DDD), documentacion fractal automatica, y validacion multi-capa. Basado en los patrones documentados en `ai_docs/doc/create-crud-entity/`.\n\n## Estructura del Plan\n\n- **7 Fases**, **3 Iteraciones** de ejecucion\n- Cada tarea tiene: tipo (feature/chore/bug), descripcion, ganancia, instrucciones, criterios de aceptacion\n- Fases 1-5 (codigo) y Fases 6-7 (docs fractal) son independientes\n\n## REGLA CRITICA: Dual Creation Pattern\n\n**IMPORTANTE**: Este proyecto es TANTO el generador como un proyecto de referencia. Por lo tanto, cada tarea que cree un template DEBE crear DOS archivos:\n\n1. **Template Jinja2** en `tac_bootstrap_cli/tac_bootstrap/templates/` → usado por el CLI para generar en OTROS proyectos\n2. **Archivo renderizado** en la raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/`) → para que ESTE proyecto tambien lo tenga\n\n### Mapeo de rutas (template → archivo en raiz):\n\n| Template (tac_bootstrap_cli/tac_bootstrap/templates/) | Archivo en raiz (/Volumes/MAc1/Celes/tac_bootstrap/) |\n|---|---|\n| `shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |\n| `shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |\n| `shared/base_service.py.j2` | `src/shared/application/base_service.py` |\n| `shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |\n| `shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |\n| `shared/database.py.j2` | `src/shared/infrastructure/database.py` |\n| `shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |\n| `shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |\n| `shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |\n| `shared/health.py.j2` | `src/shared/api/health.py` |\n| `capabilities/crud_basic/domain_entity.py.j2` | *(se genera bajo demanda con `generate entity`)* |\n| `capabilities/crud_basic/schemas.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/service.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/repository.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/routes.py.j2` | *(se genera bajo demanda)* |\n| `capabilities/crud_basic/orm_model.py.j2` | *(se genera bajo demanda)* |\n| `scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |\n| `scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |\n| `scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |\n| `claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |\n| `config/canonical_idk.yml.j2` | `canonical_idk.yml` |\n\n### Excepcion: Templates de capabilities (crud_basic, crud_authorized)\nLos templates de `capabilities/` NO se renderizan automaticamente en la raiz. Solo se generan cuando el usuario ejecuta `tac-bootstrap generate entity <name>`. Por eso no tienen archivo en raiz.\n\n### Contexto: config.yml de ESTE proyecto\n\nEl archivo `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` contiene la configuracion real de este proyecto. Los templates usan estas variables con la sintaxis `{{ config.project.name }}`, `{{ config.paths.app_root }}`, etc.\n\n**Valores actuales relevantes para renderizado:**\n```yaml\nproject:\n  name: \"tac-bootstrap\"\n  language: \"python\"\n  framework: \"none\"         # NOTA: no es FastAPI, pero architecture=ddd\n  architecture: \"ddd\"\n  package_manager: \"uv\"\n\npaths:\n  app_root: \"tac_bootstrap_cli\"   # Codigo del CLI vive aqui\n  scripts_dir: \"scripts\"\n  adws_dir: \"adws\"\n\ncommands:\n  test: \"uv run pytest\"\n  lint: \"uv run ruff check .\"\n```\n\n**IMPORTANTE - Consideracion de framework:**\n- Este proyecto tiene `framework: \"none\"` (no es una app FastAPI, es un CLI)\n- Las base classes (Fase 1) son templates para proyectos FastAPI que el CLI GENERA\n- Para la dual creation en la raiz: renderizar los templates como **ejemplo/referencia** usando los valores de config.yml, pero los imports de FastAPI/SQLAlchemy son de referencia (no se ejecutan en este proyecto)\n- Los scripts de Fase 6 SI son funcionales en este proyecto (Python, language=python)\n\n### Como implementar la dual creation:\n1. Crear el template `.j2` con variables Jinja2 (`{{ config.project.name }}`, etc.)\n2. Para renderizar el archivo en raiz, usar los valores de `config.yml`:\n   - `config.project.name` → `\"tac-bootstrap\"`\n   - `config.project.language` → `\"python\"`\n   - `config.paths.app_root` → `\"tac_bootstrap_cli\"`\n   - `config.commands.test` → `\"uv run pytest\"`\n3. Guardar el resultado en la ruta correspondiente de la raiz\n4. Verificar que AMBOS archivos existen y son consistentes\n\n### Ejemplo concreto de renderizado:\n\n**Template** (`templates/scripts/run_generators.sh.j2`):\n```bash\nREPO_ROOT=\"{{ config.paths.app_root | default('.') }}\"\n```\n\n**Renderizado en raiz** (`scripts/run_generators.sh`):\n```bash\nREPO_ROOT=\"tac_bootstrap_cli\"\n```\n\n**Template** (`templates/config/canonical_idk.yml.j2`):\n```yaml\n# Canonical IDK Vocabulary for {{ config.project.name }}\n{% if config.project.language == \"python\" %}\n  backend:\n    - api-gateway, routing, ...\n{% endif %}\n```\n\n**Renderizado en raiz** (`canonical_idk.yml`):\n```yaml\n# Canonical IDK Vocabulary for tac-bootstrap\n  backend:\n    - api-gateway, routing, ..."} ## Auto-Resolved Clarifications\n\n**Summary:** Create a synchronous dependency injection template with get_db re-export, generic service factory pattern example, and commented auth example using FastAPI conventions. No error handling (delegated to database.py). Render to src/shared/infrastructure/dependencies.py using config.yml values. Include async example in comments for reference.\n\n**Q:** Should the template use synchronous or asynchronous database sessions (Session vs AsyncSession) for the Depends pattern, or should it support both with conditional rendering based on config.database.async?\n**A:** Use synchronous Session by default with a commented async example\n*TAC Bootstrap examples are predominantly synchronous. Conditional rendering adds complexity. A commented async example provides guidance without forcing a choice, letting users uncomment/modify as needed.*\n\n**Q:** What specific example service and repository should be included in the commented example? Should it reference a concrete entity (e.g., 'User') or use generic placeholders (e.g., 'Entity', 'Resource')?\n**A:** Use generic 'Example' placeholders (ExampleService, ExampleRepository)\n*Generic names maximize template reusability and avoid suggesting a specific domain model. Users can easily rename to their actual entities (UserService, ProductService, etc.).*\n\n**Q:** Should the template include error handling patterns for dependency injection failures (e.g., database connection errors in get_db), or assume base implementations handle this?\n**A:** Assume base implementations handle errors; no explicit error handling in dependencies.py\n*Error handling belongs in database.py's get_db function (created in Task 1.6). Dependencies.py should focus on factory patterns. Duplication would violate DRY and create maintenance burden.*\n\n**Q:** The auth dependency example should follow which pattern: JWT bearer tokens, API keys, OAuth2, or leave it as a generic 'verify_token' placeholder?\n**A:** Use generic 'get_current_user' with HTTPBearer pattern as commented example\n*HTTPBearer is FastAPI's standard security pattern and works with JWT, API keys, or custom tokens. Generic naming (get_current_user) is convention without prescribing implementation details.*\n\n**Q:** Should dependencies.py import from base_service.py and base_repository.py templates (created in earlier tasks), or use concrete example implementations?\n**A:** Show example pattern without importing base classes; use concrete example types in comments\n*dependencies.py is a pattern file, not an abstract base. Importing bases would create circular dependencies. Concrete examples in comments demonstrate the pattern users will implement with their actual services/repositories.*\n\n**Q:** Where exactly should the rendered file be placed: src/shared/infrastructure/dependencies.py (per instructions) or according to the mapping table which doesn't specify this path?\n**A:** Place at src/shared/infrastructure/dependencies.py\n*Instructions explicitly state 'Crear renderizado en raiz: src/shared/infrastructure/dependencies.py'. The mapping table doesn't contradict this. Infrastructure layer is correct location for FastAPI dependency factories per DDD.*`

## Feature Description
Create a dependency injection factories template for TAC Bootstrap CLI that generates dependencies.py files for FastAPI projects. This module serves as a centralized location for FastAPI dependency factory functions, following the Depends() pattern to inject services, repositories, and authentication into route handlers. The template provides a consistent, extensible pattern for dependency injection throughout the application.

The template re-exports get_db for convenience, demonstrates the service factory pattern with generic examples, and includes commented auth patterns. It follows the Dual Creation Pattern, creating both a Jinja2 template for CLI generation and a rendered reference implementation in the project root.

## User Story
As a developer using TAC Bootstrap CLI
I want to generate dependencies.py files with FastAPI dependency factories
So that my projects have a consistent, centralized pattern for injecting services, repositories, and authentication into endpoints

## Problem Statement
FastAPI projects require dependency injection factories to:
- Inject database sessions into route handlers
- Inject services and repositories with proper initialization
- Inject authentication/authorization dependencies
- Maintain separation of concerns between layers (API, application, infrastructure)
- Provide a single source of truth for dependency factory patterns

Currently, developers must manually create these factories or copy-paste patterns, leading to inconsistent implementations and potential issues with dependency lifecycle management.

## Solution Statement
Create a Jinja2 template (`dependencies.py.j2`) that generates a dependency injection factory module. The template:
- Re-exports get_db from database.py for convenience
- Demonstrates the service factory pattern using Depends(get_db) with generic ExampleService/ExampleRepository
- Includes commented patterns for async dependencies
- Includes commented HTTPBearer auth pattern with get_current_user example
- Uses IDK docstring format with clear examples
- Delegates error handling to base implementations (database.py, auth modules)
- Remains extensible so users can add their own factory functions

Following the Dual Creation Pattern, also render a reference implementation in `src/shared/infrastructure/dependencies.py` with synchronous Session pattern.

## Relevant Files
Files necessary for implementing the feature:

### Existing Files for Pattern Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` - For understanding get_db import pattern and IDK docstring format
- `src/shared/infrastructure/database.py` - To verify get_db function exists for re-export
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2` - For understanding service patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` - For understanding repository patterns
- `config.yml` - Project configuration with values for rendering (project.name, paths.app_root, etc.)

### Existing Reference Implementations
- `src/shared/infrastructure/database.py` - Contains get_db function that will be re-exported
- `src/shared/application/base_service.py` - Shows service initialization patterns
- `src/shared/infrastructure/base_repository.py` - Shows repository initialization patterns

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2` - Jinja2 template for dependency factories (PRIMARY)
- `src/shared/infrastructure/dependencies.py` - Rendered reference implementation in project root

## Implementation Plan

### Phase 1: Research and Pattern Analysis
- Read database.py template and rendered file to understand get_db function signature
- Read base_service.py and base_repository.py templates to understand initialization patterns
- Review existing database.py to understand Session vs AsyncSession patterns
- Review config.yml to identify configuration variables

### Phase 2: Create Template
- Create `dependencies.py.j2` with:
  - IDK docstring following existing template format with comprehensive examples
  - Re-export of get_db from database.py (convenience import)
  - Generic service factory example using Depends(get_db) pattern
  - Commented async factory example for reference
  - Commented HTTPBearer auth example with get_current_user pattern
  - Clear usage examples in docstring showing route handler integration
  - Explanation of extensibility (users add their own factories)
- Focus on synchronous Session pattern by default
- No error handling (delegated to database.py and base implementations)

### Phase 3: Render Reference Implementation
- Render the template using values from config.yml:
  - `config.project.name` → "tac-bootstrap"
  - Synchronous mode (no async_mode set)
- Add header comment: "# Reference implementation - generated from dependencies.py.j2 template"
- Add clarifying comment: "# This file serves as documentation for the dependencies.py template output"
- Add clarifying comment: "# Not used by the CLI itself (tac-bootstrap has framework="none")"
- Save to `src/shared/infrastructure/dependencies.py`
- Ensure directory exists (create if needed)

### Phase 4: Validation
- Verify template file exists and is valid Jinja2
- Verify rendered file exists with correct content
- Check that both files follow existing code patterns (IDK docstring, import organization)
- Verify get_db re-export is correct
- Verify commented examples are clear and follow FastAPI conventions
- Validate that the pattern is extensible and self-documenting

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Research Existing Patterns
- Read `src/shared/infrastructure/database.py` to understand:
  - get_db function signature (Generator returning Session)
  - Import path for re-export
  - Whether it's sync or async
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2` to understand:
  - How async mode is conditionally rendered
  - IDK docstring format and structure
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2` to understand:
  - Service initialization patterns (takes repository in __init__)
  - Constructor signature patterns
- Read `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` to understand:
  - Repository initialization patterns (takes session in __init__)
  - Constructor signature patterns
- Read `config.yml` to verify project configuration structure

### Task 2: Create Jinja2 Template
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/shared/` if it doesn't exist (it should already exist)
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2` with:
  - Comprehensive IDK docstring explaining:
    - Module purpose: centralized dependency injection factories
    - Key components: get_db re-export, service factory pattern, auth pattern
    - Responsibility: provide factory functions for FastAPI Depends()
    - Invariants: each factory creates fresh instances, no error handling (delegated)
    - Usage examples showing route handler integration
    - Extensibility explanation
    - Collaborators: FastAPI Depends(), database.py, service/repository layers
  - Import get_db from database module:
    ```python
    from src.shared.infrastructure.database import get_db
    ```
  - Re-export get_db for convenience (so routes can import from dependencies.py)
  - Generic service factory example with complete pattern:
    ```python
    # Example service factory pattern
    # def get_example_service(db: Session = Depends(get_db)) -> ExampleService:
    #     """
    #     Factory for ExampleService with dependency injection.
    #
    #     Args:
    #         db: Database session injected by FastAPI
    #
    #     Returns:
    #         ExampleService: Configured service instance
    #
    #     Usage:
    #         @router.get("/examples")
    #         def list_examples(service: ExampleService = Depends(get_example_service)):
    #             return service.list_all()
    #     """
    #     repository = ExampleRepository(db)
    #     return ExampleService(repository)
    ```
  - Commented async factory example for reference:
    ```python
    # Async version (uncomment if using async_mode):
    # async def get_example_service_async(db: AsyncSession = Depends(get_db)) -> ExampleService:
    #     repository = ExampleRepository(db)
    #     return ExampleService(repository)
    ```
  - Commented HTTPBearer auth example:
    ```python
    # Example auth dependency pattern
    # from fastapi.security import HTTPBearer
    # security = HTTPBearer()
    #
    # def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    #     """
    #     Authenticate user from bearer token.
    #
    #     Args:
    #         credentials: HTTP authorization credentials
    #
    #     Returns:
    #         User: Authenticated user
    #
    #     Raises:
    #         HTTPException: 401 if token invalid
    #
    #     Usage:
    #         @router.get("/protected")
    #         def protected_route(user: User = Depends(get_current_user)):
    #             return {"user_id": user.id}
    #     """
    #     token = credentials.credentials
    #     # Implement token verification logic
    #     # user = verify_token(token)
    #     # if not user:
    #     #     raise HTTPException(status_code=401, detail="Invalid token")
    #     # return user
    #     pass
    ```
  - Clear section comments explaining where users add their own factories
  - Imports section with proper organization (standard library, third-party, local)

### Task 3: Render Reference Implementation
- Read config.yml to get actual configuration values
- Create directory `src/shared/infrastructure/` if it doesn't exist (it should already exist)
- Render the template with values from config.yml:
  - Project name: "tac-bootstrap"
  - Use synchronous mode (no async_mode configured)
- Add header comments:
  ```python
  # Reference implementation - generated from dependencies.py.j2 template
  # This file serves as documentation for the dependencies.py template output
  # Not used by the CLI itself (tac-bootstrap has framework="none")
  ```
- Write rendered content to `src/shared/infrastructure/dependencies.py`
- Verify file was created successfully

### Task 4: Verify Dual Creation
- Verify template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2`
- Verify rendered file exists at `src/shared/infrastructure/dependencies.py`
- Verify both files are consistent (rendered matches template with config.yml values substituted)
- Verify get_db re-export matches database.py function signature
- Verify commented examples follow FastAPI conventions
- Verify IDK docstring is comprehensive and matches format of other templates

### Task 5: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Fix any issues found during validation
- Confirm all tests pass

## Testing Strategy

### Unit Tests
No unit tests required for this template task. The template itself will be tested when:
- CLI generates projects using this template (integration test)
- Generated dependencies.py files are used in actual FastAPI projects

### Edge Cases
- Template should work for both sync and async modes
- Template should be extensible without modification
- Commented examples should be syntactically valid Python when uncommented
- IDK docstring should provide clear guidance for all common patterns

## Acceptance Criteria
1. Template file `dependencies.py.j2` exists with:
   - Re-export of get_db from database.py
   - Generic service factory example using Depends(get_db) pattern
   - Commented async factory example
   - Commented HTTPBearer auth example with get_current_user
   - Comprehensive IDK docstring with usage examples
   - Clear extensibility guidance
2. Rendered file `src/shared/infrastructure/dependencies.py` exists with:
   - Header comments explaining it's a reference implementation
   - Synchronous Session pattern (matching config.yml)
   - All content properly rendered from template
3. Both files follow existing code patterns (IDK docstring, import organization)
4. Depends() pattern used correctly (FastAPI convention)
5. No error handling in dependencies.py (delegated to base implementations)
6. Examples are clear, generic, and easily adaptable
7. All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This template complements database.py (created in Task 1.6) by providing factory patterns for services and repositories
- The template is designed to be self-documenting through comprehensive IDK docstrings and commented examples
- Error handling is intentionally absent - get_db handles database errors, auth functions handle auth errors
- The generic "Example" placeholder names (ExampleService, ExampleRepository) are meant to be replaced by users with their actual entity names (UserService, ProductService, etc.)
- The commented examples are syntactically valid and can be uncommented/modified as needed
- This follows the separation of concerns: database.py handles sessions, dependencies.py handles injection, routes use the factories
- The HTTPBearer pattern is FastAPI's standard and works with JWT, API keys, or custom tokens
- Async support is provided through commented examples rather than conditional rendering to keep the template simple
