# Chore: Actualizar README.md con nuevos comandos y guias

## Metadata
issue_number: `187`
adw_id: `chore_8_1`
issue_json: `{"number":187,"title":"Tarea 8.1: Actualizar README.md con nuevos comandos y guias","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_8_1\n\n**Tipo**: chore\n**Ganancia**: Los usuarios nuevos y existentes tienen documentacion completa de `generate entity`, documentacion fractal, base classes, y validacion multi-capa sin buscar en el codigo.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/README.md`\n2. Agregar las siguientes secciones NUEVAS:\n\n### Seccion: Comando `generate entity`\nAgregar despues de la seccion \"Utility Commands\":\n```markdown\n### Entity Generation (DDD Projects)\n\nGenerate complete CRUD entities with vertical slice architecture:\n\n\\`\\`\\`bash\n# Interactive wizard (recommended)\ntac-bootstrap generate entity Product\n\n# Non-interactive with fields\ntac-bootstrap generate entity Product \\\n  --capability catalog \\\n  --fields \"name:str:required,price:float:required,description:text,is_available:bool\" \\\n  --no-interactive\n\n# With authorization (row-level security)\ntac-bootstrap generate entity Order \\\n  --capability orders \\\n  --fields \"total:decimal:required,status:str:required\" \\\n  --authorized \\\n  --no-interactive\n\n# Preview without creating files\ntac-bootstrap generate entity User --dry-run\n\n# Force overwrite existing entity\ntac-bootstrap generate entity Product -c catalog --force\n\\`\\`\\`\n\n#### Available Options for `generate entity`\n\n| Option | Short | Description |\n|--------|-------|-------------|\n| `--capability` | `-c` | Capability/module name (default: entity name in kebab-case) |\n| `--fields` | `-f` | Field definitions: \"name:type[:required]\" comma-separated |\n| `--authorized` | | Generate with row-level security templates |\n| `--async` | | Use async repository (AsyncSession) |\n| `--with-events` | | Generate domain events |\n| `--interactive` | | Interactive wizard (default) |\n| `--dry-run` | | Preview without creating files |\n| `--force` | | Overwrite existing entity files |\n\n#### Field Types\n\n| Type | Python Type | SQLAlchemy Type |\n|------|------------|-----------------|\n| `str` | `str` | `String(max_length)` |\n| `int` | `int` | `Integer` |\n| `float` | `float` | `Float` |\n| `bool` | `bool` | `Boolean` |\n| `datetime` | `datetime` | `DateTime` |\n| `uuid` | `str` | `String(36)` |\n| `text` | `str` | `Text` |\n| `decimal` | `Decimal` | `Numeric` |\n| `json` | `dict` | `JSON` |\n\n#### Generated Structure\n\n\\`\\`\\`\nsrc/{capability}/\n├── domain/\n│   └── {entity}.py          # Domain model (extends BaseEntity)\n├── application/\n│   ├── schemas.py            # Create/Update/Response DTOs\n│   └── service.py            # CRUD service (extends BaseService)\n├── infrastructure/\n│   ├── models.py             # SQLAlchemy ORM model\n│   └── repository.py         # Data access (extends BaseRepository)\n└── api/\n    └── routes.py             # FastAPI CRUD endpoints\n\\`\\`\\`\n\n> **Requirement**: Entity generation requires `--architecture ddd|clean|hexagonal` and `--framework fastapi`. The shared base classes in `src/shared/` must exist (generated automatically with `init`).\n```\n\n### Seccion: Base Classes (DDD)\nAgregar despues de \"Generated Structure\":\n```markdown\n### Shared Base Classes (DDD Architecture)\n\nWhen using `--architecture ddd` with `--framework fastapi`, the CLI generates shared infrastructure in `src/shared/`:\n\n| File | Purpose |\n|------|---------|\n| `domain/base_entity.py` | Entity base with audit trail, soft delete, state management |\n| `domain/base_schema.py` | BaseCreate, BaseUpdate, BaseResponse DTOs |\n| `application/base_service.py` | Generic CRUD service with typed generics |\n| `infrastructure/base_repository.py` | Generic SQLAlchemy repository (sync) |\n| `infrastructure/base_repository_async.py` | Generic async repository |\n| `infrastructure/database.py` | SQLAlchemy session management |\n| `infrastructure/exceptions.py` | Typed exceptions with HTTP handlers |\n| `infrastructure/responses.py` | PaginatedResponse, ErrorResponse models |\n| `infrastructure/dependencies.py` | FastAPI dependency injection factories |\n| `api/health.py` | Health check endpoint |\n\nThese classes eliminate ~80% of boilerplate per entity. Each new entity inherits from them.\n```\n\n### Seccion: Fractal Documentation\nAgregar despues de \"ADW\" section:\n```markdown\n## Fractal Documentation\n\nProjects include automatic documentation generation tools:\n\n### Generate Documentation\n\n\\`\\`\\`bash\n# Run fractal documentation generators\nbash scripts/run_generators.sh\n\n# Only process changed files\nbash scripts/run_generators.sh --changed-only\n\n# Preview without writing\nbash scripts/run_generators.sh --dry-run\n\\`\\`\\`\n\n### What It Does\n\n1. **Step 1: Docstring Enrichment** (`gen_docstring_jsdocs.py`)\n   - Adds IDK-first docstrings to Python/TypeScript files\n   - Keywords, Responsibility, Invariants, Failure Modes\n\n2. **Step 2: Fractal Docs** (`gen_docs_fractal.py`)\n   - Generates one markdown per folder in `docs/`\n   - Bottom-up processing (deeper folders first)\n   - Frontmatter with IDK keywords, tags, and relationships\n\n### Slash Command\n\nUse `/generate_fractal_docs` in Claude Code:\n\\`\\`\\`\n/generate_fractal_docs changed   # Only changed files\n/generate_fractal_docs full      # All files\n\\`\\`\\`\n\n### Canonical IDK Vocabulary\n\nEdit `canonical_idk.yml` to define approved keywords for your domain. The generators use this vocabulary for consistent terminology across all documentation.\n```\n\n### Seccion: Validation\nAgregar en la seccion de Commands:\n```markdown\n### Multi-layer Validation\n\nThe CLI validates configurations in multiple layers before generating:\n\n1. **Schema** - Pydantic type validation\n2. **Domain** - Framework/language compatibility rules\n3. **Template** - Referenced templates exist\n4. **Filesystem** - Output directory writable, no conflicts\n5. **Git** - Repository state warnings\n```\n\n3. Actualizar la tabla de \"Requirements\" para incluir nuevas dependencias opcionales:\n```markdown\n## Requirements\n\n- Python 3.10+\n- Git\n- Claude Code CLI\n- SQLAlchemy (for generated DDD projects)\n- FastAPI (for generated API projects)\n\n### Optional (for Fractal Documentation)\n\n- OpenAI-compatible API (Ollama local recommended)\n- `OPENAI_BASE_URL` and `OPENAI_API_KEY` environment variables\n```\n\n4. Actualizar la version mencionada en el README de `v0.2.2` a `v0.3.0`\n\n**Criterios de aceptacion**:\n- README tiene seccion de `generate entity` con ejemplos completos\n- README tiene seccion de base classes con tabla de archivos\n- README tiene seccion de fractal documentation con uso\n- README tiene seccion de validacion multi-capa\n- Todas las versiones actualizadas a 0.3.0\n- Ejemplos de comandos son copy-pasteable y funcionales\n\n\n# FASE 8: Documentacion y Release\n\n**Objetivo**: Actualizar README con guias de los nuevos comandos y features, y crear CHANGELOG con todos los cambios de la v0.3.\n\n**Ganancia de la fase**: Los usuarios encuentran documentacion completa de las nuevas funcionalidades sin tener que leer el codigo. El CHANGELOG da visibilidad de todo lo que cambio respecto a v0.2.x.\n"}`

