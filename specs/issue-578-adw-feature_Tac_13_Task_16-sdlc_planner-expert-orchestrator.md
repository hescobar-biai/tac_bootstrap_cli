# Feature: Expert Orchestrator - Plan → Build → Improve Workflow

## Metadata
issue_number: `578`
adw_id: `feature_Tac_13_Task_16`
issue_json: `{"number": 578, "title": "[TAC-13] Task 16: Create expert orchestrator", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_16\n```\n\n**Description:**\nCreate expert orchestrator as template and implementation - plan → build → improve workflow.\n\n**Technical Steps:**\n\n#### A) Create Jinja2 Template in CLI\n\n1. **Create template file**:\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`\n\n2. **Register in scaffold_service.py**:\n   ```python\n   # TAC-13: Expert Orchestrator\n   plan.add_file(\n       action=\"create\",\n       template=\"claude/commands/expert-orchestrate.md.j2\",\n       path=\".claude/commands/expert-orchestrate.md\",\n       reason=\"Expert orchestrator - plan→build→improve workflow\"\n   )\n   ```\n\n#### B) Create Implementation File in Repo Root\n\n**File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/expert-orchestrate.md`\n\n**3-step orchestration**:\n- Step 1: Create Plan (spawn `/experts:[domain]:plan [task]`)\n- Step 2: Build (spawn `/build [path_to_plan]`)\n- Step 3: Self-Improve (spawn `/experts:[domain]:self-improve true`)\n\n**Variables**: `EXPERT_DOMAIN: $1`, `TASK_DESCRIPTION: $2`\n\n**Acceptance Criteria:**\n- ✅ **Template (.j2)** created in CLI templates\n- ✅ **Template registered** in scaffold_service.py\n- ✅ **Implementation file** in repo root\n- ✅ Spawns 3 subagents in sequence\n- ✅ Each step gets complete instructions\n- ✅ Final report synthesizes all outputs\n- ✅ Follows TAC-13 plan-build-improve pattern"}`

## Feature Description
Create an expert orchestrator command that automates the plan → build → improve workflow cycle for domain experts. This orchestrator will validate inputs, execute three sequential steps (planning, building, and self-improvement), and provide clear progress feedback with a synthesized markdown report. The orchestrator follows TAC-13's dual strategy pattern: a Jinja2 template for distribution and a working implementation in the repo root.

## User Story
As a TAC Bootstrap developer
I want to orchestrate expert workflows with a single command
So that I can execute plan → build → improve cycles without manual coordination between steps

## Problem Statement
Currently, expert workflows require manual coordination between three separate commands:
1. `/experts:[domain]:plan [task]` - Creates implementation plan
2. `/build [plan_path]` - Implements the plan
3. `/experts:[domain]:self-improve` - Validates and improves implementation

This manual orchestration is error-prone (users forget steps, pass wrong paths, skip validation) and lacks visibility into overall workflow progress. There's no single entry point that ensures all three steps execute correctly in sequence with proper error handling.

## Solution Statement
Create a meta-command `/expert-orchestrate [domain] [task]` that:
- Validates domain against known experts (adw, cli, commands, cc_hook_expert)
- Spawns three subagents sequentially with strict error handling (abort on failure)
- Extracts plan path from Step 1 output using regex pattern matching
- Provides clear progress feedback with emoji markers (🔍 Planning... 🔨 Building... ✨ Improving...)
- Synthesizes results into markdown report with sections for each step
- Follows dual strategy: Jinja2 template + working implementation

## Relevant Files
Files necessary for implementing the feature:

### Existing Files (for reference)
- `.claude/commands/build.md` - Build command pattern for Step 2
- `.claude/commands/experts/adw/question.md` - Example expert command structure
- `.claude/commands/experts/cli/self-improve.md` - Self-improve workflow pattern
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` - Planning workflow pattern
- `.claude/commands/meta-agent.md` - Meta-command pattern reference
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service where commands are registered
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2` - Template structure example

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2` - Jinja2 template
- `.claude/commands/expert-orchestrate.md` - Working implementation

## Implementation Plan

### Phase 1: Foundation - Understand Patterns
Read existing expert commands and orchestration patterns to understand:
- Expert command directory structure (`.claude/commands/experts/[domain]/`)
- Subagent spawning patterns using Task tool
- Plan file path extraction patterns (regex for `.md` paths in output)
- Error handling and progress reporting patterns
- Markdown report synthesis patterns

### Phase 2: Core Implementation - Create Template and Implementation
1. Create Jinja2 template with proper frontmatter (allowed-tools, description, argument-hint, model)
2. Implement 3-step sequential workflow with Task tool invocations
3. Add input validation for EXPERT_DOMAIN and TASK_DESCRIPTION
4. Implement plan path extraction using regex pattern matching
5. Add progress markers (🔍 Step 1: Planning... 🔨 Step 2: Building... ✨ Step 3: Improving...)
6. Implement error handling with clear abort messages
7. Create markdown report synthesis with sections for each step

### Phase 3: Integration - Register and Validate
1. Register template in `scaffold_service.py` → `_add_claude_files()` method
2. Create working implementation file in `.claude/commands/expert-orchestrate.md`
3. Validate template rendering with test config
4. Verify command appears in generated projects

## Step by Step Tasks

### Task 1: Explore Existing Patterns
- Read `.claude/commands/build.md` to understand build command structure
- Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` for expert planning patterns
- Read `.claude/commands/meta-agent.md` for meta-command orchestration patterns
- Identify subagent spawning patterns using Task tool
- Understand plan path extraction from agent outputs

