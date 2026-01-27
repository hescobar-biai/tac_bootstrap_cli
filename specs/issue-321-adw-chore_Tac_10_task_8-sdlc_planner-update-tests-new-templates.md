# Chore: Actualizar tests para validar nuevos templates

## Metadata
issue_number: `321`
adw_id: `chore_Tac_10_task_8`
issue_json: `{"number":321,"title":"Actualizar tests para validar nuevos templates","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_10_task_8\n\n- **Descripción**: Agregar tests unitarios para verificar que los nuevos templates se renderizan correctamente.\n- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_new_tac10_templates.py`\n- **Cobertura**:\n  - Test para parallel_subagents.md.j2\n  - Test para t_metaprompt_workflow.md.j2\n  - Test para cc_hook_expert_improve.md.j2\n  - Test para build_w_report.md.j2\n  - Test para settings.json.j2 con nuevos hooks\n\n\n"}`

## Chore Description

Agregar tests unitarios para verificar que los nuevos templates de TAC-10 se renderizan correctamente. Los templates incluyen:

1. **Comandos slash nuevos**:
   - `parallel_subagents.md.j2` - Orquestación de agentes paralelos
   - `t_metaprompt_workflow.md.j2` - Generador de workflows meta-prompt
   - `cc_hook_expert_improve.md.j2` - Expert para mejorar hooks de Claude Code
   - `build_w_report.md.j2` - Implementación con reporte YAML detallado

2. **Configuración actualizada**:
   - `settings.json.j2` - Con 9 nuevos hooks (PreToolUse, PostToolUse, Stop, UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd)

Los tests deben seguir el patrón establecido en `test_fractal_docs_templates.py` y `test_template_repo.py`:
- Verificar que los templates renderizan sin errores
- Validar estructura del contenido (secciones markdown, JSON válido)
- Usar fixtures de configuración mínima
- Tests organizados por clase (una por template)
- Foco en happy path, sin sobre-ingeniería de edge cases

## Relevant Files

### Existing Test Patterns
- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py` - Patrón base para tests de command templates (fixtures, estructura de clases, validación)
- `tac_bootstrap_cli/tests/test_template_repo.py` - Patrón de validación de renderizado y parsing

### Templates to Test
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Comando de orquestación paralela
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2` - Comando de meta-prompt workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` - Expert para mejora de hooks
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2` - Comando de build con reporte
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Settings con nuevos hooks

### Infrastructure
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository con método `render()`
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Modelos Pydantic (TACConfig, ProjectSpec, CommandsSpec, ClaudeConfig)

### New Files
- `tac_bootstrap_cli/tests/test_new_tac10_templates.py` - Archivo de tests nuevo a crear

## Step by Step Tasks

### Task 1: Crear estructura de test con fixtures
- Crear archivo `tac_bootstrap_cli/tests/test_new_tac10_templates.py`
- Importar módulos necesarios: `pytest`, `json`, `ast`, `yaml`
- Importar modelos del dominio: `TACConfig`, `ProjectSpec`, `CommandsSpec`, `ClaudeConfig`, `Language`, `PackageManager`
- Importar `TemplateRepository`
- Crear fixture `python_config()` con configuración mínima (similar a `test_fractal_docs_templates.py:40-54`)
- Crear fixture `template_repo()` para instanciar `TemplateRepository()`

### Task 2: Crear tests para command templates de markdown
- Crear clase `TestParallelSubagentsTemplate` con método `test_parallel_subagents_renders_valid_markdown()`
  - Renderizar template `claude/commands/parallel_subagents.md.j2`
  - Assert contenido no vacío (> 100 chars)
  - Assert secciones clave existen: "## Variables", "## Instructions", "## Workflow"
- Crear clase `TestMetapromptWorkflowTemplate` con método `test_metaprompt_workflow_renders_valid_markdown()`
  - Renderizar template `claude/commands/t_metaprompt_workflow.md.j2`
  - Assert contenido no vacío
  - Assert secciones clave existen: "## Variables", "## Instructions", "## Workflow"
