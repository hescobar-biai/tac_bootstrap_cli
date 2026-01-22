# Bug: Add Normalization for Legacy 'tac_version' Field in upgrade_service.py

## Metadata
issue_number: `106`
adw_id: `da2e1199`
issue_json: `{"number":106,"title":"Tarea 2: Agregar normalización en upgrade_service.py","body":"/bug\n**Archivos a modificar**:\n1. `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` (base)\n\n**Prompt para el agente**:\n\n```\nAbre el archivo tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py\n\nBusca el método que carga la configuración del proyecto target. Puede llamarse `_load_config`, `load_existing_config`, o similar.\n\nAntes de parsear el YAML a TACConfig, agrega normalización para compatibilidad hacia atrás:\n\n1. Busca donde se hace algo como:\n   config_data = yaml.safe_load(f)\n\n2. Después de esa línea, agrega:\n   # Normalize legacy field names for compatibility\n   if \"tac_version\" in config_data and \"version\" not in config_data:\n       config_data[\"version\"] = config_data.pop(\"tac_version\")\n\nEsto permite que proyectos viejos con tac_version se actualicen correctamente.\n\n## Verificación\n\nEjecuta: cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v"}`

## Bug Description
The upgrade service currently fails when attempting to upgrade projects that use the legacy `tac_version` field instead of the new `version` field in their `config.yml`. This is a backward compatibility issue that prevents users from upgrading projects created with older versions of TAC Bootstrap (pre-0.2.0).

When `load_existing_config()` is called in upgrade_service.py:86-100, it loads the YAML config at line 92 and then immediately sets `config_data["version"] = self.get_target_version()` at line 95. However, if the config uses the legacy `tac_version` field, the TACConfig model initialization at line 97 will fail because the Pydantic model expects a `version` field.

**Expected Behavior**: Projects with legacy `tac_version` field should be automatically normalized to use `version` field during the upgrade process.

**Actual Behavior**: Upgrade fails when encountering configs with `tac_version` instead of `version`.

## Problem Statement
Add backward compatibility normalization in `upgrade_service.py` to convert legacy `tac_version` field to `version` field before passing config data to the TACConfig Pydantic model.

## Solution Statement
Insert normalization logic in the `load_existing_config()` method immediately after loading YAML data (line 92) and before setting the version (line 95). The normalization will:
1. Check if `tac_version` exists and `version` does not exist
2. If true, rename `tac_version` to `version` using pop() to remove the legacy field
3. Allow the existing version update logic to proceed normally

This minimal change ensures backward compatibility without modifying the core TACConfig model or adding complex migration logic.

## Steps to Reproduce
1. Create a mock config.yml with legacy field:
   ```yaml
   tac_version: "0.1.0"
   project:
     name: "legacy-project"
   ```
2. Initialize UpgradeService with this config
3. Call `load_existing_config()`
4. Observe that TACConfig initialization fails due to missing `version` field

## Root Cause Analysis
The root cause is the absence of field normalization logic between YAML parsing and Pydantic model initialization. When TAC Bootstrap changed from `tac_version` to `version` in the schema, existing projects with old configs became incompatible with the upgrade process.

The current code at upgrade_service.py:86-100 performs these steps:
1. Line 92: Load YAML → `config_data` may have `tac_version` instead of `version`
2. Line 95: Set `config_data["version"]` → Overwrites if exists, creates new if doesn't exist
3. Line 97: Initialize TACConfig → Pydantic expects `version` field

The issue is that line 95 only sets the version value but doesn't handle the case where the old `tac_version` field still exists alongside the new `version` field, which could cause confusion or validation issues in stricter scenarios.

## Relevant Files
Files to fix the bug:

1. **tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py** (line 86-100)
   - Contains `load_existing_config()` method that needs normalization logic
   - Already has YAML loading and version setting logic, just missing normalization step

2. **tac_bootstrap_cli/tests/test_upgrade_service.py**
   - Existing comprehensive test suite with 30+ tests
   - Needs additional test cases to verify legacy field normalization works correctly

### New Files
None. This is a bug fix requiring only modifications to existing files.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add Normalization Logic to load_existing_config()
- Open `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py`
- Locate the `load_existing_config()` method (lines 81-100)
- Find the line `config_data = yaml.safe_load(f)` (line 92)
- After line 92, before line 95, insert the normalization code:
  ```python
  # Normalize legacy field names for compatibility
  if "tac_version" in config_data and "version" not in config_data:
      config_data["version"] = config_data.pop("tac_version")
  ```
