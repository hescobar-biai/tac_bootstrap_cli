# TAC Bootstrap

CLI en Python que crea o inyecta una **Agentic Layer** basada en Claude Code para acelerar ingenieria con patrones TAC (Tactical Agentic Coding).

## Problema que Resuelve

Muchos equipos usando IA siguen trabajando "en loop" (chat/IDE) y no logran:
- Estandarizar prompts de ingenieria
- Orquestar flujos repetibles (plan/build/test/review/ship)
- Ejecutar en paralelo (worktrees / entornos aislados)
- Tener trazabilidad completa (logs, specs, evidencias)
- Integrar triggers automaticos (cron/webhook/tareas)

## Solucion

TAC Bootstrap genera automaticamente toda la infraestructura agentica:

```
proyecto/
├── .claude/                    # Configuracion Claude Code
│   ├── settings.json           # Permisos y hooks
│   ├── commands/               # 25+ comandos slash
│   │   ├── prime.md            # Priming del agente
│   │   ├── feature.md          # Planificacion features
│   │   ├── implement.md        # Ejecucion de planes
│   │   ├── experts/            # Agent Experts (TAC-13)
│   │   └── ...
│   └── hooks/                  # Automatizacion
│       ├── pre_tool_use.py     # Validacion pre-ejecucion
│       └── post_tool_use.py    # Logging post-ejecucion
├── adws/                       # AI Developer Workflows
│   ├── adw_modules/            # Modulos compartidos
│   ├── adw_sdlc_iso.py         # Workflow SDLC completo
│   └── adw_triggers/           # Triggers automaticos
├── scripts/                    # Scripts de utilidad
├── specs/                      # Especificaciones
├── logs/                       # Logs de sesiones
└── config.yml                  # Fuente de verdad
```

## Comandos

```bash
# Crear proyecto nuevo con Agentic Layer
tac-bootstrap init my-project

# Inyectar Agentic Layer en proyecto existente
tac-bootstrap add-agentic --repo .

# Validar setup
tac-bootstrap doctor --repo .

# Re-generar desde config.yml
tac-bootstrap render --config config.yml

# Actualizar proyecto existente a la última versión
tac-bootstrap upgrade
```

## Actualizar Proyectos Existentes

Si tienes un proyecto creado con una versión anterior de TAC Bootstrap, puedes actualizarlo a los templates más recientes:

```bash
# Verificar qué se actualizaría
tac-bootstrap upgrade --dry-run

# Actualizar con backup (por defecto)
tac-bootstrap upgrade

# Actualizar sin backup
tac-bootstrap upgrade --no-backup

# Forzar actualización aunque las versiones coincidan
tac-bootstrap upgrade --force

# Actualizar proyecto específico
tac-bootstrap upgrade ./path/to/project
```

### Qué se Actualiza

El comando upgrade actualiza:
- `adws/` - AI Developer Workflows
- `.claude/` - Configuración de Claude Code
- `scripts/` - Scripts de utilidad

Se preserva:
- `src/` - Tu código de aplicación
- `config.yml` - Tu configuración (solo se actualiza la versión)
- Cualquier archivo personalizado que hayas agregado

### Backup

Por defecto, se crea un backup en `.tac-backup-{timestamp}/` antes de actualizar.
Elimínalo manualmente después de confirmar que la actualización funciona correctamente.

## Flujo de Usuario

```
tac-bootstrap init
       |
       v
¿Proyecto NUEVO o EXISTENTE?
       |
   [NUEVO]              [EXISTENTE]
       |                     |
       v                     v
  Pregunta:            Auto-detecta:
  - Lenguaje           - Lenguaje
  - Framework          - Framework
  - Arquitectura       - Package manager
  - Comandos
       |                     |
       v                     v
    GENERA AGENTIC LAYER
       |
       v
  Proyecto listo para
  trabajar con agentes!
```

## Stack Soportado

| Lenguaje | Frameworks | Package Managers |
|----------|------------|------------------|
| Python | FastAPI, Django, Flask | uv, poetry, pip |
| TypeScript | Next.js, Nest.js, Express | pnpm, npm, bun |
| JavaScript | Next.js, Express, React | pnpm, npm, bun |
| Go | Gin, Echo | go |

## Arquitecturas Soportadas

- **Simple** - Estructura plana
- **Layered** - Controllers/Services/Repositories
- **DDD** - Domain-Driven Design
- **Clean** - Clean Architecture
- **Hexagonal** - Ports & Adapters

