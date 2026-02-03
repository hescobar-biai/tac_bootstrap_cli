---
doc_type: feature
adw_id: feature_Tac_13_Task_16
date: 2026-02-03
idk:
  - expert-orchestrator
  - workflow-automation
  - plan-build-improve
  - meta-command
  - subagent-spawning
  - sequential-orchestration
  - domain-expert
  - task-tool
tags:
  - feature
  - orchestration
  - automation
  - expert-workflow
related_code:
  - .claude/commands/expert-orchestrate.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Expert Orchestrator - Plan → Build → Improve Workflow

**ADW ID:** feature_Tac_13_Task_16
**Date:** 2026-02-03
**Specification:** specs/issue-578-adw-feature_Tac_13_Task_16-sdlc_planner-expert-orchestrator.md

## Overview

The Expert Orchestrator is a meta-command that automates the complete plan → build → improve workflow cycle for domain experts. It validates inputs, spawns three sequential subagents (planning, building, and self-improvement), provides clear progress feedback with emoji markers, and generates a synthesized markdown report of all three phases.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2` for distribution to generated projects
- **Working Implementation**: `.claude/commands/expert-orchestrate.md` in repo root for immediate use
- **Service Registration**: Command registered in `scaffold_service.py` commands list
- **3-Step Sequential Workflow**: Automated orchestration with Task tool subagent spawning
- **Input Validation**: Domain validation against known experts (adw, cli, commands, cc_hook_expert)
- **Progress Tracking**: Clear emoji markers (🔍 Planning... 🔨 Building... ✨ Improving...)
- **Error Handling**: Abort-on-failure logic with actionable error messages
- **Plan Path Extraction**: Regex-based extraction of plan file paths from Step 1 output
- **Synthesis Report**: Markdown report combining all three phases with next steps

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:342`: Added "expert-orchestrate" to commands list
- `.claude/commands/expert-orchestrate.md`: Created working implementation file (300 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`: Created Jinja2 template (300 lines, identical to implementation)

### Key Changes

1. **Command Structure**: Created comprehensive meta-command with frontmatter specifying allowed-tools (Task, Read, AskUserQuestion, TodoWrite), description, argument-hint, and model (sonnet)

2. **Input Validation**: Two-stage validation checks EXPERT_DOMAIN against hardcoded list of known domains and requires TASK_DESCRIPTION with clear error messages

3. **Sequential Orchestration**: Three Task tool invocations in strict sequence:
   - Step 1: `/experts:{domain}:plan {task}` → extracts plan file path
   - Step 2: `/build {plan_path}` → implements the plan
   - Step 3: `/experts:{domain}:self-improve true` → validates and improves

4. **Plan Path Extraction**: Uses regex pattern `([a-zA-Z0-9_/\-\.]+\.md)` to extract plan file paths from planning agent output (common patterns: `specs/issue-*.md`, `specs/plan-*.md`)

5. **Error Handling Strategy**: Abort-on-failure for Steps 1-2 (sequential dependencies), warn-only for Step 3 (implementation already complete)

6. **Progress Tracking**: TodoWrite tool used to track 3 phases with emoji markers shown at each step start

7. **Synthesis Report**: Generates markdown report with sections for Planning, Building, and Self-Improvement phases, including status, key points, files changed, and next steps

8. **Service Registration**: Integrated into scaffold service's command list for automatic inclusion in generated projects

## How to Use

1. **Basic Usage**: Execute the orchestrator command with domain and task description
   ```bash
   /expert-orchestrate [domain] [task_description]
   ```

2. **Example - CLI Expert**: Orchestrate CLI improvements
   ```bash
   /expert-orchestrate cli "add help text to wizard command"
   ```

3. **Example - ADW Expert**: Create new ADW workflow
   ```bash
   /expert-orchestrate adw "create feature planning workflow"
   ```

4. **Example - Hooks Expert**: Implement hook improvements
   ```bash
   /expert-orchestrate cc_hook_expert "add git validation to pre-commit hook"
   ```

5. **Monitor Progress**: Watch for emoji markers indicating current phase
   - 🔍 Step 1/3: Planning with expert...
   - 🔨 Step 2/3: Building implementation...
   - ✨ Step 3/3: Validating and improving...

6. **Review Results**: Read synthesis report displayed at completion with plan summary, build results, improvements made, and next steps

## Configuration

### Supported Domains

The orchestrator validates against four known domains:
- `adw`: ADW workflow expert (`.claude/commands/experts/adw/`)
- `cli`: CLI generator expert (`.claude/commands/experts/cli/`)
- `commands`: Command template expert (`.claude/commands/experts/commands/`)
- `cc_hook_expert`: Claude Code hooks expert (`.claude/commands/experts/cc_hook_expert/`)

### Required Expert Commands

Each domain must have two commands available:
- `/experts:{domain}:plan [task]` - Creates implementation plan
- `/experts:{domain}:self-improve [check_git_diff]` - Validates expertise

### Report Location (Optional)

Synthesis reports are displayed to stdout and optionally saved to:
```
.claude/reports/orchestrate-{domain}-{timestamp}.md
```
File save only occurs if `.claude/reports/` directory exists.

## Testing

### Validation Commands

Verify template and implementation files exist:
```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2 && echo "✓ Template exists"
```

Verify template is registered in scaffold service:
```bash
grep "expert-orchestrate" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"
```

Verify implementation file exists:
```bash
test -f .claude/commands/expert-orchestrate.md && echo "✓ Implementation exists"
```

### Integration Testing

Run full CLI test suite to ensure no regressions:
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

Verify CLI still works:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing (Future)

Execute orchestrator command to validate end-to-end workflow:
```bash
# Example: /expert-orchestrate cli "add help text to wizard"
# Should spawn 3 subagents sequentially and produce report
```

## Notes

### Design Decisions

- **Hardcoded Domains**: Known domains are hardcoded for MVP (adw, cli, commands, cc_hook_expert) - can be made configurable later via domain registry
- **Regex Plan Path Extraction**: Uses pattern `([a-zA-Z0-9_/\-\.]+\.md)` to extract plan file paths - assumes expert plan commands output paths ending in `.md`
- **No Retry Logic**: Failures abort immediately since sequential dependencies mean retrying one step without redoing prior steps doesn't make sense
- **Stdout + Optional File**: Primary output to stdout for immediate visibility, optional save to `.claude/reports/` for record-keeping
- **No Configurability**: Timeouts, retry counts not configurable for MVP - can be added later if needed

### Implementation Notes

- Expert commands follow pattern: `/experts:{domain}:{command} [args]`
- Build command accepts optional plan file path: `/build [plan_path]`
- Self-improve commands accept boolean flag for full validation
- Task tool used for spawning subagents with proper prompt and description
- Plan path extraction robust to different output formats

### TAC-13 Dual Strategy Pattern

This feature follows TAC-13's dual strategy:
1. **Jinja2 Template**: Distributes to all generated projects via CLI scaffolding
2. **Working Implementation**: Available immediately in repo root for dogfooding and testing

Both files are functionally identical (300 lines) with template using Jinja2 syntax for config variable substitution.

### Future Enhancements

- Add optional `--parallel` flag for parallel expert scaling (TAC-13 Task 17)
- Add `--dry-run` mode to show what would be executed without running
- Add progress bar or detailed step output for better visibility
- Support custom expert domains via config file or domain registry
- Add telemetry/observability for orchestration metrics (duration, success rate, failure points)
- Implement configurable timeouts and retry logic for robustness
- Add report templates for different output formats (JSON, YAML, HTML)
