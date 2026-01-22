# Upgrade Service: Legacy Config Normalization

**ADW ID:** da2e1199
**Date:** 2026-01-22
**Specification:** specs/issue-106-adw-da2e1199-bug_planner-upgrade-config-normalization.md

## Overview

This bug fix adds backward compatibility to the upgrade service by automatically normalizing legacy `tac_version` field names to the modern `version` field. This ensures that projects created with TAC Bootstrap pre-0.2.0 can be successfully upgraded without manual config file modifications.

## What Was Built

- Normalization logic in `UpgradeService.load_existing_config()` method
- Comprehensive test coverage for three migration scenarios:
  - Legacy config with only `tac_version` field
  - Modern config with only `version` field
  - Mixed config with both fields present

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py`: Added field normalization logic in the config loading method
- `tac_bootstrap_cli/tests/test_upgrade_service.py`: Added three new test cases covering all normalization scenarios

### Key Changes

**upgrade_service.py:94-97**
- Added normalization block after YAML loading (line 92)
- Checks if legacy `tac_version` exists in loaded config data
- If `version` field is missing, copies value from `tac_version` before removing it
- If `version` field already exists, only removes the legacy `tac_version` field
- Uses `pop()` to completely remove legacy field, preventing confusion
- Executes before the version update logic (line 100) to ensure clean state

**test_upgrade_service.py:216-315**
- `test_load_existing_config_normalizes_legacy_tac_version()`: Verifies legacy configs are properly normalized
- `test_load_existing_config_preserves_existing_version()`: Ensures modern configs work without issues
- `test_load_existing_config_handles_both_fields()`: Tests edge case where both fields coexist

## How to Use

This fix is transparent to users. When running the upgrade command on projects with legacy configs:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap upgrade /path/to/legacy-project
```

The upgrade service will now:
1. Load the existing `config.yml` file
2. Automatically detect if `tac_version` field is present
3. Normalize it to `version` field if needed
4. Proceed with normal upgrade process
5. Write updated config with modern field names

## Configuration

No configuration changes required. The normalization is automatic and handles:

- **Legacy projects**: Only have `tac_version` → normalized to `version`
- **Modern projects**: Only have `version` → no changes needed
- **Transitional projects**: Have both fields → `version` takes precedence, `tac_version` is removed

## Testing

Run the upgrade service tests to verify normalization works correctly:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v -k "legacy"
```

Expected output:
```
test_upgrade_service.py::TestUpgradeService::test_load_existing_config_normalizes_legacy_tac_version PASSED
test_upgrade_service.py::TestUpgradeService::test_load_existing_config_preserves_existing_version PASSED
test_upgrade_service.py::TestUpgradeService::test_load_existing_config_handles_both_fields PASSED
```

Run all upgrade service tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v
```

## Notes

- This is a minimal, surgical fix that maintains simplicity
- No changes to the TACConfig Pydantic model or schema required
- The normalization happens before version update logic, ensuring clean separation of concerns
- Using `pop()` ensures the legacy field is completely removed from the config data
- The condition `"version" not in config_data` protects against overwriting modern configs
- All existing tests continue to pass, demonstrating zero regressions
- This approach avoids over-engineering and complex migration systems
