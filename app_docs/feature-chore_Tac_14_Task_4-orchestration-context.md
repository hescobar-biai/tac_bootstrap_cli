---
doc_type: feature
adw_id: chore_Tac_14_Task_4
date: 2026-02-04
idk:
  - orchestration
  - slash-commands
  - agent-coordination
  - planner-agent
  - build-agent
  - workflow-patterns
  - command-documentation
tags:
  - feature
  - orchestration
  - documentation
related_code:
  - .claude/commands/plan.md
  - .claude/commands/build.md
  - .claude/commands/review.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2
---

# Orchestration Context for Commands

**ADW ID:** chore_Tac_14_Task_4
**Date:** 2026-02-04
**Specification:** specs/issue-624-adw-chore_Tac_14_Task_4-chore_planner-update-commands-orchestration.md

## Overview

Enhanced three core slash commands (`/plan`, `/build`, `/review`) with orchestration context that guides users on when to use orchestrated multi-agent workflows versus direct single-phase commands. This documentation update maintains full backward compatibility while introducing users to advanced orchestration patterns introduced in TAC-14.

## What Was Built

- Orchestration patterns section in `/plan` command documentation
- Orchestration patterns section in `/build` command documentation
- Orchestration patterns section in `/review` command documentation
- Synchronized template files for generated projects
- Cross-references to specialized agents and orchestration commands

## Technical Implementation

### Files Modified

- `.claude/commands/plan.md`: Added orchestration patterns section linking to `orch_plan_w_scouts_build_review` workflow and `planner` agent
- `.claude/commands/build.md`: Added orchestration patterns section linking to `build-agent` and `orch_scout_and_build` workflow
- `.claude/commands/review.md`: Added orchestration patterns section referencing review integration in orchestrated workflows
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`: Synchronized with base command
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`: Synchronized with base command
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2`: Synchronized with base command

### Key Changes

- **Pure Additive Changes**: All modifications are non-breaking additions to existing documentation. No existing instructions were removed or altered.
- **Consistent Format**: Each command received an "## Orchestration Patterns" section at the end with clear guidance on when to use orchestration vs direct commands.
- **Cross-Linking Strategy**: Commands now reference related specialized agents (planner, build-agent) and orchestration workflows (orch_plan_w_scouts_build_review, orch_scout_and_build).
- **Template Synchronization**: Template files (.j2) were updated to match base files exactly, as orchestration documentation is static framework-level content, not project-specific.
- **User Guidance**: Each section includes 2-3 sentence explanations differentiating single-phase tasks (use direct commands) from multi-phase workflows (use orchestration).

## How to Use

### For End Users

When working with TAC Bootstrap projects, commands now provide context:

1. **Planning a feature** - Read `/plan` command to see when to use `orch_plan_w_scouts_build_review` for complex multi-phase tasks
2. **Building files** - Read `/build` command to understand when to spawn parallel `build-agent` instances vs sequential building
3. **Reviewing code** - Read `/review` command to learn about integrated review in orchestrated workflows

### For CLI Developers

When generating new projects with TAC Bootstrap CLI:

1. The template files in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` contain the orchestration context
2. Generated projects automatically include this enhanced documentation
3. No configuration changes needed - templates are static copies

## Configuration

No configuration required. Changes are purely documentation-level and apply automatically to:
- Existing TAC Bootstrap project (base files in `.claude/commands/`)
- All newly generated projects (via template files in `tac_bootstrap_cli/tac_bootstrap/templates/`)

## Testing

Verify orchestration context sections were added correctly:

```bash
grep -n "## Orchestration Patterns" .claude/commands/plan.md
```

Expected: Line number showing the new section exists in plan.md

```bash
grep -n "## Orchestration Patterns" .claude/commands/build.md
```

Expected: Line number showing the new section exists in build.md

```bash
grep -n "## Orchestration Patterns" .claude/commands/review.md
```

Expected: Line number showing the new section exists in review.md

Verify links point to existing files:

```bash
ls -la .claude/commands/orch_plan_w_scouts_build_review.md .claude/commands/orch_scout_and_build.md .claude/agents/planner.md .claude/agents/build-agent.md
```

Expected: All four referenced files exist

Verify template synchronization:

```bash
diff .claude/commands/plan.md tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2
```

Expected: No differences (templates are exact copies for static documentation)

## Notes

**Backward Compatibility**: This is purely additive documentation work. All existing command functionality remains unchanged. Commands work exactly as before - the new sections only provide additional context about orchestration alternatives.

**No Jinja2 Variables Needed**: The "Orchestration Patterns" sections are static framework-level documentation that applies to all projects. Template .j2 files are exact copies of base .md files without variable interpolation.

**Dependencies on TAC-14**: This task depends on prior TAC-14 tasks that created:
- Agent definitions (Task 2): `planner.md`, `build-agent.md`, `scout-report-suggest.md`
- Orchestration commands (Task 3): `orch_plan_w_scouts_build_review.md`, `orch_scout_and_build.md`

If those files don't exist in a project, the documentation links would be broken. This assumes TAC-14 tasks were completed in order.

**Design Philosophy**: The update follows the principle of "progressive disclosure" - users start with simple direct commands and are gradually introduced to advanced orchestration patterns as their tasks become more complex. The documentation guides this transition naturally.