## Chore Description

Actualizar el `README.md` del TAC Bootstrap CLI para documentar las nuevas funcionalidades de la versión 0.3.0:
1. Comando `generate entity` con ejemplos y opciones completas
2. Base Classes generadas para arquitectura DDD
3. Fractal Documentation (docstring enrichment + fractal docs)
4. Validación multi-capa del CLI
5. Actualización de versiones de `v0.2.2` a `v0.3.0`

Esta documentación permite a los usuarios descubrir y usar las nuevas features sin tener que revisar el código fuente.

## Relevant Files

### Files to Modify

- `tac_bootstrap_cli/README.md` - README principal que requiere:
  - Nueva sección "Entity Generation (DDD Projects)" después de "Utility Commands" (línea 262)
  - Nueva sección "Shared Base Classes (DDD Architecture)" después de la estructura de entity generation
  - Nueva sección "Fractal Documentation" después de la sección "ADW" (línea 543)
  - Nueva sección "Multi-layer Validation" en la sección Commands (línea 301)
  - Actualización de Requirements (línea 577) para agregar dependencias opcionales
  - Actualización de todas las referencias a versión de `v0.2.2` a `v0.3.0` (líneas 21, 38, 111)

### Reference Files (for context)

- `.claude/commands/conditional_docs.md` - Documentación condicional para entender el sistema de documentación fractal
- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro que define las fases del proyecto (contexto de Fase 8)

