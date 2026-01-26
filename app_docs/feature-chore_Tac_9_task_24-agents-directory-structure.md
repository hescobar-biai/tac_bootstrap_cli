---
doc_type: feature
adw_id: chore_Tac_9_task_24
date: 2026-01-26
idk:
  - templates
  - directory-structure
  - agent-definitions
  - git-tracking
  - project-generation
tags:
  - feature
  - chore
  - infrastructure
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/.gitkeep
  - .gitignore
---

# Agents Directory Structure in Templates

**ADW ID:** chore_Tac_9_task_24
**Date:** 2026-01-26
**Specification:** specs/issue-265-adw-chore_Tac_9_task_24-sdlc_planner-create-agents-directory.md

## Overview

Created the `agents/` directory within the Claude templates structure to serve as a container for agent definition files used during project generation. This foundational infrastructure establishes the directory structure for future agent-related features.

## What Was Built

- Created `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` directory
- Added `.gitkeep` file to ensure git tracks the empty directory
- Updated `.gitignore` to exclude agent output directories while preserving the template structure

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/.gitkeep`: Empty file added to ensure git tracks the directory structure
- `.gitignore`: Updated agent exclusion patterns to preserve the template directory while excluding agent output directories

### Key Changes

- Established `agents/` directory parallel to existing `commands/`, `hooks/`, and `output-styles/` template directories
- Used `.gitkeep` pattern to track empty directory structure in git
- Modified `.gitignore` with negative patterns (`!tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/`) to ensure template directory is tracked while agent outputs remain ignored
- Created format-agnostic directory that allows future tasks to define agent file formats (e.g., .py, .yaml, .json)

## How to Use

The `agents/` directory is now part of the template structure that will be copied during project generation:

1. Agent definition files can be added to `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` as templates
2. During project generation, the CLI will copy this directory structure to the target project
3. The directory remains empty until future tasks define specific agent file formats and content

## Configuration

No configuration changes required. The directory structure is automatically included in the template system.

## Testing

Verify the directory structure exists:

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/
```

Run unit tests to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting checks:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is a foundational chore that establishes directory structure without prescribing specific file formats or agent definitions
- The directory follows the existing pattern in the templates structure where other feature directories exist
- The `.gitkeep` approach ensures the directory structure is preserved in version control even when empty
- Future tasks will define the specific agent file formats and templates to be stored in this directory
