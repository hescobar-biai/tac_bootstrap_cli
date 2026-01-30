# Feature: Create scout_plan_build.md Command File

## Metadata
issue_number: `461`
adw_id: `feature_Tac_12_task_9`
issue_json: `{"number":461,"title":"[Task 9/49] [FEATURE] Create scout_plan_build.md command file","body":"## Description\n\nCreate an end-to-end workflow command: scout -> plan -> build.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout_plan_build.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`\n\n## Key Features\n- Complete implementation pipeline\n- Orchestrates multiple phases\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/scout_plan_build.md`\n\n## Wave 1 - New Commands (Task 9 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_9"}`

## Feature Description
This feature creates a new slash command `/scout_plan_build` that implements an end-to-end automated workflow orchestrating three sequential phases: scout (exploration) -> plan (design) -> build (implementation). This command embodies TAC-10 Level 4 (Delegation Prompt) pattern for workflow orchestration, enabling users to move from task description to working implementation in a single command invocation.

The command builds upon existing TAC Bootstrap commands (`/scout`, `/feature`, `/build`) by composing them into a cohesive pipeline with automatic phase transitions, summary checkpoints, and fail-fast error handling. It provides maximum automation while maintaining transparency through markdown progress reports at each phase boundary.

## User Story
As a developer using TAC Bootstrap
I want to run a single command that scouts relevant files, plans implementation, and builds the feature
So that I can go from task description to working code without manually orchestrating multiple commands

## Problem Statement
Currently, developers need to manually orchestrate multiple commands in sequence:
1. Run `/scout` to identify relevant files
2. Review scout results
3. Run `/feature` to create implementation plan
4. Review plan
5. Run `/implement` or `/build` to execute the plan

This manual orchestration is repetitive and error-prone. Users must remember the correct sequence, manually transition between phases, and handle errors at each step. For straightforward tasks where the workflow is predictable, this overhead slows down development.

The compositional ADW workflows (`adw_plan_build_iso.py`, `adw_plan_build_test_iso.py`) demonstrate that automated phase orchestration is valuable and works well in practice. We need an equivalent slash command for Claude Code sessions.

## Solution Statement
Create `/scout_plan_build` command that:

1. **Accepts clear inputs**: Task description ($1, required) and scout scale ($2, optional, defaults to 4)
2. **Orchestrates three phases automatically**:
   - **Scout Phase**: Launches parallel exploration agents to identify relevant files
   - **Plan Phase**: Creates implementation plan based on scout findings
   - **Build Phase**: Executes the plan to implement the feature
3. **Provides transparency**: Generates markdown summaries at each phase transition showing status, key findings, and next steps
4. **Fails fast**: Stops immediately on errors with clear error messages, no retry/rollback logic needed
5. **Simple templates**: Uses minimal Jinja2 templating (only `config.commands.build` for build phase customization)

This approach maximizes automation while keeping the command simple and transparent. Users who need granular control can still use individual commands (`/scout`, `/feature`, `/build`).

## Relevant Files

### Existing Files to Study
- `.claude/commands/scout.md` - Scout command pattern (lines 1-50 show parameter handling, workflow structure)
- `.claude/commands/feature.md` - Feature planning command pattern
- `.claude/commands/build.md` - Build command pattern (lines 1-26 show simple structure)
- `.claude/commands/parallel_subagents.md` - Parallel orchestration pattern (lines 1-80 show agent launch strategy)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Template example showing Jinja2 usage (lines 11-17)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Commands registration (lines 279-324)
- `adws/adw_plan_build_iso.py` - Python workflow showing phase orchestration pattern (lines 1-88)

