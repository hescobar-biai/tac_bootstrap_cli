# Feature: Create parallel_subagents.md Command File

## Metadata
issue_number: `464`
adw_id: `feature_Tac_12_task_12_2`
issue_json: `{"number":464,"title":"[Task 12/49] [FEATURE] Create parallel_subagents.md command file","body":"## Description\n\nCreate a command that orchestrates multiple subagents in parallel for divide-and-conquer tasks.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`\n\n## Key Features\n- Multi-agent orchestration\n- Parallel execution pattern\n- Task delegation\n- allowed-tools: Task\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/parallel_subagents.md`\n\n## Wave 1 - New Commands (Task 12 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_12_2"}`

## Feature Description

This feature creates a new slash command `/parallel_subagents` that implements TAC-10 Level 4 (Delegation Prompt) pattern for compute orchestration. The command enables users to launch multiple AI agents in parallel to solve complex tasks through intelligent decomposition and orchestration. Each agent works independently on its assigned subtask, and results are aggregated into a coherent summary.

The command is particularly valuable for:
- Complex multi-domain work (backend + frontend + tests + docs)
- Tasks that can be naturally decomposed into independent subtasks
- Maximizing throughput through parallel execution
- Divide-and-conquer approaches to large features

## User Story

As a developer using TAC Bootstrap
I want to orchestrate multiple AI agents in parallel for complex tasks
So that I can maximize development throughput and efficiently tackle multi-domain work through intelligent task decomposition

## Problem Statement

Complex software tasks often involve multiple independent concerns that could be tackled simultaneously:
- Implementing a feature requires backend API, frontend UI, tests, and documentation
- Refactoring a system involves multiple independent modules
- Research tasks can explore different aspects in parallel

Currently, developers must either:
1. Handle these sequentially (slow, underutilizes available compute)
2. Manually coordinate multiple agents (complex, error-prone)
3. Use ad-hoc parallelization without proper orchestration

This creates a bottleneck in development velocity and fails to leverage the full potential of AI-assisted development.

## Solution Statement

The `/parallel_subagents` command provides a structured approach to parallel agent orchestration:

1. **Intelligent Decomposition**: Analyzes the task and automatically decomposes it into COUNT independent subtasks based on natural boundaries (domain, concern, deliverable)

2. **Parallel Execution**: Launches all agents simultaneously using Claude Code's Task tool with proper parallel invocation patterns

3. **Graceful Failure Handling**: Implements a tiered failure strategy:
   - 1-2 failures → continue with successful results
   - Majority fail → report pattern and suggest alternatives
   - All fail → identify root cause and recommend different strategy

4. **Result Synthesis**: Aggregates individual agent findings into a coherent narrative with key achievements, issues encountered, and next steps

The command accepts two parameters:
- PROMPT_REQUEST ($1): Task description to be decomposed
- COUNT ($2, optional): Number of agents (default: 3, range: 2-10)

## Relevant Files

