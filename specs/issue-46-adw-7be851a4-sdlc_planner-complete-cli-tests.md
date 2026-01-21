# Feature: Complete CLI Tests

## Metadata
issue_number: `46`
adw_id: `7be851a4`
issue_json: `{"number":46,"title":"TAREA 5: Completar Tests de CLI","body":"**Archivo a modificar:** `tests/test_cli.py`\n\n**Prompt:**\n```\nExpande los tests en tests/test_cli.py para cubrir todos los comandos del CLI.\n\nActualmente solo hay 2 tests triviales. Necesitamos tests para:\n\n1. **test_version_command**: Verificar que muestra versión correcta\n2. **test_init_dry_run**: Probar init con --dry-run\n3. **test_init_with_options**: Probar init con --language, --framework\n4. **test_add_agentic_dry_run**: Probar add-agentic con --dry-run\n5. **test_doctor_healthy**: Probar doctor en directorio válido\n6. **test_doctor_with_fix**: Probar doctor --fix\n7. **test_render_dry_run**: Probar render con --dry-run\n\nUsa CliRunner de Typer para invocar comandos.\nUsa tmp_path fixture de pytest para crear directorios temporales.\n\nReferencia los tests existentes en:\n- tests/test_scaffold_service.py\n- tests/test_doctor_service.py\n\nCada test debe verificar:\n- Exit code correcto\n- Output contiene texto esperado\n- No hay excepciones no manejadas\n```\n\n**Criterios de aceptación:**\n- [ ] Al menos 7 tests nuevos\n- [ ] Cobertura de todos los comandos principales\n- [ ] Tests pasan con `uv run pytest tests/test_cli.py -v`\n\n---"}`

## Feature Description
Expand the CLI test suite in `tests/test_cli.py` to comprehensively test all commands of the TAC Bootstrap CLI. Currently, the test file contains only 2 trivial tests that check if the app exists and if help works. This feature adds 7+ comprehensive tests covering all major commands: version, init, add-agentic, doctor, and render with various options and flags.

## User Story
As a TAC Bootstrap CLI developer
I want comprehensive automated tests for all CLI commands
So that I can ensure all commands work correctly, prevent regressions, and validate command options and flags

## Problem Statement
The current test suite for the CLI interface is minimal with only 2 basic tests. This leaves all major CLI functionality untested, including:
- version command output
- init command with --dry-run and various options
- add-agentic command with --dry-run
- doctor command with and without --fix
- render command with --dry-run

Without proper CLI tests, there's risk of breaking command behavior, incorrect exit codes, missing output, or unhandled exceptions. The existing service tests (test_scaffold_service.py, test_doctor_service.py) test the underlying services but don't validate the CLI layer integration.

## Solution Statement
Create comprehensive CLI integration tests using Typer's CliRunner to invoke commands programmatically and validate their behavior. Each test will:
1. Use CliRunner to invoke the command with specific arguments
2. Create temporary directories using pytest's tmp_path fixture
3. Verify exit codes (0 for success, 1 for errors)
4. Assert expected text appears in stdout
5. Ensure no unhandled exceptions occur

The tests will follow patterns from existing service tests and validate the full CLI integration including argument parsing, service invocation, and output formatting.

## Relevant Files
Files needed to implement this feature:

- `tac_bootstrap_cli/tests/test_cli.py` - Main file to expand with new tests. Currently has 2 basic tests.
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI implementation with all commands (version, init, add-agentic, doctor, render). Needed to understand command structure and expected output.
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Reference for testing patterns, especially tmp_path usage and fixture structure.
- `tac_bootstrap_cli/tests/test_doctor_service.py` - Reference for testing doctor service functionality.
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contains __version__ constant needed for version test validation.

### New Files
None - all tests will be added to existing `tests/test_cli.py`

## Implementation Plan

### Phase 1: Setup and Infrastructure
- Review existing test patterns in test_scaffold_service.py and test_doctor_service.py
- Understand CliRunner usage patterns from Typer documentation
- Import necessary fixtures and utilities
- Add necessary imports for version checking and mocking if needed

### Phase 2: Core Command Tests
- Implement test_version_command to validate version output
- Implement test_init_dry_run to test init command preview mode
- Implement test_init_with_options to test init with explicit language, framework, package manager
- Implement test_add_agentic_dry_run to test add-agentic preview mode
- Implement test_doctor_healthy to test doctor on a valid setup
- Implement test_doctor_with_fix to test doctor's auto-fix functionality
- Implement test_render_dry_run to test render command preview mode

### Phase 3: Validation and Polish
- Run all tests and ensure they pass
- Verify exit codes are correct for all scenarios
- Ensure output assertions are specific and meaningful
- Add docstrings to all new tests explaining what they validate
- Run full test suite to ensure no regressions

## Step by Step Tasks

