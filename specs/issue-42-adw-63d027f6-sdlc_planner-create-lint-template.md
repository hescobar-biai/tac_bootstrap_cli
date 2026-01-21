# Feature: Create Template `lint.md.j2`

## Metadata
issue_number: `42`
adw_id: `63d027f6`
issue_json: `{"number":42,"title":"TAREA 1: Crear Template `lint.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/lint.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /lint.\n\nEste comando debe:\n1. Ejecutar el linter configurado en config.commands.lint\n2. Mostrar errores encontrados de forma clara\n3. Sugerir fixes automáticos si están disponibles\n\nUsa como referencia los templates existentes en:\n- tac_bootstrap/templates/claude/commands/test.md.j2\n- tac_bootstrap/templates/claude/commands/build.md.j2\n\nEl template debe usar las variables:\n- {{ config.project.name }}\n- {{ config.commands.lint }}\n- {{ config.project.language }}\n\nIncluye secciones para:\n- Descripción del comando\n- Pasos de ejecución\n- Manejo de errores\n- Output esperado\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Usa variables de config correctamente\n- [ ] Sigue el mismo formato que otros comandos"}`

## Feature Description
Create a new Jinja2 template for the `/lint` slash command that will be used by TAC Bootstrap to generate lint command files for target projects. This template will enable Claude agents to run linting tools and provide clear feedback about code quality issues.

The template is part of the TAC Bootstrap CLI system, which generates agentic layers for projects. This specific template will be rendered when users initialize or add agentic capabilities to their projects, providing them with a standardized `/lint` command.

## User Story
As a TAC Bootstrap user
I want to have a `/lint` command template in my generated agentic layer
So that Claude agents can run linting tools consistently and report code quality issues clearly

## Problem Statement
The TAC Bootstrap CLI needs to generate slash command files for target projects. Currently, there is no template for the `/lint` command, which is a critical command for maintaining code quality in agent-assisted development workflows.

Without this template:
- Users cannot have agents automatically run linting tools
- There's no standardized way for agents to report linting errors
- The generated agentic layer is incomplete

## Solution Statement
Create a Jinja2 template file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` that:

1. Follows the same structure and format as existing command templates (test.md.j2, build.md.j2)
2. Uses Jinja2 variables from the config object to render project-specific lint commands
3. Provides clear instructions for agents on how to run linters and report results
4. Handles cases where lint commands may not be configured
5. Includes sections for error handling and suggesting automatic fixes

The template will be rendered by the TemplateRepository infrastructure when generating agentic layers for target projects.

## Relevant Files
Files necessary for implementing this feature:

- `/Volumes/MAc1/Celes/tac_bootstrap/trees/1d5bb11f/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Reference template showing standard structure and format for test command
- `/Volumes/MAc1/Celes/tac_bootstrap/trees/1d5bb11f/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Reference template showing how to handle optional commands
- `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` - Shows how config structure defines commands.lint
- `/Volumes/MAc1/Celes/tac_bootstrap/PLAN_TAC_BOOTSTRAP.md` - Master plan context for understanding TAC Bootstrap architecture

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` - The new lint command template

## Implementation Plan

### Phase 1: Foundation
1. Study the existing command templates (test.md.j2 and build.md.j2) to understand:
   - File structure and markdown format
   - How Jinja2 variables are used
   - How conditional logic handles optional commands
   - The standard sections (Variables, Instructions, Report)

2. Review the config.yml structure to understand how `config.commands.lint` is defined and what other config variables should be available

### Phase 2: Core Implementation
1. Create the lint.md.j2 template file with:
   - Header and description
   - Variables section defining $ARGUMENTS
   - Instructions section with:
     - Command execution using {{ config.commands.lint }}
     - Conditional handling if lint command is not configured
     - Error analysis and reporting instructions
     - Guidance on suggesting automatic fixes
   - Report section with expected output format

2. Ensure the template matches the style and structure of existing command templates

### Phase 3: Integration
1. Verify the template file is in the correct location within the templates directory structure
2. Ensure the file follows naming conventions (.md.j2 extension)
3. Validate that Jinja2 syntax is correct and will render without errors

## Step by Step Tasks

### Task 1: Analyze Reference Templates
- Read `/Volumes/MAc1/Celes/tac_bootstrap/trees/1d5bb11f/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2`
- Read `/Volumes/MAc1/Celes/tac_bootstrap/trees/1d5bb11f/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`
- Identify common patterns, structure, and Jinja2 usage

### Task 2: Create lint.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
- Include all required sections:
  - Title: "Lint"
  - Description: "Run the linter to check code quality"
  - Variables section: document $ARGUMENTS parameter
  - Instructions section:
    - Execute lint command: `{{ config.commands.lint }} $ARGUMENTS`
    - Conditional check if lint command exists (like build.md.j2)
    - Instructions for analyzing lint errors
    - Instructions for suggesting automatic fixes when available
    - Note not to fix unless explicitly asked
  - Report section:
    - Lint status (passed/failed)
    - Number of errors/warnings
    - List of issues found
    - Suggested fixes if applicable

### Task 3: Verify Template Quality
- Check that all Jinja2 variables use correct syntax
- Ensure conditional logic is properly formatted
- Verify markdown formatting is consistent with other templates
- Confirm file uses correct variables from config object

### Task 4: Validate Implementation
- Run validation commands to ensure no regressions
- Verify the template file exists in the correct location
- Check that the template follows the same format as existing command templates

## Testing Strategy

### Unit Tests
While this task creates a template file (no unit tests for the template itself), validation will be done through:
- File existence check
- Template syntax validation (Jinja2 can render without errors)
- Comparison with reference templates to ensure consistency

### Edge Cases
- Lint command not configured (should show helpful message like build.md.j2)
- Empty $ARGUMENTS
- Lint command with various argument patterns

## Acceptance Criteria
- Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
- Template uses correct Jinja2 variable syntax: `{{ config.commands.lint }}`, `{{ config.project.name }}`, etc.
- Template follows the same structure and format as test.md.j2 and build.md.j2
- Template includes conditional handling for when lint command is not configured
- Template has clear sections: Variables, Instructions, Report
- Template includes instructions for error analysis and suggesting automatic fixes
- Template instructs agents not to auto-fix unless explicitly requested
- No syntax errors in Jinja2 template
- File uses .md.j2 extension following naming convention

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` - Verify file exists

## Notes
- This is a template creation task, not a code implementation task
- The template will be used by the TemplateRepository to generate lint commands for target projects
- The template should be simple and focused - it's a markdown file that agents will read as instructions
- Reference existing templates heavily to maintain consistency
- The actual lint command execution will happen in the target project, not in TAC Bootstrap itself
- This task is part of FASE 3 (Templates System) in the TAC Bootstrap roadmap
