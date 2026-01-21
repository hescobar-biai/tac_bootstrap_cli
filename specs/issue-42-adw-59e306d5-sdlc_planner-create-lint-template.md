# Feature: Create Template for /lint Command

## Metadata
issue_number: `42`
adw_id: `59e306d5`
issue_json: `{"number":42,"title":"TAREA 1: Crear Template `lint.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/lint.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /lint.\n\nEste comando debe:\n1. Ejecutar el linter configurado en config.commands.lint\n2. Mostrar errores encontrados de forma clara\n3. Sugerir fixes automáticos si están disponibles\n\nUsa como referencia los templates existentes en:\n- tac_bootstrap/templates/claude/commands/test.md.j2\n- tac_bootstrap/templates/claude/commands/build.md.j2\n\nEl template debe usar las variables:\n- {{ config.project.name }}\n- {{ config.commands.lint }}\n- {{ config.project.language }}\n\nIncluye secciones para:\n- Descripción del comando\n- Pasos de ejecución\n- Manejo de errores\n- Output esperado\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Usa variables de config correctamente\n- [ ] Sigue el mismo formato que otros comandos"}`

## Feature Description
Create a Jinja2 template for the `/lint` slash command that will be used by TAC Bootstrap CLI to generate lint commands for different project types. The template must follow the same structure and patterns as existing command templates (test.md.j2, build.md.j2) while providing linting-specific functionality including error reporting and auto-fix suggestions.

## User Story
As a TAC Bootstrap user
I want to have a `/lint` command available in my generated project
So that I can quickly run the configured linter, see errors clearly, and get suggestions for automatic fixes

## Problem Statement
The TAC Bootstrap CLI currently generates templates for various commands like `/test`, `/build`, `/start`, but lacks a template for the `/lint` command. Users need a standardized way to run linting tools that:
- Works consistently across different programming languages
- Executes the linter configured in `config.commands.lint`
- Presents errors in a clear, actionable format
- Suggests automatic fixes when the linter supports them
- Follows the same structure as other command templates for consistency

## Solution Statement
Create a new Jinja2 template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` that:
- Uses the existing command template structure (title, variables, instructions, report sections)
- Executes the configured lint command from `{{ config.commands.lint }}`
- Handles cases where no lint command is configured
- Provides clear instructions for analyzing and reporting lint errors
- Suggests automatic fixes when available (e.g., using `--fix` flag)
- Uses appropriate Jinja2 variables from the config model (`config.project.name`, `config.commands.lint`, `config.project.language`)

## Relevant Files

Existing command templates to use as reference:
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Test command template structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Build command template with conditional logic
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/start.md.j2` - Simple command template

Configuration model defining available variables:
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Lines 200-213 (CommandsSpec with lint field)
  - `config.commands.lint` (str, default="") - Command to run linter
  - `config.project.name` (str) - Project name
  - `config.project.language` (Language enum) - Programming language

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` - New template file for /lint command

## Implementation Plan

### Phase 1: Template Structure Design
Review existing command templates to understand the standard structure and patterns used.

### Phase 2: Template Creation
Create the lint.md.j2 template file following the established patterns with linting-specific content.

### Phase 3: Validation
Verify the template renders correctly and uses config variables properly.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review Existing Command Templates
- Read `test.md.j2` to understand basic command structure (27 lines)
- Read `build.md.j2` to understand conditional logic for optional commands (30 lines)
- Read `start.md.j2` to understand simple command structure (19 lines)
- Identify common patterns:
  - Title section (H1 heading)
  - Variables section (arguments)
  - Instructions section (numbered steps with bash code blocks)
  - Conditional logic using `{% if config.commands.X %}`
  - Error handling guidance
  - Report section (structured output format)

### Task 2: Review Config Model for Available Variables
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` lines 200-213 (CommandsSpec)
- Confirm available variables:
  - `config.commands.lint` (str, optional, default="")
  - `config.project.name` (str, required)
  - `config.project.language` (Language enum)