### Task 1: Read and understand existing code
- Read `tests/test_cli.py` to understand current test structure
- Read `tac_bootstrap/interfaces/cli.py` to understand all commands, their arguments, and expected outputs
- Read test patterns from `tests/test_scaffold_service.py` and `tests/test_doctor_service.py`
- Identify the __version__ constant location for version test

### Task 2: Implement test_version_command
- Create test that invokes `tac-bootstrap version` using CliRunner
- Assert exit code is 0
- Assert output contains version number from __version__
- Assert output contains "TAC Bootstrap" text

### Task 3: Implement test_init_dry_run
- Create test using tmp_path fixture
- Invoke `tac-bootstrap init test-project --dry-run` with no-interactive mode
- Assert exit code is 0
- Assert output contains "Dry Run" or "Preview"
- Assert output lists directories and files that would be created
- Assert no actual files/directories were created (verify tmp_path is empty)

### Task 4: Implement test_init_with_options
- Create test using tmp_path fixture
- Invoke init with explicit options: `--language python --framework fastapi --package-manager uv --no-interactive --dry-run`
- Assert exit code is 0
- Assert output contains language, framework, and package manager values
- Validate that options are properly parsed and displayed

### Task 5: Implement test_add_agentic_dry_run
- Create test using tmp_path fixture
- Create minimal project structure in tmp_path (e.g., a package.json or pyproject.toml for detection)
- Invoke `tac-bootstrap add-agentic {tmp_path} --dry-run --no-interactive`
- Assert exit code is 0
- Assert output contains "Dry Run" or "Preview"
- Assert output shows detection results
- Assert no files were modified

### Task 6: Implement test_doctor_healthy
- Create test using tmp_path fixture
- Create valid agentic layer structure (.claude/, config.yml, etc.)
- Invoke `tac-bootstrap doctor {tmp_path}`
- Assert exit code is 0
- Assert output contains "healthy" or "All checks passed"

### Task 7: Implement test_doctor_with_fix
- Create test using tmp_path fixture
- Create incomplete structure (missing directories)
- Invoke `tac-bootstrap doctor {tmp_path} --fix`
- Assert exit code is 1 (unhealthy but fixable) or appropriate code
- Assert output indicates fixes were applied
- Optionally verify directories were created

### Task 8: Implement test_render_dry_run
- Create test using tmp_path fixture
- Create a valid config.yml file in tmp_path
- Invoke `tac-bootstrap render {tmp_path}/config.yml --dry-run`
- Assert exit code is 0
- Assert output contains "Dry Run" or "Preview"
- Assert output shows what would be created/modified

### Task 9: Run validation commands
- Execute `cd tac_bootstrap_cli && uv run pytest tests/test_cli.py -v` to ensure all new tests pass
- Execute `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` to ensure no regressions
- Execute `cd tac_bootstrap_cli && uv run ruff check .` for linting
- Execute `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` for type checking

## Testing Strategy

### Unit Tests
Each test validates a specific CLI command:
- **test_version_command**: Validates version output format and content
- **test_init_dry_run**: Validates init dry-run mode doesn't create files
- **test_init_with_options**: Validates init accepts and processes CLI options
- **test_add_agentic_dry_run**: Validates add-agentic dry-run mode
- **test_doctor_healthy**: Validates doctor reports healthy on valid setup
- **test_doctor_with_fix**: Validates doctor --fix attempts repairs
- **test_render_dry_run**: Validates render dry-run mode

### Edge Cases
- Commands with invalid paths (should handle gracefully)
- Commands with missing required arguments (Typer handles this)
- Dry-run modes should never modify filesystem
- Exit codes: 0 for success, 1 for expected failures
- Output should contain expected keywords for user feedback

## Acceptance Criteria
- [x] At least 7 new comprehensive tests added to test_cli.py
- [x] All major CLI commands are tested: version, init, add-agentic, doctor, render
- [x] Each test verifies exit code, expected output text, and no exceptions
- [x] Tests use CliRunner from Typer for command invocation
- [x] Tests use tmp_path fixture for isolated temporary directories
- [x] All tests pass: `uv run pytest tests/test_cli.py -v`
- [x] No regressions in full test suite: `uv run pytest tests/ -v`
- [x] Code passes linting: `uv run ruff check .`
- [x] Code passes type checking: `uv run mypy tac_bootstrap/`

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/test_cli.py -v` - Run new CLI tests
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Full test suite
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The CLI commands may import services that are already tested separately (ScaffoldService, DoctorService, DetectService). CLI tests focus on integration, not re-testing service logic.
- Some commands may have ImportError handlers for services not yet implemented. Tests should handle these gracefully or skip them.
- Dry-run modes are critical to test as they prevent destructive operations during testing.
- Consider mocking or skipping tests for services that aren't fully implemented yet.
- The --no-interactive flag is crucial for automated testing to avoid interactive prompts.
