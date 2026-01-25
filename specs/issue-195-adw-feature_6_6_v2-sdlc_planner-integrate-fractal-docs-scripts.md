# Feature: Integrate Fractal Documentation Scripts in ScaffoldService

## Metadata
issue_number: `195`
adw_id: `feature_6_6_v2`
issue_json: `{"number":195,"title":"Tarea 6.7: Integrar scripts fractal en ScaffoldService","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_6_6_v2\n\n**Tipo**: feature\n**Ganancia**: Los scripts de documentacion fractal se incluyen automaticamente al generar proyectos, sin que el usuario tenga que agregarlos manualmente.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n2. En `build_plan()`, agregar metodo `_add_fractal_docs_scripts(plan, config)`:\n   ```python\n   def _add_fractal_docs_scripts(self, plan: ScaffoldPlan, config: TACConfig):\n       \"\"\"Add fractal documentation generation scripts.\"\"\"\n       # Scripts\n       plan.add_file(\n           template=\"scripts/gen_docstring_jsdocs.py.j2\",\n           output=\"scripts/gen_docstring_jsdocs.py\",\n           action=FileAction.CREATE,\n           executable=True,\n       )\n       plan.add_file(\n           template=\"scripts/gen_docs_fractal.py.j2\",\n           output=\"scripts/gen_docs_fractal.py\",\n           action=FileAction.CREATE,\n           executable=True,\n       )\n       plan.add_file(\n           template=\"scripts/run_generators.sh.j2\",\n           output=\"scripts/run_generators.sh\",\n           action=FileAction.CREATE,\n           executable=True,\n       )\n       # Canonical IDK vocabulary\n       plan.add_file(\n           template=\"config/canonical_idk.yml.j2\",\n           output=\"canonical_idk.yml\",\n           action=FileAction.CREATE,\n       )\n       # Slash command\n       plan.add_file(\n           template=\"claude/commands/generate_fractal_docs.md.j2\",\n           output=\".claude/commands/generate_fractal_docs.md\",\n           action=FileAction.CREATE,\n       )\n       # Docs directory\n       plan.add_directory(\"docs\")\n   ```\n3. Llamar `_add_fractal_docs_scripts()` siempre (no es condicional, todos los proyectos lo tienen)\n\n**Criterios de aceptacion**:\n- `tac-bootstrap init my-app` genera scripts/ con los 3 scripts fractal\n- `canonical_idk.yml` se genera en la raiz del proyecto\n- `.claude/commands/generate_fractal_docs.md` existe\n- Directorio `docs/` se crea vacio\n- Scripts tienen permisos de ejecucion\n\n---\n"}`

## Feature Description
Esta feature integra scripts de documentación fractal en el sistema de scaffolding de TAC Bootstrap CLI. Los scripts (gen_docstring_jsdocs.py, gen_docs_fractal.py, run_generators.sh) se generan automáticamente al crear nuevos proyectos con `tac-bootstrap init` o `tac-bootstrap add-agentic`, permitiendo documentación automática basada en LLM sin intervención manual.

## User Story
As a **developer creating a project with tac-bootstrap**
I want to **have fractal documentation scripts automatically included**
So that **I can generate IDK docstrings and fractal docs without manually copying scripts**

## Problem Statement
Los scripts de generación de documentación fractal (gen_docstring_jsdocs.py, gen_docs_fractal.py, run_generators.sh) existen como templates pero no se generan automáticamente al crear proyectos. Los usuarios deben agregarlos manualmente, lo cual es propenso a errores y reduce la adopción del sistema de documentación fractal.

## Solution Statement
Agregar un nuevo método `_add_fractal_docs_scripts()` a ScaffoldService que declare todos los archivos y directorios relacionados con fractal docs (3 scripts, 1 config, 1 slash command, 1 directory). Este método se invoca en `build_plan()` después de agregar archivos core, asegurando que todos los proyectos incluyan el sistema de documentación fractal automáticamente.

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:59-99` - build_plan() method donde se agregará llamada a _add_fractal_docs_scripts()
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:397-419` - _add_script_files() method (referencia de patrón similar, actualmente ya agrega gen_docs_fractal.py y gen_docstring_jsdocs.py pero falta run_generators.sh)
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py:118-143` - ScaffoldPlan.add_file() y add_directory() methods (API para construir el plan)

### New Files
No se crean archivos nuevos en el CLI. Los templates ya existen:
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2` (existente)
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2` (existente)
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2` (probablemente ya existe, verificar)
- `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2` (existente)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2` (existente)

## Implementation Plan

### Phase 1: Foundation
1. Verificar existencia de todos los templates requeridos (usar Glob)
2. Analizar método _add_script_files() existente para entender patrón de agregado de scripts
3. Verificar que gen_docs_fractal.py y gen_docstring_jsdocs.py ya existen en _add_script_files (líneas 407-408)

