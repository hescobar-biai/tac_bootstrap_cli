# Feature: Add cc_hook_expert_plan.md.j2 Expert Command Template

## Metadata
issue_number: `270`
adw_id: `feature_Tac_9_task_29`
issue_json: `{"number":270,"title":"Add cc_hook_expert_plan.md.j2 expert command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_29\n\n**Description:**\nCreate Jinja2 template for Claude Code hook expert planning command. First step in Plan-Build-Improve cycle.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` (CREATE - rendered)\n"}`

## Feature Description
Create a Jinja2 template for the `cc_hook_expert_plan` command that guides AI agents through the planning phase of implementing Claude Code hooks. This is the first step in the Plan-Build-Improve expert workflow cycle for hook development. The template will provide expert methodology for exploring hook requirements, understanding existing patterns, designing hook architecture, and creating implementation plans.

## User Story
As a TAC Bootstrap user
I want to generate expert planning commands for hook implementation
So that my generated projects can guide AI agents through structured hook planning workflows

## Problem Statement
The TAC Bootstrap CLI generates agentic layers for projects but currently lacks expert command templates for Claude Code hook development. Users need a planning-phase expert command that guides agents through:
1. Understanding hook requirements
2. Exploring relevant code and patterns
3. Designing hook architecture
4. Creating structured implementation plans

This template must follow established patterns (YAML frontmatter, Jinja2 variables, expert workflow structure) and integrate with the existing expert command infrastructure.

## Solution Statement
Create a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` that:
- Uses YAML frontmatter with planning-focused tools (Read, Glob, Grep, Task/Explore, EnterPlanMode, AskUserQuestion, TodoWrite)
- Accepts optional `$ARGUMENTS` for hook requirements (e.g., '/cc_hook_expert_plan pre-commit validation')
- Guides agents through Requirements → Exploration → Architecture → Plan workflow
- References Claude Code hook patterns (.claude/hooks/, settings.json configuration)
- Uses minimal Jinja2 variables (only `{{ config.project.name }}` where needed)
- Provides expert guidance as static content (universal methodology)

## Relevant Files
Files needed for implementation:

### Reference Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` - Planning command pattern with YAML frontmatter
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2` - Expert workflow structure and Jinja2 variable usage
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Simple command template pattern
- `.claude/settings.json` - Hook configuration reference (PreToolUse, PostToolUse, etc.)
- `.claude/hooks/pre_tool_use.py` - Example hook implementation
- `.claude/hooks/post_tool_use.py` - Example hook implementation

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` - The template to create

### Directory Structure
The experts directory already exists:
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/` - Target directory (has .gitkeep)

## Implementation Plan

### Phase 1: Template Structure Design
Design the YAML frontmatter and overall template structure:
- Define allowed-tools: Read, Glob, Grep, Task (Explore agent), EnterPlanMode, AskUserQuestion, TodoWrite
- Set description: 'Plan hook implementation using expert methodology'
- Set model: 'sonnet' (planning doesn't need opus)
- Define $ARGUMENTS variable for optional hook requirements

### Phase 2: Expert Workflow Content
Create the planning workflow sections:
- **Purpose**: Explain the planning phase of hook development
- **Variables**: Define HOOK_REQUIREMENTS ($ARGUMENTS) and PROJECT_NAME ({{ config.project.name }})
- **Instructions**: Guide agent through 4-phase workflow:
  1. Understand Requirements (capture hook purpose, events, constraints)
  2. Explore Codebase (find similar hooks, understand patterns)
  3. Design Architecture (hook naming, event integration, error handling)
  4. Create Plan (structured implementation document)
- **Hook Patterns**: Reference common patterns (pre_*, post_*, hook naming conventions, settings.json structure)
- **Report**: Output format for plan document location and summary

### Phase 3: Integration and Validation
Ensure template integrates correctly:
- Verify Jinja2 syntax (only use {{ config.project.name }})
- Validate YAML frontmatter format
- Ensure directory structure compatibility with CLI generator

## Step by Step Tasks

### Task 1: Create cc_hook_expert_plan.md.j2 template file
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2`
- Add YAML frontmatter with:
  - allowed-tools: Read, Glob, Grep, Task, EnterPlanMode, AskUserQuestion, TodoWrite
  - description: 'Plan hook implementation using expert methodology'
  - model: sonnet
- Add Purpose section explaining hook planning workflow
- Add Variables section:
  - HOOK_REQUIREMENTS: $ARGUMENTS
  - PROJECT_NAME: {{ config.project.name }}

### Task 2: Write expert workflow instructions
- Add Instructions section with 4-phase workflow:
  1. **Understand Requirements**:
     - Parse HOOK_REQUIREMENTS or use AskUserQuestion if empty
     - Identify hook type (PreToolUse, PostToolUse, Notification, etc.)
     - Define success criteria
  2. **Explore Codebase**:
     - Use Task tool with Explore agent to find existing hooks
     - Read .claude/settings.json to understand hook configuration
     - Identify patterns in .claude/hooks/ directory
  3. **Design Architecture**:
     - Plan hook naming (pre_*, post_*, specific event names)
     - Design integration with settings.json
     - Consider error handling and logging patterns
  4. **Create Plan**:
     - Use EnterPlanMode or write plan document to specs/
     - Include hook specification, implementation steps, testing strategy

### Task 3: Add hook patterns and examples
- Add Hook Patterns section with:
  - Common hook types from settings.json
  - Naming conventions (pre_tool_use, post_tool_use, notification, etc.)
  - Integration points (hook matcher, command structure)
  - Example patterns from existing hooks

### Task 4: Add report format
- Add Report section specifying output format:
  - Plan document location (specs/hook-{name}-plan.md)
  - Hook type and purpose summary
  - Key implementation components
  - Integration points identified

### Task 5: Validate template syntax and structure
- Verify Jinja2 syntax is correct
- Ensure YAML frontmatter parses correctly
- Validate minimal variable usage (only config.project.name)
- Check file created in correct directory

### Task 6: Run validation commands
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
3. Jinja2 variables are correctly scoped
4. Content provides clear expert guidance

### Edge Cases
- Empty $ARGUMENTS (should prompt user for requirements)
- Project without existing hooks (should guide from scratch)
- Complex hook requirements (should break down into phases)

## Acceptance Criteria
1. ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2`
2. ✅ YAML frontmatter includes all required planning tools
3. ✅ Template uses minimal Jinja2 variables (only config.project.name)
4. ✅ Expert workflow covers Requirements → Exploration → Architecture → Plan
5. ✅ Hook patterns and integration guidance included
6. ✅ Template follows established expert command patterns
7. ✅ All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate implementation:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes
- This template is ONLY for the planning phase - build and improve phases will be separate tasks
- Template file creation only - rendering will be handled by CLI generator when users run `tac_bootstrap generate`
- Expert guidance is static content (universal methodology), not project-specific
- Hook API details are intentionally generic - agents discover project-specific APIs during exploration
- Follows Plan-Build-Improve workflow pattern from TAC methodology
- Directory structure already exists with .gitkeep placeholder
