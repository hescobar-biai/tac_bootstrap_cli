# Feature: Create scout.md.j2 Template

## Metadata
issue_number: `340`
adw_id: `feature_Tac_11_task_4`
issue_json: `{"number":340,"title":"Create scout.md.j2 template","body":"feature\n/adw_sdlc_iso\n/adw_id: feature_Tac_11_task_4\n\nCreate the Jinja2 template version of the /scout command for generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2`\n\n**Implementation details:**\n- Mirror the implementation from Task 3\n- Add template variables for customization if needed"}`

## Feature Description
Create the Jinja2 template version of the `/scout` command that will be included in generated TAC Bootstrap projects. This template will convert the existing `.claude/commands/scout.md` file into a reusable Jinja2 template (scout.md.j2) that can be customized for different project configurations.

The `/scout` command implements parallel codebase exploration using multiple search strategies to identify relevant files for a given task. It's a TAC-10 Level 4 (Delegation Prompt) pattern that launches multiple exploration agents in parallel.

## User Story
As a TAC Bootstrap CLI user
I want the generated projects to include the `/scout` command template
So that generated projects can use parallel codebase exploration functionality out of the box

## Problem Statement
Currently, the `/scout` slash command exists in the base TAC Bootstrap repository at `.claude/commands/scout.md`, but there is no corresponding Jinja2 template version that can be included when generating new projects via the TAC Bootstrap CLI. This means generated projects lack the powerful parallel codebase exploration capability.

## Solution Statement
Convert the existing `.claude/commands/scout.md` file into a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2`. Follow the same conversion pattern established in Task 3 for other command templates:

1. Keep all scout command content static (search strategies, workflow, instructions)
2. Only inject `{{ config.project.name }}` where project-specific references occur
3. No scout-specific configuration options needed (YAGNI principle)
4. Scout methodology is universal and works across all project types

## Relevant Files
Files necessary for implementing this feature:

- `.claude/commands/scout.md` - Source file to convert to template (510 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Reference template showing Jinja2 conversion pattern with `{{ config.project.name }}`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/start.md.j2` - Reference template showing conditional logic patterns
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config schema (no changes needed, existing schema sufficient)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2` - New Jinja2 template for scout command

## Implementation Plan

### Phase 1: Analysis
Study the source scout.md file and identify where project-specific template variables should be injected (primarily project name references).

### Phase 2: Template Conversion
Convert scout.md to scout.md.j2 following the established pattern:
1. Copy the complete scout.md content as base
2. Replace any project name references with `{{ config.project.name }}`
3. Maintain all static content (strategies, workflow, examples, instructions)
4. Ensure all markdown formatting and structure remains intact

### Phase 3: Validation
Verify the template follows conventions and will render correctly when the CLI generates projects.

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Read Source File
- Read `.claude/commands/scout.md` completely
- Identify any project-specific references that need templating
- Confirm overall structure and content to preserve

### Task 2: Create scout.md.j2 Template
- Create new file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2`
- Copy all content from `.claude/commands/scout.md`
- Replace project-specific references with `{{ config.project.name }}` (likely minimal occurrences)
- Keep all 510 lines of content static except for template variables
- Preserve all:
  - Variables section ($1, $2, SCALE)
  - Instructions and purpose documentation
  - All 9+ search strategy definitions
  - Complete workflow (Steps 1-10)
  - Report format and examples
  - Notes, limitations, best practices
  - Integration notes and troubleshooting

### Task 3: Verify Template Quality
- Review the created template against reference templates (test.md.j2, start.md.j2)
- Ensure Jinja2 syntax is correct
- Verify no content was accidentally removed
- Confirm static content remains unchanged
- Check that template variables are minimal and follow YAGNI

### Task 4: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
No new unit tests required for this task. Existing template rendering tests in the test suite should cover the new scout.md.j2 template when they verify all templates render correctly.

### Manual Verification
After implementation:
1. Verify the scout.md.j2 file exists at the correct path
2. Confirm all 510 lines of content are preserved
3. Check that only minimal template variables were added
4. Ensure no extra configuration was added to config schema

### Edge Cases
- Empty project name: Template should still render (handled by existing config validation)
- Special characters in project name: Already handled by Jinja2 escaping
- Missing config values: Not applicable (only using existing config.project.name)

## Acceptance Criteria
- [ ] File `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2` exists
- [ ] Template contains all content from `.claude/commands/scout.md` (510 lines)
- [ ] Only `{{ config.project.name }}` template variable is used (minimal templating)
- [ ] No scout-specific config options were added to config schema
- [ ] All search strategies (file patterns, content search, architecture, dependencies, tests, config, types, docs, specialized) are preserved
- [ ] Complete workflow (Steps 1-10) is intact
- [ ] All examples, notes, limitations, and troubleshooting sections preserved
- [ ] Template follows the same conversion pattern as Task 3 templates
- [ ] All validation commands pass with zero errors

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions
- **Minimal templating**: Following YAGNI principle, only inject project name where it naturally appears
- **No scout-specific config**: Scout's exploration methodology is universal and doesn't need project-specific customization
- **Static strategies**: All search strategies (patterns, content, architecture, dependencies) remain unchanged as they work identically across project types
- **No new config schema**: Use existing `config.project.name` only, no need for `config.scout.*` options

### Why Scout Doesn't Need Heavy Customization
The `/scout` command is fundamentally a codebase exploration tool that uses universal search strategies:
- File pattern matching works the same for Python, TypeScript, Go, etc.
- Content search (grep) is language-agnostic
- Architectural analysis adapts to whatever structure exists
- Dependency mapping works across all languages

Adding project-specific customization would add complexity without clear benefit. The command's self-adapting nature makes templating unnecessary beyond basic project name injection.

### Future Considerations
If actual need emerges in the future, could consider:
- `config.scout.default_scale` - Override default SCALE value
- `config.scout.output_dir` - Customize output directory location
- `config.scout.excluded_dirs` - Additional directories to skip

However, these should only be added when users report specific needs (not speculatively).

### Implementation Pattern Consistency
This task follows the exact same pattern established in Task 3:
1. Read existing `.md` file
2. Identify minimal template variable needs
3. Convert to `.md.j2` with Jinja2 syntax
4. Preserve all static content
5. No config schema changes
6. Validate with existing test suite
