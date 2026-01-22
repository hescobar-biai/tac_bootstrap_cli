# UpgradeService Comprehensive Test Suite

**ADW ID:** 566c67fe
**Date:** 2026-01-21
**Specification:** specs/issue-87-adw-566c67fe-sdlc_planner-upgrade-service-tests.md

## Overview

Comprehensive unit test suite for the `UpgradeService` that validates all core functionality, edge cases, and critical behaviors of the upgrade system. The tests ensure safe and reliable upgrades of TAC Bootstrap projects while preserving user code and enabling rollback capabilities.

## What Was Built

- Complete test suite covering 17+ test scenarios
- Two test classes: `TestUpgradeService` (core functionality) and `TestUpgradeServiceEdgeCases` (edge cases)
- Mock-based testing to prevent real I/O operations
- Critical validation tests for config version updates and rollback mechanisms
- Comprehensive backup exclusion and user code preservation tests

### Test Coverage Areas

- **Version Detection**: Reading version from config.yml, handling missing files, pre-0.2.0 projects without version field
- **Version Comparison**: Detecting upgrade requirements based on semantic versioning
- **Backup Creation**: Creating backups of agentic layer while excluding user code
- **Preview Generation**: Listing changes for "Create" vs "Update" operations
- **Config Loading**: Loading and merging existing configuration
- **Successful Upgrade**: Preserving user code, updating config version, regenerating agentic layer
- **Edge Cases**: Corrupt config, missing directories, rollback on failure, backup failures, old file removal

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_upgrade_service.py`: Complete 491-line test suite with comprehensive coverage

### Key Changes

1. **Fixture Infrastructure**: Created `mock_project` fixture that sets up realistic project structure with:
   - config.yml (version 0.1.0)
   - Agentic layer directories (adws/, .claude/, scripts/)
   - User code directory (src/main.py)

2. **Core Functionality Tests (TestUpgradeService)**:
   - Version detection tests for all scenarios (present, missing, no field)
   - Backup creation with verification of exclusions
   - Preview generation for existing and missing directories
   - Config loading with version updates

3. **Critical Tests**:
   - `test_perform_upgrade_updates_config_version`: Validates config.yml gets updated to target version
   - `test_perform_upgrade_rollback_on_failure`: Verifies automatic rollback when scaffold fails
   - `test_perform_upgrade_aborts_on_backup_failure`: Ensures upgrade doesn't proceed if backup fails

4. **Edge Case Tests (TestUpgradeServiceEdgeCases)**:
   - Corrupt YAML handling
   - Missing directory detection
   - Old file removal verification
   - Multiple failure scenarios

5. **Mock Strategy**: Uses `unittest.mock.patch` to mock `ScaffoldService.scaffold_project` preventing real template rendering during tests

## How to Use

### Running the Test Suite

Execute the UpgradeService tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v --tb=short
```

### Running Specific Test Classes

Test only core functionality:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py::TestUpgradeService -v
```

Test only edge cases:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py::TestUpgradeServiceEdgeCases -v
```

### Running Individual Tests

Run a specific test by name:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py::TestUpgradeService::test_create_backup -v
```

### Running with Coverage Report

Get coverage metrics for UpgradeService:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py --cov=tac_bootstrap.application.upgrade_service --cov-report=term-missing
```

## Configuration

No additional configuration required. Tests use pytest's built-in `tmp_path` fixture for filesystem isolation.

### Test Dependencies

The test file imports:
- `pytest`: Test framework
- `unittest.mock`: Mocking utilities
- `yaml`: YAML parsing
- `tac_bootstrap.__version__`: CLI version constant
- `tac_bootstrap.application.upgrade_service.UpgradeService`: Service under test
- `tac_bootstrap.domain.models.TACConfig`: Configuration model

## Testing Strategy

### Mock-Based Unit Testing

Tests use `unittest.mock.patch` to mock `ScaffoldService.scaffold_project`, preventing:
- Real template rendering
- Actual filesystem modifications
- External dependencies during tests

