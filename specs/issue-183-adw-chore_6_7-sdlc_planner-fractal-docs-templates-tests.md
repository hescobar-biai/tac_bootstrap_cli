# Chore: Tests para documentacion fractal

## Metadata
issue_number: `183`
adw_id: `chore_6_7`
issue_json: `{"number":183,"title":"Tarea 6.8: Tests para documentacion fractal","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_6_7\n\n**Tipo**: chore\n**Ganancia**: Verificar que los templates de docs fractal renderizan correctamente para distintas configuraciones de proyecto.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tests/test_fractal_docs_templates.py`\n2. Tests:\n   - `test_gen_docstring_renders_for_python` - Template con language=python renderiza\n   - `test_gen_docstring_renders_for_typescript` - Template con language=typescript\n   - `test_gen_docs_fractal_renders` - Template genera script valido\n   - `test_run_generators_renders` - Bash script valido\n   - `test_canonical_idk_renders_python` - YAML valido con keywords Python\n   - `test_canonical_idk_renders_typescript` - YAML valido con keywords TS\n   - `test_generate_fractal_docs_command_renders` - Slash command valido\n   - `test_scaffold_includes_fractal_scripts` - ScaffoldService incluye scripts\n   - `test_conditional_docs_includes_fractal_rules` - Reglas agregadas correctamente\n\n**Criterios de aceptacion**:\n- `uv run pytest tests/test_fractal_docs_templates.py` pasa\n- Todos los templates generan contenido parseable (Python compilable, YAML parseable, Bash ejecutable)\n\n---\n"}`

## Chore Description
Crear tests unitarios completos para los templates relacionados con fractal documentation. Estos templates incluyen:
- Scripts de generación Python (gen_docstring_jsdocs.py.j2, gen_docs_fractal.py.j2)
- Scripts bash (run_generators.sh.j2)
- Configuración YAML (canonical_idk.yml.j2)
- Comandos slash (generate_fractal_docs.md.j2)
- Documentación condicional (conditional_docs.md.j2)

Los tests deben verificar que:
1. Los templates renderizan sin errores para distintas configuraciones (Python/TypeScript)
2. El contenido generado es válido (Python compilable con ast.parse, YAML parseable, bash con shebang)
3. Las variables de configuración se interpolan correctamente
4. ScaffoldService incluye los scripts fractal en el scaffolding
5. Las reglas fractal están presentes en conditional_docs

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2` - Template para generación de docstrings
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2` - Template principal de generación fractal
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2` - Script bash que ejecuta generadores
- `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2` - Template YAML con keywords por lenguaje
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2` - Slash command template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2` - Documentación condicional con reglas fractal
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Servicio que aplica templates
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Repositorio de templates Jinja2
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests existentes del scaffold service (para referencia)
- `tac_bootstrap_cli/tests/test_template_repo.py` - Tests existentes de template repo (para referencia)

### New Files
- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py` - Suite de tests para templates fractal

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Explorar estructura de tests existentes
- Leer `tac_bootstrap_cli/tests/test_scaffold_service.py` para entender patrones de testing
- Leer `tac_bootstrap_cli/tests/test_template_repo.py` para ver cómo se testean templates
- Identificar fixtures reutilizables (TACConfig, ProjectSpec, etc.)
- Verificar si existe helper para renderizar templates

### Task 2: Crear fixtures para ProjectConfig
- Crear fixture `python_config` con `language=Language.PYTHON`
- Crear fixture `typescript_config` con `language=Language.TYPESCRIPT`
- Usar configuraciones mínimas inline (no archivos externos)
- Incluir campos necesarios: project.name, project.language, commands, claude

### Task 3: Implementar tests de renderizado Python
- `test_gen_docstring_renders_for_python`:
  - Renderizar `gen_docstring_jsdocs.py.j2` con python_config
  - Validar con `ast.parse()` que es Python válido
  - Verificar len(output.strip()) > 50
- `test_gen_docstring_renders_for_typescript`:
  - Renderizar con typescript_config
  - Validar con `ast.parse()`
  - Verificar contenido no vacío
- `test_gen_docs_fractal_renders`:
  - Renderizar `gen_docs_fractal.py.j2`
  - Validar sintaxis Python con `ast.parse()`
  - Verificar shebang presente

### Task 4: Implementar tests de scripts bash
- `test_run_generators_renders`:
  - Renderizar `run_generators.sh.j2`
  - Verificar comienza con `#!/bin/bash`
  - Verificar estructura básica (no ejecutar, no shellcheck)
  - Verificar len(output.strip()) > 50

### Task 5: Implementar tests de YAML
- `test_canonical_idk_renders_python`:
  - Renderizar `canonical_idk.yml.j2` con python_config
  - Parsear con `yaml.safe_load()`
  - Verificar keywords Python presentes: "class", "def", "import", "async"
  - Verificar al menos 2-3 keywords presentes
- `test_canonical_idk_renders_typescript`:
  - Renderizar con typescript_config
  - Parsear YAML
  - Verificar keywords TypeScript: "interface", "type", "class", "async", "export"

### Task 6: Implementar tests de slash commands
- `test_generate_fractal_docs_command_renders`:
  - Renderizar `generate_fractal_docs.md.j2`
  - Verificar es markdown válido (no vacío, tiene headers)
  - Verificar menciona comandos: "changed", "full"
  - Verificar len(output.strip()) > 50

### Task 7: Implementar tests de integración con ScaffoldService
- `test_scaffold_includes_fractal_scripts`:
  - Crear ScaffoldService().build_plan(config)
  - Verificar file_paths incluye:
    - `scripts/gen_docstring_jsdocs.py`
    - `scripts/gen_docs_fractal.py`
    - `scripts/run_generators.sh`
  - No ejecutar apply_plan, solo verificar build_plan

### Task 8: Implementar tests de conditional_docs
- `test_conditional_docs_includes_fractal_rules`:
  - Renderizar `conditional_docs.md.j2`
  - Verificar contiene sección "Fractal Documentation"
  - Verificar menciona `/generate_fractal_docs`
  - Verificar menciona `canonical_idk.yml`

### Task 9: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Verificar cero regresiones en tests existentes
- Verificar todos los nuevos tests pasan

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py -v --tb=short` - Tests nuevos
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Usar `ast.parse()` para validar Python (no ejecutar código)
- Usar `yaml.safe_load()` para validar YAML
- Para bash, solo verificar shebang y estructura básica (no shellcheck)
- Tests deben ser rápidos y aislados (unit tests, no integration)
- Verificar tanto que renderiza SIN errores como que el OUTPUT es válido
- Si template renderiza vacío o whitespace, debe FALLAR el test
- Keywords Python: class, def, import, async
- Keywords TypeScript: interface, type, class, async, export
- Seguir patrones de `test_scaffold_service.py` para fixtures y assertions
