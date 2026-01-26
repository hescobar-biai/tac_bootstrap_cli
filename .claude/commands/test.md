# Application Validation Test Suite

Run comprehensive tests for tac-bootstrap, returning results in JSON format.

## Purpose

Validate the application before making changes:
- Detect syntax and type errors
- Identify broken tests
- Verify build works
- Ensure code quality

## Variables

TEST_COMMAND_TIMEOUT: 5 minutes

## Instructions

- Execute each test in sequence
- Capture result (passed/failed) and error messages
- IMPORTANT: Return ONLY the JSON array with results
- If a test passes, omit the error field
- If a test fails, include error message
- Execute all tests even if some fail
- Command timeout: `TEST_COMMAND_TIMEOUT`

## Test Execution Sequence

**If tac_bootstrap_cli/ exists:**

1. **Python Syntax Check**
   - Command: `cd tac_bootstrap_cli && uv run python -m py_compile **/*.py`
   - test_name: "python_syntax_check"
   - test_purpose: "Validate Python syntax by compiling source files"

2. **Code Quality Check**
   - Command: `uv run ruff check .`
   - test_name: "backend_linting"
   - test_purpose: "Validate Python code quality"

3. **Type Check**
   - Command: `uv run mypy tac_bootstrap_cli`
   - test_name: "type_check"
   - test_purpose: "Validate types with mypy"

4. **Unit Tests**
   - Command: `uv run pytest`
   - test_name: "unit_tests"
   - test_purpose: "Execute all unit tests"

5. **Application Smoke Test**
   - Command: `uv run tac-bootstrap --help --help`
   - test_name: "app_smoke_test"
   - test_purpose: "Verify application starts correctly"


**If tac_bootstrap_cli/ does NOT exist:**

1. **Structure Check**
   - Command: `ls tac_bootstrap_cli/`
   - test_name: "structure_check"
   - test_purpose: "Verify application structure exists"
   - Note: This test will fail indicating the application does not exist yet

## Report

- IMPORTANT: Return results as JSON array
- Order with failed tests first
- Include all tests in output

### Output Structure

```json
[
  {
    "test_name": "string",
    "passed": boolean,
    "execution_command": "string",
    "test_purpose": "string",
    "error": "optional string"
  }
]
```

### Example Output

```json
[
  {
    "test_name": "unit_tests",
    "passed": false,
    "execution_command": "uv run pytest",
    "test_purpose": "Execute all unit tests",
    "error": "AssertionError: Expected X but got Y"
  },
  {
    "test_name": "python_syntax_check",
    "passed": true,
    "execution_command": "cd tac_bootstrap_cli && python -m py_compile **/*.py",
    "test_purpose": "Validate Python syntax by compiling source files"
  }
]
```
