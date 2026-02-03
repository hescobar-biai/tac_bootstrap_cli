# Feature: Meta-Prompt Generator Command

## Metadata
issue_number: `575`
adw_id: `feature_Tac_13_Task_13`
issue_json: `{"number": 575, "title": "[TAC-13] Task 13: Create meta-prompt generator", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_13\n```\n\n**Description:**\nCreate meta-prompt command as template and implementation. This is \"prompts that create prompts\" - the foundation of meta-agentics.\n\n**Technical Steps:**\n\n#### A) Create Jinja2 Template in CLI\n\n1. **Create template file**:\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`\n\n2. **Register in scaffold_service.py**:\n   ```python\n   # TAC-13: Meta-Prompt Generator\n   plan.add_file(\n       action=\"create\",\n       template=\"claude/commands/meta-prompt.md.j2\",\n       path=\".claude/commands/meta-prompt.md\",\n       reason=\"Meta-prompt generator - prompts that create prompts\"\n   )\n   ```\n\n#### B) Create Implementation File in Repo Root\n\n1. **Create complete meta-prompt generator**:\n\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md`"}`

## Feature Description

Create a meta-prompt generator slash command that enables AI agents to generate new slash commands from natural language descriptions. This is the foundation of "meta-agentics" - systems that create systems. The feature implements the dual strategy pattern where both a Jinja2 template (for CLI generation) and a concrete implementation file (in the repository) are created.

## User Story

As a TAC Bootstrap user
I want to describe a new command in natural language
So that an AI agent can generate a complete, production-ready slash command following TAC standards

## Problem Statement

Creating new slash commands manually is time-consuming and error-prone. Each command must follow TAC Bootstrap standards (YAML frontmatter, variables, instructions, workflow structure). This repetitive work can be automated through meta-programming - creating prompts that generate other prompts.

## Solution Statement

Implement a `/meta-prompt` command that:
1. Accepts a natural language description of a desired command
2. Studies existing command patterns in the codebase
3. Generates a complete slash command file following TAC standards
4. Creates both the Jinja2 template (for CLI) and implementation file (for repo)

The solution follows TAC-13's dual strategy: template files enable generation in new projects, implementation files provide living reference examples.

## Relevant Files

Files needed to implement this feature:

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Register new template in `_add_claude_files` method
- `.claude/commands/t_metaprompt_workflow.md` - Existing meta-prompt workflow for reference
- `.claude/commands/feature.md` - Example of TAC command structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Example Jinja2 template structure

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` - Jinja2 template for CLI generation
- `.claude/commands/meta-prompt.md` - Implementation file in repository

## Implementation Plan

### Phase 1: Foundation
1. Study existing meta-prompt pattern in `t_metaprompt_workflow.md`
2. Analyze TAC command structure from multiple examples (`feature.md`, `implement.md`, etc.)
3. Understand dual strategy pattern from existing implementations

### Phase 2: Core Implementation
1. Create Jinja2 template (`meta-prompt.md.j2`) with:
   - YAML frontmatter with allowed tools
   - Variables section accepting command description
   - Instructions for analyzing user request
   - Workflow for generating complete commands
   - Report format specifying output structure
2. Create implementation file (`.claude/commands/meta-prompt.md`) with identical content but no Jinja2 variables

### Phase 3: Integration
1. Register template in `scaffold_service.py` in the `_add_claude_files` method
2. Add to commands list so it's included in all generated projects
3. Validate template renders correctly
4. Test end-to-end generation

## Step by Step Tasks

### Task 1: Create Jinja2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`
- Include YAML frontmatter with:
  - `allowed-tools: Write, Read, Glob, Grep, TodoWrite`
  - `description: Generate a new slash command from user description`
  - `argument-hint: [command_description]`
  - `model: opus`
- Define variables section with `USER_PROMPT_REQUEST: $ARGUMENTS`
- Write instructions explaining meta-prompt concept
- Create workflow with 5 steps:
  1. Study existing commands
  2. Analyze user request
  3. Design command structure
  4. Generate complete command file
  5. Validate generated command
- Define report format with summary, usage example, next steps

### Task 2: Create Repository Implementation
- Create file `.claude/commands/meta-prompt.md`
- Use identical content to the Jinja2 template (no template variables needed for this command)
- Ensure file is production-ready and immediately usable

### Task 3: Register Template in Scaffold Service
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- In `_add_claude_files` method, add to `commands` list:
  - Add `"meta-prompt"` to the commands array (after line 348, in the appropriate section)
- The existing loop will automatically register the template

### Task 4: Validation
- Run validation commands to ensure zero regressions
- Verify template file exists at correct path
- Verify implementation file exists at correct path
- Verify registration in scaffold_service.py
- Test template renders without errors
- Test generated command follows TAC standards

## Testing Strategy

### Unit Tests
- Template rendering test: Verify meta-prompt.md.j2 renders without errors
- Registration test: Verify template is included in scaffold plan
- File existence test: Verify both template and implementation files exist
- Content validation test: Verify generated commands have required sections

### Integration Tests
- End-to-end CLI test: Generate a new project and verify meta-prompt.md is created
- Command execution test: Use /meta-prompt to generate a sample command
- Validation test: Verify generated command follows TAC format

### Edge Cases
- Empty or minimal command description
- Complex multi-step workflow request
- Command requiring special tools or permissions
- Command with multiple variables

## Acceptance Criteria

1. Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`
2. Implementation file exists at `.claude/commands/meta-prompt.md`
3. Template is registered in `scaffold_service.py` commands list
4. Both files contain:
   - YAML frontmatter with allowed tools
   - Variables section with USER_PROMPT_REQUEST
   - Instructions explaining meta-prompt concept
   - 5-step workflow for command generation
   - Report format specification
5. Template renders without errors when CLI generates projects
6. Generated commands follow TAC format (frontmatter + variables + instructions + workflow + report)
7. All validation commands pass with zero regressions

## Validation Commands

Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- This is Task 13 in the TAC-13 roadmap (Phase 3: Meta-Agentics)
- The meta-prompt pattern is foundational for later tasks (meta-agent generator, expert orchestrator)
- The command uses Opus model for higher quality prompt generation
- Future enhancement: Add validation that generated commands follow TAC standards automatically
- The dual strategy enables both reusability (via templates) and immediate testing (via repo files)
- Consider adding examples of generated commands to documentation in future iterations
