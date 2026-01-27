---
doc_type: feature
adw_id: chore_Tac_10_task_7
date: 2026-01-27
idk:
  - gitkeep
  - template
  - jinja2
  - scaffold
  - directory-structure
  - agents
tags:
  - feature
  - chore
  - infrastructure
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2
  - agents/hook_logs/.gitkeep
  - .gitignore
---

# .gitkeep Templates for Agents Directories

**ADW ID:** chore_Tac_10_task_7
**Date:** 2026-01-27
**Specification:** specs/issue-313-adw-chore_Tac_10_task_7-sdlc_planner-create-gitkeep-agents-templates.md

## Overview

Added .gitkeep files to maintain empty directory structure for agents subdirectories (`hook_logs/` and `context_bundles/`) in both the TAC Bootstrap repository itself and in the Jinja2 templates used during project scaffolding. This ensures Git tracks these directories even when empty, maintaining consistent structure across generated projects.

## What Was Built

- Jinja2 template files for `.gitkeep` in agents subdirectories
- Direct `.gitkeep` files in tac_bootstrap repository
- Updated `.gitignore` to allow tracking these specific directories

## Technical Implementation

### Files Modified

- `.gitignore`: Added exception rules to allow `agents/hook_logs/` directory tracking (previously ignored under `agents/*`)
- `agents/hook_logs/.gitkeep`: New empty file to enable Git tracking of empty directory
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2`: New empty Jinja2 template
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2`: New empty Jinja2 template

### Key Changes

- Created dual-location .gitkeep files: templates for scaffold generation and direct files for tac_bootstrap itself
- .gitkeep files are intentionally empty - they serve only as placeholders to make Git track parent directories
- No Jinja2 variables needed in template files as .gitkeep files have no content
- Followed existing pattern where `agents/context_bundles/` was already tracked, extended to `agents/hook_logs/`
- Templates in `structure/` directory are auto-discovered during scaffold process, requiring no manual registration

## How to Use

### For Generated Projects

When running `tac-bootstrap scaffold`, the CLI automatically:

1. Copies all templates from `templates/structure/` to the target project
2. Processes `.j2` files through Jinja2 (though .gitkeep templates remain empty)
3. Creates `agents/hook_logs/` and `agents/context_bundles/` directories with .gitkeep files

This happens transparently without user intervention.

### For TAC Bootstrap Repository

The .gitkeep files in the tac_bootstrap repository itself ensure that:

1. `agents/hook_logs/` directory is tracked by Git even when no log files exist
2. Fresh clones of the repository maintain correct directory structure
3. Consistency between repository structure and generated project structure

## Configuration

No configuration changes required. The template discovery mechanism automatically includes all files in `templates/structure/` during scaffolding.

The `.gitignore` patterns ensure that:
- Most content under `agents/*` is ignored (logs and temporary agent outputs)
- Specific subdirectories (`agents/hook_logs/`, `agents/context_bundles/`) are explicitly tracked
- Template directories are always tracked

## Testing

Verify template files exist:

```bash
find tac_bootstrap_cli/tac_bootstrap/templates/structure/agents -name '.gitkeep.j2'
```

Verify direct .gitkeep files exist in repository:

```bash
find agents -name '.gitkeep'
```

Run unit tests to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check linting passes:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test CLI still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- .gitkeep is a convention, not a Git feature - any filename would work, but .gitkeep clearly communicates intent
- Empty directories are not tracked by Git by design; .gitkeep files work around this limitation
- This chore maintains the principle that tac_bootstrap uses the same structure it generates for other projects
- The dual-location approach (templates + direct files) ensures both scaffold outputs and the repository itself maintain consistent structure
