# Feature: Parallel Expert Scaling Command

## Metadata
issue_number: `579`
adw_id: `feature_Tac_13_Task_17`
issue_json: `{"number": 579, "title": "[TAC-13] Task 17: Create parallel expert scaling command", "body": "Create parallel expert scaler as template and implementation - 3-10 agents for consensus."}`

## Feature Description
Create a parallel expert scaling command that spawns 3-10 independent agents to analyze the same task, then synthesizes their outputs into a consensus report. This implements the TAC-13 meta-agentic pattern of "parallel expert consensus" for validation, where multiple specialized agents work independently and their results are aggregated to identify agreement, conflicts, and recommendations.

The command follows the TAC Bootstrap dual strategy: Jinja2 template in CLI + registration in scaffold_service.py + working implementation in repo root.

## User Story
As a developer working on complex architectural decisions
I want to consult multiple independent expert agents in parallel
So that I can identify consensus patterns, competing perspectives, and make informed decisions based on diverse analytical viewpoints

## Problem Statement
Complex technical decisions benefit from multiple perspectives, but manually spawning and synthesizing outputs from multiple agents is tedious and error-prone. Current tools like `/parallel_subagents` focus on task decomposition (splitting work), not expert consensus (same task, multiple perspectives).

Without a dedicated consensus mechanism:
- Engineers miss valuable alternative viewpoints
- No systematic way to identify agreement vs. divergence
- Manual synthesis of multiple agent outputs is time-consuming
- Groupthink risk when relying on single-agent analysis

## Solution Statement
Implement a `/expert-parallel` command with a 4-phase workflow:
1. **Validation Phase**: Validate inputs (domain, task, num_agents 3-10)
2. **Spawn Phase**: Launch N isolated agents with identical task prompts
3. **Monitor Phase**: Track agent completion with blocking wait and progress updates
4. **Synthesis Phase**: Use opus model to aggregate outputs, identify consensus/conflicts, generate structured markdown report

Key design decisions:
- **Complete isolation**: Agents work independently until synthesis (prevent groupthink)
- **Partial failure tolerance**: Continue with minimum 2 successful agents
- **Opus-powered synthesis**: Use strongest model for complex aggregation work
- **Transparency**: Store full agent outputs in scratchpad, show summaries in report
- **30min per-agent timeout**: Allow thorough expert-level analysis

## Relevant Files
Files needed to implement this feature:

1. **tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2**
   - Jinja2 template for the command (will be used by CLI to generate projects)
   - Must use `{{ config.project.name }}` and other Jinja2 variables

2. **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py**
   - Registration point for all command templates
   - Add "expert-parallel" to commands list around line 345

3. **.claude/commands/expert-parallel.md**
   - Working implementation file in repo root (reference version)
   - Used by tac_bootstrap project itself during development

4. **.claude/commands/expert-orchestrate.md**
   - Reference for meta-command patterns and synthesis reporting
   - Shows proper error handling and progress tracking

5. **.claude/commands/parallel_subagents.md**
   - Reference for parallel agent spawning patterns
   - Different use case (decomposition) but similar parallel execution mechanics

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2` (template)
- `.claude/commands/expert-parallel.md` (implementation)

## Implementation Plan

### Phase 1: Foundation
**Study existing patterns and understand requirements**

1. Read reference files to understand patterns:
   - `.claude/commands/expert-orchestrate.md` - meta-command structure, synthesis reporting
   - `.claude/commands/parallel_subagents.md` - parallel agent spawning mechanics
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` - Jinja2 template example

2. Understand the dual strategy pattern:
   - Template (.j2) uses Jinja2 variables like `{{ config.project.name }}`
   - Registration in scaffold_service.py adds to commands list
   - Implementation file is the working version in repo root

### Phase 2: Core Implementation
**Create the expert-parallel command implementation**

1. Create working implementation file `.claude/commands/expert-parallel.md` with:
   - **Frontmatter**: allowed-tools (Task, Read, TodoWrite, Write), description, argument-hint, model: sonnet
   - **Variables**: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3, default: 3)
   - **4-Phase Workflow**:
     - Phase 1: Validate inputs (domain non-empty, task non-empty, num_agents 3-10 range)
     - Phase 2: Spawn N parallel agents using Task tool (single message with multiple invocations)
     - Phase 3: Monitor execution with blocking wait, show "X/N agents completed" progress updates
     - Phase 4: Synthesis with opus model - aggregate outputs, identify themes/conflicts, generate markdown report
   - **Error Handling**: Partial failure tolerance (minimum 2 successes required), clear error messages
   - **Output Format**: Markdown with sections: Consensus, Conflicts, Recommendations
   - **Transparency**: Link to full agent outputs stored in scratchpad directory