### Phase 2: Core Implementation
1. Crear método privado `_add_fractal_docs_scripts(plan, config)` en ScaffoldService
2. Declarar 5 archivos usando plan.add_file():
   - scripts/gen_docstring_jsdocs.py (template, executable=True)
   - scripts/gen_docs_fractal.py (template, executable=True)
   - scripts/run_generators.sh (template, executable=True)
   - canonical_idk.yml (template, en raíz del proyecto)
   - .claude/commands/generate_fractal_docs.md (template)
3. Declarar 1 directorio usando plan.add_directory():
   - docs/

### Phase 3: Integration
1. Remover gen_docs_fractal.py y gen_docstring_jsdocs.py de _add_script_files() (evitar duplicación)
2. Llamar _add_fractal_docs_scripts(plan, config) en build_plan() después de _add_structure_files()
3. Verificar que templates existe usando Glob antes de ejecutar tests

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verificar existencia de templates
- Usar Glob para buscar scripts/gen_docstring_jsdocs.py.j2
- Usar Glob para buscar scripts/gen_docs_fractal.py.j2
- Usar Glob para buscar scripts/run_generators.sh.j2
- Usar Glob para buscar config/canonical_idk.yml.j2
- Usar Glob para buscar claude/commands/generate_fractal_docs.md.j2
- Documentar templates faltantes (si aplica)

### Task 2: Analizar código existente
- Leer scaffold_service.py completo para entender patrones
- Identificar líneas donde gen_docs_fractal.py y gen_docstring_jsdocs.py se agregan actualmente (_add_script_files)
- Identificar punto de inserción óptimo para llamar _add_fractal_docs_scripts()

### Task 3: Implementar _add_fractal_docs_scripts()
- Agregar método privado después de _add_structure_files()
- Seguir exactamente el código proporcionado en issue body
- Usar FileAction.CREATE para todos los archivos (idempotente)
- Usar executable=True para los 3 scripts
- Agregar reason strings descriptivos a cada operación

### Task 4: Integrar en build_plan()
- Remover gen_docs_fractal.py y gen_docstring_jsdocs.py de _add_script_files() para evitar duplicación
- Llamar _add_fractal_docs_scripts(plan, config) en build_plan() después de _add_structure_files()
- Verificar que el orden de operaciones sea correcto (directorios antes de archivos)

### Task 5: Ejecutar Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
Extender tests existentes en test_scaffold_service.py:
- test_build_plan_includes_fractal_docs_scripts()
  - Assert que plan.files contiene 5 archivos fractal
  - Assert que plan.directories contiene "docs"
  - Assert que scripts tienen executable=True
  - Assert que canonical_idk.yml está en raíz (output="canonical_idk.yml")
- test_apply_plan_creates_fractal_docs()
  - Aplicar plan a directorio temporal
  - Assert que scripts/ contiene gen_docstring_jsdocs.py, gen_docs_fractal.py, run_generators.sh
  - Assert que canonical_idk.yml existe en raíz
  - Assert que .claude/commands/generate_fractal_docs.md existe
  - Assert que docs/ directory existe
  - Assert que scripts tienen permisos ejecutables

### Edge Cases
- Templates faltantes: El sistema existente debe manejar errores de template (no agregar validación especial)
- Directorio docs/ ya existe: add_directory() debe ser no-op (idempotente)
- Archivos fractal ya existen: FileAction.CREATE debe saltarlos (no sobrescribir)

## Acceptance Criteria
- `tac-bootstrap init my-app` genera scripts/ con los 3 scripts fractal (gen_docstring_jsdocs.py, gen_docs_fractal.py, run_generators.sh)
- `canonical_idk.yml` se genera en la raíz del proyecto (no en config/)
- `.claude/commands/generate_fractal_docs.md` existe en .claude/commands/
- Directorio `docs/` se crea vacío
- Scripts tienen permisos de ejecución (verificar con ls -l)
- No hay duplicación de gen_docs_fractal.py y gen_docstring_jsdocs.py (solo en fractal section, no en _add_script_files)
- Tests unitarios pasan con cero regresiones
- Linting y type checking pasan sin errores

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Auto-Resolved Clarifications indican que este método debe agregarse después de archivos core, near the end of build_plan()
- No requiere validación especial de templates (confiar en framework existente)
- canonical_idk.yml va en raíz del proyecto, no en subdirectorio config/ (el template está en templates/config/ para organización interna)
- Templates ya deben existir de tareas anteriores (6.1-6.5)
- Esta es una tarea de integración pura: no crear templates, solo declararlos en el plan
- FileAction.CREATE es seguro para repos existentes (skip if exists)
- Scripts bash (.sh) y Python (.py) necesitan executable=True
