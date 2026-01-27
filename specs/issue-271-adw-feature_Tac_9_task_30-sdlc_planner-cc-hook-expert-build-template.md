# Feature: Add cc_hook_expert_build.md.j2 Expert Command Template

## Metadata
issue_number: `271`
adw_id: `feature_Tac_9_task_30`
issue_json: `{"number":271,"title":"Add cc_hook_expert_build.md.j2 expert command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_30\n\n**Description:**\nCreate Jinja2 template for Claude Code hook expert build command. Second step in Plan-Build-Improve cycle.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md` (CREATE - rendered)\n"}`

## Feature Description
Create a Jinja2 template for the `cc_hook_expert_build` command that guides AI agents through the implementation (build) phase of Claude Code hooks. This is the second step in the Plan-Build-Improve expert workflow cycle for hook development. The template will provide expert methodology for executing the planned solution, implementing hook code step-by-step, validating functionality with tests and linting, and handling common implementation issues.

## User Story
As a TAC Bootstrap user
I want to generate expert build commands for hook implementation
So that my generated projects can guide AI agents through structured hook execution workflows that follow the plans they created

## Problem Statement
The TAC Bootstrap CLI has the planning phase (`cc_hook_expert_plan`) but lacks the execution phase for Claude Code hook development. Users need a build-phase expert command that guides agents through:
1. Referencing and executing the implementation plan
2. Writing hook code following established patterns
3. Integrating hooks with settings.json configuration
4. Validating implementation with tests and linting
5. Troubleshooting common issues during implementation

This template must create workflow continuity with the planning phase, follow established patterns (YAML frontmatter, Jinja2 variables, expert workflow structure), and integrate with the existing expert command infrastructure.

## Solution Statement
Create a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2` that:
- Uses YAML frontmatter with implementation-focused tools (Read, Write, Edit, Bash, TodoWrite, Glob, Grep)
- Accepts optional `$ARGUMENTS` for build context or plan reference (e.g., '/cc_hook_expert_build specs/hook-pre-commit-plan.md')
- Guides agents through Plan Review → Implementation → Integration → Validation workflow
- References the prior plan document and provides step-by-step execution guidance
- Includes validation checkpoints (tests, linting) and troubleshooting guidance
- Uses minimal Jinja2 variables ({{ config.project.name }}, {{ config.commands.test }})
- Provides expert guidance as static content with project-specific commands via config

## Relevant Files
Files needed for implementation:

### Reference Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` - Planning phase template (predecessor workflow)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Implementation command pattern with TodoWrite
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2` - Expert workflow structure with validation steps
- `.claude/settings.json` - Hook configuration reference
- `.claude/hooks/pre_tool_use.py` - Example hook implementation
- `.claude/hooks/post_tool_use.py` - Example hook implementation
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config schema for available variables

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2` - The template to create

### Directory Structure
The experts directory already exists:
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/` - Target directory (has cc_hook_expert_plan.md.j2)

## Implementation Plan

### Phase 1: Template Structure Design
Design the YAML frontmatter and overall template structure:
- Define allowed-tools: Read, Write, Edit, Bash, TodoWrite, Glob, Grep (implementation-focused)
- Set description: 'Build hook implementation following expert plan'
- Set model: 'sonnet' (implementation can use sonnet for most work)
- Define $ARGUMENTS variable for optional plan reference or build context

### Phase 2: Expert Workflow Content
Create the build workflow sections:
- **Purpose**: Explain the build phase as workflow continuation from planning
- **Variables**: Define BUILD_CONTEXT ($ARGUMENTS), PROJECT_NAME ({{ config.project.name }}), TEST_COMMAND ({{ config.commands.test }})
- **Instructions**: Guide agent through 4-phase workflow:
  1. Review Plan (locate plan document, parse key decisions, set up TodoWrite tasks)
  2. Implement Hook (write hook code following patterns, integrate with settings.json)
  3. Validate Implementation (run tests, linting, manual smoke tests)
  4. Troubleshoot Issues (common errors, debugging strategies, iteration guidance)
- **Implementation Patterns**: Reference hook code patterns, settings.json integration, error handling
- **Quality Checks**: Test execution, lint checks, manual validation steps
- **Report**: Output format for implementation completion and validation results

### Phase 3: Integration and Validation
Ensure template integrates correctly:
- Verify Jinja2 syntax (only use config.project.name, config.commands.test)
- Validate YAML frontmatter format
- Ensure workflow continuity with planning phase
- Ensure directory structure compatibility with CLI generator

## Step by Step Tasks

### Task 1: Create cc_hook_expert_build.md.j2 template file
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2`
- Add YAML frontmatter with:
  - allowed-tools: Read, Write, Edit, Bash, TodoWrite, Glob, Grep
  - description: 'Build hook implementation following expert plan'
  - model: sonnet
- Add Purpose section explaining:
  - Build phase as second step in Plan-Build-Improve cycle
  - Workflow continuation from cc_hook_expert_plan
  - Focus on executing the planned solution
- Add Variables section:
  - BUILD_CONTEXT: $ARGUMENTS
  - PROJECT_NAME: {{ config.project.name }}
  - TEST_COMMAND: {{ config.commands.test }}