### New Files

Ningún archivo nuevo requerido, solo modificación del README existente.

## Step by Step Tasks

### Task 1: Leer el README actual y planificar las inserciones

- Leer `tac_bootstrap_cli/README.md` completo
- Identificar los puntos exactos de inserción para cada sección nueva
- Verificar la estructura markdown existente para mantener consistencia

### Task 2: Agregar sección "Entity Generation (DDD Projects)"

- Insertar después de la sección "Utility Commands" (después de línea 262)
- Incluir ejemplos de uso interactivo y no-interactivo
- Documentar todas las opciones con tabla completa
- Incluir tabla de Field Types con mapeo Python/SQLAlchemy
- Mostrar estructura de archivos generados
- Agregar nota de requerimientos (architecture ddd + framework fastapi)

### Task 3: Agregar sección "Shared Base Classes (DDD Architecture)"

- Insertar inmediatamente después de la estructura de entity generation
- Crear tabla con todos los archivos base en `src/shared/`
- Describir el propósito de cada clase base
- Destacar el beneficio de reducción de boilerplate (~80%)

### Task 4: Agregar sección "Fractal Documentation"

- Insertar después de la sección "ADW" (después de línea 543)
- Documentar el comando `bash scripts/run_generators.sh` con opciones
- Explicar los dos pasos: docstring enrichment + fractal docs
- Incluir ejemplos del slash command `/generate_fractal_docs`
- Mencionar `canonical_idk.yml` para vocabulario IDK

### Task 5: Agregar sección "Multi-layer Validation"

- Insertar en la sección "Commands" (cerca de línea 301)
- Listar las 5 capas de validación:
  1. Schema (Pydantic)
  2. Domain (Framework compatibility)
  3. Template (Template existence)
  4. Filesystem (Directory writable)
  5. Git (Repository state)

### Task 6: Actualizar sección Requirements

- Modificar la sección existente (línea 577)
- Agregar SQLAlchemy y FastAPI como dependencias para proyectos generados
- Agregar subsección "Optional (for Fractal Documentation)"
- Listar OpenAI-compatible API y variables de entorno necesarias

### Task 7: Actualizar todas las versiones de v0.2.2 a v0.3.0

- Buscar todas las ocurrencias de `v0.2.2` en el README
- Reemplazar con `v0.3.0` en:
  - Línea 21: `git clone --branch v0.2.2`
  - Línea 38: `git clone --branch v0.2.2`
  - Línea 111: `git clone --branch v0.2.2`

### Task 8: Validar la documentación

- Verificar que todos los ejemplos de código son copy-pasteable
- Confirmar que las tablas markdown están correctamente formateadas
- Revisar que los enlaces internos funcionan
- Ejecutar Validation Commands para verificar que no se rompió nada

### Task 9: Ejecutar Validation Commands

- Correr todos los comandos de validación para confirmar cero regresiones
- Verificar que el CLI sigue funcionando correctamente

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- Mantener el tono y estilo del README existente
- Los ejemplos deben ser funcionales y realistas
- Las tablas deben estar alineadas correctamente para mejor legibilidad
- Esta es documentación de la versión 0.3.0, que representa un salto significativo en funcionalidad respecto a 0.2.2
- La sección de Entity Generation es una de las features más importantes de esta versión
- Los usuarios deben poder copiar-pegar los comandos y que funcionen de inmediato
