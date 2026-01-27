---
doc_type: feature
adw_id: feature_Tac_10_task_6
date: 2026-01-26
idk:
  - scaffold-service
  - directory-operation
  - agents
  - hook-logs
  - context-bundles
  - gitkeep
tags:
  - feature
  - scaffolding
  - agents
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/domain/plan.py
---

# Agents Directories Scaffolding Support

**ADW ID:** feature_Tac_10_task_6
**Date:** 2026-01-26
**Specification:** specs/issue-311-adw-feature_Tac_10_task_6-sdlc_planner-agents-directories.md

## Overview

Added automatic creation of agent-related subdirectories during project scaffolding. The scaffold service now creates `agents/hook_logs/` and `agents/context_bundles/` directories with `.gitkeep` files to support agent execution logging and context persistence.

## What Was Built

- Added `agents/hook_logs/` directory for storing hook execution logs
- Added `agents/context_bundles/` directory for agent context bundle persistence
- Added `.gitkeep` files in both subdirectories to ensure Git tracking of empty directories
- Updated scaffold service to include these directories in all generated projects

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added two directory operations and two file operations in the `_add_directories()` method

### Key Changes

- Added directory entries in the `directories` list at lines 120-121:
  - `("agents/hook_logs", "Hook execution logs")`
  - `("agents/context_bundles", "Agent context bundles")`
- Added `.gitkeep` file operations after directory creation (lines 130-142):
  - `agents/hook_logs/.gitkeep` with empty content
  - `agents/context_bundles/.gitkeep` with empty content
- Used `FileAction.CREATE` to avoid overwriting existing files
- Maintained consistency with existing scaffolding patterns

## How to Use

This feature is automatic. When generating a new project with TAC Bootstrap, the agent directories are created automatically:

1. Run the scaffold command (or any command that creates a new project):
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap scaffold --config-file path/to/config.yaml
```

2. The generated project will include the following structure:
```
project_root/
└── agents/
    ├── hook_logs/
    │   └── .gitkeep
    └── context_bundles/
        └── .gitkeep
```

3. Hooks and agents can now write to these directories without runtime errors:
   - Hooks write logs to `agents/hook_logs/`
   - Agents persist context bundles to `agents/context_bundles/`

## Configuration

No additional configuration is required. The directories are created for all projects by default as part of the standard scaffolding process.

## Testing

Run unit tests to validate the scaffolding service:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v
```

Run full test suite to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This feature is part of TAC-10, which adds comprehensive agent support to generated projects
- The directories follow a hierarchical structure: `agents/` (parent) → `hook_logs/` and `context_bundles/` (children)
- `.gitkeep` files are standard Git convention to preserve empty directories in version control
- `DirectoryOperation` is idempotent and will not fail if directories already exist
- `FileAction.CREATE` ensures `.gitkeep` files are only created if they don't exist
- The feature increments the scaffold plan counters by 2 directories and 2 files
