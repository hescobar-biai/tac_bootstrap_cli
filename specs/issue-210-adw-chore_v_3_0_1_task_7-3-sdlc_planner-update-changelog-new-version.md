# Chore: Actualizar CHANGELOG con nueva version

## Metadata
issue_number: `210`
adw_id: `chore_v_3_0_1_task_7-3`
issue_json: `{"number":210,"title":"Actualizar CHANGELOG con nueva version","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_3_0_1_task_7-3\n\n### Archivos a modificar\n- **Archivo raiz**: `CHANGELOG.md`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2` (crear si no existe)\n\n### Contexto\nDespues de completar las tareas anteriores, es necesario documentar los cambios en el CHANGELOG siguiendo el formato Keep a Changelog y Semantic Versioning.\n\n### Determinar version\n- Si solo hay fixes de bugs: incrementar PATCH (0.x.Y)\n- Si hay nuevas features sin breaking changes: incrementar MINOR (0.X.0)\n- El conjunto de cambios incluye:\n  - 1 bug fix (config.yml)\n  - 2 features (--once en triggers)\n  - 3 mejoras de documentacion\n  - **Recomendacion**: incrementar MINOR por las nuevas features\n\n### Formato del CHANGELOG\n```markdown\n# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\nand this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n## [Unreleased]\n\n## [0.X.0] - YYYY-MM-DD\n\n### Added\n- `--once` flag in `trigger_cron.py` for single execution cycle\n- `--once` flag in `trigger_issue_chain.py` for single execution cycle\n- Documentation for `trigger_issue_chain.py` in ADWs README\n- Trigger polling configuration section in ADWs README\n- Complete docstring in `adw_triggers/__init__.py` with all available triggers\n\n### Fixed\n- `config.yml` structure aligned with `TACConfig` schema\n- Moved `allowed_paths` and `forbidden_paths` into `agentic.safety` section\n- Restructured `workflows` configuration under `agentic.workflows`\n- Added missing `claude` configuration section\n\n### Changed\n- N/A\n\n## [0.X-1.0] - Previous date\n...\n```\n\n### Pasos a ejecutar\n1. Determinar la version actual leyendo `CHANGELOG.md` o `pyproject.toml`\n2. Calcular la nueva version (MINOR bump por features)\n3. Abrir `CHANGELOG.md` (o crearlo si no existe)\n4. Agregar nueva entrada con:\n   - Numero de version siguiendo SemVer\n   - Fecha en formato YYYY-MM-DD\n   - Secciones Added, Fixed, Changed segun corresponda\n   - Descripcion concisa de cada cambio\n5. Si el template `CHANGELOG.md.j2` no existe, crearlo con estructura base\n6. Verificar que el formato sigue Keep a Changelog\n\n### Criterios de aceptacion\n- [ ] `CHANGELOG.md` tiene entrada para la nueva version\n- [ ] La version sigue Semantic Versioning (MAJOR.MINOR.PATCH)\n- [ ] La fecha esta en formato ISO (YYYY-MM-DD)\n- [ ] Todos los cambios de las tareas 1-6 estan documentados\n- [ ] El formato sigue Keep a Changelog (Added, Fixed, Changed, etc.)\n- [ ] El template `.j2` existe y tiene estructura base\n- [ ] Verificar con:\n  ```bash\n  # Verificar que existe entrada reciente\n  head -30 CHANGELOG.md\n\n  # Verificar formato de fecha\n  grep -E \"^\\#\\# \\[.+\\] - [0-9]{4}-[0-9]{2}-[0-9]{2}\" CHANGELOG.md\n\n  # Verificar que menciona --once\n  grep \"\\-\\-once\" CHANGELOG.md"}`

## Chore Description

Documentar los cambios implementados en las tareas 1-6 del conjunto de mejoras v3.0.1 en el archivo CHANGELOG.md siguiendo el formato Keep a Changelog y Semantic Versioning.

Los cambios incluyen:
- 1 bug fix: alineación de estructura de config.yml con schema TACConfig
- 2 features: flags `--once` en trigger_cron.py y trigger_issue_chain.py
- 3 mejoras de documentación: docs de trigger_issue_chain.py, sección de trigger polling config, y docstrings completos en __init__.py

Dado que incluye nuevas features (flags --once), se debe incrementar la version MINOR desde 0.3.0 a 0.4.0.

## Relevant Files

Archivos para completar la chore:

- `CHANGELOG.md` - Archivo principal de changelog en raíz del proyecto. Actualmente en versión 0.3.0 (2026-01-25). Se agregará nueva entrada para 0.4.0.