### New Files to Create
- `.claude/commands/scout_plan_build.md` - Base command file in TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2` - Jinja2 template for CLI generation

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add 'scout_plan_build' to commands list at line 324

## Implementation Plan

### Phase 1: Foundation - Create Base Command File
Create `.claude/commands/scout_plan_build.md` following the established command pattern:
- Header with command name and description
- Variables section defining $1 (USER_PROMPT) and $2 (SCALE)
- Instructions section with TAC-10 pattern documentation
- Workflow section with scout/plan/build orchestration logic
- Report section with markdown output format

### Phase 2: Core Implementation - Build Orchestration Logic
Implement the three-phase workflow in the command file:
- Phase transitions with markdown summaries
- Error handling with fail-fast behavior
- Parameter validation and defaults
- Integration with existing `/scout`, `/feature`, `/build` commands

### Phase 3: Integration - Template and Registration
Create Jinja2 template and register command:
- Create minimal template with `config.commands.build` interpolation
- Add 'scout_plan_build' to scaffold_service.py commands list
- Ensure template follows existing patterns (build.md.j2, scout.md.j2)

## Step by Step Tasks

### Task 1: Study Reference Patterns
- Read `.claude/commands/scout.md` (lines 1-80) to understand parameter handling
- Read `.claude/commands/parallel_subagents.md` (lines 1-80) to understand orchestration patterns
- Read `adws/adw_plan_build_iso.py` to understand phase chaining
- Identify common patterns for variable handling, error messaging, and report format

### Task 2: Create Base Command File
- Create `.claude/commands/scout_plan_build.md`
- Add header section:
  - Title: "Scout Plan Build - End-to-End Implementation Workflow"
  - Description explaining the three-phase orchestration
- Add Variables section:
  - USER_PROMPT: $1 (required - task description)
  - SCALE: $2 (optional - scout scale, default: 4, range: 2-10)
- Add Instructions section:
  - TAC-10 Level 4 pattern reference
  - When to use this command (straightforward features, known workflow)
  - When NOT to use (complex tasks needing manual control, unclear requirements)

### Task 3: Implement Scout Phase
- Add Workflow section with Step 1: Scout Phase
- Parse and validate input parameters:
  - Extract USER_PROMPT from $1 (error if missing)
  - Extract SCALE from $2 (default to 4 if not provided)
  - Validate SCALE is in range [2, 10]
- Launch `/scout` command with parameters
- Handle scout errors (fail fast with message)
- Generate Phase 1 Summary markdown:
  - Phase name: "Scout"
  - Status: "Completed" or "Failed"
  - Key findings: Number of files discovered, main categories
  - Transition: "Proceeding to plan phase..."

### Task 4: Implement Plan Phase
- Add Step 2: Plan Phase to Workflow section
- Use scout results as context for planning
- Launch `/feature` command (delegate to existing feature planning logic)
- Handle plan errors (fail fast with message)
- Generate Phase 2 Summary markdown:
  - Phase name: "Plan"
  - Status: "Completed" or "Failed"
  - Key findings: Plan file location, major implementation steps
  - Transition: "Proceeding to build phase..."

### Task 5: Implement Build Phase
- Add Step 3: Build Phase to Workflow section
- Launch `/build` command (or `/implement` if plan file provided)
- Handle build errors (fail fast with message)
- Generate Phase 3 Summary markdown:
  - Phase name: "Build"
  - Status: "Completed" or "Failed"
  - Key deliverables: Files created/modified, tests passed
  - Final summary: Overall workflow status

### Task 6: Add Report Section
- Create Report section with final output format:
  - Overall workflow status (success/failed, which phase failed)
  - Summary of each phase (brief)
  - Links to artifacts (plan file, created files)
  - Validation commands to run next
- Add error message templates for common failures:
  - Scout found no files
  - Plan creation failed
  - Build errors

### Task 7: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`
- Copy structure from `.claude/commands/scout_plan_build.md`
- Add Jinja2 conditional for build command:
  ```jinja2
  {% if config.commands.build %}
     {{ config.commands.build }}
  {% else %}
     uv run pytest
  {% endif %}
  ```
- Keep template simple - most content is static orchestration logic
- Ensure template formatting matches existing templates (build.md.j2, scout.md.j2)

### Task 8: Register Command in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list at line 279-324
- Add `"scout_plan_build"` to the list after `"build_w_report"` (line 324)
- Verify the command will be automatically registered via the loop at line 326-332
- Ensure alphabetical/logical ordering maintained