2. Design agent isolation strategy:
   - Each agent receives identical task prompt: "You are expert #{N} in {EXPERT_DOMAIN}. Analyze: {TASK}"
   - No access to other agents' outputs until synthesis phase
   - Each agent gets 30min timeout (configurable via Task tool timeout parameter)

3. Design synthesis algorithm:
   - Collect all successful agent outputs
   - Group similar responses to identify themes
   - Quantify agreement levels (e.g., "7/10 agents agree...")
   - Explicitly call out conflicting viewpoints with supporting evidence
   - Generate consensus recommendations only where agreement exists
   - Mark areas of divergence with categorized perspectives

### Phase 3: Integration
**Create template and register in CLI**

1. Create Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`:
   - Copy content from `.claude/commands/expert-parallel.md`
   - Replace project name references with `{{ config.project.name }}`
   - Ensure all Jinja2 variables follow existing template patterns

2. Register template in `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`:
   - Add "expert-parallel" to commands list (around line 345, after "expert-orchestrate")
   - Follows existing pattern: added to list, then loop handles registration
   - No explicit TAC-13 Task 17 comment needed (follows pattern in lines 330-360)

3. Verify template rendering:
   - Ensure .j2 template is valid Jinja2 syntax
   - Check that all project-specific values use config variables
   - Validate no hardcoded absolute paths

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Study Reference Patterns
- Read `.claude/commands/expert-orchestrate.md` to understand meta-command structure
- Read `.claude/commands/parallel_subagents.md` to understand parallel spawning mechanics
- Read a Jinja2 template example to understand variable usage patterns
- Document key patterns: frontmatter structure, variable syntax, workflow organization

### Task 2: Create Working Implementation
- Create `.claude/commands/expert-parallel.md` with complete 4-phase workflow
- Include frontmatter with allowed-tools, description, argument-hint, model
- Define variables: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3)
- Implement Phase 1: Input validation (domain, task, num_agents 3-10 range)
- Implement Phase 2: Parallel agent spawning (single message, multiple Task invocations)
- Implement Phase 3: Monitor with progress updates ("X/N completed")
- Implement Phase 4: Opus-powered synthesis with markdown report structure
- Add error handling: partial failure tolerance (min 2 successes), clear error messages
- Add transparency: link to full outputs in scratchpad directory
- Include usage examples in command documentation

### Task 3: Create Jinja2 Template
- Copy `.claude/commands/expert-parallel.md` to `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
- Replace project name references with `{{ config.project.name }}`
- Ensure all config variables follow existing template patterns
- Validate Jinja2 syntax (no syntax errors)
- Verify no hardcoded absolute paths remain

### Task 4: Register in Scaffold Service
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list around line 345 (after "expert-orchestrate")
- Add "expert-parallel" to the commands list
- Verify registration follows existing pattern (list entry, loop handles file creation)
- No need for explicit TAC-13 comment (follows established pattern)

### Task 5: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify template file exists: `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
- Verify registration: `grep "expert-parallel" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Verify implementation file: `test -f .claude/commands/expert-parallel.md`
- Run unit tests: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run linting: `cd tac_bootstrap_cli && uv run ruff check .`
- Run type check: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run smoke test: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required - this follows established command registration pattern. Existing tests in `tac_bootstrap_cli/tests/` validate:
- Template rendering (Jinja2 syntax)
- File creation via scaffold_service
- Config validation

### Edge Cases
The command itself must handle these edge cases (in Phase 1 validation):

1. **Invalid NUM_AGENTS**:
   - NUM_AGENTS < 3: Display error "Minimum 3 agents required for consensus"
   - NUM_AGENTS > 10: Cap at 10, display warning about resource constraints
   - NUM_AGENTS not an integer: Display error with usage example

2. **Empty or missing parameters**:
   - EXPERT_DOMAIN empty: Display error with valid domains list
   - TASK empty: Display error with usage example
   - NUM_AGENTS not provided: Default to 3

3. **Agent failures during execution** (Phase 3 monitoring):
   - 1-2 agents fail: Continue with successful results, mark failures in synthesis
   - 3+ agents fail but ≥2 succeed: Partial consensus report with warning
   - <2 agents succeed: Abort with error, insufficient data for consensus

4. **Synthesis edge cases** (Phase 4):
   - No consensus reached: Report divergence explicitly with categorized perspectives
   - All agents agree: Report strong consensus with supporting evidence
   - Timeout during synthesis: Retry once, then fail with stored agent outputs

### Manual Testing
After implementation, manually test with:
```bash
# Test with default (3 agents)
/expert-parallel "security" "evaluate authentication approach for API"

