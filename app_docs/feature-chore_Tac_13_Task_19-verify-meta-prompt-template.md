---
doc_type: feature
adw_id: chore_Tac_13_Task_19
date: 2026-02-03
idk:
  - meta-prompt
  - template-verification
  - dual-strategy
  - scaffold-service
  - jinja2
  - project-agnostic
tags:
  - feature
  - verification
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - .claude/commands/meta-prompt.md
---

# Verify Meta-Prompt Template

**ADW ID:** chore_Tac_13_Task_19
**Date:** 2026-02-03
**Specification:** specs/issue-581-adw-chore_Tac_13_Task_19-chore_planner-verify-meta-prompt-template.md

## Overview

This verification task confirms the meta-prompt template implementation from TAC-13 Task 13 is complete and properly integrated. The task validates that the template exists, is registered in scaffold_service.py, and has a corresponding repo root implementation following the dual strategy pattern.

## What Was Built

This was a verification-only task that confirmed:

- Template file exists at correct location with proper structure
- Repo root implementation exists and matches template
- Registration is complete in scaffold_service.py
- Template is project-agnostic (no language-specific assumptions)
- Jinja2 variables are minimal per CLAUDE.md guidance

## Technical Implementation

### Files Modified

- `specs/issue-581-adw-chore_Tac_13_Task_19-chore_planner-verify-meta-prompt-template.md`: Specification for verification task
- `specs/issue-581-adw-chore_Tac_13_Task_19-chore_planner-verify-meta-prompt-template-checklist.md`: Validation checklist documenting verification results
- `.mcp.json`: Updated MCP configuration
- `playwright-mcp-config.json`: Updated Playwright configuration

### Key Changes

- Confirmed template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` has proper YAML frontmatter with allowed-tools, description, argument-hint
- Validated template uses minimal Jinja2 variables: `{{ config.project.name }}` and `{{ config.paths.templates_dir }}`
- Verified "meta-prompt" registration in scaffold_service.py commands list at line 343
- Confirmed template structure matches TAC standards with variables section, instructions & workflow, and report section
- Validated consistency between template and repo root implementation at `.claude/commands/meta-prompt.md`

## How to Use

This feature is for maintainers verifying the integrity of the meta-prompt template implementation. The verification process follows a three-layer pattern:

1. Check template file existence and structure
2. Verify registration in scaffold_service.py
3. Confirm repo root implementation exists and is consistent

## Configuration

No configuration required. The verification uses existing files:

- Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`
- Implementation: `.claude/commands/meta-prompt.md`
- Registration: `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (line 343)

## Testing

Verify template exists:

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"
```

Verify repo root implementation:

```bash
test -f .claude/commands/meta-prompt.md && echo "✓ Implementation exists" || echo "✗ Implementation missing"
```

Verify registration in commands list:

```bash
grep '"meta-prompt"' tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered in commands list" || echo "✗ Not registered"
```

Run full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check linting:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

CLI smoke test:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

This verification task is part of TAC-13's dual strategy implementation pattern where templates are both created in the CLI generator and implemented in the repo root. The three-layer verification ensures:

1. Template exists with proper structure
2. Template is registered in scaffold_service.py
3. Implementation exists in repo root

The meta-prompt follows meta-agentics pattern (prompts creating prompts) and is fully project-agnostic, working across any language or framework. All automated validations passed (716 tests, linting, CLI smoke test).
