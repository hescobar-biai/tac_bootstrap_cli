---
doc_type: feature
adw_id: feature_Tac_11_task_4
date: 2026-01-27
idk:
  - jinja2-template
  - slash-command
  - parallel-exploration
  - codebase-discovery
  - delegation-prompt
  - tac-10-level-4
tags:
  - feature
  - template
  - scout
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2
  - .claude/commands/scout.md
---

# Scout Command Jinja2 Template

**ADW ID:** feature_Tac_11_task_4
**Date:** 2026-01-27
**Specification:** specs/issue-340-adw-feature_Tac_11_task_4-sdlc_planner-scout-template.md

## Overview

Created a Jinja2 template version of the `/scout` slash command for TAC Bootstrap generated projects. This template enables projects to include parallel codebase exploration functionality that uses multiple search strategies to identify relevant files for a given task.

## What Was Built

- **scout.md.j2 Template**: Complete 509-line Jinja2 template for the `/scout` command
- **Minimal Templating**: Only injects `{{ config.project.name }}` where project-specific references occur
- **Universal Search Strategies**: Preserved all 9+ search strategies that work across all project types
- **Complete Workflow**: Maintained the full 10-step workflow for parallel exploration

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2`: New Jinja2 template created from `.claude/commands/scout.md` (509 lines)

### Key Changes

1. **Template Conversion**: Converted the existing `.claude/commands/scout.md` file to a Jinja2 template following the same pattern established in Task 3
2. **Static Content Preservation**: Kept all scout command content static including:
   - Variables section ($1 for USER_PROMPT, $2 for SCALE)
   - Complete instructions and purpose documentation
   - All 9+ search strategy definitions (file patterns, content search, architecture, dependencies, tests, config, types, docs, specialized)
   - Full workflow (Steps 1-10) for parallel agent delegation
   - Report format with frequency-based relevance scoring
   - Examples, notes, limitations, best practices, troubleshooting
3. **Minimal Project-Specific Variables**: Only `{{ config.project.name }}` is injected where project references naturally appear
4. **No Configuration Schema Changes**: Uses existing config structure, no scout-specific options added (following YAGNI principle)

## How to Use

When generating a new project with TAC Bootstrap CLI, the `/scout` command will be automatically included in the generated `.claude/commands/` directory:

1. **Generate a new project**:
```bash
cd tac_bootstrap_cli
uv run tac-bootstrap init my-project
```

2. **The generated project will include**: `.claude/commands/scout.md` with full parallel exploration functionality

3. **Use the scout command** in the generated project:
```bash
/scout "find authentication related files"
/scout "database migration logic" 3
/scout "API endpoint handlers" 6
```

## Configuration

No scout-specific configuration is required. The template uses:
- `{{ config.project.name }}` - Existing project name from base configuration

The scout methodology is universal and works across all project types without requiring customization. Search strategies automatically adapt to whatever codebase structure exists.

## Testing

Run the full validation suite to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting checks:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Run smoke test to verify CLI works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

- **Minimal templating**: Following YAGNI principle, only inject project name where it naturally appears. Scout's exploration methodology is universal and doesn't need project-specific customization.
- **No scout-specific config**: All search strategies (patterns, content, architecture, dependencies) remain unchanged as they work identically across Python, TypeScript, Go, and other project types.
- **Static strategies preserved**: File pattern matching, content search (grep), architectural analysis, and dependency mapping are all language-agnostic and self-adapting.
- **TAC-10 Level 4 pattern**: Implements Delegation Prompt pattern with parallel agent execution for maximum exploration coverage.

### Implementation Pattern Consistency

This task follows the exact conversion pattern established in Task 3:
1. Read existing `.md` file completely
2. Identify minimal template variable needs
3. Convert to `.md.j2` with Jinja2 syntax
4. Preserve all static content (510 lines → 509 lines in template)
5. No config schema changes
6. Validate with existing test suite

### Why Scout Doesn't Need Heavy Customization

The `/scout` command uses universal search strategies that work across all languages and project types:
- File pattern matching adapts to any naming convention
- Content search (grep) is language-agnostic
- Architectural analysis works with any structure
- Dependency mapping identifies imports/references in any language

Adding project-specific customization would add complexity without clear benefit. The command's self-adapting nature makes heavy templating unnecessary.
