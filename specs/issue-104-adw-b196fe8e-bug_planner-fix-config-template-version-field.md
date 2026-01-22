# Bug: Fix config.yml.j2 template to use 'version' instead of 'tac_version'

## Metadata
issue_number: `104`
adw_id: `b196fe8e`
issue_json: `{"number":104,"title":"Tarea 1: Cambiar template config.yml.j2 de tac_version a version","body":"/bug\n**Archivos a modificar**:\n1. `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2` (template)\n\n\n**Prompt para el agente**:\n\n```\nAbre el archivo tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2\n\nBusca la línea que contiene:\ntac_version: \"{{ config.version }}\"\n\nReemplázala con:\nversion: \"{{ config.version }}\"\n\nEste cambio hace que nuevos proyectos generen el campo correcto que el modelo TACConfig espera.\n\n## Verificación\n\nEjecuta: cd tac_bootstrap_cli && uv run pytest tests/ -q\nTodos los tests deben pasar (o mostrar errores relacionados con tests que esperan tac_version).\n```"}`

## Bug Description
The Jinja2 template file `config.yml.j2` generates a `tac_version` field in the rendered config.yml file, but the TACConfig Pydantic model in `domain/models.py` expects a `version` field instead. This mismatch causes inconsistency between generated configuration files and the data model that reads them.

**Symptoms:**
- New projects generated with `tac-bootstrap init` will have config.yml files with `tac_version: "x.x.x"`
- The TACConfig model (line 426 in domain/models.py) defines `version: str` not `tac_version: str`
- This creates a schema mismatch between generated configs and the model

**Expected Behavior:**
- Template should generate `version: "{{ config.version }}"` to match the TACConfig model
- Generated config.yml files should be directly parseable by TACConfig without field name mismatches

## Problem Statement
Fix the field name inconsistency in the config.yml.j2 template to ensure generated configuration files match the TACConfig Pydantic model schema.

## Solution Statement
Change the field name in line 6 of `tac_bootstrap/templates/config/config.yml.j2` from `tac_version` to `version`, and update any tests that verify the old field name to expect the new correct field name.

## Steps to Reproduce
1. Generate a new project: `cd tac_bootstrap_cli && uv run tac-bootstrap init --dry-run`
2. Inspect the rendered config.yml (or template directly)
3. Observe field name is `tac_version`
4. Compare with TACConfig model at line 426 in domain/models.py
5. Note the field is named `version` not `tac_version`

## Root Cause Analysis
The template file `config.yml.j2` was created with the field name `tac_version`, but the Pydantic model was designed with the field name `version`. This is a simple naming inconsistency between the template and the model definition.

Looking at the code:
- Template (line 6): `tac_version: "{{ config.version }}"`
- Model (line 426-429): `version: str = Field(default=__version__, description="TAC Bootstrap version used to generate this project")`

The comment in line 5 of the template says "TAC Bootstrap release version" which matches the model's field description, confirming these are meant to be the same field with different names.

## Relevant Files
Files to fix the bug:

1. **tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2** (line 6)
   - Template file that generates config.yml
   - Contains the incorrect field name `tac_version`
   - Needs to be changed to `version`

2. **tac_bootstrap_cli/tests/test_scaffold_service.py** (lines 645, 649)
   - Test file that validates generated config.yml content
   - Contains assertions checking for `tac_version` field
   - Needs to be updated to check for `version` instead

3. **tac_bootstrap_cli/tests/test_upgrade_service.py** (line 281)
   - Test file that constructs expected config structure
   - Uses `tac_version` key in dictionary
   - Needs to be changed to `version` key

### New Files
None required.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Update config.yml.j2 template
- Open `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`
- Locate line 6: `tac_version: "{{ config.version }}"`
- Replace with: `version: "{{ config.version }}"`
- This makes the generated config match TACConfig model schema

### Task 2: Update test_scaffold_service.py assertions
- Open `tac_bootstrap_cli/tests/test_scaffold_service.py`
- Find line 645: `assert "tac_version" in parsed, "tac_version field should be in config.yml"`
- Replace with: `assert "version" in parsed, "version field should be in config.yml"`
- Find line 649: `assert parsed["tac_version"] == "0.2.0", "tac_version should default to 0.2.0"`
- Replace with: `assert parsed["version"] == "0.2.0", "version should default to 0.2.0"`

### Task 3: Update test_upgrade_service.py expected data
- Open `tac_bootstrap_cli/tests/test_upgrade_service.py`
- Find line 281: `"tac_version": config.version,`
- Replace with: `"version": config.version,`

### Task 4: Execute Validation Commands
- Run all validation commands listed below to ensure zero regressions

## Validation Commands
Ejecutar todos los comandos para validar el fix con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a simple field name fix with no behavior changes
- All occurrences of `tac_version` need to be changed to `version` for consistency
- The TACConfig model already uses the correct field name (`version`)
- No database migrations or backward compatibility concerns since this only affects newly generated projects
