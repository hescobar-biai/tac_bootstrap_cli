---
doc_type: feature
adw_id: feature_Tac_12_task_9_2
date: 2026-01-30
idk:
  - orchestration
  - workflow-automation
  - agent-delegation
  - task-tool
  - scout-plan-build
  - jinja2
  - cli-scaffolding
tags:
  - feature
  - command
  - workflow
  - automation
related_code:
  - .claude/commands/scout_plan_build.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Scout-Plan-Build Orchestration Command

**ADW ID:** feature_Tac_12_task_9_2
**Date:** 2026-01-30
**Specification:** specs/issue-461-adw-feature_Tac_12_task_9_2-sdlc_planner-scout-plan-build-command.md

## Overview

Created a `/scout_plan_build` command that orchestrates a complete end-to-end implementation pipeline by automatically executing three sequential phases: scout exploration, implementation planning, and code building. This command eliminates manual context switching between phases and provides full automation from task description to working code.

## What Was Built

- **Base Command File**: `.claude/commands/scout_plan_build.md` with complete orchestration workflow
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2` for CLI generation
- **Scaffold Integration**: Updated `scaffold_service.py` to include new command in generated projects
- **Validation Checklist**: Comprehensive acceptance criteria and testing documentation

## Technical Implementation

### Files Modified

- `.claude/commands/scout_plan_build.md`: Complete workflow orchestration command with frontmatter, parameter handling, and three-phase execution logic
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`: Template version using `{{ config.project.name }}` and `{{ config.project.description }}` variables
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:332`: Added `"scout_plan_build"` to commands list for template rendering

### Key Changes

1. **Three-Phase Workflow Orchestration**:
   - Phase 1 (Scout): Launches `Explore` subagent with configurable scale (2-10 parallel strategies) for comprehensive file discovery
   - Phase 2 (Plan): Launches `Plan` subagent with scout results to create structured implementation plan
   - Phase 3 (Build): Launches `general-purpose` subagent with plan path for sequential code implementation

2. **Parameter Validation and Defaults**:
   - `TASK_DESCRIPTION` (required): Task to implement, fails fast if missing
   - `SCALE` (optional, default 4): Number of parallel scout strategies, validated range 2-10
   - `THOROUGHNESS` (optional, default medium): Plan depth level (quick/medium/thorough)

3. **Error Handling and Progress Indicators**:
   - Fail-fast behavior: halts immediately on any phase failure
   - Clear progress messages between phases (e.g., "Scout phase complete, starting plan...")
   - Comprehensive error reporting indicating which phase failed

4. **State Passing Between Phases**:
   - Scout results explicitly passed to plan agent via prompt parameter
   - Plan file path extracted and passed to build agent
   - No reliance on shared filesystem state beyond final plan file

5. **Template Rendering**:
   - Uses Jinja2 variables for project context (`config.project.name`, `config.project.description`)
   - Maintains all workflow logic from base command
   - Registered in scaffold service for automatic inclusion in generated projects

## How to Use

### Basic Usage

Run the command with a task description:

```bash
/scout_plan_build "implement user authentication system"
```

### With Custom Parameters

Adjust scout scale and plan thoroughness:

```bash
/scout_plan_build "add API rate limiting" 6 thorough
```

### Expected Workflow

1. Command validates parameters and launches scout phase
2. Scout explores codebase using parallel strategies, reports discovered files
3. Plan phase receives scout results and creates implementation plan
4. Build phase receives plan and implements code sequentially
5. Final report shows all phase results and git changes

### When to Use

- Starting a complete feature from scratch
- Need comprehensive file discovery before planning
- Want full automation without manual phase coordination
- Have clear task description and want end-to-end execution

### When NOT to Use

- Already know which files to modify (use `/plan` + `/build`)
- Only need file discovery (use `/scout`)
- Want to review plan before building (run phases separately)
- Trivial single-file changes (direct editing)

## Configuration

### Command Frontmatter

```yaml
allowed-tools: Task, Read, Write
description: End-to-end workflow orchestrating scout, plan, and build phases
model: claude-sonnet-4-5-20250929
```

### Parameter Defaults

- **SCALE**: 4 (balanced exploration)
- **THOROUGHNESS**: medium (balanced planning depth)

### Agent Type Selection

- **Scout**: `Explore` subagent (specialized for codebase exploration)
- **Plan**: `Plan` subagent (specialized for implementation planning)
- **Build**: `general-purpose` subagent (versatile for implementation)

## Testing

### Test Base Command in Repository

Run with example task:

```bash
/scout_plan_build "add logging to service layer" 4 medium
```

### Validate Template Rendering

Check template syntax and command registration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Verify Linting and Type Checking

Ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test CLI

Verify command appears in generated projects:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Architectural Decisions

- **Fail-Fast Error Handling**: Workflow halts immediately on phase failure with clear error messages indicating which phase failed, preventing cascading failures
- **Explicit State Passing**: Scout results and plan paths passed via Task tool prompt parameters instead of relying on shared filesystem state
- **Agent Type Specialization**: Uses different subagent types for each phase (Explore, Plan, general-purpose) to leverage specialized capabilities
- **Parameter Validation**: Strict input validation with sensible defaults (SCALE=4, THOROUGHNESS=medium) optimized for common use cases

### Similar Implementations

- `.claude/commands/scout.md`: Parallel exploration patterns with configurable scale
- `.claude/commands/plan.md`: Plan generation workflow with thoroughness levels
- `.claude/commands/build.md`: Sequential implementation approach with progress tracking
- `plan_w_scouters.md.j2`: Example of scout+plan orchestration (two-phase workflow)

### Future Enhancements

Potential improvements for future iterations:
- Add `--skip-scout` flag to reuse cached scout results
- Support plan file caching and reuse across invocations
- Parallel build execution for independent plan tasks
- Integration with `/review` command for automated post-build validation
- JSON output format for programmatic consumption
- Agent execution time tracking and performance reporting
