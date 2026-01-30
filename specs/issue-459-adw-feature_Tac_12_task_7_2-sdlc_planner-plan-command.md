# Feature: Create Simple Planning Command (plan.md)

## Metadata
issue_number: `459`
adw_id: `feature_Tac_12_task_7_2`
issue_json: `{"number":459,"title":"[Task 7/49] [FEATURE] Create plan.md command file","body":"## Description\n\nCreate a simple planning command without scout agents. SIMPLER than plan_w_scouters.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`\n\n## Key Features\n- Model: claude-opus-4-1-20250805\n- allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit\n- Simple 5-step workflow (no scouts)\n- Saves to specs/ directory\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan.md`\n\n## Wave 1 - New Commands (Task 7 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_7_2"}`

## Feature Description

Create a simplified planning command `/plan` that helps users create implementation plans without the overhead of scout agent exploration. This command provides a streamlined, 5-step workflow for planning tasks: understand requirements, read relevant files, design approach, write plan, and save to specs/ directory.

The command is designed to be SIMPLER than `/plan_w_scouters` by removing the parallel scout exploration phase while maintaining the same structured plan output format.

## User Story

As a developer using TAC Bootstrap CLI
I want to create quick implementation plans without waiting for scout exploration
So that I can rapidly document simple features or tasks that don't require extensive codebase discovery

## Problem Statement

The current planning commands (`/plan_w_scouters`, `/plan_w_docs`) are comprehensive but may be overkill for simple planning tasks. They involve parallel scout agents or documentation fetching which adds latency and complexity.

For straightforward features where the developer already knows which files to work with, or for small codebases where exploration overhead isn't justified, a simpler planning workflow is needed.

## Solution Statement

