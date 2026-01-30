# Feature: Create build-agent.md Agent Definition

## Metadata
issue_number: `466`
adw_id: `feature_Tac_12_task_14`
issue_json: `{"number":466,"title":"[Task 14/49] [FEATURE] Create build-agent.md agent definition","body":"## Description\n\nCreate a specialized agent for implementing individual files in parallel builds.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/build-agent.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`\n\n## Key Features\n- name: build-agent\n- tools: Write, Read, Edit, Grep, Glob, Bash, TodoWrite\n- model: sonnet\n- color: blue\n- Specialized for ONE file implementation\n- 6-step workflow with verification\n- Structured report format\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n- Ensure `.claude/agents/` directory is created\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md`\n\n## Wave 2 - New Agents (Task 14 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_14"}`

## Feature Description
Create a specialized build-agent for implementing individual files in parallel build workflows. This agent will be a file implementation specialist that focuses on writing one specific file based on detailed instructions and context. The agent follows a 6-step workflow with verification and produces structured reports on implementation quality.

This is part of Wave 2 - New Agents for TAC-12, enhancing the parallel build capabilities of the TAC Bootstrap framework.

## User Story
As a TAC Bootstrap user
I want to have a specialized build-agent that can implement individual files in parallel
So that I can efficiently generate multiple files concurrently during the build phase with high quality and proper verification

## Problem Statement
Currently, TAC Bootstrap lacks a specialized agent definition for parallel file implementation during the build phase. Users need a focused agent that can:
- Take detailed instructions for a single file implementation
- Follow a systematic workflow to understand context, implement, and verify
- Produce structured reports on implementation quality
- Work efficiently as part of parallel build workflows

Without this agent definition, the parallel build workflows cannot properly delegate file implementation tasks to specialized agents.

## Solution Statement
Create a build-agent definition that:
1. Copies the proven reference implementation from TAC-12
2. Creates both the base agent file and Jinja2 template for CLI generation
3. Integrates into the scaffold service to be included in all generated projects
4. Ensures the .claude/agents/ directory is properly created

The agent will implement a rigorous 6-step workflow:
1. Read and analyze the specification thoroughly
2. Gather context by reading referenced files
3. Understand codebase conventions
4. Implement the file according to specification
5. Verify the implementation with type checks, linting, and tests
6. Report completion status with structured output

## Relevant Files
Files necessary for implementing the feature:

- **Reference Source:**
  - `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md` - Reference implementation to copy

- **Base Repository:**
  - `.claude/agents/build-agent.md` - Agent definition in base repository (to be created)

- **CLI Templates:**
  - `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2` - Jinja2 template for CLI generation (to be created)

- **Scaffold Service:**
  - `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that orchestrates scaffolding, needs update to include build-agent

### New Files
- `.claude/agents/build-agent.md` - Base agent definition file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2` - Jinja2 template

## Implementation Plan

### Phase 1: Foundation
Read the reference file and validate it's accessible. Understand the existing agent registration pattern in scaffold_service.py by examining how other agents (docs-scraper, meta-agent, research-docs-fetcher) are registered.

### Phase 2: Core Implementation
1. Copy the reference file content to create the base repository agent file at `.claude/agents/build-agent.md`
2. Create the Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`
3. Update scaffold_service.py to include build-agent in the agents list

### Phase 3: Integration
Verify the integration by checking that:
- The .claude/agents/ directory creation is already handled (it is, at line 112 in scaffold_service.py)
- The agent follows the same registration pattern as existing agents
- The template structure matches existing agent templates

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Validate Reference File Access
- Read the reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md`
- Verify the content includes the 6-step workflow and structured report format
- If inaccessible, fail fast with clear error message

### Task 2: Create Base Repository Agent File
- Create `.claude/agents/build-agent.md` in the base repository
- Copy the content exactly from the reference file
- Verify file was created successfully

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`
- Copy the content from the reference file as-is (no templating variables for now)
- Follow the same format as existing agent templates (docs-scraper, meta-agent, research-docs-fetcher)
- Verify template was created successfully

### Task 4: Update Scaffold Service
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- In the `_add_claude_files` method, add build-agent to the agents list (around line 411-422)
- Add tuple: `("build-agent.md", "Parallel build file implementation agent")`
- Follow the exact same pattern as existing agents
- Ensure placement is logical (add after existing agents, before output_styles section)

### Task 5: Verify Directory Creation
- Confirm that `.claude/agents/` directory creation is already handled in scaffold_service.py
- This should be at line 112 in the `_add_directories` method
- No changes needed if already present

### Task 6: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify the changes integrate properly with existing code
- Confirm type checking, linting, and tests all pass

## Testing Strategy

### Unit Tests
No new unit tests are required for this feature as it's primarily adding static configuration files. However, we should verify:
- The scaffold service properly includes the build-agent in plans
- Template rendering works correctly for the new agent
- File creation follows the correct patterns

### Edge Cases
- **Reference file inaccessible**: Should fail fast with clear error during implementation
- **Template rendering**: Verify template renders without Jinja2 errors
- **Directory existence**: Ensure .claude/agents/ directory is created even if it doesn't exist
- **Force mode**: Verify agent file creation respects force flag in scaffold_service.py

## Acceptance Criteria
- [ ] Reference file `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md` is successfully read
- [ ] Base repository file `.claude/agents/build-agent.md` is created with exact content from reference
- [ ] Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2` is created
- [ ] Template contains the complete 6-step workflow and structured report format
- [ ] `scaffold_service.py` includes build-agent in the agents list using the same pattern as existing agents
- [ ] `.claude/agents/` directory creation is confirmed in `_add_directories` method
- [ ] All validation commands pass:
  - Unit tests pass
  - Ruff linting passes
  - Mypy type checking passes
  - CLI smoke test passes
- [ ] Agent follows Claude Code agent definition format with frontmatter metadata
- [ ] Agent name, description, tools, model, and color are correctly specified

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The reference file is from a proven TAC-12 implementation, so we copy it exactly
- No templating variables are needed initially - agent definitions are typically project-agnostic
- The agent is designed to work as part of parallel build workflows, receiving detailed instructions for single file implementations
- The 6-step workflow ensures rigorous implementation with proper verification
- The structured report format provides clear visibility into implementation quality and potential issues
- Directory creation for .claude/agents/ is already handled in scaffold_service.py at line 112
- This is Task 14 of 49 in Wave 2 - New Agents for TAC-12 integration
