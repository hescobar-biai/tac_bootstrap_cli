# Chore: Tests para audit trail

## Metadata
issue_number: `158`
adw_id: `chore_3_3`
issue_json: `{"number":158,"title":"Tarea 3.3: Tests para audit trail","body":"/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_3_3\n\n**Tipo**: chore\n**Ganancia**: Verificar que la metadata se registra correctamente en todos los flujos.\n\n**Instrucciones para el agente**:\n\n1. Agregar tests en `tac_bootstrap_cli/tests/test_scaffold_service.py`:\n   - `test_init_generates_bootstrap_metadata` - config.yml tiene seccion bootstrap\n   - `test_bootstrap_metadata_has_valid_timestamp` - ISO8601 parseable\n   - `test_bootstrap_metadata_has_correct_version` - Coincide con __version__\n   - `test_upgrade_updates_last_upgrade` - last_upgrade se actualiza\n\n**Criterios de aceptacion**:\n- Tests pasan\n- Metadata presente en todos los flujos (init, upgrade)\n\n# FASE 3: Audit Trail y Metadata\n\n**Objetivo**: Registrar metadata de generacion en config.yml para trazabilidad.\n\n**Ganancia de la fase**: Saber exactamente cuando se genero el proyecto, con que version del CLI, y cuando fue la ultima actualizacion. Util para upgrades y debugging.\n\n"}`

## Chore Description
Add comprehensive tests to verify that bootstrap metadata is correctly registered in all flows (init and upgrade). The metadata is stored in a top-level `metadata` field in config.yml with the following structure:
- `generated_at`: ISO8601 timestamp string
- `generated_by`: TAC Bootstrap version identifier (e.g., "tac-bootstrap v0.2.0")
- `schema_version`: Integer (default: 2)
- `last_upgrade`: ISO8601 timestamp string or None

The metadata is generated during scaffold_service.apply_plan() (around line 591) and should be updated during UpgradeService.perform_upgrade().

## Relevant Files
Files needed to complete the chore:

- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Add new test class for metadata tests
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that generates metadata (line 591)
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - Service that updates metadata during upgrades
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - BootstrapMetadata model definition (lines 406-497)
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contains __version__ for comparison

### New Files
None. All tests will be added to existing test_scaffold_service.py file.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add test class for bootstrap metadata tests
Create a new test class `TestScaffoldServiceBootstrapMetadata` in test_scaffold_service.py at the end of the file, following the existing test class pattern with proper fixtures.

### Task 2: Implement test_init_generates_bootstrap_metadata
Add test that verifies:
- scaffold_service.build_plan() + apply_plan() generates a config.yml
- The config.yml contains a top-level `metadata` field (not `bootstrap`)
- The metadata field has all expected fields: `generated_at`, `generated_by`, `schema_version`, `last_upgrade`
- Do NOT validate field values in this test (that's for the other tests)
- Use tempfile.TemporaryDirectory() for isolation

### Task 3: Implement test_bootstrap_metadata_has_valid_timestamp
Add test that verifies:
- scaffold_service.apply_plan() generates metadata with `generated_at` field
- The `generated_at` timestamp can be parsed using `datetime.fromisoformat()`
- Do NOT validate that timestamp is reasonable/recent (avoid flakiness)
- Use tempfile.TemporaryDirectory() for isolation

### Task 4: Implement test_bootstrap_metadata_has_correct_version
Add test that verifies:
- scaffold_service.apply_plan() generates metadata with `generated_by` field
- Import `__version__` from `tac_bootstrap` (following existing pattern at scaffold_service.py:585)
- The `generated_by` field matches the expected format: f"tac-bootstrap v{__version__}"
- Use tempfile.TemporaryDirectory() for isolation

### Task 5: Implement test_upgrade_updates_last_upgrade
Add test that verifies:
- After initial scaffold_service.apply_plan(), `metadata.last_upgrade` is None
- After UpgradeService.perform_upgrade(), read the updated config.yml
- Verify `metadata.last_upgrade` is now a non-None ISO8601 timestamp string
- Verify the timestamp can be parsed with `datetime.fromisoformat()`
- Do NOT compare timestamps or check order (avoid complexity/flakiness)
- Use tempfile.TemporaryDirectory() for isolation

### Task 6: Validate all tests pass
Run validation commands to ensure all tests pass with zero regressions.

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceBootstrapMetadata -v --tb=short` - Run new tests
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Full test suite
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The metadata field name in config.yml is `metadata`, not `bootstrap` (despite the issue description)
- BootstrapMetadata is defined at models.py:406-497 with duplicate definitions (use the one referenced by scaffold_service.py)
- Use existing test patterns from test_scaffold_service.py (tempfile.TemporaryDirectory at line 208)
- Import __version__ from tac_bootstrap (same as scaffold_service.py:585)
- Tests should use YAML parsing to read config.yml and verify metadata structure
- Do not validate timestamp reasonableness (e.g., not in future) to avoid test flakiness
- Each test should have a single responsibility (one aspect of metadata validation)
- The upgrade flow in UpgradeService.perform_upgrade() calls scaffold_service.apply_plan() which should update the metadata
