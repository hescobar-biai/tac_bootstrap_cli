# Plan de Tareas: Complementar tac_bootstrap_cli con TAC-10

## Información del Plan

- **Fecha**: 2026-01-26
- **Versión Objetivo**: 0.5.0
- **Repositorio**: /Users/hernandoescobar/Documents/Celes/tac_bootstrap/
- **CLI Path**: /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/

---

## Tareas

### Tarea 1

**[FEATURE] Crear template parallel_subagents.md.j2 para delegación multi-agente**

- **Descripción**: Crear un nuevo template de comando que permita lanzar múltiples agentes en paralelo para tareas complejas. Este template implementa el patrón Level 4 (Delegation Prompt) de TAC-10.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`
- **Contenido**:
  - Frontmatter con description y argument-hint
  - Variables: PROMPT_REQUEST ($1), COUNT ($2)
  - Workflow de 4 pasos: Parse Input, Design Agent Prompts, Launch Parallel Agents, Collect & Summarize

---

### Tarea 2

**[FEATURE] Crear template t_metaprompt_workflow.md.j2 para generar prompts**

- **Descripción**: Crear un meta-prompt (Level 6) que genera nuevos prompts siguiendo el formato consistente de TAC. Incluye documentación de referencia y un Specified Format template.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2`
- **Contenido**:
  - Frontmatter con allowed-tools (Write, Edit, WebFetch, Task)
  - Variables: HIGH_LEVEL_PROMPT ($ARGUMENTS)
  - Documentation links para slash commands
  - Specified Format template con estructura estándar (metadata, variables, workflow, report)

---

### Tarea 3

**[FEATURE] Crear template cc_hook_expert_improve.md.j2 para self-improvement**

- **Descripción**: Completar el sistema de expertos con el prompt de mejora continua (Level 7). Analiza cambios recientes y actualiza las secciones de Expertise de los prompts plan y build.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`
- **Contenido**:
  - Workflow de 5 pasos: Establish Expertise, Analyze Recent Changes, Determine Relevance, Extract and Apply Learnings, Report
  - Lógica de early return si no hay learnings relevantes
  - Report format estructurado

---

### Tarea 4

**[FEATURE] Crear template build_w_report.md.j2 con reporte YAML estructurado**

- **Descripción**: Variante del comando build que genera un reporte YAML detallado de los cambios realizados (files, lines_changed, description).
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2`
- **Contenido**:
  - Frontmatter con allowed-tools (Read, Write, Edit, Bash, MultiEdit)
  - Variables: PATH_TO_PLAN ($ARGUMENTS)
  - Workflow: Read plan, implement, run git diff
  - Report format YAML: work_changes array

---

### Tarea 5

**[FEATURE] Actualizar settings.json.j2 con hooks adicionales integrados**

- **Descripción**: Modificar el template de settings.json para incluir todos los hooks de TAC-10 integrados con universal_hook_logger y context_bundle_builder.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`
- **Cambios**:
  - Agregar hook UserPromptSubmit con context_bundle_builder --type user_prompt
  - Agregar hook SubagentStop con universal_hook_logger
  - Agregar hook Notification con universal_hook_logger
  - Agregar hook PreCompact con universal_hook_logger
  - Agregar hook SessionStart con universal_hook_logger
  - Agregar hook SessionEnd con universal_hook_logger
  - Modificar PreToolUse para incluir universal_hook_logger antes de pre_tool_use.py
  - Modificar PostToolUse para incluir context_bundle_builder con matcher "Read|Write"
  - Modificar Stop para incluir universal_hook_logger antes de stop.py

---

### Tarea 6

**[FEATURE] Actualizar scaffold_service.py para crear directorios de agents**

- **Descripción**: Modificar el servicio de scaffolding para crear los directorios necesarios para logs de hooks y context bundles.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- **Cambios**:
  - En la función `build_plan()`, agregar DirectoryOperation para `agents/hook_logs/`
  - Agregar DirectoryOperation para `agents/context_bundles/`
  - Agregar .gitkeep files en ambos directorios

---

### Tarea 7

**[CHORE] Crear templates .gitkeep para directorios agents**

- **Descripción**: Crear templates .gitkeep para los nuevos directorios de agents que se crearán durante el scaffold.
- **Archivos**:
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2`