- Ensure proper indentation (12 spaces to match surrounding code)

### Task 2: Add Test Cases for Legacy Field Normalization
- Open `tac_bootstrap_cli/tests/test_upgrade_service.py`
- Add three new test methods in the `TestUpgradeService` class after line 214:
  1. `test_load_existing_config_normalizes_legacy_tac_version()` - Test that `tac_version` is converted to `version`
  2. `test_load_existing_config_preserves_existing_version()` - Test that existing `version` field is not overwritten by normalization
  3. `test_load_existing_config_handles_both_fields()` - Test that when both `tac_version` and `version` exist, `version` takes precedence

### Task 3: Implement Test Case 1 - Normalize Legacy Field
- Add test method:
  ```python
  def test_load_existing_config_normalizes_legacy_tac_version(self, tmp_path: Path) -> None:
      """load_existing_config should normalize legacy 'tac_version' to 'version'."""
      # Create config with legacy tac_version field
      config_file = tmp_path / "config.yml"
      config_data = {
          "tac_version": "0.1.0",
          "schema_version": 1,
          "project": {
              "name": "legacy-project",
              "language": "python",
              "package_manager": "uv",
          },
          "commands": {
              "start": "python main.py",
              "test": "pytest",
          },
          "claude": {
              "settings": {
                  "project_name": "legacy-project",
              }
          },
      }
      with open(config_file, "w") as f:
          yaml.dump(config_data, f)

      service = UpgradeService(tmp_path)
      config = service.load_existing_config()

      assert config is not None
      assert isinstance(config, TACConfig)
      assert config.project.name == "legacy-project"
      # Version should be updated to target (not legacy value)
      assert config.version == __version__
  ```

### Task 4: Implement Test Case 2 - Preserve Existing Version
- Add test method:
  ```python
  def test_load_existing_config_preserves_existing_version(self, tmp_path: Path) -> None:
      """load_existing_config should preserve existing 'version' field."""
      # Create config with modern version field
      config_file = tmp_path / "config.yml"
      config_data = {
          "version": "0.1.5",
          "schema_version": 1,
          "project": {
              "name": "modern-project",
              "language": "python",
              "package_manager": "uv",
          },
          "commands": {
              "start": "python main.py",
              "test": "pytest",
          },
          "claude": {
              "settings": {
                  "project_name": "modern-project",
              }
          },
      }
      with open(config_file, "w") as f:
          yaml.dump(config_data, f)

      service = UpgradeService(tmp_path)
      config = service.load_existing_config()

      assert config is not None
      assert isinstance(config, TACConfig)
      # Version should be updated to target
      assert config.version == __version__
  ```

### Task 5: Implement Test Case 3 - Handle Both Fields
- Add test method:
  ```python
  def test_load_existing_config_handles_both_fields(self, tmp_path: Path) -> None:
      """load_existing_config should keep 'version' when both fields present."""
      # Create config with both tac_version and version (migration in progress)
      config_file = tmp_path / "config.yml"
      config_data = {
          "tac_version": "0.0.9",  # Old field
          "version": "0.1.0",      # New field (should take precedence)
          "schema_version": 1,
          "project": {
              "name": "migrating-project",
              "language": "python",
              "package_manager": "uv",
          },
          "commands": {
              "start": "python main.py",
              "test": "pytest",
          },
          "claude": {
              "settings": {
                  "project_name": "migrating-project",
              }
          },
      }
      with open(config_file, "w") as f:
          yaml.dump(config_data, f)

      service = UpgradeService(tmp_path)
      config = service.load_existing_config()

      assert config is not None
      assert isinstance(config, TACConfig)
      # Version should be updated to target (not legacy value)
      assert config.version == __version__
  ```

### Task 6: Run All Validation Commands
- Execute all validation commands to ensure zero regressions:
  - `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v`
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
  - `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Validation Commands
Ejecutar todos los comandos para validar el fix con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v` - Test the specific service
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a minimal, surgical fix targeting only the normalization issue
- No changes to TACConfig model or schema required
- The fix uses pop() to completely remove the legacy field, preventing confusion
- When both fields exist, the condition `and "version" not in config_data` ensures we don't overwrite the modern field
- The existing version update logic at line 95 remains unchanged and continues to work correctly
- All three test scenarios are covered: legacy only, modern only, and both fields present
- This approach maintains simplicity and avoids over-engineering
