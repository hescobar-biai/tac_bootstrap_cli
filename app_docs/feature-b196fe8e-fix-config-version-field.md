# Fix config.yml Template Field Name (tac_version → version)

**ADW ID:** b196fe8e
**Date:** 2026-01-22
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/b196fe8e/specs/issue-104-adw-b196fe8e-bug_planner-fix-config-template-version-field.md

## Overview

Fixed a field name inconsistency in the config.yml.j2 Jinja2 template where generated configuration files used `tac_version` but the TACConfig Pydantic model expected `version`. This bug caused schema mismatches between generated configs and the domain model that parses them.

## What Was Built

- Updated config.yml.j2 template to use `version` field name (config.yml.j2:6)
- Updated test assertions to verify `version` field instead of `tac_version` (test_scaffold_service.py:645, 649)
- Removed duplicate `tac_version` field from test fixture data (test_upgrade_service.py:281)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`: Changed field name from `tac_version` to `version` in line 6
- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Updated assertions to check for `version` field instead of `tac_version`
- `tac_bootstrap_cli/tests/test_upgrade_service.py`: Removed redundant `tac_version` key from test config data

### Key Changes

- **Template Fix**: Line 6 of config.yml.j2 now renders `version: "{{ config.version }}"` instead of `tac_version: "{{ config.version }}"`, ensuring generated config files match the TACConfig model schema defined in domain/models.py:426-429
- **Test Alignment**: Test assertions now verify the correct field name `version`, ensuring tests validate the actual model schema
- **Duplicate Removal**: Removed duplicate `tac_version` entry in test_upgrade_service.py that would have created configs with both fields

## How to Use

This fix is automatically applied when:

1. **Generating new projects**: Run `tac-bootstrap init` and the generated config.yml will have the correct `version` field
   ```bash
   cd tac_bootstrap_cli
   uv run tac-bootstrap init my-project
   # Resulting config.yml will contain: version: "0.2.0"
   ```

2. **Testing scaffolding**: The scaffold service tests now validate the correct field
   ```bash
   cd tac_bootstrap_cli
   uv run pytest tests/test_scaffold_service.py -v -k "test_adw_scaffold_generates_config"
   ```

## Configuration

No configuration changes required. The fix is transparent:

- **Before**: Generated configs had `tac_version: "0.2.0"` (incorrect)
- **After**: Generated configs have `version: "0.2.0"` (correct, matches TACConfig model)

The TACConfig Pydantic model already expected `version` field:
```python
# domain/models.py:426-429
version: str = Field(
    default=__version__,
    description="TAC Bootstrap version used to generate this project"
)
```

## Testing

Run the full test suite to validate the fix:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Specific tests that validate this fix:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceADWCompleteness::test_adw_scaffold_generates_config -v
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v
```

## Notes

- This is a breaking change for newly generated projects, but only affects the field name in config.yml
- Existing projects that already have `tac_version` in their config.yml will need manual migration to `version`
- No backward compatibility concerns since this only affects newly generated projects from this version forward
- The TACConfig model already used the correct field name (`version`), so this fix brings the template in line with the model
- All tests pass with zero regressions after the fix