Create a new `/plan` command that follows a simplified 5-step workflow:
1. **Understand requirements** - Parse issue metadata and clarify task scope
2. **Read relevant files** - Use Read, Glob, Grep tools to gather context
3. **Design approach** - Think through the implementation strategy
4. **Write implementation plan** - Document the plan using standard format
5. **Save to specs/** - Write plan file to specs/ directory

This approach removes the scout exploration phase from `/plan_w_scouters` while maintaining the same structured plan format. The agent uses `claude-opus-4-1-20250805` model with allowed-tools (Read, Write, Edit, Glob, Grep, MultiEdit) to provide sufficient capability for manual exploration and planning.

Following the pattern established in `plan_w_scouters.md.j2` template, we'll create both:
- Base file: `.claude/commands/plan.md` (reference implementation)
- Template file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` (for CLI generation)

## Relevant Files

Files needed to implement the feature:

### Existing Files to Modify

1. **`tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`** (lines 278-330)
   - Add "plan" to the commands list so it gets scaffolded
   - Insert in the commands list between other planning commands

### New Files

2. **`.claude/commands/plan.md`**
   - Base reference implementation of the plan command
   - Uses hardcoded paths (specs/, TAC Bootstrap CLI, etc.)
   - Serves as the canonical version for tac_bootstrap itself

3. **`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`**
   - Jinja2 template version with config variables
   - Uses `{{ config.project.name }}`, `{{ config.project.description }}`, `{{ config.paths.specs_dir }}`
   - Generated into target projects by scaffold_service.py

## Implementation Plan

### Phase 1: Foundation
- Read and understand `plan_w_scouters.md` structure
- Identify sections to remove (scout exploration workflow)
- Identify sections to simplify (instructions, workflow steps)
- Determine template variables needed

### Phase 2: Core Implementation
- Create `.claude/commands/plan.md` base file
- Simplify workflow to 5 steps (no scouts)
- Remove scout-specific sections from plan format
- Update model and allowed-tools configuration
- Add instructions for manual file exploration

### Phase 3: Template Creation
- Create Jinja2 template version at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`
- Replace hardcoded values with template variables
- Ensure compatibility with existing config schema

### Phase 4: Integration
- Add "plan" to commands list in scaffold_service.py
- Position it appropriately among other planning commands
- Verify template rendering works correctly

## Step by Step Tasks

### Task 1: Understand plan_w_scouters.md Structure
- Read `.claude/commands/plan_w_scouters.md` completely
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` template
- Identify sections that are scout-specific vs generic planning
- Note the plan format structure (metadata, description, tasks, validation, etc.)

### Task 2: Create Base plan.md File
- Create `.claude/commands/plan.md`
- Copy frontmatter structure (allowed-tools, description)
- Update model to `claude-opus-4-1-20250805`
- Update allowed-tools to `Read, Write, Edit, Glob, Grep, MultiEdit`
- Update description to reflect simplified workflow
- Write simplified 5-step workflow instructions
- Remove all scout-related sections
- Keep plan format structure without scout exploration summary
- Maintain same variable structure (issue_number, adw_id, issue_json)
- Update examples to reflect simpler approach

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`
- Copy content from `.claude/commands/plan.md`
- Replace "TAC Bootstrap CLI" with `{{ config.project.name }}`
- Replace hardcoded "specs/" with `{{ config.paths.specs_dir }}`
- Add conditional blocks for validation commands using:
  - `{{ config.commands.test }}`
  - `{{ config.commands.lint }}`
  - `{{ config.commands.typecheck }}`
- Use pattern from plan_w_scouters.md.j2 for reference
- Add `{{ config.commands.install }}` for library installation instructions

### Task 4: Update scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Find the commands list (around line 279-330)
- Add "plan" to the list after "plan_w_docs" and before other commands
- Ensure proper indentation and formatting

### Task 5: Validation
- Run validation commands to ensure no regressions:
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
  - `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Manually test template rendering by running scaffold with test config
- Verify plan.md is created in target project's .claude/commands/

## Testing Strategy

### Unit Tests

No new unit tests required for this task as it's adding template files. Existing `test_scaffold_service.py` tests will verify:
- Commands list includes "plan"
- Template rendering works for plan.md.j2
- Generated plan.md has correct content

### Integration Tests

Manual verification:
1. Run `tac-bootstrap generate` or `tac-bootstrap upgrade` on a test project
2. Verify `.claude/commands/plan.md` is created
3. Verify template variables are correctly substituted
4. Try invoking `/plan <issue_number> <adw_id> <issue_json>` in Claude Code
5. Verify plan file is created in specs/ directory

### Edge Cases

- Specs directory doesn't exist - agent should create it automatically (instruction in command)
- Plan file already exists - agent should ask user what to do (instruction in command)
- Missing template variables - scaffold validation should catch this
- Empty issue_json - agent should handle gracefully and ask for clarification

## Acceptance Criteria

1. **Base File Created**
   - `.claude/commands/plan.md` exists in repository
   - Uses model: `claude-opus-4-1-20250805`
   - Uses allowed-tools: `Read, Write, Edit, Glob, Grep, MultiEdit`
   - Contains 5-step workflow (understand, read, design, plan, save)
   - Does NOT contain scout-related sections
   - Instructs agent to create specs/ if needed
   - Instructs agent to ask user about file conflicts

2. **Template File Created**
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` exists
   - Uses template variables: `{{ config.project.name }}`, `{{ config.paths.specs_dir }}`, etc.
   - Follows same structure as base file but with Jinja2 substitutions
   - Compatible with existing TACConfig schema

3. **scaffold_service.py Updated**
   - "plan" added to commands list in `_add_claude_files` method
   - Positioned appropriately in the list (after plan_w_docs)
   - Template path correctly mapped

4. **All Tests Pass**
   - Unit tests pass: `pytest tests/ -v`
   - Linting passes: `ruff check .`
   - Type checking passes: `mypy tac_bootstrap/`
   - Smoke test passes: `tac-bootstrap --help`

5. **Template Renders Correctly**
   - Running `tac-bootstrap generate` creates `.claude/commands/plan.md` in target project
   - Template variables are correctly substituted
   - Generated file is valid markdown with proper frontmatter

6. **Command Works in Claude Code**
   - Can invoke `/plan <args>` in Claude Code
   - Agent follows 5-step workflow
   - Plan file is created in specs/ directory
   - Output format matches specification

## Validation Commands

Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Simplifications from plan_w_scouters.md

This command removes:
- Scout Exploration Workflow (steps 1-9)
- Scout Exploration Summary section in plan format
- Parallel Task tool invocations for scouts
- Scout result aggregation logic
- High-confidence file scoring
- Notes sections about scout configuration rationale
- Performance characteristics of scout execution
- Troubleshooting for scout failures

This command keeps:
- Same plan format (metadata, description, user story, problem/solution statements, etc.)
- Same validation commands structure
- Same variable passing (issue_number, adw_id, issue_json)
- Same output format requirements (relative path only)

### Template Variables Used

Minimal config variables for simplicity:
- `{{ config.project.name }}` - Project name
- `{{ config.project.description }}` - Project description
- `{{ config.paths.specs_dir }}` - Specs directory path
- `{{ config.commands.test }}` - Test command (conditional)
- `{{ config.commands.lint }}` - Lint command (conditional)
- `{{ config.commands.typecheck }}` - Type check command (conditional)
- `{{ config.commands.install }}` - Package install command

### Agent Workflow Instructions

The command instructs the agent to:
1. Parse issue JSON and understand requirements
2. Use Read/Glob/Grep to explore relevant files manually
3. Design implementation approach based on findings
4. Write structured plan following format template
5. Create specs/ directory if it doesn't exist
6. Ask user about file conflicts (don't auto-overwrite)
7. Save plan and output ONLY the relative path

### When to Use This Command

Use `/plan` when:
- Simple, straightforward features where files are known
- Small codebases where exploration is quick
- Time-sensitive planning where scout overhead isn't justified
- Developer already has good codebase familiarity

Use `/plan_w_scouters` when:
- Complex features requiring comprehensive file discovery
- Large codebases with many architectural layers
- Unclear which files need modification
- Want high-confidence file recommendations from parallel exploration

### Future Enhancements

- Add optional `--with-scouts` flag to upgrade to scout-based planning
- Support custom plan templates via config
- Integration with `/implement` to auto-feed discovered files
- Plan validation and completeness checking