### Task 2: Create Jinja2 Template
- Create file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`
- Add frontmatter with allowed-tools: [Task, Read, AskUserQuestion, TodoWrite]
- Add description, argument-hint, model (sonnet)
- Define variables: `EXPERT_DOMAIN: $1`, `TASK_DESCRIPTION: $2`
- Implement input validation section (validate domain, require task description)
- Implement Step 1: Spawn `/experts:[domain]:plan [task]` using Task tool
- Implement plan path extraction using regex pattern: `([a-zA-Z0-9_/\-\.]+\.md)`
- Implement Step 2: Spawn `/build [plan_path]` using Task tool
- Implement Step 3: Spawn `/experts:[domain]:self-improve true` using Task tool
- Add error handling with abort-on-failure logic
- Add progress markers: 🔍 Step 1: Planning... 🔨 Step 2: Building... ✨ Step 3: Improving...
- Create markdown report synthesis section with Plan Summary, Build Results, Improvements Made

### Task 3: Register Template in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate `_add_claude_files()` method around line 282
- Find the commands list (around line 295)
- Add "expert-orchestrate" to commands list before TAC-13 comment section
- Add comment: `# TAC-13: Expert Orchestrator`
- Verify template will be registered with loop at line 353-359

### Task 4: Create Working Implementation
- Create file: `.claude/commands/expert-orchestrate.md`
- Copy structure from template (same content but with actual values, no Jinja2 variables)
- Verify frontmatter is valid YAML
- Verify allowed-tools list includes Task, Read, AskUserQuestion, TodoWrite
- Test variable parsing for $1 and $2
- Ensure all three Task tool invocations have proper syntax
- Verify regex pattern for plan path extraction
- Verify error messages are clear and actionable

### Task 5: Validation
- Execute validation commands (listed below)
- Verify template file exists at correct path
- Verify template is registered in scaffold_service.py
- Verify implementation file exists in repo root
- Test template rendering with sample config
- Verify command would work in generated projects

## Testing Strategy

### Unit Tests
No new unit tests required (command validation tested through integration)

### Integration Tests
1. **Template Validation**: Verify template file exists and is registered
   ```bash
   test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2 && echo "✓ Template"
   grep "expert-orchestrate" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
   ```

2. **Implementation Validation**: Verify implementation file exists and has correct structure
   ```bash
   test -f .claude/commands/expert-orchestrate.md && echo "✓ Repo file"
   ```

3. **Manual Test**: Execute command manually (future)
   ```bash
   # /expert-orchestrate cli "add help text to wizard"
   # Should spawn 3 subagents sequentially and produce report
   ```

### Edge Cases
- **Invalid domain**: Should error with "Unknown domain. Valid domains: adw, cli, commands, cc_hook_expert"
- **Missing task**: Should error with "Usage: /expert-orchestrate [domain] [task_description]"
- **Plan step fails**: Should abort with "Plan step failed to produce valid plan file"
- **Build step fails**: Should abort with clear error from build agent
- **Cannot extract plan path**: Should abort with "Could not extract plan file path from planning step"

## Acceptance Criteria
- ✅ Template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`
- ✅ Template registered in `scaffold_service.py` commands list
- ✅ Implementation file created at `.claude/commands/expert-orchestrate.md`
- ✅ Command validates EXPERT_DOMAIN against known domains: ['adw', 'cli', 'commands', 'cc_hook_expert']
- ✅ Command requires TASK_DESCRIPTION or errors with usage message
- ✅ Command spawns 3 subagents sequentially using Task tool
- ✅ Each step shows progress message with emoji markers
- ✅ Command extracts plan path from Step 1 output using regex
- ✅ Command passes plan path to Step 2 (build)
- ✅ Command aborts on any failure with clear error message
- ✅ Command outputs markdown report with sections for each step
- ✅ Report optionally saved to `.claude/reports/orchestrate-{domain}-{timestamp}.md`
- ✅ Follows TAC-13 dual strategy pattern (template + implementation)

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2 && echo "✓ Template exists"

# Verify template is registered
grep "expert-orchestrate" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"

# Verify implementation exists
test -f .claude/commands/expert-orchestrate.md && echo "✓ Implementation exists"

# Run unit tests (existing tests should pass)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions
- **Hardcoded domain list**: Known domains are hardcoded for MVP (adw, cli, commands, cc_hook_expert). Can be made configurable later if needed.
- **Regex for path extraction**: Using pattern `([a-zA-Z0-9_/\-\.]+\.md)` to extract plan file paths from Step 1 output. Assumes expert plan commands output paths ending in `.md`.
- **No retry logic**: Failures abort immediately. Sequential dependency means retrying one step without redoing prior steps doesn't make sense.
- **Stdout report + optional file**: Primary output to stdout for immediate visibility. Optional save to `.claude/reports/` for record-keeping.
- **No configurability**: Timeouts, retry counts, etc. are not configurable for MVP. Can be added later if needed.

### Implementation Notes
- Expert commands follow pattern: `/experts:[domain]:[command] [args]`
- Build command accepts optional plan file path: `/build [plan_path]`
- Self-improve commands may accept boolean flag for full validation
- Task tool used for spawning subagents with proper prompt and description
- Plan path extraction should be robust to different output formats

### Future Enhancements
- Add optional `--parallel` flag for parallel expert scaling (TAC-13 Task 17)
- Add `--dry-run` mode to show what would be executed
- Add progress bar or detailed step output
- Support custom expert domains via config file
- Add telemetry/observability for orchestration metrics