---

### Tarea 8

**[CHORE] Actualizar tests para validar nuevos templates**

- **Descripción**: Agregar tests unitarios para verificar que los nuevos templates se renderizan correctamente.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_new_tac10_templates.py`
- **Cobertura**:
  - Test para parallel_subagents.md.j2
  - Test para t_metaprompt_workflow.md.j2
  - Test para cc_hook_expert_improve.md.j2
  - Test para build_w_report.md.j2
  - Test para settings.json.j2 con nuevos hooks

---

### Tarea 9

**[CHORE] Copiar nuevos templates a la raíz del proyecto tac_bootstrap**

- **Descripción**: Sincronizar los nuevos templates creados en tac_bootstrap_cli con la estructura actual de .claude/ en la raíz del proyecto.
- **Archivos destino**:
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/t_metaprompt_workflow.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_w_report.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
- **Nota**: Renderizar templates sin variables Jinja2 para uso directo en el proyecto

---

### Tarea 10

**[CHORE] Actualizar settings.json en la raíz con hooks integrados**

- **Descripción**: Actualizar el settings.json de la raíz del proyecto para reflejar la nueva configuración de hooks.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`
- **Cambios**: Aplicar la misma estructura de hooks definida en Tarea 5

---

### Tarea 11

**[CHORE] Crear directorios agents en la raíz del proyecto**

- **Descripción**: Crear la estructura de directorios para logs y context bundles en la raíz del proyecto.
- **Directorios**:
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/hook_logs/`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/context_bundles/`
- **Archivos**: Agregar .gitkeep en cada directorio

---

### Tarea 12

**[CHORE] Ejecutar suite de tests completa**

- **Descripción**: Ejecutar todos los tests del proyecto para verificar que no hay regresiones.
- **Comando**: `uv run pytest tac_bootstrap_cli/tests/ -v`
- **Criterio de éxito**: Todos los tests pasan sin errores

---

### Tarea 13

**[CHORE] Actualizar CHANGELOG.md e incrementar versión a 0.5.0**

- **Descripción**: Documentar todos los cambios introducidos en esta iteración y actualizar la versión del proyecto.
- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- **Contenido del changelog**:
```markdown
## [0.5.0] - 2026-01-26

### Added
- Nuevo template `parallel_subagents.md.j2` para delegación multi-agente (TAC-10 Level 4)
- Nuevo template `t_metaprompt_workflow.md.j2` para generación de prompts (TAC-10 Level 6)
- Nuevo template `cc_hook_expert_improve.md.j2` para self-improvement (TAC-10 Level 7)
- Nuevo template `build_w_report.md.j2` con reporte YAML estructurado
- Hooks adicionales: UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd
- Integración de universal_hook_logger en todos los hooks
- Directorios `agents/hook_logs/` y `agents/context_bundles/` en scaffold

### Changed
- settings.json.j2 actualizado con configuración completa de hooks
- scaffold_service.py ahora crea estructura de directorios agents/
```

---

## Verificación Final

```bash
# 1. Ejecutar tests
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
uv run pytest tac_bootstrap_cli/tests/ -v

# 2. Verificar templates se cargan correctamente
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
repo = TemplateRepository()
templates = ['parallel_subagents.md.j2', 't_metaprompt_workflow.md.j2', 'build_w_report.md.j2']
for t in templates:
    print(f'Template {t}: OK')
"

# 3. Dry-run de scaffold
uv run tac-bootstrap init --name test-tac10 --language python --framework fastapi --dry-run
```
