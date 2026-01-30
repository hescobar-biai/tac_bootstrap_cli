# Feature: Create parallel_subagents.md Command File

## Metadata
issue_number: `464`
adw_id: `feature_Tac_12_task_12`
issue_json: `{"number":464,"title":"[Task 12/49] [FEATURE] Create parallel_subagents.md command file","body":"## Description\n\nCreate a command that orchestrates multiple subagents in parallel for divide-and-conquer tasks.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`\n\n## Key Features\n- Multi-agent orchestration\n- Parallel execution pattern\n- Task delegation\n- allowed-tools: Task\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/parallel_subagents.md`\n\n## Wave 1 - New Commands (Task 12 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_12"}`

## Feature Description
The parallel_subagents command enables orchestration of multiple Claude Code agents running concurrently to solve complex tasks through decomposition. It implements the TAC-10 Level 4 Delegation Prompt pattern, allowing users to specify a task and number of agents (2-10, default 3), then automatically decomposes the work into independent subtasks, launches agents in parallel using concurrent Task tool invocations, and synthesizes results into a coherent report.

The command is already fully implemented in both the base repository (.claude/commands/parallel_subagents.md) and as a Jinja2 template (tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2). The implementation includes sophisticated failure handling, validation logic, and structured reporting patterns.

## User Story
As a developer working with TAC Bootstrap
I want to leverage parallel agent orchestration for divide-and-conquer tasks
So that I can maximize throughput on complex multi-domain work like implementing features across backend, frontend, tests, and documentation simultaneously

## Problem Statement
Complex software tasks often involve multiple independent concerns that could execute in parallel (e.g., API development, UI implementation, test creation, documentation). Traditional sequential execution wastes time and compute resources. While the Task tool enables agent delegation, manually coordinating multiple agents requires boilerplate orchestration logic. Users need a standardized command that handles decomposition, parallel execution, failure resilience, and result synthesis.

## Solution Statement
Create a /parallel_subagents command that automates the full orchestration lifecycle. The command accepts a task description and agent count, validates inputs (rejecting COUNT=1, capping at 10), analyzes the task to identify natural decomposition boundaries, designs independent agent prompts with clear scopes and success criteria, launches all agents via concurrent Task tool invocations in a single message, waits for completion, handles partial failures gracefully (continuing with successes), and presents a structured report with per-agent results plus an overall synthesis.

The implementation is static content requiring no project-specific configuration, making it identical between the .md base file and .j2 template.

## Relevant Files
Files necessary for implementing the feature:

- `.claude/commands/parallel_subagents.md` (130 lines)
  - **Already exists**: Contains complete implementation with Variables, Instructions, Workflow, Report sections
  - **Purpose**: Provides the command logic that agents execute when users invoke /parallel_subagents
  - **Key sections**: COUNT validation (lines 38-43), parallel launch pattern (lines 69-78), failure handling (lines 84-87, 126-129)

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` (130 lines)
  - **Already exists**: Identical to .md file with no Jinja2 variables
  - **Purpose**: Template for CLI to generate command in target projects
  - **Relevance**: Ensures generated projects include this command

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (924 lines)
  - **Already includes parallel_subagents**: Line 321 in commands list
  - **Purpose**: Orchestrates scaffold plan building and template rendering
  - **Relevance**: Registers command for inclusion during scaffolding

### New Files
No new files needed - all three required files already exist with correct content.

## Implementation Plan

### Phase 1: Verification
Verify existing implementation matches requirements from issue #464 and auto-resolved clarifications. Confirm files are identical and properly registered.

### Phase 2: Documentation
Document the implementation status, verify template fidelity, and ensure no discrepancies exist between base file and template.

### Phase 3: Validation
Run validation commands to ensure zero regressions and proper integration with the CLI scaffolding system.

## Step by Step Tasks

### Task 1: Verify Base Command File
- Read `.claude/commands/parallel_subagents.md` (already done in investigation)
- Confirm it contains all required sections: Variables, Instructions, Workflow, Report
- Verify COUNT validation logic: default 3, range 2-10, error on 1, cap at 10
- Verify parallel execution pattern: single message with multiple Task invocations (line 72)
- Verify failure handling: tiered approach for 1-2 failures vs majority vs all (lines 84-87, 126-129)
- Verify input format: PROMPT_REQUEST ($1) and COUNT ($2) variables (lines 7-8)

### Task 2: Verify Template File
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` (already done)
- Confirm it is byte-identical to the base .md file
- Verify no Jinja2 variables are present (static content pattern, like background.md.j2)
- Confirm this matches the pattern for commands without project-specific configuration

### Task 3: Verify Scaffold Service Registration
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (already done)
- Confirm `parallel_subagents` appears in the commands list at line 321
- Verify the template reference in `_add_claude_files` method points to correct template path
- Ensure no duplicate or conflicting entries exist

### Task 4: Cross-Reference with Background Command
- Compare implementation pattern with `.claude/commands/background.md` and its .j2 template
- Verify parallel_subagents follows same static content pattern (no variables)
- Confirm both use similar structure but different execution strategies (background uses run_in_background: true, parallel uses concurrent Task calls)
- Document the complementary nature of these commands in implementation notes

### Task 5: Validation Commands
Execute all validation commands to ensure zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
- Test scaffold plan generation includes parallel_subagents command
- Test template rendering produces correct output file
- Test commands list includes parallel_subagents in proper alphabetical position
- Test template path resolution for parallel_subagents.md.j2

### Edge Cases
- Verify scaffold service handles missing template gracefully (should not occur)
- Test force mode doesn't skip parallel_subagents command creation
- Verify file permissions if command marked executable (currently not needed)
- Test CREATE action respects existing files in target projects

## Acceptance Criteria
- `.claude/commands/parallel_subagents.md` exists and contains complete implementation (130 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` exists and is identical to base file
- `scaffold_service.py` includes `parallel_subagents` in commands list at line 321
- Both files implement the exact same logic with no Jinja2 variables in template
- All validation commands pass with zero errors or warnings
- Generated projects via `tac-bootstrap init` include `/parallel_subagents` command
- Command implements TAC-10 Level 4 (Delegation Prompt) pattern correctly
- COUNT validation enforces range 2-10 with default 3
- Parallel execution uses concurrent Task tool invocations in single message
- Failure handling follows tiered resilience pattern
- Report structure matches specification with Agent Results and Overall Summary sections

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
### Implementation Status
All three required files already exist and are properly configured:
1. Base command file is complete and feature-rich (130 lines)
2. Template is byte-identical to base file (static content, no variables)
3. Scaffold service already registers command in proper position

### Design Decisions
- **No Jinja2 Variables**: Command logic is universal and doesn't require project-specific customization, following the same pattern as background.md
- **Static Content Pattern**: Template is identical to base file, ensuring consistency across generated projects
- **TAC-10 Level 4 Pattern**: Implements Delegation Prompt orchestration for compute management
- **Complementary to Background**: While /background delegates async long-running tasks (run_in_background: true), /parallel_subagents delegates synchronous divide-and-conquer decomposition (concurrent Task calls)

### No Additional Libraries Needed
All functionality uses existing Claude Code SDK capabilities (Task tool with subagent_type and concurrent invocation patterns).

### Verification Outcome
This task is essentially complete - the implementation was already done in a previous wave. The verification phase confirms all requirements are met and no changes are needed. This plan serves as documentation and validation checklist rather than an implementation guide.
