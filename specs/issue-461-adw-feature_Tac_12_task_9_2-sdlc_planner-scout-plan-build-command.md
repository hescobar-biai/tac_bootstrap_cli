# Feature: Scout-Plan-Build Orchestration Command

## Metadata
issue_number: `461`
adw_id: `feature_Tac_12_task_9_2`
issue_json: `{"number":461,"title":"[Task 9/49] [FEATURE] Create scout_plan_build.md command file","body":"## Description\n\nCreate an end-to-end workflow command: scout -> plan -> build.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout_plan_build.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`\n\n## Key Features\n- Complete implementation pipeline\n- Orchestrates multiple phases\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/scout_plan_build.md`\n\n## Wave 1 - New Commands (Task 9 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_9_2"}`

## Feature Description

Create a `/scout_plan_build` command that orchestrates a complete implementation workflow by sequentially executing three phases:
1. **Scout Phase**: Parallel codebase exploration to discover relevant files
2. **Plan Phase**: Implementation planning based on scout results
3. **Build Phase**: Sequential implementation of the plan

This command provides end-to-end automation from file discovery through implementation, reducing manual context switching and ensuring comprehensive coverage.

## User Story

As a developer using TAC Bootstrap
I want to execute a complete implementation pipeline with a single command
So that I can go from task description to implemented code without manually coordinating scout, plan, and build phases

## Problem Statement

Currently, developers must manually orchestrate three separate commands (`/scout`, `/plan`, `/build`) when implementing features:
- They must wait for scout results, then manually invoke planning with context
- They must wait for plan completion, then manually trigger build
- Context from each phase must be manually passed to the next
- Errors in any phase require manual intervention and retry

This manual orchestration is time-consuming, error-prone, and interrupts developer flow.

## Solution Statement

Create a `/scout_plan_build` command that:
- Accepts a task description (required) and optional scale/thoroughness parameters
- Launches scout agent to explore codebase and identify relevant files
- Passes scout results to plan agent to create implementation plan
- Passes plan to build agent for sequential implementation
- Halts immediately on any phase failure with clear error reporting
- Provides simple text progress indicators between phases

The implementation will:
- Use the Task tool with appropriate subagent types (Explore, Plan, general-purpose)
- Pass outputs explicitly between phases via prompt parameters
- Follow existing patterns from `/scout`, `/plan`, and `/build` commands
- Register as a standalone workflow command in `scaffold_service.py`

**Reference Implementations:**
- `.claude/commands/scout.md` - Scout phase patterns (lines 1-510)
- `.claude/commands/plan.md` - Plan phase patterns (lines 1-326)
- `.claude/commands/build.md` - Build phase patterns (lines 1-82)

## Relevant Files

### Existing Files to Modify

1. **`tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`** (lines 316-332)
   - Add `"scout_plan_build"` to commands list
   - Ensures template is rendered during scaffold generation

### New Files

2. **`.claude/commands/scout_plan_build.md`**
   - Base command file in the repository
   - Production implementation of orchestration workflow

3. **`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`**
   - Jinja2 template for CLI generation
   - Uses `config.project.name` and `config.project.description` variables

## Implementation Plan

### Phase 1: Foundation
- Read and analyze existing scout, plan, and build command files
- Understand Task tool usage patterns for agent delegation
- Identify state passing mechanisms between agents
- Review scaffold_service.py structure for command registration

### Phase 2: Core Implementation
- Create base command file `.claude/commands/scout_plan_build.md`
- Implement workflow orchestration logic:
  - Parameter parsing (task_description, scale, thoroughness)
  - Scout phase launch with Task tool (subagent_type: Explore)
  - Plan phase launch with scout context
  - Build phase launch with plan context
  - Error handling for phase failures
  - Progress indicators
- Create Jinja2 template version for CLI generation

### Phase 3: Integration
- Update `scaffold_service.py` commands list
- Test command file in base repository
- Verify template rendering with sample config
- Validate end-to-end workflow execution

## Step by Step Tasks

### Task 1: Analyze Reference Commands
- Read `.claude/commands/scout.md` to understand scout agent invocation pattern
- Read `.claude/commands/plan.md` to understand plan generation approach
- Read `.claude/commands/build.md` to understand sequential implementation pattern
- Document key patterns: Task tool usage, parameter handling, output formats

### Task 2: Create Base Command File
- Create `.claude/commands/scout_plan_build.md` with frontmatter:
  ```yaml
  ---
  allowed-tools: Task, Read, Write
  description: End-to-end workflow orchestrating scout, plan, and build phases
  model: claude-sonnet-4-5-20250929
  ---
  ```
- Implement Variables section:
  - `TASK_DESCRIPTION: $1` (required)
  - `SCALE: $2` (optional, default: 4)
  - `THOROUGHNESS: $3` (optional, default: medium)
- Implement Instructions section with orchestration workflow
- Implement Workflow section with three sequential steps:
  - Step 1: Launch scout agent with Task tool
  - Step 2: Parse scout results, launch plan agent with scout context
  - Step 3: Parse plan results, launch build agent with plan path
- Implement error handling for each phase
- Add progress indicators (e.g., "Scout phase complete, starting plan...")
- Implement Report section with execution summary

### Task 3: Create Jinja2 Template
- Copy base command to `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`
- Add Jinja2 variables:
  - `{{ config.project.name }}` for project-specific context
  - `{{ config.project.description }}` for contextual information
