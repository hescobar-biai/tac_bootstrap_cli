# Feature: Crear template parallel_subagents.md.j2 para delegación multi-agente

## Metadata
issue_number: `306`
adw_id: `feature_Tac_10_task_1`
issue_json: `{"number":306,"title":"Crear template parallel_subagents.md.j2 para delegación multi-agente","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_1\n\n\n- **Descripción**: Crear un nuevo template de comando que permita lanzar múltiples agentes en paralelo para tareas complejas. Este template implementa el patrón Level 4 (Delegation Prompt) de TAC-10.\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`\n- **Contenido**:\n  - Frontmatter con description y argument-hint\n  - Variables: PROMPT_REQUEST ($1), COUNT ($2)\n  - Workflow de 4 pasos: Parse Input, Design Agent Prompts, Launch Parallel Agents, Collect & Summarize\n- **Nota**: El template .j2 usa variables Jinja2, el archivo .md es la versión renderizada para uso directo\n\n\n"}`

## Feature Description
Crear un nuevo template de comando que implemente el patrón Level 4 (Delegation Prompt) de TAC-10, permitiendo lanzar múltiples agentes en paralelo para trabajar en tareas complejas. Este comando acepta una descripción de tarea de alto nivel y un número de agentes (con valor por defecto de 3), descompone la tarea automáticamente, lanza los agentes en paralelo usando el Task tool, y agrega los resultados en un resumen estructurado en formato markdown.

El template debe existir en dos formas:
1. **Template Jinja2 (.j2)**: Fuente autorizada para el generador TAC Bootstrap CLI, con variables Jinja2 interpolables
2. **Archivo renderizado (.md)**: Versión completamente renderizada para uso directo en este repositorio (dogfooding)

## User Story
As a TAC Bootstrap user
I want to delegate complex tasks to multiple parallel agents
So that I can decompose and solve problems faster using compute orchestration

## Problem Statement
Los usuarios necesitan un mecanismo para descomponer tareas complejas en subtareas paralelas y ejecutarlas simultáneamente con múltiples agentes. Actualmente no existe un comando estandarizado que:
- Acepte tareas arbitrarias
- Determine automáticamente la estrategia de descomposición
- Lance múltiples agentes en paralelo
- Agregue resultados de forma estructurada
- Maneje fallos parciales con resiliencia

## Solution Statement
Crear un template de comando `/parallel_subagents` que implemente el patrón de delegación Level 4 de TAC-10. El comando seguirá la arquitectura Input → Workflow → Output con:
- Variables parametrizadas (PROMPT_REQUEST, COUNT con default 3, rango 2-10)
- Workflow de 4 pasos explícitos
- Guía para que el agente evalúe la idoneidad de la paralelización
- Formato de reporte estructurado en markdown con secciones por agente
- Instrucciones para manejar fallos parciales con resiliencia

## Relevant Files
Archivos necesarios para implementar la feature:

- `.claude/commands/background.md` - Comando existente de delegación que sirve como referencia de estructura y patrones
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` - Template Jinja2 correspondiente para ver patrón de variables
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Otro template de referencia para ver formato de workflow consistente
- `ai_docs/doc/Tac-10_1.md` - Documentación de Level 4 (Delegation Prompts) y estructura de prompts
- `ai_docs/doc/plan_tasks_Tac_10.md` - Especificación detallada de la Tarea 1 con requisitos exactos
- `config.yml` - Para verificar estructura de variables disponibles para interpolación Jinja2

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Template Jinja2 con variables interpolables
- `.claude/commands/parallel_subagents.md` - Versión renderizada para uso directo en este repo

## Implementation Plan

### Phase 1: Foundation
Investigar patrones existentes en templates de comandos para entender:
- Estructura de frontmatter y variables
- Formato de secciones (Variables, Instructions, Workflow, Report)
- Convenciones de Jinja2 usadas en templates actuales
- Cómo se usa el Task tool para lanzar agentes en paralelo

### Phase 2: Core Implementation
Crear ambos archivos del template:
1. Crear template Jinja2 (.j2) con variables interpolables
2. Renderizar versión .md para dogfooding en este repo

### Phase 3: Integration
Verificar que el nuevo comando funciona correctamente:
- Tests de renderizado del template
- Validación de formato y estructura
- Smoke test del comando en este repo

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Investigar patrones de templates existentes
- Leer `.claude/commands/background.md` para entender patrón de delegación
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` para ver uso de variables Jinja2
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` para ver formato de workflow
- Leer `ai_docs/doc/Tac-10_1.md` para entender teoría de Level 4 Delegation Prompts
- Leer `ai_docs/doc/plan_tasks_Tac_10.md` para ver especificación exacta de Tarea 1

### Task 2: Crear template Jinja2 parallel_subagents.md.j2
- Crear archivo en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`
- Incluir frontmatter con:
  - `description`: "Launch multiple agents in parallel to solve complex tasks through decomposition and orchestration"
  - `argument-hint`: "<task_description> [agent_count]"
