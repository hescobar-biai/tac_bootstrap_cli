# Wizard Tests Suite

**ADW ID:** f3a4daef
**Date:** 2026-01-21
**Specification:** specs/issue-47-adw-f3a4daef-sdlc_planner-create-wizard-tests.md

## Overview

Created a comprehensive test suite for the wizard module (`tac_bootstrap/interfaces/wizard.py`) that enables automated testing of interactive CLI prompts without requiring manual user input. The tests use mocked Rich components to simulate user interaction and verify wizard behavior across multiple scenarios.

## What Was Built

- Complete test file with 13+ test cases covering all wizard functions
- Mock fixtures for Rich components (Console, Prompt, Confirm)
- Test classes organized by wizard type:
  - `TestSelectFromEnum` - Enum selection with filtering and edge cases
  - `TestRunInitWizard` - New project initialization wizard
  - `TestRunAddAgenticWizard` - Add agentic layer to existing repos
  - `TestWizardEdgeCases` - Edge cases and error conditions
- Sample fixture for detected project attributes

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_wizard.py`: New test file (411 lines) with comprehensive wizard test coverage

### Key Changes

- **Mock Fixtures** (lines 30-65): Created reusable pytest fixtures that patch Rich components at the module level to prevent terminal output and simulate user input
- **Enum Selection Tests** (lines 73-152): Verified `select_from_enum()` function handles defaults, filtering, and edge cases like empty option lists
- **Init Wizard Tests** (lines 160-260): Tested new project wizard with defaults, custom values, preset languages, and cancellation scenarios
- **Add Agentic Tests** (lines 268-352): Tested existing repo wizard using detected project values and override scenarios
- **Edge Case Tests** (lines 360-411): Validated empty command strings, preset value shortcuts, and prompt count optimization

### Test Coverage

The test suite validates:
1. **User input simulation**: Mocking Prompt.ask() and Confirm.ask() with side_effect sequences
2. **Default value handling**: Ensuring defaults are used when user presses Enter
3. **Filtering logic**: Testing enum filtering by language/framework compatibility
4. **Cancellation flow**: Verifying SystemExit(0) when user cancels at confirmation
5. **Detected values**: Testing that add-agentic wizard pre-fills detected project attributes
6. **Error conditions**: ValueError when no valid enum options remain after filtering

## How to Use

### Running the Tests

Execute the wizard test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py -v --tb=short
```

Run specific test class:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py::TestSelectFromEnum -v
```

Run specific test case:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py::TestRunInitWizard::test_wizard_with_all_defaults -v
```

### Running Full Test Suite

Verify no regressions in existing tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Configuration

No configuration needed. Tests use:
- `unittest.mock.patch` for mocking Rich components
- `pytest.fixture` for reusable test dependencies
- `pytest.raises` for exception testing

## Testing

All validation commands pass:

```bash
# Wizard tests specifically
cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py -v --tb=short

# Full unit test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Mocking Strategy

The tests follow the mocking pattern used in `test_scaffold_service.py`:

```python
@pytest.fixture
def mock_prompt():
    """Mock Prompt.ask to simulate user input."""
    with patch("tac_bootstrap.interfaces.wizard.Prompt.ask") as mock:
        yield mock
```

**Key points:**
- Patch at module level: `tac_bootstrap.interfaces.wizard.Prompt.ask`
- Use `side_effect` for multiple sequential prompts
- Use `return_value` for single prompt mocking
- Verify console.print was called to confirm output shown to users

### Test Organization

Tests are organized into logical classes matching the wizard functions:
- `TestSelectFromEnum`: 5 tests for enum selection logic
- `TestRunInitWizard`: 4 tests for new project initialization
- `TestRunAddAgenticWizard`: 3 tests for existing repo workflow
- `TestWizardEdgeCases`: 2 tests for edge cases and optimizations

### Coverage Summary

**13 test cases** covering:
- ✅ Enum selection with defaults
- ✅ Enum filtering by compatibility
- ✅ Empty option error handling
- ✅ Init wizard with all defaults
- ✅ Init wizard with custom values
- ✅ Preset language skips prompts
- ✅ Cancellation raises SystemExit(0)
- ✅ Add agentic uses detected values
- ✅ Add agentic allows overrides
- ✅ Empty command strings accepted
- ✅ Preset values optimize prompt count

### Related Files

- **tac_bootstrap/interfaces/wizard.py**: Module being tested
- **tac_bootstrap/domain/models.py**: Enum definitions (Language, Framework, PackageManager, etc.)
- **tests/test_scaffold_service.py**: Reference for mocking patterns
- **tests/test_plan.py**: Reference for test class organization
