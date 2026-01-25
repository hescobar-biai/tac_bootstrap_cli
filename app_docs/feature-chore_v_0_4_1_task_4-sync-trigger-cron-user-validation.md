---
doc_type: feature
adw_id: chore_v_0_4_1_task_4
date: 2026-01-25
idk:
  - trigger-cron
  - user-validation
  - github-assignment
  - jinja2-template
  - adw-triggers
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2
---

# Trigger Cron Template User Validation Sync

**ADW ID:** chore_v_0_4_1_task_4
**Date:** 2026-01-25
**Specification:** /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/chore_v_0_4_1_task_4/specs/issue-220-adw-chore_v_0_4_1_task_4-chore_planner-sync-trigger-cron-template.md

## Overview

Synchronized the `trigger_cron.py.j2` Jinja2 template with the root `trigger_cron.py` file to include user assignment validation logic. This ensures that the cron trigger only processes GitHub issues assigned to the current user and automatically assigns issues when triggering workflows.

## What Was Built

- **User validation imports**: Added `get_current_gh_user`, `is_issue_assigned_to_me`, and `assign_issue_to_me` function imports to template
- **Assignment filtering**: Added check in issue processing loop to skip issues not assigned to current user
- **Auto-assignment**: Added automatic issue assignment when triggering workflows
- **User display**: Added current user information in startup messages

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`: Updated Jinja2 template to match root file with user validation logic while preserving template variables

### Key Changes

- **Imports (lines 44-50)**: Added three user-related functions from `adw_modules.github` module
- **Issue filtering (lines 295-297)**: Added `is_issue_assigned_to_me()` check in `check_and_process_issues()` to skip unassigned issues
- **Workflow assignment (lines 218-222)**: Added `assign_issue_to_me()` call in `trigger_workflow()` with error handling
- **Startup messages (lines 352-356)**: Added current user display and assignment policy message in `main()` function
- **Template preservation**: Maintained all Jinja2 variable substitutions like `{{ config.project.name }}` and `{{ config.agentic.cron_interval | default(20) }}`

## How to Use

The template is automatically used when generating new projects with TAC Bootstrap CLI. The generated `trigger_cron.py` will include user validation logic.

1. Generate a new project or regenerate triggers using TAC Bootstrap CLI
2. The generated `trigger_cron.py` will automatically filter issues by current GitHub user
3. When a workflow is triggered, the issue will be auto-assigned to the executing user
4. View startup messages to confirm current user and filtering policy

## Configuration

No additional configuration required. The template uses existing Jinja2 variables:

- `{{ config.project.name }}`: Project name for logging
- `{{ config.agentic.cron_interval | default(20) }}`: Polling interval (default 20 seconds)

## Testing

Validate that the template changes don't introduce regressions.

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to ensure code quality.

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Verify CLI still works correctly.

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- The source file `adws/adw_triggers/trigger_cron.py` serves as the authoritative reference
- User validation prevents concurrent work conflicts when multiple users run cron triggers
- Auto-assignment ensures proper issue tracking and ownership
- Template variables are preserved to maintain dynamic configuration support
