---
doc_type: feature
adw_id: feature_Tac_9_task_29
date: 2026-01-26
idk:
  - jinja2-template
  - claude-code-hooks
  - expert-workflow
  - yaml-frontmatter
  - plan-build-improve
  - hook-patterns
  - settings-json
tags:
  - feature
  - template
  - expert-command
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2
---

# Claude Code Hook Expert Planning Template

**ADW ID:** feature_Tac_9_task_29
**Date:** 2026-01-26
**Specification:** specs/issue-270-adw-feature_Tac_9_task_29-sdlc_planner-cc-hook-expert-plan-template.md

## Overview

Added a Jinja2 template for the `cc_hook_expert_plan` expert command that guides AI agents through the planning phase of implementing Claude Code hooks. This is the first step in the Plan-Build-Improve workflow cycle for hook development, providing expert methodology for exploring requirements, understanding patterns, designing architecture, and creating implementation plans.

## What Was Built

- **Expert Planning Template**: Created `cc_hook_expert_plan.md.j2` template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/`
- **4-Phase Workflow**: Structured guidance through Requirements → Exploration → Architecture → Plan phases
- **Hook Patterns Documentation**: Comprehensive reference for 7 common hook types (PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit)
- **YAML Frontmatter Configuration**: Defined planning-focused tools (Read, Glob, Grep, Task/Explore, EnterPlanMode, AskUserQuestion, TodoWrite)
- **Integration Guidance**: Documented settings.json configuration, JSON input/output structure, exit code strategy, and naming conventions

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` (NEW): 221-line Jinja2 template with expert planning workflow
- `specs/issue-270-adw-feature_Tac_9_task_29-sdlc_planner-cc-hook-expert-plan-template.md` (NEW): Feature specification
- `specs/issue-270-adw-feature_Tac_9_task_29-sdlc_planner-cc-hook-expert-plan-template-checklist.md` (NEW): Implementation checklist

### Key Changes

1. **Template Structure**: Created YAML frontmatter defining `allowed-tools`, `description`, and `model: sonnet` for planning phase
2. **Variable Definitions**: Established `HOOK_REQUIREMENTS` ($ARGUMENTS) and `PROJECT_NAME` ({{ config.project.name }}) as template variables
3. **Workflow Instructions**: Implemented 4-phase methodology covering requirement gathering, codebase exploration, architectural design, and plan creation
4. **Hook Patterns Reference**: Documented 7 common hook types with use cases, naming conventions, settings.json structure, exit code strategy (0/1/2), and JSON input format
5. **Expert Guidance**: Provided static, universal methodology that guides agents through systematic hook planning without project-specific assumptions

## How to Use

### For TAC Bootstrap Users

1. Generate a new project with TAC Bootstrap CLI:
   ```bash
   cd tac_bootstrap_cli
   uv run tac-bootstrap generate
   ```

2. In the generated project, use the expert planning command:
   ```bash
   /cc_hook_expert_plan pre-commit validation with security checks
   ```
   Or without arguments to be prompted:
   ```bash
   /cc_hook_expert_plan
   ```

3. The agent will guide you through:
   - Understanding hook requirements
   - Exploring existing hook patterns in your codebase
   - Designing hook architecture
   - Creating an implementation plan at `specs/hook-{name}-plan.md`

### For Template Developers

When extending or modifying the template:
- Use minimal Jinja2 variables (only `{{ config.project.name }}` where needed)
- Keep expert guidance static and universal
- Follow established YAML frontmatter patterns
- Reference existing hooks for integration examples

## Configuration

### Template Variables

- `{{ config.project.name }}`: Project name from TAC Bootstrap configuration (used minimally)
- `$ARGUMENTS`: Optional hook requirements passed by user

### YAML Frontmatter

- **allowed-tools**: Read, Glob, Grep, Task, EnterPlanMode, AskUserQuestion, TodoWrite
- **description**: 'Plan hook implementation using expert methodology'
- **model**: sonnet (planning phase doesn't require opus)

### Hook Types Covered

1. **PreToolUse**: Validation, blocking dangerous commands, pre-processing
2. **PostToolUse**: Logging results, post-processing, cleanup
3. **Notification**: External integrations, alerts
4. **Stop**: Session cleanup, final reporting
5. **SubagentStop**: Subagent result processing
6. **PreCompact**: Context preservation before summarization
7. **UserPromptSubmit**: Prompt logging, user input pre-processing

## Testing

### Validate Template Syntax

Ensure Jinja2 template renders correctly:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Check Code Quality

Verify linting and type checking:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test CLI

Confirm CLI generator still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Integration Test

Generate a test project and verify the command renders correctly:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap generate
# Navigate to generated project
# Check .claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md exists
# Verify YAML frontmatter is valid
# Confirm variables are correctly substituted
```

## Notes

- This template is **ONLY** for the planning phase - build and improve phases will be separate templates
- Template file creation only - rendering happens when users run `tac_bootstrap generate` CLI command
- Expert guidance is static content (universal methodology), not project-specific - agents discover project APIs during exploration
- Hook API details are intentionally generic to work across different project types
- Follows Plan-Build-Improve workflow pattern from TAC methodology
- Directory structure `experts/cc_hook_expert/` already existed with .gitkeep placeholder
- All validation commands passed with zero regressions
- Template uses minimal Jinja2 variables to maintain universality across projects
