---
doc_type: bug_fix
adw_id: bug_v_3_0_1_task_1
date: 2026-01-25
idk:
  - config-schema
  - pydantic-validation
  - yaml-structure
  - template-jinja2
  - domain-model
tags:
  - bug
  - configuration
  - schema
related_code:
  - config.yml
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
  - tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2
  - tac_bootstrap_cli/tests/test_upgrade_cli.py
  - tac_bootstrap_cli/tests/test_value_objects.py
---

# Fix config.yml Schema Structure Alignment

**ADW ID:** bug_v_3_0_1_task_1
**Date:** 2026-01-25
**Specification:** specs/issue-204-adw-bug_v_3_0_1_task_1-sdlc_planner-fix-config-schema-structure.md

## Overview

This bug fix corrects the structure of `config.yml` to align with the Pydantic model `TACConfig` defined in the domain layer. The configuration file had keys located at incorrect nesting levels, causing validation errors when loading the configuration.

## What Was Fixed

- **Moved safety paths**: `allowed_paths` and `forbidden_paths` relocated from root level to `agentic.safety` section
- **Restructured workflows**: Moved `workflows` configuration into `agentic.workflows` with only `default` and `available` keys
- **Added Claude section**: Created new top-level `claude` section containing `settings` and `commands` that were previously nested incorrectly
- **Updated version format**: Changed version from integer `1` to semantic version string `"0.3.0"` and added `schema_version: 1`
- **Updated template**: Fixed `config.yml.j2` Jinja2 template to generate correct structure for new projects

## Technical Implementation

### Files Modified

- `config.yml`: Reorganized YAML structure to match TACConfig schema
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Updated version examples in docstrings from v0.3.0 to v0.2.0
- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`: Updated template comment to reflect correct version
- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`: Version reference update
- `tac_bootstrap_cli/tests/test_upgrade_cli.py`: Updated test fixtures to use correct schema structure
- `tac_bootstrap_cli/tests/test_value_objects.py`: Updated version strings in tests

### Key Changes

1. **Safety Configuration**: `allowed_paths` and `forbidden_paths` moved from root level (lines 50-58 in old config) to nested under `agentic.safety`

2. **Workflows Configuration**: Simplified `workflows` section and moved it from root to `agentic.workflows`, removing incorrect `settings` and `commands` subkeys

3. **Claude Configuration**: Created new top-level `claude` section with:
   - `settings`: Contains `project_name`, `preferred_style`, `allow_shell`
   - `commands`: Contains paths to slash command files

4. **Version Schema**: Added explicit `version: "0.3.0"` and `schema_version: 1` fields at root level

## Schema Structure

The corrected structure follows this hierarchy:

```yaml
version: "0.3.0"
schema_version: 1
project: {...}
paths: {...}
commands: {...}
agentic:
  safety:
    allowed_paths: [...]
    forbidden_paths: [...]
  workflows:
    default: "sdlc_iso"
    available: [...]
claude:
  settings: {...}
  commands: {...}
```

## How to Verify

The fix ensures that the configuration validates correctly against the Pydantic models without raising validation errors.

### Verification Steps

1. Verify the config structure matches the schema
2. Ensure all nested sections are properly aligned
3. Confirm no root-level keys violate the schema
4. Test that config loads successfully in Python

## Testing

Validate that config.yml loads without errors:

```bash
cd tac_bootstrap_cli && uv run python -c "
import yaml
from tac_bootstrap.domain.models import TACConfig
with open('../config.yml') as f:
    data = yaml.safe_load(f)
config = TACConfig(**data)
print('Validation successful:', config.project.name)"
```

Run the full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify linting and type checking:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This fix is a surgical restructuring of the YAML configuration without changing functionality
- All existing values were preserved, only the nesting structure was corrected
- The Jinja2 template was updated to prevent this issue in newly generated projects
- No new dependencies were added
- Version bumped from `1` (integer) to `"0.3.0"` (string) to match semantic versioning conventions
