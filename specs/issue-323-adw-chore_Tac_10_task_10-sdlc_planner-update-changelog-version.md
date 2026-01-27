# Chore: Actualizar CHANGELOG.md e incrementar versión a 0.5.1

## Metadata
issue_number: `323`
adw_id: `chore_Tac_10_task_10`
issue_json: `{"number":323,"title":"Actualizar CHANGELOG.md e incrementar versión a 0.5.1","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_10_task_10\n\n-- **Descripción**: Documentar todos los cambios introducidos en esta iteración y actualizar la versión del proyecto.\n- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`\n- **Contenido del changelog**:\n```markdown\n## [0.5.1] - 2026-01-26\n\n### Added\n- Nuevo template `parallel_subagents.md.j2` para delegación multi-agente (TAC-10 Level 4)\n- Nuevo template `t_metaprompt_workflow.md.j2` para generación de prompts (TAC-10 Level 6)\n- Nuevo template `cc_hook_expert_improve.md.j2` para self-improvement (TAC-10 Level 7)\n- Nuevo template `build_w_report.md.j2` con reporte YAML estructurado\n- Hooks adicionales: UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd\n- Integración de universal_hook_logger en todos los hooks\n- Directorios `agents/hook_logs/` y `agents/context_bundles/` en scaffold\n\n### Changed\n- settings.json.j2 actualizado con configuración completa de hooks\n- scaffold_service.py ahora crea estructura de directorios agents/\n```\n\n---\n\n## Verificación Final\n\n```bash\n# 1. Ejecutar tests\ncd /Users/hernandoescobar/Documents/Celes/tac_bootstrap\nuv run pytest tac_bootstrap_cli/tests/ -v\n\n# 2. Verificar templates se cargan correctamente\nuv run python -c \"\nfrom tac_bootstrap.infrastructure.template_repo import TemplateRepository\nrepo = TemplateRepository()\ntemplates = ['parallel_subagents.md.j2', 't_metaprompt_workflow.md.j2', 'build_w_report.md.j2']\nfor t in templates:\n    print(f'Template {t}: OK')\n\"\n\n# 3. Dry-run de scaffold\nuv run tac-bootstrap init --name test-tac10 --language python --framework fastapi --dry-run"}`

## Chore Description
Documentar todos los cambios introducidos durante la iteración TAC-10 en el CHANGELOG.md y actualizar la versión del proyecto de 0.5.0 a 0.5.1 en el archivo pyproject.toml. Esta actualización refleja la adición de nuevos templates para comandos avanzados (parallel_subagents, t_metaprompt_workflow, cc_hook_expert_improve, build_w_report), hooks adicionales, y cambios en la estructura del scaffold.

## Relevant Files
Archivos necesarios para completar esta tarea:

- **CHANGELOG.md**: Archivo principal donde se documenta el historial de cambios del proyecto siguiendo Keep a Changelog format
- **tac_bootstrap_cli/pyproject.toml**: Archivo de configuración del paquete Python que contiene la versión actual (0.5.0) que debe incrementarse a 0.5.1
- **tac_bootstrap_cli/tests/**: Directorio de tests para validar que la actualización no introduce regresiones

### New Files
No se requieren archivos nuevos. Solo se editarán archivos existentes.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar CHANGELOG.md con versión 0.5.1
- Leer el contenido actual de CHANGELOG.md
- Insertar la nueva sección [0.5.1] después de la línea 7 (antes de la sección [0.5.0])
- Agregar el contenido especificado en el issue:
  - Sección Added con los 7 nuevos templates/features
  - Sección Changed con 2 actualizaciones
- Mantener el formato Keep a Changelog
- Verificar que la fecha sea 2026-01-26

### Task 2: Incrementar versión en pyproject.toml
- Leer tac_bootstrap_cli/pyproject.toml
- Cambiar el campo version de "0.5.0" a "0.5.1" en la línea 3
- Mantener todo el formato del archivo intacto

### Task 3: Ejecutar validation commands
- Ejecutar todos los comandos de validación para verificar cero regresiones
- Verificar que pytest pasa todos los tests
- Verificar que ruff check no reporta errores
- Verificar que el CLI carga correctamente

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Esta es una chore de documentación y versionado, no requiere cambios de código funcional
- La versión 0.5.1 es un incremento patch según Semantic Versioning
- El CHANGELOG debe insertarse en orden cronológico descendente (más reciente primero)
- Los cambios documentados corresponden a la iteración TAC-10 completa
- La fecha especificada en el issue es 2026-01-26, mantener esa fecha en el changelog
