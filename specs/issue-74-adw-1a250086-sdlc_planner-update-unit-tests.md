# Chore: Update Unit Tests for add-agentic Existing Repo Scenario

## Metadata
issue_number: `74`
adw_id: `1a250086`
issue_json: `{"number":74,"title":"Tarea 3: Actualizar tests unitarios","body":"### Descripción\nVerificar y actualizar tests para cubrir el escenario de `add-agentic` en repositorios existentes.\n\n### Prompt\n\n```\nRevisa y actualiza los tests del scaffold_service para cubrir el caso de add-agentic en repos existentes.\n\n**Archivo de tests**: tac_bootstrap_cli/tests/test_scaffold_service.py\n\n**Verificar que existe un test para**:\n1. `build_plan()` con `existing_repo=True` genera archivos con `FileAction.CREATE`\n2. `apply_plan()` crea archivos cuando no existen\n3. `apply_plan()` NO sobrescribe archivos existentes (respeta `FileAction.CREATE`)\n\n**Si no existen, crear tests como**:\n\n```python\ndef test_build_plan_existing_repo_creates_templates():\n    \"\"\"Verify add-agentic creates templates for existing repos.\"\"\"\n    service = ScaffoldService()\n    config = create_test_config()\n\n    plan = service.build_plan(config, existing_repo=True)\n\n    # Should have claude files with CREATE action (not SKIP)\n    claude_files = [op for op in plan.operations if '.claude/' in str(op.path)]\n    assert len(claude_files) > 0\n    for op in claude_files:\n        assert op.action == FileAction.CREATE, f\"{op.path} should be CREATE, not {op.action}\"\n\ndef test_apply_plan_does_not_overwrite_existing():\n    \"\"\"Verify CREATE action doesn't overwrite existing files.\"\"\"\n    # Setup: create a file that already exists\n    # Run apply_plan with CREATE action\n    # Verify file was not modified\n```\n\n**Ejecutar tests**:\n```bash\ncd tac_bootstrap_cli\nmake test\n```\n\n**Criterios de aceptación**:\n- [ ] Tests cubren el caso de existing_repo=True\n- [ ] Tests verifican que CREATE no sobrescribe\n- [ ] Todos los tests pasan"}`

## Chore Description
Actualizar y expandir los tests unitarios del `ScaffoldService` para verificar el comportamiento correcto del escenario `add-agentic` (when `existing_repo=True`). El issue requiere confirmar que:

1. `build_plan()` con `existing_repo=True` genera archivos con `FileAction.CREATE` (no SKIP)
2. `apply_plan()` crea archivos cuando no existen
3. `apply_plan()` NO sobrescribe archivos existentes cuando la acción es `FileAction.CREATE`

Actualmente, el archivo de tests tiene:
- `test_build_plan_existing_repo_creates_files` (línea 134) - verifica que existing_repo=True usa CREATE action
- `test_apply_plan_idempotent` (línea 297) - verifica que apply_plan es idempotente
- `test_apply_plan_skips_existing_files` (línea 261) - verifica que archivos con SKIP action no se sobrescriben

Sin embargo, falta un test explícito que verifique que `FileAction.CREATE` NO sobrescribe archivos existentes durante `apply_plan()`.

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Archivo principal de tests del ScaffoldService. Necesita agregar test explícito para verificar que CREATE no sobrescribe.
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Implementación del ScaffoldService. Revisar lógica de apply_plan (líneas 428-510) para entender comportamiento de FileAction.CREATE.
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Definición de FileAction enum para confirmar acciones disponibles.
- `tac_bootstrap_cli/Makefile` - Para ejecutar tests con `make test`.

### New Files
No se requieren archivos nuevos.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analizar Tests Existentes
- Leer `tac_bootstrap_cli/tests/test_scaffold_service.py` líneas 134-152 (test_build_plan_existing_repo_creates_files)
- Leer `tac_bootstrap_cli/tests/test_scaffold_service.py` líneas 297-312 (test_apply_plan_idempotent)
- Leer `tac_bootstrap_cli/tests/test_scaffold_service.py` líneas 261-282 (test_apply_plan_skips_existing_files)
- Confirmar que estos tests cubren parcialmente los requisitos

### Task 2: Analizar Implementación de apply_plan
- Leer `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` líneas 428-510
- Confirmar lógica en líneas 465-473: cuando file_path.exists() y action==CREATE y not force, se incrementa files_skipped
- Verificar que esta lógica implementa correctamente el comportamiento esperado

### Task 3: Crear Test Explícito para CREATE No Sobrescribe
- Agregar nuevo test `test_apply_plan_create_does_not_overwrite_existing` en la clase `TestScaffoldServiceApplyPlan`
- El test debe:
  1. Crear un directorio temporal con tempfile.TemporaryDirectory()
  2. Crear un archivo manualmente con contenido "ORIGINAL CONTENT"
  3. Construir un plan con build_plan() que incluya ese archivo con action=CREATE
  4. Ejecutar apply_plan() sin force=True
  5. Verificar que el archivo mantiene el contenido original "ORIGINAL CONTENT"
  6. Verificar que result.files_skipped >= 1

### Task 4: Reforzar Test de existing_repo=True con Verificación de Claude Files
- Revisar test existente `test_build_plan_existing_repo_creates_files` (línea 134)
- Agregar verificación específica para archivos .claude/ con action=CREATE
- Ejemplo: filtrar archivos claude y verificar que todos tienen FileAction.CREATE

### Task 5: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Verificar que todos los tests pasan
- Verificar que no hay regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short` - Tests del scaffold service
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- El test `test_apply_plan_idempotent` ya verifica parcialmente este comportamiento al ejecutar apply_plan dos veces, pero no verifica explícitamente el contenido de archivos existentes
- El test nuevo debe ser más directo: crear archivo manualmente, intentar apply_plan con CREATE, verificar que no se sobrescribe
- El comportamiento esperado está en scaffold_service.py líneas 465-473: si exists() y action==CREATE y not force → skip
- Los tests existentes ya cubren la mayoría de los casos, solo falta hacer el comportamiento más explícito y verificable
