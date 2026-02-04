---
doc_type: feature
adw_id: chore_Tac_13_Task_22
date: 2026-02-03
idk:
  - dual-strategy
  - template-registration
  - scaffold-service
  - expert-parallel
  - meta-agentics
  - validation
tags:
  - feature
  - verification
  - tac-13
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - .claude/commands/expert-parallel.md
  - specs/issue-584-adw-chore_Tac_13_Task_22-sdlc_planner-verify-expert-parallel.md
---

# Expert-Parallel Template Verification

**ADW ID:** chore_Tac_13_Task_22
**Date:** 2026-02-03
**Specification:** specs/issue-584-adw-chore_Tac_13_Task_22-sdlc_planner-verify-expert-parallel.md

## Overview

This verification task confirmed that the expert-parallel template was successfully created in TAC-13 Task 17 with complete dual strategy implementation. The task validated all three required components of the dual strategy pattern and ensured proper integration into the scaffold service.

## What Was Built

This was a verification-only task. The components verified include:

- Jinja2 template for expert-parallel command generation
- Template registration in scaffold_service.py
- Working implementation in repository root
- Specification and checklist documentation for the verification process

## Technical Implementation

### Files Modified

No code files were modified in this task. Only documentation files were created:

- `specs/issue-584-adw-chore_Tac_13_Task_22-sdlc_planner-verify-expert-parallel.md`: Detailed specification for the verification task
- `specs/issue-584-adw-chore_Tac_13_Task_22-sdlc_planner-verify-expert-parallel-checklist.md`: Validation checklist with test results
- `.mcp.json` and `playwright-mcp-config.json`: Minor configuration path updates for worktree

### Key Changes

- Verified template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
- Confirmed registration in `scaffold_service.py` at line 346
- Validated implementation at `.claude/commands/expert-parallel.md`
- Documented that all 3 components of dual strategy pattern are present
- Confirmed template and implementation have matching structure and frontmatter
- Verified command is auto-discovered by Claude Code (no manual skills registration needed)

## How to Use

This task is about verification, not new functionality. The expert-parallel command itself implements a 4-phase parallel expert consensus workflow:

1. **Validate**: Check parameters (domain, task, num_agents)
2. **Spawn**: Launch 3-10 expert agents in parallel
3. **Monitor**: Track progress of all agents
4. **Synthesize**: Combine results with Opus model

Usage of the expert-parallel command:
```bash
/expert-parallel <EXPERT_DOMAIN> <TASK> [NUM_AGENTS]
```

Where:
- EXPERT_DOMAIN: Domain expertise area (e.g., "security", "performance")
- TASK: Task description for experts
- NUM_AGENTS: Optional number of agents (default: 3, range: 3-10)

## Configuration

The dual strategy pattern requires three components for each command:

1. **Template** (.j2 file): Located in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
2. **Registration**: Entry in `scaffold_service.py` command_files list
3. **Implementation**: Working file in `.claude/commands/` for repository use

All three components were verified to exist and work correctly.

## Testing

All automated validations passed:

```bash
# Unit tests (718 tests)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
# Linting
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo "✓ Template"
```

```bash
# Verify registration
grep "expert-parallel" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
```

## Notes

**About Dual Strategy Pattern:**
TAC-13 uses a "dual strategy" pattern where each command/skill requires 3 components:
1. Template (.j2 file) - For CLI generation
2. Registration (entry in scaffold_service.py) - To include template in scaffolding
3. Implementation (file in repo root) - Working version for this repository

**Task 17 Context:**
The expert-parallel command was originally created in Task 17 with:
- 4-phase workflow (validate, spawn, monitor, synthesize)
- Variables: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3, default 3)
- Range validation: 3-10 agents
- Opus model for synthesis

**Similar Commands:**
This verification task follows the same pattern used for:
- expert-orchestrate.md (Task 16/Task 21 verification)
- meta-agent.md (Task 14)
- meta-prompt.md (Task 13)

All TAC-13 meta-agentics features use the dual strategy pattern for consistency and maintainability.