- Definir sección Variables:
  - `PROMPT_REQUEST`: $1 (task description)
  - `COUNT`: $2 (number of agents, default: 3, range: 2-10)
- Crear sección Instructions con:
  - Guía para evaluar idoneidad de paralelización
  - Explicación de cuándo usar vs no usar este comando
  - Estrategia ligera de descomposición: por dominio/concern, mínimo overlap, deliverables claros
  - Manejo de COUNT=1 como caso de error
- Crear sección Workflow con 4 pasos:
  1. **Parse Input**: Validar PROMPT_REQUEST, determinar COUNT (default 3 si no especificado), validar rango 2-10
  2. **Design Agent Prompts**: Descomponer tarea en COUNT subtareas con mínimo overlap y deliverables claros
  3. **Launch Parallel Agents**: Usar Task tool con múltiples invocaciones en un solo mensaje, cada agente con prompt específico
  4. **Collect & Summarize**: Agregar resultados de agentes, manejar fallos parciales, reportar en formato estructurado
- Crear sección Report con formato:
  - `## Agent N: [Task Name]` con bullet points de key findings
  - `## Overall Summary` con síntesis coherente
  - Instrucción de continuar si fallos parciales, reportar patrón si todos fallan

### Task 3: Crear versión renderizada parallel_subagents.md
- Crear archivo en `.claude/commands/parallel_subagents.md`
- Copiar contenido del template .j2 pero remover cualquier sintaxis Jinja2 (o usar valores por defecto si aplica)
- Este archivo es la versión "dogfooded" para uso directo en este repo
- Verificar que mantiene consistencia con el template .j2

### Task 4: Verificar templates contra patrones existentes
- Comparar estructura con `background.md` para consistencia de formato
- Verificar que sigue convenciones de Input → Workflow → Output
- Confirmar que frontmatter es válido
- Validar que Variables están bien definidas con defaults y tipos claros

### Task 5: Ejecutar validation commands
- Ejecutar todos los comandos de validación para verificar cero regresiones
- Hacer smoke test del comando en este repo si es posible

## Testing Strategy

### Unit Tests
- Test de renderizado del template Jinja2 con config por defecto
- Test de que frontmatter se parsea correctamente
- Test de que variables se interpolan correctamente
- Test de estructura de secciones (Variables, Instructions, Workflow, Report)

### Edge Cases
- COUNT fuera de rango (< 2 o > 10)
- COUNT = 1 (caso de error explícito)
- PROMPT_REQUEST vacío o malformado
- Tarea que no es adecuada para paralelización (debe continuar con advertencia)

## Acceptance Criteria
- El template Jinja2 `parallel_subagents.md.j2` existe y es válido sintácticamente
- El archivo renderizado `parallel_subagents.md` existe y es funcional
- Ambos archivos siguen el formato estándar: frontmatter + Variables + Instructions + Workflow + Report
- El workflow tiene exactamente 4 pasos explícitos
- Las variables PROMPT_REQUEST y COUNT están definidas con defaults y validaciones claras
- El formato de Report es estructurado (secciones por agente + Overall Summary)
- Incluye instrucciones de manejo de errores parciales
- Incluye guía para evaluar idoneidad de paralelización
- COUNT=1 se trata como caso de error con recomendación alternativa
- Estrategia de descomposición sigue principios: por dominio/concern, mínimo overlap, deliverables claros
- El template sigue convenciones Jinja2 consistentes con otros templates existentes
- Los comandos de validación pasan sin regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Este comando implementa Level 4 (Delegation Prompt) de TAC-10, representando un paso significativo en capacidad de orquestación
- El patrón de agentes paralelos es S-tier en usefulness pero A-tier en skill required según TAC-10
- La doble naturaleza del archivo (.j2 generator source + .md dogfooded example) es fundamental al propósito de TAC Bootstrap
- El default de 3 agentes es un sweet spot entre paralelización significativa y evitar sobrecarga de recursos
- El rango 2-10 fue elegido basado en: mínimo 2 para forzar verdadera paralelización, máximo 10 para prevenir agotamiento de recursos
- La aceptación de input arbitrario con evaluación guiada por el agente es más flexible que validación estricta
- El formato de reporte estructurado (markdown con secciones) es parseable, legible y consistente con patrones TAC
- La resiliencia ante fallos parciales es crítica para trabajo paralelo real
- Este template será usado por otros proyectos generados con TAC Bootstrap, por lo que debe ser robusto y bien documentado
