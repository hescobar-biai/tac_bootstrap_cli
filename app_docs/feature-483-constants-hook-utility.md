---
doc_type: feature
adw_id: issue-483
date: 2026-01-31
idk:
  - constants-module
  - hook-utilities
  - jinja2-template
  - scaffold-service
  - shared-configuration
  - logging-utilities
  - safety-configuration
tags:
  - feature
  - hook-utilities
  - infrastructure
related_code:
  - .claude/hooks/utils/constants.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Create constants.py Hook Utility

**ADW ID:** issue-483
**Date:** 2026-01-31
**Specification:** specs/issue-483-adw-feature_Tac_12_task_31-sdlc_planner-create-constants-hook-utility.md

## Overview

Created a shared constants utility module for Claude Code hooks in TAC Bootstrap. This provides centralized definitions for file system paths, project metadata, and safety configuration used across multiple hook utilities, with both a reference implementation and a Jinja2 template for CLI-generated projects.

## What Was Built

- **Base constants.py** - Reference implementation with logging utilities and environment configuration
- **Jinja2 Template** - Dynamic template that substitutes project-specific configuration values
- **Scaffold Integration** - Updated scaffold_service.py to include constants.py in hook utilities scaffolding

## Technical Implementation

### Files Modified/Created

- `.claude/hooks/utils/constants.py` - Base constants module with session logging utilities
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Jinja2 template for dynamic constants generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Updated to register constants.py in hook utilities list

### Key Changes

- **Base Implementation**: Provides `LOG_BASE_DIR` constant with environment override support and helper functions `get_session_log_dir()` and `ensure_session_log_dir()` for managing session-specific logging directories
- **Template Implementation**: Substitutes project metadata (`project.name`, `project.language`, `package_manager`), directory paths from configuration, and safety constraints (`forbidden_paths`, `allowed_paths`)
- **Scaffold Registration**: Integrated at scaffold action with template type and documented reason for inclusion in generated projects
- **Consistent Pattern**: Uses `config` object pattern for template variables, matching other hook utility templates

## How to Use

### In TAC Bootstrap Base Repository

Access the base constants in hook utilities:

```python
from .constants import LOG_BASE_DIR, get_session_log_dir, ensure_session_log_dir

# Get session log directory
session_logs = get_session_log_dir("session-123")

# Ensure session log directory exists
log_path = ensure_session_log_dir("session-456")
```

### In Generated Projects

When TAC Bootstrap CLI generates a new agentic layer project, it automatically scaffolds `constants.py` with project-specific values:

```python
# In generated .claude/hooks/utils/constants.py
PROJECT_NAME = "my-project"
LANGUAGE = "python"
LOG_DIR = "logs"
SPECS_DIR = "specs"
ADWS_DIR = "adws"

# Safety constraints specific to the project
FORBIDDEN_PATHS = [".env", "secrets/"]
ALLOWED_PATHS = ["src/", "tests/"]
```

## Configuration

The Jinja2 template substitutes values from the project configuration object:

- `config.project.name` - Project name
- `config.project.language` - Programming language
- `config.project.package_manager` - Package manager used
- `config.paths.logs_dir` - Logging directory
- `config.paths.specs_dir` - Specifications directory
- `config.paths.adws_dir` - AI Developer Workflows directory
- `config.paths.scripts_dir` - Scripts directory
- `config.paths.prompts_dir` - Prompts directory
- `config.paths.worktrees_dir` - Worktrees directory
- `config.agentic.safety.forbidden_paths` - Paths agents cannot modify
- `config.agentic.safety.allowed_paths` - Paths agents can modify

## Testing

Verify the base constants module imports correctly:

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
python3 -c "from .claude.hooks.utils.constants import LOG_BASE_DIR, get_session_log_dir; print('Constants imported successfully')"
```

Verify the template renders without syntax errors:

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v -k constants
```

Run full test suite to ensure no regressions:

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

Verify scaffold integration:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

## Notes

- Constants remain environment-agnostic; environment-specific values should use `os.environ.get()` with defaults
- The template uses Jinja2 conditional syntax (`{%- for %}`) to handle list iteration for safety paths
- Session logging utilities follow the pattern of organizing logs by session ID for better debugging and isolation
- Constants are scaffolded early in the hook utilities generation pipeline to ensure availability for other utilities
- Naming conventions follow Python standards: UPPER_CASE for module-level constants, snake_case for functions
