---
allowed-tools: Task, Read, Glob, Grep, WebFetch
description: Enhanced planning with documentation exploration
---

# Planning with Documentation Exploration

Crear un plan para implementar una nueva funcionalidad en TAC Bootstrap CLI explorando documentación relevante antes de planificar.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANTE: Estás creando un plan para implementar una nueva funcionalidad del TAC Bootstrap CLI.
- El plan se usará para guiar la implementación con agentic coding.
- CRITICAL: Crear el plan usando ruta RELATIVA `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/filename.md`, NO `/Users/.../specs/filename.md`
- IMPORTANTE: Antes de planificar, explorar documentación relevante siguiendo el flujo de trabajo de exploración de documentación.
- IMPORTANTE: Reemplazar cada <placeholder> en el formato con valores reales.
- Usar el reasoning model: pensar cuidadosamente sobre requerimientos y approach.
- Seguir patrones y convenciones existentes del proyecto.
- Si necesitas una nueva librería, usar `uv add` y reportarlo en Notes.
- Mantener simplicidad - no usar decoradores innecesarios.

## Documentation Exploration Workflow

Antes de crear el plan, ejecutar este flujo de trabajo de exploración de documentación:

### Step 1: Search Local Documentation

Usar Task tool con subagent_type="Explore" y thoroughness="medium" para:

1. **Search ai_docs/** - Buscar patrones arquitecturales, guías, y documentación del curso TAC (doc-1 a doc-8):
   - Prompt: "Find architectural patterns, guidelines, and TAC course documentation relevant to {issue_title}. Focus on: design patterns, service architecture, template patterns, and any relevant TAC course content."

2. **Search app_docs/** - Buscar documentación específica del proyecto:
   - Prompt: "Find project-specific documentation related to {issue_title}. Look for: API documentation, configuration guides, integration patterns, and implementation examples."

3. **Search specs/** - Buscar patrones de implementación recientes:
   - Prompt: "Find recent implementation plans and specifications related to {issue_title}. Identify: similar features, common patterns, architectural decisions, and reusable approaches."

### Step 2: Optional Web Documentation

Si la feature requiere frameworks/librerías específicas, usar WebFetch para:
- Documentación oficial de frameworks
- Best practices de librerías
- Guías de integración
- IMPORTANTE: Solo usar WebFetch si es necesario para la feature específica

### Step 3: Summarize Documentation Findings

Crear un resumen de las top 5-10 fuentes de documentación más relevantes:
- Título y ubicación del documento
- Relevancia para la feature (1 frase)
- Insights clave o patrones aplicables (2-3 bullet points)

### Step 4: Identify Documentation Gaps

Notar cualquier gap en documentación que pueda afectar la planificación:
- Documentación faltante que sería útil
- Áreas donde las guías son incompletas
- Inconsistencias entre documentación y código actual

### Step 5: Proceed with Planning

Usar los insights de documentación para informar:
- Implementation Plan - alinear con patrones existentes
- Solution Statement - incorporar best practices documentadas
- Testing Strategy - seguir estrategias documentadas
- Notes section - incluir referencias a documentación relevante y gaps identificados

## Graceful Handling of Missing Documentation

Si documentación no está disponible o Task/Explore falla:
- CONTINUAR con la planificación normalmente
- Loggear advertencia en Notes section del plan
- Basar decisiones en conocimiento general y análisis de código
- No bloquear ejecución por falta de documentación

## Relevant Files

Archivos clave para TAC Bootstrap CLI:

- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro con todas las tareas
- `CLAUDE.md` - Guía para agentes
- `config.yml` - Configuración del proyecto
- `ai_docs/` - Documentación del curso TAC y guías arquitecturales
- `app_docs/` - Documentación específica del proyecto
- `specs/` - Especificaciones y planes de implementación
- `tac_bootstrap_cli/` - Código fuente del CLI (si existe)
  - `tac_bootstrap/domain/` - Modelos Pydantic
  - `tac_bootstrap/application/` - Servicios
  - `tac_bootstrap/infrastructure/` - Templates, FS
  - `tac_bootstrap/interfaces/` - CLI, Wizard
- `prompts/templates/` - Templates de prompts

Leer `.claude/commands/conditional_docs.md` para documentación adicional requerida.

## Plan Format

```md
# Feature: <nombre de la feature>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Documentation Exploration Summary
<insertar resumen de documentación explorada - top 5-10 fuentes>

### Relevant Documentation Found
1. **<doc title>** (`<path>`) - <relevancia>
   - <insight clave 1>
   - <insight clave 2>

2. **<doc title>** (`<path>`) - <relevancia>
   - <insight clave>

### Documentation Gaps
- <gap 1>
- <gap 2>

## Feature Description
<describir la feature en detalle, su propósito y valor>

## User Story
As a <tipo de usuario>
I want to <acción/objetivo>
So that <beneficio/valor>

## Problem Statement
<definir claramente el problema u oportunidad que esta feature aborda>

## Solution Statement
<describir el approach propuesto y cómo resuelve el problema, INFORMADO POR DOCUMENTACIÓN EXPLORADA>

## Relevant Files
Archivos necesarios para implementar la feature:

<listar archivos relevantes con descripción de por qué son relevantes>

### New Files
<listar archivos nuevos que se crearán>

## Implementation Plan

### Phase 1: Foundation
<trabajo fundacional antes de implementar la feature principal>

### Phase 2: Core Implementation
<implementación principal de la feature>

### Phase 3: Integration
<integración con funcionalidad existente>

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: <nombre>
- <detalle>
- <detalle>

### Task 2: <nombre>
- <detalle>

<El último paso debe ejecutar Validation Commands>

## Testing Strategy

### Unit Tests
<tests unitarios necesarios>

### Edge Cases
<casos edge a probar>

## Acceptance Criteria
<criterios específicos y medibles para considerar la feature completa>

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
<notas adicionales, consideraciones futuras, o contexto relevante>
<INCLUIR referencias a documentación relevante y gaps identificados>
```

## Feature
Extraer detalles de la feature de la variable `issue_json` (parsear JSON y usar campos title y body).

## Report

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it using RELATIVE PATH (e.g., `specs/filename.md`), then return ONLY the path

CRITICAL FILE CREATION RULES:
- When using the Write tool, use RELATIVE paths only: `specs/filename.md`
- NEVER use absolute paths like `/Users/.../specs/filename.md`
- The file will be created in the current working directory

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the RELATIVE path like:
```
specs/issue-37-adw-e4dc9574-sdlc_planner-feature-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I can see that...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines
- Absolute paths (starting with /)

ONLY output the bare RELATIVE path. This is machine-parsed.