- Crear clase `TestBuildWithReportTemplate` con método `test_build_w_report_renders_valid_markdown()`
  - Renderizar template `claude/commands/build_w_report.md.j2`
  - Assert contenido no vacío
  - Assert secciones clave existen: "## Variables", "## Instructions"

### Task 3: Crear tests para expert template
- Crear clase `TestCCHookExpertImproveTemplate` con método `test_cc_hook_expert_improve_renders_valid_markdown()`
  - Renderizar template `claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`
  - Assert contenido no vacío
  - Assert secciones clave existen: "## Variables", "## Instructions"
  - Assert menciona "hook" o "expert" en el contenido (validación semántica)

### Task 4: Crear tests para settings.json.j2 con validación de hooks
- Crear clase `TestSettingsTemplateWithHooks`
- Método `test_settings_renders_valid_json()`:
  - Renderizar template `claude/settings.json.j2`
  - Assert contenido no vacío
  - Parsear con `json.loads()` (validar JSON válido)
  - Assert estructura tiene claves "permissions" y "hooks"
- Método `test_settings_includes_all_nine_hooks()`:
  - Renderizar template `claude/settings.json.j2`
  - Parsear JSON
  - Assert `parsed["hooks"]` contiene 9 keys: `PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`, `SubagentStop`, `Notification`, `PreCompact`, `SessionStart`, `SessionEnd`
- Método `test_settings_hooks_reference_correct_scripts()`:
  - Renderizar template `claude/settings.json.j2`
  - Parsear JSON
  - Para cada hook, verificar que el comando menciona `universal_hook_logger.py` o el script hook correspondiente
  - Assert `context_bundle_builder.py` está mencionado en PostToolUse y UserPromptSubmit

### Task 5: Agregar docstrings y validación completa
- Agregar docstring al módulo explicando propósito (validar templates TAC-10)
- Agregar docstrings a cada clase explicando qué template testea
- Agregar docstrings a cada método test explicando qué verifica
- Revisar que todos los asserts tienen mensajes descriptivos

### Task 6: Ejecutar validation commands
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_new_tac10_templates.py -v --tb=short` - Verificar que todos los tests pasan
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Verificar cero regresiones en toda la suite
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .` - Verificar linting pasa
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test del CLI

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_new_tac10_templates.py -v --tb=short` - Tests del nuevo archivo
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Template Rendering Pattern

Todos los tests siguen este patrón básico:
```python
content = template_repo.render("path/to/template.j2", config)
assert len(content.strip()) > 50  # No vacío
# Validación específica (JSON parsing, secciones markdown, etc.)
```

### Configuración Mínima

Usar `python_config` fixture con:
- `ProjectSpec` básico (name, language=PYTHON, package_manager=UV)
- `CommandsSpec` básico (start, test)
- `ClaudeConfig` básico (settings con project_name)

Esto sigue el patrón de `test_fractal_docs_templates.py` líneas 40-54.

### Hooks Validation

Los 9 hooks esperados en `settings.json.j2`:
1. PreToolUse - llama universal_hook_logger.py + pre_tool_use.py
2. PostToolUse - llama context_bundle_builder.py + post_tool_use.py
3. Stop - llama universal_hook_logger.py + stop.py
4. UserPromptSubmit - llama context_bundle_builder.py
5. SubagentStop - llama universal_hook_logger.py + subagent_stop.py
6. Notification - llama universal_hook_logger.py + notification.py
7. PreCompact - llama universal_hook_logger.py + pre_compact.py
8. SessionStart - llama universal_hook_logger.py
9. SessionEnd - llama universal_hook_logger.py

### No Over-Engineering

- No testear edge cases (missing variables, conditionals)
- No testear renderizado exhaustivo de cada línea
- Foco en: 1) renderiza sin error, 2) estructura válida
- Si templates fallan con config mínima, arreglar templates (no tests)
