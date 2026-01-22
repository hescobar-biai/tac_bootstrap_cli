# Centralized Version Constant

**ADW ID:** 7a8b363e
**Date:** 2026-01-21
**Specification:** specs/issue-81-adw-7a8b363e-chore_planner-centralized-version-constant.md

## Overview

This feature centralizes the version string for TAC Bootstrap CLI into a single source of truth (`__version__` in `__init__.py`), eliminating version duplication across the codebase. The version was also updated from 0.1.0 to 0.2.0 and a new `--version` CLI flag was added.

## What Was Built

- Centralized version constant in `tac_bootstrap/__init__.py`
- Version import in domain models to use centralized constant
- New `--version` / `-v` CLI flag with callback handler
- Updated version string from 0.1.0 to 0.2.0
- Updated tests to reflect new version
- Explicit `__all__` export for version constant

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/__init__.py`: Updated version to 0.2.0 and added `__all__` export
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Added import of `__version__` and changed `TACConfig.version` field to use it as default
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Added `version_callback()` function and `--version` option to main callback
- `tac_bootstrap_cli/tests/test_version.py`: Updated test to expect version 0.2.0

### Key Changes

- **Single source of truth**: `__version__ = "0.2.0"` is defined only in `__init__.py` and imported everywhere else
- **TACConfig default**: The `TACConfig.version` field now uses `default=__version__` instead of hardcoded string
- **Dual version commands**:
  - `tac-bootstrap --version` shows simple output: `TAC Bootstrap v0.2.0`
  - `tac-bootstrap version` shows rich panel with additional information
- **No circular imports**: Safe architecture - `__init__.py` only defines constants, domain models import from it
- **Explicit exports**: Added `__all__ = ["__version__"]` for clarity

## How to Use

### Check CLI Version

Use the standard `--version` flag (also accepts `-v` shorthand):

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --version
# Output: TAC Bootstrap v0.2.0
```

### View Detailed Version Information

Use the `version` command for a richer display:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap version
```

### Import Version in Code

```python
from tac_bootstrap import __version__

print(f"Running TAC Bootstrap {__version__}")
```

## Configuration

The `TACConfig` model automatically uses the centralized version as its default:

```python
from tac_bootstrap.domain.models import TACConfig

config = TACConfig()
assert config.version == "0.2.0"  # Uses __version__ from __init__.py
```

The version field remains overridable, which allows the upgrade system to preserve the original generator version when reading existing config files.

## Testing

Run the version-related tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_version.py -v
```

Run full test suite to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --version
cd tac_bootstrap_cli && uv run tac-bootstrap version
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- The version is intentionally kept as a simple string without strict semver validation
- The `--version` flag uses `is_eager=True` to ensure it executes before other command processing
- No risk of circular imports: `__init__.py` only defines the constant and doesn't import from other modules
- The version field in `TACConfig` remains mutable to support upgrade scenarios where existing configs may have different versions
- This pattern follows standard Python packaging conventions where `__version__` is the canonical version source
