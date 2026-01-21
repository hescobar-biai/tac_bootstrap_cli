# Feature: Create lint.md.j2 Template

## Metadata
issue_number: `42`
adw_id: `e43f8346`
issue_json: `{"number":42,"title":"TAREA 1: Crear Template lint.md.j2","body":"**Archivo a crear:** tac_bootstrap/templates/claude/commands/lint.md.j2\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /lint.\n\nEste comando debe:\n1. Ejecutar el linter configurado en config.commands.lint\n2. Mostrar errores encontrados de forma clara\n3. Sugerir fixes automáticos si están disponibles\n\nUsa como referencia los templates existentes en:\n- tac_bootstrap/templates/claude/commands/test.md.j2\n- tac_bootstrap/templates/claude/commands/build.md.j2\n\nEl template debe usar las variables:\n- {{ config.project.name }}\n- {{ config.commands.lint }}\n- {{ config.project.language }}\n\nIncluye secciones para:\n- Descripción del comando\n- Pasos de ejecución\n- Manejo de errores\n- Output esperado\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Usa variables de config correctamente\n- [ ] Sigue el mismo formato que otros comandos"}`

## Feature Description
This task involves creating a Jinja2 template for the `/lint` slash command that will be generated when TAC Bootstrap creates an agentic layer for new projects. The template already exists in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`, so this is actually about verifying that the existing template is correct and meets all requirements.

The lint command template should:
- Execute the configured linter from `config.commands.lint`
- Display errors clearly
- Suggest automatic fixes when available
- Follow the same pattern as existing command templates (test.md.j2, build.md.j2)

## User Story
As a TAC Bootstrap user
I want a `/lint` command template that executes my project's linter
So that generated agentic layers can check code quality automatically

## Problem Statement
TAC Bootstrap needs to generate slash commands for projects it bootstraps. The `/lint` command is essential for maintaining code quality in agentic workflows. The template must be flexible enough to work with different programming languages and linting tools (ruff, eslint, etc.) while following a consistent format with other command templates.

## Solution Statement
Verify that the existing `lint.md.j2` template in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` is complete and follows the established patterns. The template should:
- Use Jinja2 variables from the `config` object
- Handle cases where no lint command is configured
- Provide clear instructions for error handling
- Format output consistently with other templates

## Relevant Files
Files necessary for implementing the feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` - The template file that already exists
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Reference template for pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Reference template for pattern
- `config.yml` - Shows the structure of config variables used in templates

### New Files
No new files need to be created - the template already exists.

## Implementation Plan

### Phase 1: Verification
Verify that the existing template meets all requirements from the issue.

### Phase 2: Testing
Test template rendering to ensure it works correctly with various configurations.

### Phase 3: Documentation
Document any findings or ensure the template is properly integrated.

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Verify existing template
- Read the existing `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` file
- Compare it against the reference templates (test.md.j2, build.md.j2)
- Verify it uses the correct config variables: `config.commands.lint`, `config.project.name`, `config.project.language`
- Confirm it has sections for: description, execution steps, error handling, output format

### Task 2: Test template rendering
- Create a minimal test to verify the template renders without errors
- Test with a config that has a lint command defined
- Test with a config where lint command is missing (should handle gracefully)
- Verify the rendered output matches expected format

### Task 3: Review acceptance criteria
- Confirm template renderizes without errors ✓
- Confirm template uses config variables correctly ✓
- Confirm template follows same format as other commands ✓

### Task 4: Run validation commands
- Execute all validation commands to ensure no regressions
- Verify linting passes
- Verify type checking passes
- Verify tests pass

## Testing Strategy

### Unit Tests
No specific unit tests needed for a template file, but should verify:
- Template syntax is valid Jinja2
- Template renders with sample config data
- Rendered output contains expected sections

### Edge Cases
- Config without `config.commands.lint` defined - should show "No lint command configured"
- Config with extra arguments in lint command
- Different language configurations (python, javascript, etc.)

## Acceptance Criteria
- [x] Template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
- [ ] Template renders without Jinja2 syntax errors
- [ ] Template correctly uses `{{ config.commands.lint }}` variable
- [ ] Template includes conditional check for when lint command is not configured
- [ ] Template follows same structure as test.md.j2 and build.md.j2 (Variables, Instructions, Report sections)
- [ ] Template provides clear error handling instructions
- [ ] Template specifies expected output format

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The template already exists and appears to be correctly implemented based on the file read
- This task is primarily verification rather than creation
- The existing template follows the same pattern as test.md.j2 and build.md.j2
- The template correctly uses conditional rendering for when lint command is not configured
- Consider adding a test to verify all command templates render correctly as part of the test suite