---

## Desarrollo del Generador

Este repositorio contiene el codigo fuente del generador TAC Bootstrap.

### Estructura del Generador

```
tac_bootstrap/
├── .claude/                    # [TEMPLATE] Comandos y hooks de ejemplo
│   ├── commands/               # 25+ comandos slash como templates
│   └── hooks/                  # Hooks Python como templates
├── adws/                       # [TEMPLATE] AI Developer Workflows
│   ├── adw_modules/            # Modulos reutilizables
│   └── adw_triggers/           # Triggers para automatizacion
├── scripts/                    # [TEMPLATE] Scripts de utilidad
├── ai_docs/                    # Documentacion de referencia (TAC 1-8)
├── PLAN_TAC_BOOTSTRAP.md       # Plan de implementacion detallado
└── tac_bootstrap_cli/          # [A CREAR] CLI Python del generador
    ├── domain/models.py        # Modelos Pydantic
    ├── application/            # Servicios (scaffold, detect, doctor)
    ├── infrastructure/         # Templates Jinja2, filesystem
    └── interfaces/cli.py       # Comandos Typer
```

### Plan de Implementacion

Ver [PLAN_TAC_BOOTSTRAP.md](PLAN_TAC_BOOTSTRAP.md) para el plan completo con:
- 9 fases de desarrollo
- Cada tarea como prompt para agente LLM
- Codigo de templates completo
- Criterios de aceptacion

### Desarrollo con Agentic Coding

Cada tarea del plan esta escrita como un prompt completo. Para implementar:

```bash
# 1. Abrir el plan
cat PLAN_TAC_BOOTSTRAP.md

# 2. Copiar el prompt de la tarea (ej: TAREA 1.1)
# 3. Ejecutar con Claude Code
claude -p "[prompt de la tarea]"

# 4. Verificar criterios de aceptacion
# 5. Continuar con siguiente tarea
```

### Comandos Disponibles (Desarrollo)

```bash
# Slash commands para desarrollo
/prime              # Preparar contexto del proyecto
/feature            # Planificar nueva funcionalidad
/implement <plan>   # Ejecutar un plan
/test               # Correr tests
/commit             # Crear commit

# ADW Workflows
uv run adws/adw_sdlc_iso.py --issue 123
uv run adws/adw_patch_iso.py --issue 456 --fix "descripcion"
```

### Development with Makefile

El CLI incluye un `Makefile` en `tac_bootstrap_cli/` con comandos convenientes para desarrollo.

#### Quick Commands

| Comando | Descripción |
|---------|-------------|
| `make install` | Instalar dependencias |
| `make install-dev` | Instalar con dependencias de desarrollo |
| `make dev` | Ejecutar CLI en modo desarrollo (smoke test) |
| `make lint` | Verificar código con ruff |
| `make lint-fix` | Verificar código con auto-fix |
| `make format` | Formatear código con ruff |
| `make typecheck` | Verificar tipos con mypy |
| `make test` | Correr todos los tests |
| `make test-v` | Correr tests con salida verbose |
| `make test-cov` | Correr tests con reporte de coverage |
| `make test-watch` | Correr tests en modo watch |
| `make build` | Construir paquete wheel |
| `make clean` | Limpiar archivos generados y caches |
| `make cli-help` | Mostrar ayuda del CLI |
| `make cli-version` | Mostrar versión del CLI |
| `make help` | Mostrar todos los comandos disponibles |

#### Development Workflow

1. Clonar el repositorio
   ```bash
   git clone <repo-url>
   cd tac_bootstrap
   ```

2. Instalar dependencias de desarrollo
   ```bash
   cd tac_bootstrap_cli
   make install-dev
   ```

3. Hacer cambios en el código

4. Verificar y formatear código
   ```bash
   make lint format
   ```

5. Ejecutar tests
   ```bash
   make test
   ```

6. Hacer commit de cambios
   ```bash
   git add .
   git commit -m "descripcion del cambio"
   ```

#### Running the CLI locally

```bash
# Ver ayuda general
make cli-help

# Ver versión
make cli-version

# Probar comando init (ejemplo)
uv run tac-bootstrap init my-project --dry-run

# Probar comando doctor (ejemplo)
uv run tac-bootstrap doctor
```

**Nota:** Los comandos `make` deben ejecutarse desde el directorio `tac_bootstrap_cli/` o usando `make -C tac_bootstrap_cli <target>` desde la raíz del repositorio.

