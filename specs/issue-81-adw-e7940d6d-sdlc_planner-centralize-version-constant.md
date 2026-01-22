# Feature: Centralize Version Constant

## Metadata
issue_number: `81`
adw_id: `e7940d6d`
issue_json: `{"number":81,"title":"TAREA 2: Crear constante de versión centralizada","body":"*Archivo**: `tac_bootstrap_cli/tac_bootstrap/__init__.py`\n\n**Descripción**: Crear constante `__version__` centralizada que se use en todo el proyecto.\n\n**Cambios**:\n\n```python\n\"\"\"TAC Bootstrap - Agentic Layer Generator.\"\"\"\n\n__version__ = \"0.2.0\"\n__all__ = [\"__version__\"]\n```\n\n**Archivo**: `tac_bootstrap_cli/tac_bootstrap/domain/models.py`\n\n**Cambios**:\n\n```python\nfrom tac_bootstrap import __version__\n\nclass TACConfig(BaseModel):\n    version: str = Field(default=__version__, ...)\n```\n\n**Archivo**: `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`\n\n**Cambios**:\n\n```python\nfrom tac_bootstrap import __version__\n\n@app.callback()\ndef main(\n    version: bool = typer.Option(None, \"--version\", \"-v\", callback=version_callback)\n):\n    \"\"\"TAC Bootstrap - Agentic Layer Generator.\"\"\"\n    pass\n\ndef version_callback(value: bool):\n    if value:\n        print(f\"TAC Bootstrap v{__version__}\")\n        raise typer.Exit()\n```\n\n**Criterios de Aceptación**:\n- [ ] `__version__` definida en `__init__.py`\n- [ ] CLI muestra versión con `tac --version`\n- [ ] `TACConfig.version` usa `__version__` como default\n- [ ] Un solo lugar para actualizar versión\n"}`

## Feature Description
This feature implements a centralized version constant `__version__` in the TAC Bootstrap CLI package. Currently, the version is hardcoded as "0.1.0" in `__init__.py` and as default "0.2.0" in `TACConfig.version` field. This creates inconsistency and makes version management difficult. The feature will update the version to "0.2.0" across all files and ensure all version references use the single source of truth from `__init__.py`.

## User Story
As a TAC Bootstrap maintainer
I want to have a single centralized version constant
So that version updates only need to happen in one place and all components use the same version number

## Problem Statement
The current implementation has version information scattered across multiple files:
- `__init__.py` has `__version__ = "0.1.0"`
- `models.py` has `version: str = Field(default="0.2.0", ...)` hardcoded
- CLI already imports and uses `__version__` correctly

This creates version inconsistencies and makes it error-prone to update versions. When bumping versions, developers must remember to update multiple files, increasing the risk of mismatches.

## Solution Statement
Centralize version management by:
1. Updating `__version__` to "0.2.0" in `__init__.py` and adding it to `__all__`
2. Making `TACConfig.version` import and use `__version__` as its default value
3. Ensuring CLI continues using the centralized version constant
4. Validating that all components reference the same version source

This approach follows Python packaging best practices where `__version__` in `__init__.py` serves as the single source of truth.

## Relevant Files
Files needed to implement the feature:

- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contains the centralized `__version__` constant that needs to be updated to "0.2.0"
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Contains `TACConfig` model with hardcoded version field that needs to import from `__init__.py`
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Already correctly imports `__version__` but needs validation

### New Files
None - all changes are to existing files

## Implementation Plan

### Phase 1: Update Version Constant
Update the `__version__` constant in `__init__.py` from "0.1.0" to "0.2.0" and ensure proper exports.

### Phase 2: Integrate Version in Models
Update `TACConfig.version` field in `models.py` to use the imported `__version__` as default instead of hardcoded "0.2.0".

### Phase 3: Validation
Verify that CLI version display and all version references work correctly with the centralized constant.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Update __init__.py with new version
- Read current `tac_bootstrap_cli/tac_bootstrap/__init__.py` file
- Update `__version__` from "0.1.0" to "0.2.0"
- Add `__all__ = ["__version__"]` to properly export the version constant
- Keep the existing docstring

### Task 2: Update models.py to use centralized version
- Read current `tac_bootstrap_cli/tac_bootstrap/domain/models.py` file
- Verify `from tac_bootstrap import __version__` is already present (it is at line 11)
- Update `TACConfig.version` field (line 424-427) to use `default=__version__` instead of `default="0.2.0"`
- Ensure the Field description remains: "TAC Bootstrap version used to generate this project"
- Maintain all other Field parameters unchanged

### Task 3: Verify CLI integration
- Read `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` to confirm it already imports and uses `__version__` correctly
- No changes needed - file already imports at line 11 and uses in lines 49 and 74

### Task 4: Run validation commands
- Execute all Validation Commands listed below
- Verify CLI shows "TAC Bootstrap v0.2.0" when running version commands
- Ensure all tests pass with zero regressions
- Confirm type checking passes

## Testing Strategy

### Unit Tests
- Test that `__version__` can be imported from package root: `from tac_bootstrap import __version__`
- Test that `TACConfig().version` equals `__version__`
- Test that CLI `--version` output includes the correct version string
- Test version string format is semantic versioning compatible

### Edge Cases
- Import `__version__` before TACConfig is imported (verify no circular dependencies)
- Instantiate TACConfig without providing version parameter (should use default)
- Instantiate TACConfig with explicit version parameter (should allow override)
- Verify version persists correctly when config is serialized to YAML

## Acceptance Criteria
- `__version__ = "0.2.0"` defined in `__init__.py`
- `__all__ = ["__version__"]` added to `__init__.py` for proper exports
- CLI shows "TAC Bootstrap v0.2.0" with `tac-bootstrap version` command
- CLI shows version with `tac-bootstrap --version` (if implemented)
- `TACConfig.version` uses `__version__` as default value
- When TACConfig is instantiated without version param, it gets "0.2.0"
- Only one place (`__init__.py`) needs to be updated for version bumps
- All tests pass without regressions
- Type checking passes without errors

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Smoke test version command
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap import __version__; from tac_bootstrap.domain.models import TACConfig; assert TACConfig().version == __version__; print(f'✓ Version consistency verified: {__version__}')"` - Version consistency test

## Notes
- The version update from "0.1.0" to "0.2.0" suggests this is a minor version bump, likely reflecting new features added in recent tasks
- The `__version__` constant follows standard Python packaging conventions (PEP 396)
- The centralized version approach makes it easy to automate version bumping in CI/CD pipelines
- Future consideration: Could use `importlib.metadata.version()` for even more robust version management, but the current approach is simpler and sufficient
- The TACConfig.version field should remain mutable to allow generated projects to track which version of TAC Bootstrap created them, even if the generator is later upgraded
