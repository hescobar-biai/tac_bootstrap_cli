---
doc_type: feature
adw_id: feature_Tac_12_task_7_2
date: 2026-01-30
idk:
  - slash-command
  - planning
  - claude-agent
  - jinja2-template
  - scaffold-service
  - implementation-plan
tags:
  - feature
  - planning
  - command
related_code:
  - .claude/commands/plan.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Simple Planning Command (/plan)

**ADW ID:** feature_Tac_12_task_7_2
**Date:** 2026-01-30
**Specification:** specs/issue-459-adw-feature_Tac_12_task_7_2-sdlc_planner-plan-command.md

## Overview

Created a simplified `/plan` slash command that enables rapid implementation planning through a streamlined 5-step workflow. Unlike `/plan_w_scouters` which uses parallel scout agents for comprehensive exploration, this command provides quick planning for straightforward features where developers already know which files to work with.

## What Was Built

- **Base command file**: `.claude/commands/plan.md` with simplified workflow
- **Jinja2 template**: `plan.md.j2` for CLI generation into target projects
- **Scaffold integration**: Updated `scaffold_service.py` to include plan command
- **5-step workflow**: Understand → Read → Design → Plan → Save
- **Model configuration**: Uses `claude-opus-4-1-20250805` with focused toolset

## Technical Implementation

### Files Modified

- **`.claude/commands/plan.md`**: Base reference implementation for TAC Bootstrap itself
  - Configured with allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
  - 5-step workflow without scout exploration overhead
  - Instructions for manual file exploration using Glob/Grep
  - Structured plan format with metadata, user story, implementation tasks

- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`**: Template for CLI generation
  - Uses Jinja2 variables: `{{ config.project.name }}`, `{{ config.paths.specs_dir }}`
  - Conditional validation commands: `{{ config.commands.test }}`, `{{ config.commands.lint }}`
  - Compatible with existing TACConfig schema

- **`tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`**: Added "plan" to commands list
  - Positioned after "plan_w_scouters" in the commands array (line 330)
  - Ensures template is rendered during `generate` or `upgrade` operations

### Key Changes

- **Simplified from plan_w_scouters**: Removed scout exploration workflow (steps 1-9), scout result aggregation, high-confidence file scoring, and parallel Task tool invocations
- **Retained structure**: Maintains same plan format (metadata, description, user story, problem/solution statements, tasks, validation) as comprehensive planning commands
- **Manual exploration**: Agent uses Read/Glob/Grep tools directly instead of delegating to scout subagents
- **Output format**: Same machine-parseable output (relative path only) as other planning commands
- **Specs directory**: Plans saved to `specs/issue-{number}-adw-{id}-sdlc_planner-{name}.md`

## How to Use

### In TAC Bootstrap Repository

1. Invoke the command with issue metadata:
```bash
/plan 459 feature_Tac_12_task_7_2 '{"number":459,"title":"Create plan command",...}'
```

2. Agent follows 5-step workflow:
   - Parses issue JSON to understand requirements
   - Explores codebase with Glob/Grep/Read
   - Designs implementation approach
   - Writes structured plan
   - Saves to specs/ directory

3. Outputs relative path:
```
specs/issue-459-adw-feature_Tac_12_task_7_2-sdlc_planner-plan-command.md
```

### In Generated Projects

After running `tac-bootstrap generate` or `upgrade`:

1. The `/plan` command becomes available in `.claude/commands/plan.md`
2. Template variables are substituted with project-specific values
3. Validation commands reflect project's test/lint/typecheck setup
4. Specs directory path uses project's configuration

## Configuration

### Command Frontmatter

```yaml
allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
description: Create implementation plans with simple file exploration workflow
model: claude-opus-4-1-20250805
```

### Template Variables Used

- `{{ config.project.name }}` - Project name in instructions
- `{{ config.project.description }}` - Project description
- `{{ config.paths.specs_dir }}` - Directory for saving plans (default: "specs/")
- `{{ config.commands.test }}` - Test command (conditional)
- `{{ config.commands.lint }}` - Lint command (conditional)
- `{{ config.commands.typecheck }}` - Type check command (conditional)
- `{{ config.commands.install }}` - Package install command

### When to Use /plan vs /plan_w_scouters

**Use `/plan` when:**
- Simple, straightforward features where files are known
- Small codebases where manual exploration is quick
- Time-sensitive planning without scout overhead
- Developer already has good codebase familiarity

**Use `/plan_w_scouters` when:**
- Complex features requiring comprehensive file discovery
- Large codebases with many architectural layers
- Unclear which files need modification
- Want high-confidence file recommendations from parallel exploration

## Testing

### Validation Commands

All validation commands pass with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Verification

Test template rendering:

```bash
# Generate test project
tac-bootstrap generate --config test-config.yml

# Verify plan.md created
ls -la test-project/.claude/commands/plan.md

# Check template substitution
cat test-project/.claude/commands/plan.md | grep -A 2 "Instructions"
```

Test command execution in Claude Code:

```bash
# In Claude Code CLI, invoke:
/plan 123 test_adw_id '{"number":123,"title":"Test feature"}'

# Verify plan created in specs/
ls -la specs/issue-123-adw-test_adw_id-sdlc_planner-*.md
```

## Notes

- The command follows TAC Bootstrap's architectural patterns: base file in `.claude/commands/` serves as reference, Jinja2 template in `templates/` for generation
- Plan format matches other planning commands to ensure consistency across workflows
- Agent receives explicit instructions to create specs/ directory if needed and ask user about file conflicts
- Future enhancements could include `--with-scouts` flag to upgrade to scout-based planning, custom plan templates via config, and plan validation checking
- This command is part of Wave 1 - New Commands (Task 7 of 13) in the TAC Bootstrap roadmap
