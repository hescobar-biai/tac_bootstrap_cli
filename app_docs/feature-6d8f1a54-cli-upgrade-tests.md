# CLI Upgrade Tests

**ADW ID:** 6d8f1a54
**Date:** 2026-01-22
**Specification:** specs/issue-88-adw-6d8f1a54-sdlc_planner-cli-upgrade-tests.md

## Overview

Comprehensive integration tests for the `tac-bootstrap upgrade` CLI command that validate argument handling, user messaging, confirmation prompts, and proper integration with the UpgradeService. These tests complement the unit tests in `test_upgrade_service.py` by focusing on the CLI interface layer rather than the business logic.

## What Was Built

- Integration test suite for CLI upgrade command with 9 test cases
- Edge case coverage for version mismatches (newer project version scenario)
- Mock-based tests that isolate CLI behavior from service implementation
- User interaction testing including confirmation prompts and cancellation flows
- Flag validation for `--dry-run`, `--force`, and `--no-backup` options

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_upgrade_cli.py`: Added comprehensive CLI integration tests with one new test for newer project version scenario

### Key Changes

- **Test coverage for all CLI flags**: Validates `--dry-run`, `--force`, `--no-backup` flags work correctly
- **User interaction testing**: Simulates user confirmation (`y/n` input) using CliRunner's input parameter
- **Edge case handling**: Tests missing config, version mismatches, upgrade failures, and downgrade prevention
- **Mock strategy**: All tests mock UpgradeService to isolate CLI behavior and avoid I/O operations
- **Exit code validation**: Ensures proper exit codes (0 for success, 1 for errors) across all scenarios

## How to Use

### Running CLI Upgrade Tests

Execute the CLI upgrade test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py -v --tb=short
```

### Running Specific Test

Run a single test case:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py::test_upgrade_newer_project_version -v
```

### Full Test Suite

Run all tests including upgrade service tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Configuration

No special configuration required. Tests use:
- **pytest fixtures**: `tmp_path` for temporary directories
- **CliRunner**: Typer's testing utility for CLI invocation
- **unittest.mock**: For mocking UpgradeService dependencies

## Testing

The test suite covers 9 scenarios:

1. **test_upgrade_command_no_config**: Missing config.yml error handling (tac_bootstrap_cli/tests/test_upgrade_cli.py:13)
2. **test_upgrade_command_already_up_to_date**: Project at current version (tac_bootstrap_cli/tests/test_upgrade_cli.py:21)
3. **test_upgrade_command_dry_run**: Preview changes without applying (tac_bootstrap_cli/tests/test_upgrade_cli.py:38)
4. **test_upgrade_command_user_cancels**: User declines confirmation prompt (tac_bootstrap_cli/tests/test_upgrade_cli.py:62)
5. **test_upgrade_command_success**: Successful upgrade with backup (tac_bootstrap_cli/tests/test_upgrade_cli.py:82)
6. **test_upgrade_command_no_backup**: Upgrade without backup using `--no-backup` (tac_bootstrap_cli/tests/test_upgrade_cli.py:104)
7. **test_upgrade_command_force**: Force upgrade with `--force` flag (tac_bootstrap_cli/tests/test_upgrade_cli.py:126)
8. **test_upgrade_command_failure**: Service upgrade failure handling (tac_bootstrap_cli/tests/test_upgrade_cli.py:147)
9. **test_upgrade_newer_project_version**: Downgrade prevention (newer project version) (tac_bootstrap_cli/tests/test_upgrade_cli.py:167)

Run the complete suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py -v --tb=short
```

## Notes

### Test Responsibilities

The CLI tests (TAREA 7) complement the service tests (TAREA 6) with different focus areas:

**CLI Tests (test_upgrade_cli.py)**:
- CLI argument parsing and validation
- User-facing messages and prompts
- Exit codes and error handling at CLI layer
- Integration with UpgradeService (mocked)
- User interaction flows (confirmation, cancellation)

**Service Tests (test_upgrade_service.py)**:
- Business logic for upgrade operations
- Real file I/O operations
- Backup creation and rollback
- Directory exclusions and filtering
- Config.yml version updates

### Mocking Strategy

All CLI tests mock UpgradeService to:
- Isolate CLI behavior from service implementation
- Avoid real filesystem I/O (tested separately in service tests)
- Enable simulation of various service responses (success, failure, version checks)
- Keep tests fast and deterministic

### Edge Case: Downgrade Not Supported

The new test `test_upgrade_newer_project_version` validates that when a project's version is newer than the CLI version (e.g., project at 0.9.0, CLI at 0.2.0), the upgrade command:
- Returns exit code 0 (not an error)
- Shows "already up to date" message
- Does NOT perform any upgrade operations
- Does NOT support downgrade functionality

This prevents accidental data loss or breaking changes from downgrading projects.
