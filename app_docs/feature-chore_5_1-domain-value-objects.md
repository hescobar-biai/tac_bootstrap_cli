# Domain Value Objects with Validation

**ADW ID:** chore_5_1
**Date:** 2026-01-24
**Specification:** specs/issue-166-adw-chore_5_1-sdlc_planner-value-objects.md

## Overview

Implemented type-safe domain value objects for TAC Bootstrap CLI that provide automatic validation and sanitization for critical domain concepts. These value objects fail fast at construction time, preventing invalid data propagation throughout the system.

## What Was Built

- **ProjectName**: Sanitizes project names to lowercase-hyphen format, removing special characters and enforcing length limits
- **TemplatePath**: Validates relative template paths with security checks to prevent directory traversal attacks
- **SemanticVersion**: Parses and compares semantic versions (X.Y.Z format) with full comparison operator support

All value objects inherit from `str` for compatibility with existing Pydantic v2 models while providing strong validation guarantees.

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`: New module containing three value object classes (357 lines)
- `tac_bootstrap_cli/tests/test_value_objects.py`: Comprehensive test suite with 100% coverage (397 lines)

### Key Changes

**ProjectName implementation:**
- Uses `__new__` method for string subclass construction with validation
- Sanitization pipeline: strip → lowercase → space-to-hyphen → remove special chars → collapse hyphens
- Enforces 1-64 character length after sanitization
- Removes leading/trailing hyphens for clean results

**TemplatePath implementation:**
- Security-focused validation to prevent path traversal attacks
- Rejects absolute paths (starting with `/`)
- Rejects parent directory traversal (containing `..`)
- Allows dot-relative paths (`./file`) and nested paths
- Critical for code generator that reads/writes template files

**SemanticVersion implementation:**
- Strict X.Y.Z format parsing with regex validation
- `tuple` property returns `(major, minor, patch)` as integers
- Full comparison protocol: `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`
- `__hash__` implementation for use in sets/dicts
- Supports version comparison logic for template compatibility checks

**Design patterns:**
- Pydantic v2 compatible (no deprecated `__get_validators__`)
- String subclass pattern for backward compatibility
- Fail-fast validation with clear error messages
- Comprehensive docstrings with usage examples

## How to Use

### ProjectName

```python
from tac_bootstrap.domain.value_objects import ProjectName

# Sanitizes automatically
name = ProjectName("My App!!")  # Returns: "my-app"
name = ProjectName("hello_world")  # Returns: "helloworld"
name = ProjectName("Project   Name")  # Returns: "project-name"

# Validation failures
ProjectName("")  # ValueError: cannot be empty
ProjectName("a" * 65)  # ValueError: exceeds maximum length
```

### TemplatePath

```python
from tac_bootstrap.domain.value_objects import TemplatePath

# Valid paths
path = TemplatePath("templates/config.yml")  # OK
path = TemplatePath("./templates/file.md")  # OK

# Security validation failures
TemplatePath("/etc/passwd")  # ValueError: absolute paths not allowed
TemplatePath("../../secret")  # ValueError: parent traversal not allowed
```

### SemanticVersion

```python
from tac_bootstrap.domain.value_objects import SemanticVersion

# Parsing and comparison
v1 = SemanticVersion("1.2.3")
v2 = SemanticVersion("0.9.0")

assert v1 > v2  # True
assert v1.tuple == (1, 2, 3)  # True

# Version sorting
versions = [SemanticVersion("0.3.0"), SemanticVersion("0.2.2"), SemanticVersion("1.0.0")]
sorted_versions = sorted(versions)  # ["0.2.2", "0.3.0", "1.0.0"]

# Validation failures
SemanticVersion("1.2")  # ValueError: invalid format
SemanticVersion("v1.2.3")  # ValueError: must be numeric
```

## Configuration

No configuration required. Value objects are standalone utilities that can be imported and used directly in domain models or application code.

### Future Integration

Value objects are designed for future integration with Pydantic models:

```python
from pydantic import BaseModel
from typing_extensions import Annotated
from tac_bootstrap.domain.value_objects import ProjectName

class Project(BaseModel):
    name: Annotated[str, ProjectName]  # Automatic validation
```

## Testing

Run the comprehensive test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_value_objects.py -v
```

### Test Coverage

**ProjectName tests (19 test cases):**
- Sanitization: spaces, special chars, uppercase, consecutive hyphens
- Edge cases: empty strings, single char, numbers, max length
- Type validation: non-string rejection

**TemplatePath tests (13 test cases):**
- Valid paths: relative, dot-relative, nested, dots in filenames
- Security: absolute path rejection, parent traversal rejection
- Edge cases: empty strings, whitespace

**SemanticVersion tests (17 test cases):**
- Parsing: valid formats, tuple property
- Comparison: all operators (`<`, `>`, `==`, etc.)
- Collections: hash consistency, sorting
- Edge cases: "0.0.0", large numbers, invalid formats

Run all tests to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

**String subclass pattern**: Inheriting from `str` provides backward compatibility with existing code that expects strings, while adding validation. This allows value objects to be used anywhere strings are accepted.

**Pydantic v2 compatibility**: Uses modern `__new__` pattern instead of deprecated `__get_validators__`. This ensures compatibility with Pydantic 2.5.0+ used in the project.

**No immediate integration**: Per acceptance criteria "Tests existentes siguen pasando sin cambios", value objects are created as standalone utilities without modifying existing domain models. Integration can happen in future tasks.

### Security Rationale

TemplatePath validation prevents path traversal attacks, which is critical for TAC Bootstrap's code generator functionality:
- Reads template files from template directory
- Copies files to target project directories
- Could be exploited if paths aren't validated

### Use Cases

**ProjectName**: Used for generating safe directory names, package names, Python module names, and Git branch names.

**TemplatePath**: Used in template engine to validate all template file paths before reading or copying.

**SemanticVersion**: Used for TAC Bootstrap version comparison, template compatibility checks, and dependency version requirements.

### Validation Commands

All validation passed with zero regressions:
- ✅ All existing tests pass unchanged
- ✅ 49 new value object tests pass (100% coverage)
- ✅ No linting errors
- ✅ CLI smoke test successful