# Test with custom agent count
/expert-parallel "architecture" "assess microservices vs monolith for this project" 5

# Test with edge cases (validation)
/expert-parallel "" "test task" 3  # Empty domain - should error
/expert-parallel "domain" "" 3     # Empty task - should error
/expert-parallel "domain" "task" 2 # Too few - should error
/expert-parallel "domain" "task" 15 # Too many - should cap at 10
```

## Acceptance Criteria
- ✅ Template file created: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
- ✅ Template uses Jinja2 variables (e.g., `{{ config.project.name }}`)
- ✅ Template registered in scaffold_service.py (added to commands list around line 345)
- ✅ Implementation file exists: `.claude/commands/expert-parallel.md`
- ✅ Command has proper frontmatter (allowed-tools, description, argument-hint, model)
- ✅ Variables defined: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3, default: 3)
- ✅ Phase 1 validates inputs: domain non-empty, task non-empty, num_agents in 3-10 range
- ✅ Phase 2 spawns 3-10 agents in parallel using single message with multiple Task invocations
- ✅ Phase 3 monitors with blocking wait and progress updates
- ✅ Phase 4 synthesis uses opus model explicitly
- ✅ Synthesis produces markdown report with sections: Consensus, Conflicts, Recommendations
- ✅ Partial failure handling: continues with ≥2 successful agents
- ✅ Full agent outputs stored in scratchpad and linked in report
- ✅ Clear error messages for validation failures and insufficient successes
- ✅ All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Verify files exist
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo "✓ Template"
grep "expert-parallel" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
test -f .claude/commands/expert-parallel.md && echo "✓ Repo file"

# Run test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions
1. **Why opus for synthesis?** Aggregating 3-10 agent outputs, identifying patterns, and resolving conflicts requires strongest reasoning capability. The cost is justified by the quality of consensus analysis.

2. **Why 3-10 agent range?** Minimum 3 provides basic triangulation. Maximum 10 balances resource constraints (30min × 10 = 5hrs compute) with practical ceiling for consensus analysis. More agents = diminishing returns.

3. **Why blocking monitor vs non-blocking?** Simplicity. Non-blocking monitoring adds significant complexity (polling, state management) without clear benefit for this use case. User expects results and can wait.

4. **Why minimum 2 successes?** Single agent success provides no consensus data. Two agents enable basic agreement/disagreement analysis, though results will note limited confidence.

5. **Why 30min agent timeout?** Expert-level analysis requires thorough exploration. Shorter timeouts rush analysis; longer timeouts have diminishing returns. 30min matches typical deep-dive exploration sessions.

### Differences from /parallel_subagents
- **/parallel_subagents**: Task decomposition (different subtasks in parallel)
- **/expert-parallel**: Expert consensus (same task, multiple perspectives)
- Different use cases, complementary patterns

### Future Enhancements (Out of Scope)
- Resume capability for partial failures (YAGNI for initial version)
- Dynamic timeout adjustment based on task complexity
- Agent diversity enforcement (different models, different prompting strategies)
- Consensus confidence scoring algorithm
- Integration with /expert-orchestrate for full plan→build→validate workflow

### TAC-13 Context
This is Task 17 of the TAC-13 meta-agentics implementation. It builds on:
- Tasks 1-12: Expert frameworks (question, self-improve, expertise.yaml)
- Task 13: Meta-prompt generator
- Task 14: Meta-agent generator
- Task 16: Expert orchestrator (plan→build→improve)
- Task 17: **Parallel expert scaling** (this feature)

The complete meta-agentic layer enables: prompts that create prompts, agents that create agents, orchestrators that manage workflows, and consensus mechanisms that validate decisions.