### Task 3: Create lint.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
- Follow the structure from existing templates:
  - Title: "# Lint"
  - Description: "Run the linter to check code quality and style."
  - Variables section: `$ARGUMENTS` for optional linter arguments
  - Instructions section with numbered steps:
    1. Check if lint command is configured (conditional)
    2. Run the lint command with arguments
    3. Analyze errors if any
    4. Suggest auto-fix if available (e.g., `--fix` flag)
    5. Do NOT attempt to fix unless explicitly asked
  - Report section with structured output:
    - Lint status (clean/errors/warnings)
    - Total issues found
    - List of errors/warnings
    - Auto-fix suggestions
- Use Jinja2 conditional: `{% if config.commands.lint %}` ... `{% else %}` ... `{% endif %}`
- Use template variables: `{{ config.commands.lint }}`, `{{ config.project.name }}`, `{{ config.project.language }}`
- Include helpful guidance about common linters per language
- Add clear error handling instructions

### Task 4: Verify Template Syntax
- Ensure Jinja2 syntax is correct
- Verify all variables exist in the config model
- Check that conditional blocks are properly closed
- Validate markdown formatting
- Ensure consistency with other command templates

### Task 5: Final Validation
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
The template will be tested as part of the existing template rendering tests:
- `tests/test_template_repo.py` - Template rendering with lint command configured
- `tests/test_template_repo.py` - Template rendering without lint command (empty string)
- `tests/test_scaffold_service.py` - Verify lint.md.j2 is included in generated commands

### Edge Cases
- No lint command configured (`config.commands.lint = ""`)
- Lint command with complex flags (e.g., `uv run ruff check . --fix --show-fixes`)
- Different programming languages (Python, TypeScript, JavaScript, Go, Rust, Java)
- Linter-specific features (auto-fix, format on save, ignore patterns)

## Acceptance Criteria
1. [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
2. [ ] Template follows same structure as test.md.j2 and build.md.j2
3. [ ] Uses `{{ config.commands.lint }}` variable correctly
4. [ ] Includes conditional logic for when lint command is not configured
5. [ ] Provides clear instructions for running linter and analyzing output
6. [ ] Suggests auto-fix when available
7. [ ] Includes proper error handling guidance
8. [ ] Uses markdown formatting consistent with other commands
9. [ ] All Jinja2 variables exist in CommandsSpec model
10. [ ] Template renders without errors
11. [ ] Follows the "do NOT fix unless asked" pattern from test.md.j2

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Template Structure Reference
Based on existing templates, the structure should be:

```markdown
# Lint

Run the linter to check code quality and style.

## Variables
- $ARGUMENTS: Optional linter arguments

## Instructions

1. Run the linter:
{% if config.commands.lint %}
   ```bash
   {{ config.commands.lint }} $ARGUMENTS
   ```
{% else %}
   No lint command configured for this project.
{% endif %}

2. If linter reports issues:
   - Analyze the error/warning output
   - Identify the root cause
   - Check if auto-fix is available (e.g., --fix flag)
   - Do NOT attempt to fix unless explicitly asked

3. Report results

## Report
- Lint status: clean/errors/warnings
- Total issues: X errors, Y warnings
- Issues: (list if any)
- Auto-fix available: yes/no
```

### Common Linters by Language
The template could reference common linters:
- **Python**: ruff, pylint, flake8, mypy (type checking)
- **TypeScript/JavaScript**: eslint, prettier, tsc (type checking)
- **Go**: golangci-lint, gofmt
- **Rust**: clippy, rustfmt
- **Java**: checkstyle, spotbugs, pmd

### Integration with ScaffoldService
The ScaffoldService should automatically include this template when building the plan:
- File will be discovered via template repository's `list_templates("claude/commands")`
- Rendered with the project's TACConfig
- Written to `.claude/commands/lint.md` in the target project

### No Code Changes Required
This task only involves creating a template file. No changes to:
- Domain models (CommandsSpec already has lint field)
- Application services (template discovery is automatic)
- Infrastructure (template rendering works for all .j2 files)
- Tests (existing tests cover template rendering)
