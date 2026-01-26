# Feature: Add quick-plan.md.j2 Command Template

## Metadata
issue_number: `264`
adw_id: `feature_Tac_9_task_23`
issue_json: `{"number":264,"title":"Add quick-plan.md.j2 command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_23\n\n**Description:**\nCreate Jinja2 template for `/quick-plan` slash command. Enables rapid implementation planning with architect pattern.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/quick-plan.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/quick-plan.md` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for the `/quick-plan` slash command that enables rapid implementation planning using an architect pattern. This command provides a streamlined version of planning workflows similar to `/feature` and `/bug` commands, allowing developers to quickly create concise implementation plans without extensive ceremony.

The template will be static (no variable substitution) and follow the established pattern from `prime_cc.md.j2`, serving as both a template for generated projects and a reference implementation for this repository.

## User Story
As a developer using TAC Bootstrap
I want to use the `/quick-plan` command
So that I can rapidly create concise implementation plans for straightforward development tasks without the overhead of full feature planning workflows

## Problem Statement
Currently, developers must use heavyweight planning commands like `/feature` or `/bug` which require extensive metadata and formal structure. For quick implementations or exploratory work, this overhead slows down the development flow. There's a need for a lightweight planning command that captures the essence of architect-driven planning while reducing ceremony.

## Solution Statement
Create a static Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` by copying the source content from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/quick-plan.md`. Additionally, render this template to `.claude/commands/quick-plan.md` in this repository for immediate dogfooding.

The template will:
- Be static with no Jinja2 variable substitution
- Follow the same structure as other command templates
- Enable rapid plan creation with minimal required fields
- Integrate seamlessly with the existing command ecosystem
- Support the architect pattern for structured planning

## Relevant Files
Files necessary for implementing the feature:

### Source Files
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/quick-plan.md` - Source command template to copy from
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Reference pattern for static templates

### Target Template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` (CREATE) - Template for generator

### Rendered Implementation
- `.claude/commands/quick-plan.md` (CREATE) - Rendered version for this repo

### Reference Files
- `.claude/commands/prime_cc.md` - Example of rendered static template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Example of command template structure

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` (CREATE)
- `.claude/commands/quick-plan.md` (CREATE)

## Implementation Plan

### Phase 1: Foundation
1. Read source file from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/quick-plan.md`
2. Verify it's valid markdown and follows command template structure
3. Understand the command's purpose and workflow

### Phase 2: Core Implementation
1. Create static Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
2. Copy content from source file exactly (no modifications)
3. Verify template structure matches other command templates

### Phase 3: Integration
1. Render template to `.claude/commands/quick-plan.md` for immediate use in this repo
2. Verify the rendered command is identical to the template (since it's static)
3. Test the command is discoverable in Claude Code interface

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and Validate Source File
- Read source file from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/quick-plan.md`
- Verify it contains valid markdown with frontmatter
- Verify it has the standard sections: Variables, Instructions, Report, etc.
- Confirm it follows the architect pattern for planning

### Task 2: Create Jinja2 Template
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` if it doesn't exist (it should)
- Write file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- Copy source content exactly as-is (no Jinja2 variables, no modifications)
- Verify file was created successfully

### Task 3: Render Template for This Repository
- Read the newly created template file
- Write rendered version to `.claude/commands/quick-plan.md`
- Since template is static, rendered content should be identical
- Verify file was created successfully

### Task 4: Validation and Testing
- Compare template and rendered files to ensure they're identical
- Verify markdown structure is valid
- Verify frontmatter is present and valid
- Check file permissions are correct (readable)
- Execute Validation Commands below

## Testing Strategy

### Unit Tests
No unit tests required for this feature as it's a static template file. Testing focuses on validation of file content and structure.

### Manual Verification
1. Template file exists at correct path
2. Rendered file exists at correct path
3. Both files are identical (since no variable substitution)
4. Files contain valid markdown with frontmatter
5. Command is discoverable in Claude Code (appears in command list)

### Edge Cases
- Verify template handles special characters in markdown correctly
- Ensure frontmatter YAML is valid
- Confirm no unintended Jinja2 syntax in content

## Acceptance Criteria
- [ ] Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- [ ] Rendered file exists at `.claude/commands/quick-plan.md`
- [ ] Both files contain identical content (static template)
- [ ] Content is valid markdown with valid YAML frontmatter
- [ ] Template follows the pattern established by `prime_cc.md.j2`
- [ ] No Jinja2 variables or logic in the template (pure static content)
- [ ] All validation commands pass with zero errors
- [ ] Command is discoverable in Claude Code interface

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2 && echo "Template exists" || echo "ERROR: Template missing"` - Verify template exists
- `test -f .claude/commands/quick-plan.md && echo "Rendered file exists" || echo "ERROR: Rendered file missing"` - Verify rendered file exists
- `diff tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2 .claude/commands/quick-plan.md && echo "Files identical (expected for static template)" || echo "Note: Files differ (expected if template has variables)"` - Compare files

## Notes

### Design Decisions
- **Static Template**: Following the clarifications, this template has no Jinja2 variables. It's a pure passthrough that will be identical across all generated projects.
- **Dogfooding**: Creating the rendered version in `.claude/commands/` allows this repository to immediately use the command, following the pattern where tac_bootstrap both generates and uses these templates.
- **Pattern Consistency**: Following the `prime_cc.md.j2` pattern which demonstrates how static templates should be structured.

### Future Considerations
- If future requirements demand project-specific customization, variables like `config.project.name` or `config.paths.specs_dir` could be added
- Consider adding template validation to the generator CLI to ensure all command templates are valid markdown
- May want to add a test suite that validates all command templates can be rendered successfully

### Dependencies
No new dependencies required. Uses existing Jinja2 templating infrastructure.

### Related Issues
This is part of Phase 9 (TAC_9) which focuses on creating command templates for the generator CLI. Related tasks include creating templates for other slash commands like `/prime_cc`, `/feature`, `/bug`, etc.