### Task 9: Validation and Testing
Execute validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run all tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Lint code
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Verify CLI works
- Manual test: Check that template renders correctly
- Manual test: Verify command appears in scaffold output

## Testing Strategy

### Unit Tests
Not required for this task - we are creating a command file (documentation/workflow), not Python code with business logic. The command orchestrates existing tested commands (`/scout`, `/feature`, `/build`).

### Integration Tests
- **Template Rendering Test**: Verify that scout_plan_build.md.j2 renders correctly with sample config
- **Command Registration Test**: Verify that 'scout_plan_build' appears in scaffolded .claude/commands/ directory
- **Workflow Logic Test**: Manual test by running command in a test project and verifying phase transitions

### Edge Cases
- **Missing required parameter**: $1 (USER_PROMPT) not provided -> error message
- **Invalid SCALE**: $2 outside range [2, 10] -> validation error or auto-correction
- **Scout phase failure**: Scout finds no files -> fail fast with informative message
- **Plan phase failure**: Feature planning encounters error -> fail fast, no partial build
- **Build phase failure**: Build errors occur -> report error, no auto-retry
- **No build command configured**: Template should handle missing config.commands.build gracefully

## Acceptance Criteria

1. ✅ `.claude/commands/scout_plan_build.md` created with complete workflow documentation
   - Clear variable definitions ($1 USER_PROMPT, $2 SCALE)
   - Three-phase orchestration logic (scout -> plan -> build)
   - Markdown summaries at each phase transition
   - Fail-fast error handling documented

2. ✅ `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2` template created
   - Mirrors base command structure
   - Uses `config.commands.build` for build phase customization
   - No other Jinja2 variables (keep it simple)
   - Properly formatted and linted

3. ✅ `scaffold_service.py` updated with command registration
   - 'scout_plan_build' added to commands list at appropriate location (line 324)
   - No syntax errors introduced
   - Command will be included in scaffolding operations

4. ✅ Command follows established patterns
   - Consistent with `/scout`, `/feature`, `/build` command structure
   - Uses TAC-10 Level 4 Delegation Prompt pattern
   - Clear documentation of when to use vs. when NOT to use
   - Professional tone, no unnecessary superlatives

5. ✅ All validation commands pass
   - Tests: `uv run pytest tests/ -v --tb=short` (0 failures)
   - Linting: `uv run ruff check .` (0 errors)
   - Type checking: `uv run mypy tac_bootstrap/` (0 errors)
   - CLI smoke test: `uv run tac-bootstrap --help` (works)

## Validation Commands
Execute these commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests must pass
- `cd tac_bootstrap_cli && uv run ruff check .` - No linting errors
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - No type errors
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - CLI works
- Manual: Verify `.claude/commands/scout_plan_build.md` is well-formed markdown
- Manual: Verify template renders correctly with sample config

## Notes

### Design Decisions
- **No resume capability**: Users can use individual commands (`/scout`, `/feature`, `/build`) for granular control. Adding resume state tracking adds complexity without clear user demand (YAGNI principle).
- **Fail fast, no retry**: Scout and plan are read-only operations - no rollback needed. Build phase has its own error handling. Keeping it simple.
- **Auto-continue phases**: No approval gates between phases. Users can cancel mid-execution if needed. The command name implies full automation.
- **Minimal templating**: Only `config.commands.build` needs project-specific customization. Orchestration logic is universal.

### Related Work
- Part of Wave 1 (New Commands) - Task 9 of 13 in TAC-12 integration plan
- Builds on existing TAC-10 delegation patterns established in `/scout` and `/parallel_subagents`
- Complements Python ADW workflows (`adw_plan_build_iso.py`) with slash command equivalent

### Future Enhancements (Out of Scope)
- Resume from failed phase
- Parallel phase execution (scout + plan concurrently)
- Conditional phases (e.g., skip scout if files known)
- Metrics/telemetry for phase durations