- `tac_bootstrap_cli/pyproject.toml` - Contiene versión canónica del proyecto (0.3.0). Se usa como referencia para determinar versión actual.

- `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2` - Template Jinja2 para generar CHANGELOG.md en proyectos generados. Actualmente no existe, debe crearse.

- `adws/adw_triggers/trigger_cron.py` - Para verificar implementación del flag --once

- `adws/adw_triggers/trigger_issue_chain.py` - Para verificar implementación del flag --once

- `adws/README.md` - Para verificar documentación añadida sobre triggers

- `adws/adw_triggers/__init__.py` - Para verificar docstrings completos

- `config.yml` - Para verificar cambios en estructura alineada con TACConfig

### New Files

- `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2` - Template base para CHANGELOG.md

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verificar versión actual y cambios implementados

- Leer `CHANGELOG.md` para confirmar versión actual (0.3.0)
- Leer `tac_bootstrap_cli/pyproject.toml` para confirmar consistencia de versión
- Verificar implementación de los cambios mencionados:
  - Leer `adws/adw_triggers/trigger_cron.py` para confirmar flag --once
  - Leer `adws/adw_triggers/trigger_issue_chain.py` para confirmar flag --once
  - Leer `adws/README.md` para confirmar documentación de triggers
  - Leer `adws/adw_triggers/__init__.py` para confirmar docstrings
  - Leer `config.yml` para confirmar reestructuración

### Task 2: Actualizar CHANGELOG.md con nueva versión 0.4.0

- Abrir `CHANGELOG.md`
- Insertar nueva entrada después de la sección [0.3.0] con:
  - Versión: `[0.4.0]`
  - Fecha: `2026-01-25`
  - Sección `### Added` con:
    - `--once` flag in `adws/adw_triggers/trigger_cron.py` for single execution cycle
    - `--once` flag in `adws/adw_triggers/trigger_issue_chain.py` for single execution cycle
    - Documentation for `trigger_issue_chain.py` in `adws/README.md`
    - Trigger polling configuration section in `adws/README.md`
    - Complete docstring in `adws/adw_triggers/__init__.py` with all available triggers
  - Sección `### Fixed` con:
    - `config.yml` structure aligned with `TACConfig` schema
    - Moved `allowed_paths` and `forbidden_paths` into `agentic.safety` section
    - Restructured `workflows` configuration under `agentic.workflows`
    - Added missing `claude` configuration section
  - Sección `### Changed` (vacía si no aplica o con "N/A")
- Preservar todas las entradas de versiones anteriores

### Task 3: Crear template CHANGELOG.md.j2

- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2`
- Contenido del template:
  - Estructura base siguiendo formato Keep a Changelog
  - Header con referencias a Keep a Changelog y Semantic Versioning
  - Sección `[Unreleased]` vacía
  - Comentario indicando que versiones se agregan manualmente
  - Usar variables Jinja2 para metadata del proyecto: `{{ config.project.name }}`
  - El template proporciona estructura inicial, no gestión dinámica de versiones

### Task 4: Validar formato y contenido

- Ejecutar comandos de verificación:
  ```bash
  head -30 CHANGELOG.md
  grep -E "^\## \[.+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}" CHANGELOG.md
  grep "\-\-once" CHANGELOG.md
  ```
- Verificar que:
  - Entrada [0.4.0] - 2026-01-25 existe
  - Formato de fecha es correcto (ISO)
  - Todas las secciones Added y Fixed están completas
  - El término "--once" aparece en el changelog
  - Template .j2 existe y tiene estructura válida

### Task 5: Ejecutar Validation Commands

- Ejecutar todos los comandos de validación para asegurar cero regresiones:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
  cd tac_bootstrap_cli && uv run ruff check .
  cd tac_bootstrap_cli && uv run tac-bootstrap --help
  ```

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `head -30 CHANGELOG.md` - Verificar entrada nueva
- `grep -E "^\## \[.+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}" CHANGELOG.md` - Verificar formato de fecha
- `grep "\-\-once" CHANGELOG.md` - Verificar mención de feature

## Notes

- La versión actual es 0.3.0 (confirmada en CHANGELOG.md y pyproject.toml)
- La nueva versión será 0.4.0 (MINOR bump por nuevas features --once)
- Fecha de release: 2026-01-25 (fecha actual)
- Esta tarea NO actualiza pyproject.toml - solo CHANGELOG.md y su template
- El template CHANGELOG.md.j2 proporciona estructura inicial para proyectos generados, pero el mantenimiento del changelog es típicamente manual
- Todos los cambios mencionados en el issue deben estar ya implementados en tareas previas (1-6)