### Task 2: Write expert build workflow instructions
- Add Instructions section with 4-phase workflow:
  1. **Review Plan**:
     - Locate plan document (from BUILD_CONTEXT or specs/ directory)
     - Parse key implementation decisions
     - Set up TodoWrite tasks for step-by-step tracking
     - Identify files to create/modify
  2. **Implement Hook**:
     - Write hook script following plan specifications
     - Follow naming conventions and patterns from exploration
     - Integrate with .claude/settings.json (add hook configuration)
     - Implement error handling (exit codes 0/1/2)
     - Add logging and session management as needed
  3. **Validate Implementation**:
     - Run {{ config.commands.test }} for tests
     - Run linting/type checks (ruff, mypy if applicable)
     - Manual smoke test (invoke command that triggers hook)
     - Verify hook appears in settings.json correctly
  4. **Troubleshoot Issues**:
     - Common errors (JSON parsing, exit codes, permission issues)
     - Debugging strategies (check logs, verify stdin/stdout, test hook manually)
     - Iteration guidance (refine based on test results)

### Task 3: Add implementation patterns and examples
- Add Implementation Patterns section with:
  - Hook code structure (stdin JSON parsing, logic, stdout/stderr, exit code)
  - settings.json integration (hook type, matcher pattern, command structure)
  - Error handling patterns (try/except, exit codes, error messages)
  - Logging patterns (session tracking, output formatting)
  - Example code snippets from similar hooks

### Task 4: Add quality checks and validation steps
- Add Quality Checks section with:
  - Test execution: `{{ config.commands.test }}` or project-specific test commands
  - Linting: `ruff check .` (if Python) or equivalent
  - Type checking: `mypy` (if applicable)
  - Manual validation: Trigger hook with test command
  - Settings validation: Verify hook registered in .claude/settings.json

### Task 5: Add troubleshooting guidance
- Add Validation & Troubleshooting section with:
  - Common implementation errors:
    - JSON parsing failures (malformed stdin)
    - Incorrect exit codes (blocking when should warn)
    - Permission issues (script not executable)
    - Import errors (missing dependencies)
  - Debugging steps:
    - Check hook logs/output
    - Test hook script directly with sample JSON input
    - Verify environment variables ($CLAUDE_PROJECT_DIR)
    - Validate settings.json syntax
  - Iteration guidance:
    - If tests fail, fix and re-validate
    - If hook doesn't trigger, check matcher pattern
    - If blocking incorrectly, review exit code logic

### Task 6: Add report format
- Add Report section specifying output format:
  - Hook implementation status (completed, files created/modified)
  - Validation results (tests passed, linting clean)
  - Integration confirmation (settings.json updated)
  - Next steps reminder (move to improve phase if refinements needed)

### Task 7: Add usage guidance
- Add Usage section at top explaining:
  - When to use this command (after completing planning phase)
  - How to reference the plan (pass plan path or agent finds it)
  - What happens in build phase (execute plan, validate, troubleshoot)
  - Workflow context (Plan → Build → Improve cycle)

### Task 8: Validate template syntax and structure
- Verify Jinja2 syntax is correct
- Ensure YAML frontmatter parses correctly
- Validate minimal variable usage (config.project.name, config.commands.test)
- Check workflow continuity with planning phase
- Ensure file created in correct directory

### Task 9: Run validation commands
Execute all validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required - this is a template file addition. Existing template rendering tests will validate Jinja2 syntax.

### Manual Validation
1. Template renders correctly with CLI generator
2. YAML frontmatter is valid
3. Jinja2 variables are correctly scoped (config.project.name, config.commands.test)
4. Content provides clear expert guidance for implementation
5. Workflow creates continuity with planning phase

### Edge Cases
- Empty $ARGUMENTS (should guide to find plan in specs/)
- Plan document not found (should prompt user or search specs/)
- Tests fail during validation (should provide troubleshooting guidance)
- Hook doesn't trigger after implementation (debugging checklist)

## Acceptance Criteria
- [x] Template file created at correct path: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2`
- [x] YAML frontmatter includes implementation-focused tools (Read, Write, Edit, Bash, TodoWrite, Glob, Grep)
- [x] Purpose section explains build phase and workflow continuation
- [x] Variables section defines BUILD_CONTEXT, PROJECT_NAME, TEST_COMMAND
- [x] Instructions guide through 4-phase workflow (Review → Implement → Validate → Troubleshoot)
- [x] Implementation Patterns section provides hook code guidance
- [x] Quality Checks section specifies validation steps
- [x] Validation & Troubleshooting section provides debugging guidance
- [x] Report section specifies output format
- [x] Usage section explains when/how to use command
- [x] Template uses minimal Jinja2 variables (only config.project.name, config.commands.test)
- [x] All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This template creates workflow continuity between planning and improvement phases
- The build phase is about implementing/executing planned solutions, not software compilation
- Validation checkpoints ensure quality before moving to improvement phase
- Troubleshooting guidance helps agents handle common implementation issues autonomously
- Generic guidance with config variables maintains flexibility across diverse project types
- Minimal Jinja2 variables reduce template complexity while providing necessary project context
