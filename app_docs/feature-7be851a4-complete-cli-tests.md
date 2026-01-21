# Complete CLI Tests

**ADW ID:** 7be851a4
**Date:** 2026-01-21
**Specification:** specs/issue-46-adw-7be851a4-sdlc_planner-complete-cli-tests.md

## Overview

Comprehensive CLI integration tests were implemented for TAC Bootstrap CLI, expanding the test suite from 2 trivial tests to 9 complete tests covering all major commands. The new tests validate version display, project initialization, agentic layer addition, health checking, and template rendering with various flags and options.

## What Was Built

- **test_version_command**: Validates version output format and content
- **test_init_dry_run**: Tests init command preview mode without file creation
- **test_init_with_options**: Tests init with explicit language, framework, and package manager flags
- **test_add_agentic_dry_run**: Tests add-agentic preview mode with auto-detection
- **test_doctor_healthy**: Tests doctor command on a valid agentic layer setup
- **test_doctor_with_fix**: Tests doctor's auto-fix functionality on incomplete setup
- **test_render_dry_run**: Tests render command preview mode with config file

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_cli.py`: Added 284 lines with 7 comprehensive CLI integration tests

### Key Changes

- **Import additions**: Added `json`, `Path`, `yaml`, and `__version__` imports to support test scenarios
- **Test infrastructure**: All tests use Typer's `CliRunner` for command invocation and pytest's `tmp_path` fixture for isolated test environments
- **Exit code validation**: Each test verifies exit code is 0 for success or 1 for expected failures
- **Output assertions**: Tests validate expected keywords in stdout (e.g., "Dry Run", "Preview", "healthy", "fix")
- **Filesystem isolation**: Dry-run tests verify no files/directories are created; other tests create realistic project structures in tmp_path
- **Realistic test data**: Tests create valid pyproject.toml, config.yml, settings.json, and directory structures to simulate real-world scenarios

## How to Use

### Running CLI Tests Only

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_cli.py -v
```

### Running Specific Test

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_cli.py::test_version_command -v
```

### Running Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v
```

### Running with Coverage

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_cli.py -v --cov=tac_bootstrap.interfaces.cli
```

## Configuration

No additional configuration required. Tests use:
- **CliRunner**: Typer's built-in test client for command invocation
- **tmp_path**: Pytest fixture for temporary directory creation
- **--no-interactive**: Flag to disable prompts during automated testing
- **--dry-run**: Flag to preview operations without modifying filesystem

## Testing

All tests validate:
1. **Exit code correctness**: 0 for success, 1 for handled errors
2. **Expected output text**: Commands display appropriate messages and indicators
3. **No unhandled exceptions**: Commands gracefully handle all scenarios
4. **Filesystem safety**: Dry-run modes never modify files

### Example Test Output

```bash
$ cd tac_bootstrap_cli && uv run pytest tests/test_cli.py -v

tests/test_cli.py::test_app_exists PASSED
tests/test_cli.py::test_help_command PASSED
tests/test_cli.py::test_version_command PASSED
tests/test_cli.py::test_init_dry_run PASSED
tests/test_cli.py::test_init_with_options PASSED
tests/test_cli.py::test_add_agentic_dry_run PASSED
tests/test_cli.py::test_doctor_healthy PASSED
tests/test_cli.py::test_doctor_with_fix PASSED
tests/test_cli.py::test_render_dry_run PASSED

===== 9 passed in 0.42s =====
```

## Notes

- **Integration focus**: Tests validate CLI layer integration, not re-testing service logic (services have separate test files: test_scaffold_service.py, test_doctor_service.py)
- **Dry-run critical**: Dry-run tests prevent destructive operations during testing and verify preview mode works correctly
- **Realistic structures**: Tests create valid pyproject.toml, config.yml with proper YAML/JSON formatting to match real-world usage
- **Fixture reuse**: Tests follow existing patterns from test_scaffold_service.py and test_doctor_service.py for consistency
- **No mocking**: Tests use real CLI command invocation with isolated tmp_path directories instead of mocking, providing true integration testing
- **Future expansion**: Additional edge case tests can be added for error scenarios (invalid paths, missing arguments, malformed configs)
