# Feature: Create question.md.j2 Template

## Metadata
issue_number: `341`
adw_id: `feature_Tac_11_task_6`
issue_json: `{"number":341,"title":"Create question.md.j2 template","body":"feature\n/adw_sdlc_iso\n/adw_id: feature_Tac_11_task_6\n\nCreate the Jinja2 template version of the /question command for generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`\n\n**Implementation details:**\n- Mirror the implementation from Task 5\n- Use read-only tool restrictions"}`

## Feature Description
Create a Jinja2 template version of the `/question` command that will be used to generate the command for projects created by the TAC Bootstrap CLI. This template will enable generated projects to have a read-only Q&A capability for exploring project structure, architecture, and documentation. The template should convert the existing `.claude/commands/question.md` file (created in Task 5 / issue-329) to Jinja2 format while maintaining its complete functionality.

## User Story
As a TAC Bootstrap CLI user
I want the `/question` command to be automatically generated in my project
So that I can use read-only Q&A to explore and understand my project structure without making any modifications

## Problem Statement
The `/question` command currently exists in the TAC Bootstrap project itself (`.claude/commands/question.md`), but generated projects need their own version created from a Jinja2 template. Without this template, users of generated projects won't have access to the powerful read-only Q&A functionality that helps them understand their codebase through natural language queries.

## Solution Statement
Convert the existing `.claude/commands/question.md` file to a Jinja2 template (`question.md.j2`) that can be rendered during project generation. Since the `/question` command is inherently generic and discovers project structure dynamically through git operations, the template will be largely static with minimal to no project-specific configuration variables. This approach preserves the command's flexibility while ensuring it works correctly for any generated project.

## Relevant Files

### Existing Files
- `.claude/commands/question.md` - Source implementation from Task 5 (92 lines, read-only Q&A with 5-step workflow)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Example template showing Jinja2 patterns with config variables
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/*.j2` - 38+ existing command templates for reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` - New template to be created

## Implementation Plan

### Phase 1: Analysis
Review the source `.claude/commands/question.md` file to understand its structure, workflow, and whether any parts require project-specific customization through Jinja2 variables.

### Phase 2: Template Creation
Create `question.md.j2` by converting the source file to Jinja2 format. Keep the template largely static since the command is inherently generic. The command's power comes from its dynamic git-based exploration, not from static configuration.

### Phase 3: Validation
Ensure the template is valid Jinja2 that will render to valid markdown matching the structure and functionality of the original `question.md` file.

## Step by Step Tasks

### Task 1: Read Source Implementation
- Read `.claude/commands/question.md` to understand the complete 5-step workflow
- Identify the command structure: Variables, Instructions, Report format
- Note the read-only safety constraints and git-based exploration approach
- Verify there are no project-specific references that need Jinja2 variables

### Task 2: Create Jinja2 Template
- Create new file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`
- Copy the complete content from `.claude/commands/question.md`
- Keep the template static (no config variables needed) since:
  - The command uses generic git operations (ls-files) that work for any project
  - The workflow (analyze → explore → read docs → read files → synthesize) is universal
  - Read-only restrictions don't depend on project configuration
  - The command's flexibility comes from runtime discovery, not static config
- Ensure all markdown formatting, code blocks, and structured sections are preserved exactly
- Verify Jinja2 syntax is valid (even for a static template, it should parse cleanly)

### Task 3: Verify Template Structure
- Confirm the template includes all sections from the original:
  - Title and description
  - Variables section (QUESTION: $ARGUMENTS)
  - Instructions with 5-step workflow
  - Guidance Notes
  - Report format with structured output
  - Safety Notes
- Ensure line count and content match the original (92 lines)
- Verify all code examples and bash snippets are intact

### Task 4: Validation
- Run validation commands to ensure no regressions
- Confirm the template file is properly located in the templates directory
- Verify the template would render correctly for generated projects

## Testing Strategy

### Unit Tests
No pytest tests required - this is a command definition file (markdown template), not executable code. The template system itself will validate rendering.

### Edge Cases
- Template must render valid markdown for any project type
- Git operations in the template work regardless of project language or framework
- Read-only constraints are inherent to the command instructions, not configuration-dependent

### Manual Verification
- Visually inspect the template to ensure it matches the source file
- Confirm all sections are present and properly formatted
- Verify Jinja2 syntax is valid (no unclosed tags or invalid expressions)

## Acceptance Criteria
- [ ] File `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` exists
- [ ] Template content matches `.claude/commands/question.md` structure exactly (92 lines)
- [ ] All 5 workflow steps are present and complete
- [ ] Variables section defines QUESTION: $ARGUMENTS
- [ ] Instructions include read-only constraints and git exploration guidance
- [ ] Report format includes all sections: Answer, Supporting Evidence, Documentation References, Conceptual Explanation, Limitations
- [ ] Safety Notes emphasize read-only mode with no modifications allowed
- [ ] Template is valid Jinja2 (parses without errors)
- [ ] Template is largely static with no unnecessary config variables
- [ ] All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The `/question` command is inherently generic and discovers project structure dynamically via git ls-files
- Unlike `/prime` which uses many config variables (project.name, project.language, commands.*, etc.), `/question` requires minimal to no customization
- The command's power comes from runtime exploration, not static configuration
- Keeping the template static preserves flexibility and ensures it works for any project type
- This follows the pattern established in Task 5 (issue-329) which created the original `.claude/commands/question.md`
- The template enables read-only Q&A for all generated projects, providing a safe exploration tool