### Publicar CLI al Repositorio de Distribución

El CLI se distribuye en un repositorio separado usando **git subtree**. Esto permite mantener el desarrollo en el monorepo pero publicar solo el CLI.

#### Configuración Inicial (ya realizada)

```bash
# Remote de distribución
git remote add tac-cli-dist https://github.com/celes-app/tac-cli-dist.git
```

#### Publicar Cambios

Después de hacer cambios en `tac_bootstrap_cli/`:

```bash
# 1. Commit tus cambios normalmente
git add .
git commit -m "feat: descripcion del cambio"

# 2. Push al monorepo (origin)
git push origin main

# 3. Sincronizar al repo de distribución
git subtree push --prefix=tac_bootstrap_cli tac-cli-dist main
```

#### Crear un Release

Después de sincronizar cambios importantes:

```bash
# 1. Actualizar versión en pyproject.toml (tac_bootstrap_cli/pyproject.toml)
# version = "0.2.0"

# 2. Commit y sincronizar
git add . && git commit -m "chore: bump version to 0.2.0"
git push origin main
git subtree push --prefix=tac_bootstrap_cli tac-cli-dist main

# 3. Crear release en GitHub
gh release create v0.2.0 \
  --repo celes-app/tac-cli-dist \
  --title "v0.2.0" \
  --notes "Release notes aquí"
```

> **Nota**: El tag en el README del CLI (`git clone --branch v0.1.0`) debe actualizarse cuando se crea un nuevo release.

#### Repositorios

| Repositorio | URL | Contenido |
|-------------|-----|-----------|
| Monorepo (desarrollo) | `hescobar-biai/tac_bootstrap_cli` | Todo el proyecto |
| Distribución (público) | `celes-app/tac-cli-dist` | Solo `tac_bootstrap_cli/` |

---

## Arquitectura Interna

### Modelos de Dominio

```python
# config.yml -> TACConfig
TACConfig
├── project: ProjectSpec       # nombre, lenguaje, framework, arquitectura
├── paths: PathsSpec           # rutas de directorios
├── commands: CommandsSpec     # start, test, lint, build
├── agentic: AgenticSpec       # worktrees, logging, safety
└── claude: ClaudeConfig       # settings.json, comandos
```

### Flujo de Generacion

```
config.yml
    |
    v
TACConfig (Pydantic validation)
    |
    v
ScaffoldService.build_plan()
    |
    v
ScaffoldPlan (lista de operaciones)
    |
    v
ScaffoldService.apply_plan()
    |
    v
Templates Jinja2 renderizados
    |
    v
Archivos generados en disco
```

## TAC-12 Integration

TAC-12 transforms TAC Bootstrap into a complete agentic engineering platform with four core capabilities:

**Agents** - Advanced orchestration with isolated workflows (`adw_*_iso.py` scripts) that enable parallel execution, safety isolation, and complete traceability. Each workflow runs independently in its own context.

**Hooks** - Automated validation, logging, and event handling through hook scripts in `.claude/hooks/`. Hooks intercept tool execution, validate inputs, log outcomes, and send notifications—creating a complete feedback loop.

**Observability** - KPI tracking and state management utilities providing visibility into agentic execution. Track metrics like execution time, tool invocations, and decision outcomes.

**Agent Experts (TAC-13)** - Self-improving agents that evolve domain-specific mental models through an ACT → LEARN → REUSE loop. Expert agents maintain expertise files (max 1000 lines YAML) that capture patterns, decisions, and institutional knowledge for high-risk domains like security, billing, and complex architectures.

### Quick Start

Run your first TAC-12 workflow:

```bash
uv run adws/adw_sdlc_iso.py --issue 123
```

This executes a complete SDLC workflow: plan → implement → test → review → ship.

For comprehensive guidance, see [CLAUDE.md](CLAUDE.md) for development commands, [adws/README.md](adws/README.md) for workflow details, and [ai_docs/](ai_docs/) for the complete TAC course.

---

## Referencia: Curso TAC

Este proyecto implementa los conceptos del curso **Tactical Agentic Coding (TAC)**:

| Leccion | Concepto | Implementacion |
|---------|----------|----------------|
| TAC-1 | Stop Coding | CLI genera codigo, no lo escribes |
| TAC-2 | KPIs Agenticos | Tracking en adw_modules |
| TAC-3 | Templates | .claude/commands/*.md |
| TAC-4 | ADWs | adws/*.py workflows |
| TAC-5 | Feedback Loops | hooks/ + tests |
| TAC-6 | Review & Document | /review, /document |
| TAC-7 | Zero-Touch | adw_sdlc_zte_iso.py |
| TAC-8 | Prioritize Agentics | 50%+ tiempo en capa agentica |
| TAC-13 | Agent Experts | .claude/commands/experts/ |

Ver [ai_docs/doc/](ai_docs/doc/) para documentacion completa del curso.

---

## Orchestrator Test 3

Test 3 validates the complete orchestrator v2 workflow with database persistence, multi-agent coordination, and real-time WebSocket streaming capabilities.

### What Test 3 Validates

- **Database Persistence**: Agent logs, chat history, and orchestrator state are stored in PostgreSQL
- **Multi-Agent Workflows**: Multiple agents can be created and managed concurrently
- **WebSocket Streaming**: Real-time message delivery between frontend and backend
- **Session Management**: Chat sessions maintain continuity across page refreshes
- **Cost Tracking**: Token usage and USD costs are accumulated correctly
- **Event Streaming**: Agent events, thinking blocks, and tool usage are captured and broadcast

### Running Test 3

```bash
# 1. Ensure database migrations are applied
uv run python apps/orchestrator_db/run_migrations.py

# 2. Start the orchestrator backend
cd apps/orchestrator_3_stream
./start_be.sh

# 3. In another terminal, start the frontend
./start_fe.sh

# 4. Open browser to http://127.0.0.1:5175

# 5. Send messages and verify:
#    - Chat history loads from database
#    - Responses stream in real-time via WebSocket
#    - Messages persist after page refresh
#    - Typing indicators appear during processing
#    - Cost information updates correctly
```

### Verification Steps

1. **Chat Interface Works**: Type a message and see the response appear in real-time
2. **Database Persistence**: Refresh the page - chat history loads automatically
3. **WebSocket Streaming**: Response chunks appear immediately (not buffered)
4. **Multi-Turn Conversation**: Multiple messages maintain context correctly
5. **Session Continuity**: Resume session with `--session <id>` flag after restart

### Example Conversation

```
User: Create an agent called "builder"
Orchestrator: [via Claude SDK] Created agent 'builder'

User: Ask builder to create a Python script
Orchestrator: [dispatches task to builder, streams response]

User: What tasks are pending?
Orchestrator: [queries agent database, shows status]
```

### Architecture Overview

**Backend** (FastAPI + PostgreSQL + asyncpg):
- `apps/orchestrator_3_stream/backend/main.py` - WebSocket server and REST endpoints
- `apps/orchestrator_3_stream/backend/modules/orchestrator_service.py` - Claude SDK integration
- `apps/orchestrator_3_stream/backend/modules/database.py` - PostgreSQL operations
- Real-time event streaming via WebSocket `/ws` endpoint

**Frontend** (Vue 3 + TypeScript + Pinia):
- `apps/orchestrator_3_stream/frontend/src/components/OrchestratorChat.vue` - Chat UI
- `apps/orchestrator_3_stream/frontend/src/stores/orchestratorStore.ts` - State management
- Auto-scroll during message send and streaming
- Typing indicators and connection status display

### References

- **Implementation**: `apps/orchestrator_3_stream/README.md` (complete feature documentation)
- **Database Schema**: `apps/orchestrator_db/README.md`
- **Test Details**: See full E2E test results in orchestrator_3_stream README

## Licencia

MIT

ROLE:
You are an autonomous software engineering agent acting as:
- Senior Software Engineer
- Technical Project Manager
- Release Manager

You have full ownership over task decomposition, technical accuracy, execution ordering, and release hygiene.
Do NOT ask questions. Make reasonable technical assumptions when required.
If assumptions are needed, they MUST be documented explicitly in an "Assumptions" section inside the plan.

---

## OBJECTIVE

Create a **detailed, execution-ready task plan** in Markdown format that defines **all required repository changes**, including:

- Root changes
- CLI scaffolding changes
- Template creation and registration
- Documentation updates
- Parallel execution strategy
- Release versioning and changelog update

The output MUST be directly usable as:
- An execution checklist
- An agentic parallel execution plan (TAC / ADW compatible)

---

## REPOSITORY ROOTS (ABSOLUTE PATHS — MANDATORY)

All file paths referenced in tasks MUST be absolute and use ONLY the following bases:

- Repository root:
  /Users/hernandoescobar/Documents/Celes/tac_bootstrap/

- CLI root:
  /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/

---

## OUTPUT FILE (MANDATORY)

Create a new Markdown file at:

/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/plan_tasks.md

This file MUST contain the **entire task plan** and NOTHING else.

---

## SCOPE & RESPONSIBILITIES

You are responsible for:

- Decomposing work into **explicit, atomic technical tasks**
- Correctly classifying each task
- Ensuring tasks are:
  - Actionable
  - Unambiguous
  - Independently executable
- Listing **exact files and directories affected** (absolute paths)
- Ensuring:
  - Template creation
  - Template registration
  - Documentation updates
- Defining **parallel execution groups**
- Closing the plan with a **semantic version bump and CHANGELOG update**

---

## TASK STRUCTURE RULES (STRICT – NON-NEGOTIABLE)

Each task MUST:

- Be independent (ONE responsibility per task)
- Start with EXACTLY ONE prefix:
  - [BUG]     → Defect or incorrect behavior
  - [FEATURE] → New functionality or capability
  - [CHORE]   → Maintenance, refactor, infra, or documentation
- Include ALL of the following:
  - **Title** (short, precise)
  - **Description** (technical steps + acceptance criteria)
  - **Impacted Paths** (absolute paths only)
- Be executable **without further clarification**
- Avoid vague language such as:
  - "update", "improve", "adjust", "refactor"
  unless **what / where / why / expected outcome** are explicitly stated

---

## REQUIRED TASK COVERAGE (NON-NEGOTIABLE)

### A) Root-Level Modifications
- Identify and modify relevant root-level files under:
  /Users/hernandoescobar/Documents/Celes/tac_bootstrap/
- Each logical change MUST be a separate task

---

### B) Templates (Create + Modify + Register)

You MUST include tasks that:

1. Create and/or modify templates under:
   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/

2. Register ALL new templates in:
   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

Each template-related task MUST specify:
- Template filename(s)
- Purpose of the template
- Expected generated output
- Registration logic in `scaffold_service.py`

---

### C) CLI README Update + Table ("Cuadro")

You MUST include tasks that update:

/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md

Requirements:
- Document all new commands, agents, templates, or workflows
- Add or update a **Markdown table ("cuadro")**, consistent with the existing README style
- The task MUST specify:
  - Section header where the table is added
  - Column definitions
  - Example rows

---

## PARALLEL EXECUTION GROUPS (MANDATORY SECTION)

The plan MUST include a dedicated section:

## Parallel Execution Groups

This section MUST include a **Markdown table** that groups tasks for parallel execution using agentic parallelism.

Rules:
- Tasks in the same group MUST have **NO dependencies between them**
- Dependencies MUST be explicitly declared between groups
- Task numbers MUST reference the numbered tasks defined earlier in the plan

### Required Table Format

| Grupo | Tareas | Cantidad | Dependencia | Descripción |
|------|--------|----------|-------------|-------------|
| P1 | 1–N | X | Ninguna | Descripción clara del tipo de tareas |
| P2 | … | … | P1 | Dependencia explícita |
| … | … | … | … | … |
| SEQ | Final Task | 1 | TODOS | CHANGELOG y versión final |

- The **SEQ** group is mandatory and MUST contain ONLY the CHANGELOG task
- This table MUST be logically consistent with task ordering

---

## ORDERING & EXECUTION LOGIC

- Tasks MUST be numbered sequentially
- Ordering MUST reflect real execution dependencies
- Parallel groups MUST align with task numbering
- The plan must be directly usable by:
  - Humans
  - Autonomous agents
  - Parallel agent execution systems (TAC / ADWs)

---

## CHANGELOG & VERSIONING (FINAL TASK — ABSOLUTE LAST)

The FINAL task MUST:

- Update:
  /Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md
- Increment version following **Semantic Versioning**
- Summarize ALL changes introduced by the plan
- Be classified as:
  [CHORE]
- Be the LAST task in the file (no tasks allowed after)

---

## OUTPUT CONSTRAINTS (STRICT)

In your response:

- Output **ONLY** the contents of `plan_tasks.md`
- Use clean Markdown
- Use headings, numbered tasks, and bullet points
- Include an "Assumptions" section ONLY if required
- Do NOT:
  - Execute code
  - Explain reasoning outside the plan
  - Add commentary outside the Markdown

---

BEGIN.

sammy
test iso v3 ok

number