This enables fast, isolated unit tests that validate logic without I/O overhead.

### Fixture-Based Setup

The `mock_project` fixture creates realistic project structure:
- Valid config.yml with all required fields
- Agentic layer directories with dummy content
- User code directory (src/) to verify preservation

### Critical Verification Points

1. **Config Version Update**: `test_perform_upgrade_updates_config_version` ensures config.yml reflects target version after upgrade
2. **Rollback on Failure**: `test_perform_upgrade_rollback_on_failure` mocks scaffold failure and verifies backup restoration
3. **Backup Exclusions**: `test_create_backup` confirms user code (src/) is NOT included in backup
4. **User Code Preservation**: `test_perform_upgrade_preserves_user_code` verifies src/main.py survives upgrade

### Edge Case Coverage

- **Pre-0.2.0 Projects**: Projects without version field default to "0.1.0"
- **Corrupt Config**: Invalid YAML handled gracefully (returns None)
- **Missing Directories**: Preview shows "Create" instead of "Update"
- **Backup Failure**: Upgrade aborts if backup creation fails
- **Scaffold Failure**: Automatic rollback from backup

## Test List

### TestUpgradeService (Core Functionality)

1. `test_get_current_version` - Read version from config.yml
2. `test_get_current_version_missing_file` - Handle missing config.yml
3. `test_get_current_version_no_version_field` - Default to "0.1.0" for old projects
4. `test_get_target_version` - Return CLI version
5. `test_needs_upgrade_true` - Detect upgrade requirement
6. `test_needs_upgrade_false_same_version` - Detect up-to-date projects
7. `test_create_backup` - Create backup with correct exclusions
8. `test_get_changes_preview` - List upgrade changes
9. `test_get_changes_preview_missing_directories` - Show "Create" for missing dirs
10. `test_load_existing_config` - Load and update config
11. `test_perform_upgrade_preserves_user_code` - Preserve src/ during upgrade
12. `test_perform_upgrade_with_backup` - Create backup during upgrade
13. `test_perform_upgrade_updates_config_version` - Update version in config.yml

### TestUpgradeServiceEdgeCases

1. `test_upgrade_invalid_config` - Handle corrupt YAML
2. `test_upgrade_missing_directories` - Detect missing agentic layer
3. `test_perform_upgrade_rollback_on_failure` - Rollback when scaffold fails
4. `test_perform_upgrade_aborts_on_backup_failure` - Abort when backup fails
5. `test_perform_upgrade_removes_old_files` - Remove old agentic layer files

## Notes

### Development Context

This test suite was created as **TAREA 6** in the TAC Bootstrap CLI upgrade system implementation plan. It provides critical validation for the `UpgradeService` (TAREA 3) before integration with the CLI command (TAREA 4).

### Test Execution Results

All 17+ tests pass successfully, providing confidence that:
- Version detection works correctly for all project types
- Backups are created safely without including user code
- Upgrades preserve user code while updating agentic layer
- Config.yml version field is updated correctly
- Rollback mechanisms work when failures occur
- Edge cases are handled gracefully

### Relationship to Other Components

- **UpgradeService** (`tac_bootstrap/application/upgrade_service.py`): Service under test
- **Upgrade CLI** (`tac_bootstrap/interfaces/cli_upgrade.py`): Uses UpgradeService (tested separately in `test_upgrade_cli.py`)
- **ScaffoldService**: Mocked in these tests to prevent real template rendering

### Coverage Notes

The test suite achieves comprehensive coverage of:
- All public methods of UpgradeService
- Critical user code preservation logic
- Backup creation and restoration
- Config version update mechanism
- Error handling and rollback

### Future Enhancements

Out of scope for MVP but documented in spec:
- Concurrent upgrade handling
- Disk space validation before upgrade
- Backup permission preservation (handled automatically by shutil.copytree)
- Backup name collision handling (timestamp precision sufficient)