### Existing Files (For Reference)
- `.claude/commands/parallel_subagents.md` - Base repository command file (already exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Jinja2 template (already exists)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:325` - Already includes `parallel_subagents` in commands list
- `.claude/commands/background.md` - Reference for similar orchestration command pattern
- `.claude/commands/build_in_parallel.md` - Reference for parallel execution patterns

### New Files
None - all required files already exist

## Implementation Plan

### Phase 1: Validation
Verify that all required components are already in place and properly integrated.

### Phase 2: Testing
Validate the command works correctly in both base repository and generated projects.

### Phase 3: Documentation
Ensure the command is properly documented and integrated into the TAC Bootstrap system.

## Step by Step Tasks

### Task 1: Verify Base Repository Command File
- Confirm `.claude/commands/parallel_subagents.md` exists in base repository
- Verify command structure follows TAC-10 Level 4 pattern
- Check Variables section (PROMPT_REQUEST, COUNT with proper defaults)
- Verify Instructions section contains When to Use/NOT Use guidance
- Confirm Workflow section has all 4 steps (Parse, Design, Launch, Collect)
- Verify Report section defines proper output format
- Check COUNT validation logic (range 2-10, default 3)
- Verify error handling strategy is documented

### Task 2: Verify Jinja2 Template
- Confirm `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` exists
- Verify template is identical to base file (no Jinja2 variables needed per clarifications)
- Confirm template preserves all sections: Variables, Instructions, Workflow, Report
- Verify no config interpolation needed (static content)

### Task 3: Verify scaffold_service.py Registration
- Confirm `parallel_subagents` is in commands list at scaffold_service.py:325
- Verify it's placed in correct group (TAC-9/10: Context and agent delegation commands)
- Confirm template path reference is correct: `claude/commands/parallel_subagents.md.j2`
- Verify action type is `FileAction.CREATE` (creates only if doesn't exist)

### Task 4: Test Command in Base Repository
- Execute validation commands to ensure no regressions
- Manually test `/parallel_subagents` command if possible
- Verify command parses input correctly
- Test COUNT validation (default, range, caps)
- Verify parallel agent launch pattern

### Task 5: Test CLI Generation
- Run `tac-bootstrap --help` to confirm CLI works
- Test generating a new project with `tac-bootstrap scaffold`
- Verify generated project includes `.claude/commands/parallel_subagents.md`
- Confirm generated command file is identical to template
- Test command in generated project context

### Task 6: Execute Validation Commands
- Run `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run `cd tac_bootstrap_cli && uv run ruff check .`
- Run `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify all commands pass with zero errors

## Testing Strategy

### Unit Tests
Since the command file is a markdown template without Python code:
- No new unit tests required
- Existing scaffold_service tests already cover command registration
- Template rendering tests already validate Jinja2 templates

### Integration Tests
- Verify command appears in generated `.claude/commands/` directory
- Confirm template rendering produces valid markdown
- Test that scaffold_service.py includes command in commands list

### Edge Cases
- COUNT=1 (should error with recommendation to use Task tool)
- COUNT>10 (should cap at 10 with warning)
- COUNT not specified (should default to 3)
- COUNT non-integer (should validate and error)
- Task not suitable for parallelization (should warn but continue)
- All agents fail (should identify root cause)
- Majority fail (should report pattern)
- 1-2 agents fail (should continue with successful results)

### Manual Testing
- Test command execution with valid task and default COUNT
- Test with explicit COUNT values (2, 5, 10)
- Test error cases (COUNT=1, COUNT=15)
- Verify parallel launch pattern (single message with multiple Task calls)
- Verify result synthesis and reporting format

## Acceptance Criteria

1. ✅ Command file exists at `.claude/commands/parallel_subagents.md` in base repository
2. ✅ Template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`
3. ✅ Command is registered in `scaffold_service.py` commands list
4. ✅ Command follows TAC-10 Level 4 (Delegation Prompt) pattern
5. ✅ Variables section properly defines PROMPT_REQUEST and COUNT with correct defaults
6. ✅ Instructions section provides clear When to Use/NOT Use guidance
7. ✅ Workflow section has all required steps: Parse, Design, Launch, Collect
8. ✅ COUNT validation implemented (range 2-10, default 3, proper error handling)
9. ✅ Parallel execution pattern documented (single message with multiple Task calls)
10. ✅ Error handling strategy documented for partial and total failures
11. ✅ Report format properly structured (Agent Results + Overall Summary)
12. ✅ Template is static content (no Jinja2 variables needed)
13. ✅ All validation commands pass with zero errors
14. ✅ Command appears in generated projects
15. ✅ No regressions introduced to existing functionality

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Implementation Status
Based on investigation, all required components already exist:
- ✅ Base repository command file is complete and follows TAC-10 pattern
- ✅ Jinja2 template exists and is identical to base (no variables needed)
- ✅ Command is already registered in scaffold_service.py at line 325
- ✅ Command is properly placed in "TAC-9/10: Context and agent delegation commands" group

### Key Design Decisions (from Auto-Resolved Clarifications)
1. **Input Format**: Single task that gets auto-divided by the orchestrating agent
2. **Failure Handling**: Wait for all agents, then aggregate with graceful degradation
3. **Output Format**: Individual agent sections + synthesized overall summary
4. **Agent Limits**: 2-10 agents (hard cap), default 3
5. **Dependencies**: Only independent parallel tasks (no dependency orchestration)
6. **Jinja2 Variables**: None needed (static orchestration logic)
7. **Inter-Agent Communication**: Completely isolated agents
8. **Use Cases**: Multi-domain work, complex decomposable tasks

### Task Assessment
**This appears to be a verification task rather than implementation task.** All required files exist and are properly integrated. The implementation plan focuses on validation and testing to confirm everything works correctly.

### Related Commands
- `/background` - Similar orchestration pattern for background execution
- `/build_in_parallel` - Parallel execution with batching
- `/scout` - Parallel codebase exploration
- `/plan_w_scouters` - Planning with parallel scouts

### Future Enhancements (Out of Scope)
- Dynamic agent count optimization based on task complexity
- Inter-agent communication for loosely coupled subtasks
- Progress streaming as agents complete
- Agent result caching for repeated subtasks
- Cost estimation based on COUNT and task complexity
