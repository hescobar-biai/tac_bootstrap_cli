---
doc_type: feature
adw_id: chore_Tac_9_task_28
date: 2026-01-26
idk:
  - template-repository
  - directory-structure
  - expert-agents
  - template-discovery
  - test-coverage
  - gitkeep
tags:
  - feature
  - infrastructure
  - templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/.gitkeep
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/.gitkeep
  - tac_bootstrap_cli/tests/test_template_repo.py
---

# Expert Agents Directory Structure

**ADW ID:** chore_Tac_9_task_28
**Date:** 2026-01-26
**Specification:** specs/issue-269-adw-chore_Tac_9_task_28-chore_planner-expert-agents-directory-structure.md

## Overview

Created the foundational directory structure `templates/claude/commands/experts/cc_hook_expert/` within the TAC Bootstrap CLI template system to organize expert agent commands. This infrastructure establishes a dedicated space for specialized agent commands that can be generated in future projects.

## What Was Built

- Expert agents directory structure at `templates/claude/commands/experts/`
- Claude Code hook expert subdirectory at `templates/claude/commands/experts/cc_hook_expert/`
- `.gitkeep` files to preserve empty directories in version control
- Test validation for nested directory discovery in template repository

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/.gitkeep`: Ensures parent experts directory is tracked in git
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/.gitkeep`: Ensures cc_hook_expert subdirectory is tracked in git
- `tac_bootstrap_cli/tests/test_template_repo.py`: Added test case `test_list_templates_discovers_nested_directories` to validate template discovery

### Key Changes

- Created two-level nested directory structure following existing pattern: `commands/{category}/{subcategory}/`
- Added `.gitkeep` convention to preserve empty directories (git doesn't track empty directories by default)
- Implemented test that verifies `TemplateRepository.list_templates()` discovers templates in nested expert directories
- Test validates that `.gitkeep` files are ignored during template discovery while the directory structure is preserved
- Followed YAGNI principle: only created `cc_hook_expert` subdirectory as specified, no additional expert types

## How to Use

This is infrastructure work that prepares the template system for future expert agent commands. When expert agent command templates are added to the `cc_hook_expert/` directory:

1. Add template files (e.g., `some_expert.md.j2`) to `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/`
2. The `TemplateRepository` will automatically discover them via `list_templates()`
3. Generated projects will include the experts directory structure with the expert commands

## Configuration

No configuration changes required. The directory structure integrates automatically with the existing template repository system.

## Testing

Run unit tests to verify directory structure discovery:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::TestTemplateDiscovery::test_list_templates_discovers_nested_directories -v
```

Run full test suite to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to verify code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run smoke test to verify CLI still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This directory structure uses standard permissions (755/default)
- The template repository's `list_templates()` method automatically discovers files in this new structure through recursive directory traversal
- `.gitkeep` files are filtered out during template listing to avoid treating them as templates
- Future tasks will populate this directory with actual expert agent command templates (e.g., for Claude Code hooks, repository analysis, etc.)
- Follows snake_case naming convention consistent with existing template structure
