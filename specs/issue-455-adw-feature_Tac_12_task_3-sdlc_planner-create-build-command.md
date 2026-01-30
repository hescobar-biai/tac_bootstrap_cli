# Feature: Create /build Command for Sequential Plan Implementation

## Metadata
issue_number: `455`
adw_id: `feature_Tac_12_task_3`
issue_json: `{"number":455,"title":"[Task 3/49] [FEATURE] Create build.md command file","body":"## Description\n\nCreate a simple sequential build command that implements a plan top-to-bottom without parallelization.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`\n\n## Key Features\n- Simple sequential implementation\n- Reads plan from PATH_TO_PLAN\n- Ultrathink and implement\n- Validation with git diff --stat\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build.md`\n\n## Wave 1 - New Commands (Task 3 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_3"}`

## Feature Description
Create a new `/build` command for Claude Code that reads an implementation plan from a markdown file and executes it sequentially, step-by-step, without parallelization. The command is designed for AI agents to implement plans methodically with clear progress visibility and validation feedback.

This command differs from the existing `/build` command (which runs `uv build` for Python packages) by focusing on plan implementation rather than package building. It will need to replace the current build.md command file.

## User Story
As a developer using Claude Code with TAC Bootstrap
I want to execute a /build command that reads and implements a plan file sequentially
So that I can have the AI agent implement complex features step-by-step with clear progress tracking and validation

## Problem Statement
Currently, developers need to manually guide AI agents through implementation plans or copy-paste plan steps into prompts. There's no standardized command to:
- Read a plan file from a known location (specs/plan.md or specs/issue-*.md)
- Execute the plan steps sequentially with visible progress
- Stop on first failure to prevent cascading errors
- Show what changed after implementation (git diff --stat)
- Provide consistent error handling and reporting

## Solution Statement
Create a `/build` slash command that:
1. Accepts an optional path to a plan file (defaults to specs/plan.md)
2. Reads and parses the markdown plan file
3. Instructs the AI agent to think carefully about each step ("ultrathink")
4. Executes steps sequentially, showing progress for each step
5. Stops execution on first error with clear error reporting
6. Displays `git diff --stat` upon completion to show changes
7. Suggests running /test after successful completion

The implementation consists of:
- Replacing `.claude/commands/build.md` in the base repository
- Creating/updating `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` template
- The command is already listed in scaffold_service.py (line 282), so no changes needed there

## Relevant Files
Files necessary for implementing the feature:

### Existing Files to Modify/Replace
- `.claude/commands/build.md` - Current build command (replace with new plan-based build)
  - Currently runs `uv build` for Python package building
  - Will be replaced with plan implementation logic

### Existing Template Files to Create/Update
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Template version
  - Currently exists with Jinja2 variables for build command
  - Will be updated to use plan file path configuration

### Reference Files (Read-Only)
- `scaffold_service.py:279-332` - Commands list (build.md already included)
- `.claude/commands/implement.md` - Similar command structure for reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Template reference

### New Files
None - all files already exist

## Implementation Plan

### Phase 1: Foundation
Read and understand existing command patterns and template structure:
1. Review `.claude/commands/implement.md` to understand command structure
2. Review template variables available in build.md.j2
3. Identify the plan file path configuration pattern from config.yml

### Phase 2: Core Implementation
Create the new build command content:
1. Replace `.claude/commands/build.md` with plan-based implementation logic
2. Update `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` template
3. Ensure Jinja2 variables are properly used for configurability

### Phase 3: Integration
Verify integration with existing infrastructure:
1. Confirm scaffold_service.py already includes build.md (line 282)
2. Test template rendering works correctly
3. Validate command follows TAC Bootstrap patterns

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review existing patterns
- Read `.claude/commands/implement.md` for command structure reference
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` for template patterns
- Understand how $ARGUMENTS is used and how config variables are referenced

### Task 2: Replace base command file
- Replace `.claude/commands/build.md` with new content:
  - Add command description explaining plan-based implementation
  - Define $ARGUMENTS variable for optional plan file path
  - Create Instructions section:
    - Step 1: Locate plan file (default: specs/plan.md or first issue-*.md in specs/)
    - Step 2: Read and parse the plan file
    - Step 3: Think carefully about implementation approach ("ultrathink")
    - Step 4: Execute each step sequentially, showing progress
    - Step 5: Stop on first error with clear error message
    - Step 6: Display git diff --stat upon completion
  - Create Report section:
    - Implementation status (success/failed at step X)
    - Steps completed vs total
    - Files changed (git diff --stat output)
    - Suggestion to run /test after success

### Task 3: Update template file
- Update `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`:
  - Use `{{ config.paths.specs_dir | default('specs') }}` for plan directory
  - Use `{{ config.project.name }}` if needed for context
  - Keep most content static with minimal Jinja2 variables
  - Ensure template matches base file structure

### Task 4: Verify integration
- Confirm scaffold_service.py line 282 includes "build" in commands list
- No code changes needed to scaffold_service.py
- Validate build.md.j2 follows existing template patterns

### Task 5: Run validation commands
Execute all validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required - this is a template/documentation change. Existing template rendering tests in pytest suite will validate:
- Template renders without errors
- Jinja2 variables are properly substituted
- Generated command files are valid markdown

### Edge Cases
Manual testing scenarios to verify:
1. Command works with default plan path (specs/plan.md)
2. Command works with explicit plan path via $ARGUMENTS
3. Command handles missing plan file gracefully
4. Command stops on step failure and reports clear error
5. git diff --stat displays correctly after changes
6. Template renders correctly with different config values

## Acceptance Criteria
1. `.claude/commands/build.md` contains plan-based implementation logic (not package building)
2. Template `build.md.j2` uses proper Jinja2 variables for configuration
3. Command instructs agent to read plan from specs directory
4. Command includes sequential execution with progress visibility
5. Command includes "ultrathink" instruction for careful implementation
6. Command stops on first error with clear reporting
7. Command displays git diff --stat upon completion
8. Command suggests running /test after success
9. scaffold_service.py already includes build in commands list (verified)
10. All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This command replaces the existing `/build` which runs `uv build` for Python packages
- The new `/build` is focused on implementing plans, not building packages
- Plan files are expected to be markdown (.md) format only initially
- PATH_TO_PLAN defaults to specs/plan.md or auto-detects first issue-*.md file
- "Ultrathink" is a prompt directive for the AI agent, not a technical command
- No automatic rollback on failure - users can use git to revert if needed
- Display git diff --stat is informational only, no validation thresholds
- Command operates independently but suggests /test in output
- Sequential execution means all steps must succeed for overall success
- Future enhancement: support for JSON/YAML plans could be added later