- Keep agent types hardcoded (scout/Explore, plan/Plan, build/general-purpose)
- Preserve all workflow logic from base file

### Task 4: Register Command in Scaffold Service
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list in `_add_claude_files` method (around line 279)
- Add `"scout_plan_build"` to commands list after `"plan"` entry
- Verify file action uses `FileAction.CREATE` pattern

### Task 5: Test and Validate
- Test base command file in current repository:
  - Run `/scout_plan_build "example task description" 4 medium`
  - Verify scout phase executes and produces output
  - Verify plan phase receives scout context
  - Verify build phase receives plan
- Test template rendering:
  - Use validation commands below to ensure no regressions
  - Verify template syntax is valid
- Verify command registration:
  - Check that `scaffold_service.py` includes new command
  - Run validation commands

### Task 6: Execute Validation Commands
- Run all validation commands to ensure zero regressions
- Fix any issues discovered
- Verify command appears in generated projects

## Testing Strategy

### Unit Tests

No new unit tests required - this is a command file addition, not code logic.

### Integration Tests

1. **Base Command Execution:**
   - Verify `/scout_plan_build` command can be invoked
   - Test with various parameter combinations
   - Test error handling when phases fail

2. **Template Rendering:**
   - Verify template renders without Jinja2 errors
   - Verify generated command file is syntactically valid
   - Test with different config values

3. **Scaffold Integration:**
   - Verify command appears in `scaffold_service.py` commands list
   - Verify template is included in generated projects

### Edge Cases

1. **Missing Parameters:**
   - Invoke without TASK_DESCRIPTION - should error with clear message
   - Invoke with invalid SCALE value - should validate and cap/error

2. **Phase Failures:**
   - Scout phase fails - should halt with error, not continue to plan
   - Plan phase fails - should halt with error, not continue to build
   - Build phase fails - should report failure clearly

3. **Empty Results:**
   - Scout finds no files - plan should receive empty context and handle gracefully
   - Plan generates minimal plan - build should execute minimal steps

## Acceptance Criteria

1. **Base Command File Exists**
   - File `.claude/commands/scout_plan_build.md` created
   - Contains proper frontmatter with allowed-tools and description
   - Implements Variables, Instructions, Workflow, and Report sections

2. **Jinja2 Template Exists**
   - File `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2` created
   - Uses `{{ config.project.name }}` and `{{ config.project.description }}`
   - Renders without Jinja2 syntax errors

3. **Command Registered in Scaffold Service**
   - `scaffold_service.py` includes `"scout_plan_build"` in commands list
   - Command appears after `"plan"` in the list
   - Uses same template rendering pattern as other commands

4. **Workflow Orchestration Works**
   - Accepts TASK_DESCRIPTION parameter (required)
   - Accepts optional SCALE and THOROUGHNESS parameters
   - Launches scout phase with Task tool (subagent_type: Explore)
   - Passes scout results to plan phase
   - Passes plan to build phase
   - Halts on any phase failure

5. **Progress Indicators Present**
   - Shows "Launching scout phase..." message
   - Shows "Scout phase complete, starting plan..." message
   - Shows "Plan phase complete, starting build..." message
   - Shows final summary with all phase results

6. **Error Handling Implemented**
   - Missing TASK_DESCRIPTION produces clear error
   - Scout phase failure halts workflow
   - Plan phase failure halts workflow
   - Build phase failure reported clearly

7. **All Validation Commands Pass**
   - No pytest failures
   - No ruff check violations
   - No mypy type errors
   - Smoke test succeeds

## Validation Commands

Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Architectural Decisions

1. **Agent Type Selection:**
   - Scout: Use `Explore` subagent (specialized for codebase exploration)
   - Plan: Use `Plan` subagent (specialized for implementation planning)
   - Build: Use `general-purpose` subagent (versatile for implementation)

2. **State Passing Mechanism:**
   - Explicit state passing via Task tool `prompt` parameter
   - Scout results embedded in plan agent prompt
   - Plan file path passed to build agent prompt
   - No reliance on shared filesystem state beyond final plan file

3. **Error Handling Philosophy:**
   - Halt immediately on any phase failure (fail-fast)
   - No automatic retry or recovery
   - Clear error messages indicating which phase failed
   - User can manually retry individual phases if needed

4. **Parameter Defaults:**
   - `SCALE: 4` (balanced exploration, matches scout default)
   - `THOROUGHNESS: medium` (balanced planning depth)
   - Chosen to optimize for common use cases while allowing customization

5. **Template Variables:**
   - Use only project metadata (`name`, `description`)
   - Hardcode agent types (stable, command-specific)
   - Avoid referencing `config.commands` to prevent coupling

### Similar Implementations Referenced

- `.claude/commands/scout.md` - Parallel exploration patterns
- `.claude/commands/plan.md` - Plan generation workflow
- `.claude/commands/build.md` - Sequential implementation approach
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` - Example of scout+plan orchestration

### Future Enhancements

Potential improvements for future iterations:
- Add `--skip-scout` flag to start from planning (reuse cached scout results)
- Support for plan file caching and reuse
- Parallel build execution for independent plan tasks
- Integration with `/review` command for post-build validation
- JSON output format for programmatic consumption
- Agent execution time tracking and reporting

### Dependencies

No new library dependencies required. Uses existing:
- Task tool (built-in Claude Code capability)
- Read/Write tools for plan file handling
- Existing scout/plan/build agent implementations
