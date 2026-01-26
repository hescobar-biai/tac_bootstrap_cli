# Feature: Add concise-done.md.j2 output style template

## Metadata
issue_number: `233`
adw_id: `feature_Tac_9_task_2`
issue_json: `{"number":233,"title":"Add concise-done.md.j2 output style template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_2\n\n\n**Description:**\nCreate Jinja2 template for the \"concise-done\" output style. This style instructs Claude to respond with minimal \"Done.\" confirmations, reducing output tokens significantly.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/output-styles/concise-done.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/output-styles/concise-done.md` (CREATE - rendered)\n"}`

## Feature Description

Create a Jinja2 template for the "concise-done" output style. This output style provides Claude with instructions to minimize output by responding with brief "Done." confirmations rather than verbose explanations. This significantly reduces token usage while maintaining effective task completion communication.

The feature involves:
1. Creating a static Markdown template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2`
2. Creating the rendered output at `.claude/output-styles/concise-done.md` for reference/distribution

## User Story

As a TAC Bootstrap developer
I want to have a concise-done output style template
So that generated projects can instruct Claude to minimize confirmations and reduce token consumption

## Problem Statement

The "concise-done" output style is needed to optimize Claude's response patterns. Currently, there is no template for this output style. When Claude agents are instructed to minimize output tokens, they should respond with minimal confirmations ("Done." or brief status updates) rather than verbose explanations. This requires an output style instruction file that communicates this behavior to Claude.

## Solution Statement

Create a static Markdown file that serves as an output style instruction. The file will:
- Be a Jinja2 template with no variable substitution (static content)
- Contain clear, actionable prose instructions for Claude's behavior
- Guide Claude to respond with minimal "Done." confirmations
- Be placed in the template directory for scaffolding
- Be rendered to `.claude/` for project distribution/reference

The template follows the existing project pattern where `.j2` files in `tac_bootstrap_cli/tac_bootstrap/templates/` are rendered and placed in `.claude/` directories.

## Relevant Files

### Existing Related Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/` - Directory for output style templates
- `.claude/output-styles/` - Directory for rendered output styles
- `.claude/commands/` - Similar instruction files for reference (e.g., document.md, implement.md)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Jinja2 template (CREATE)
- `.claude/output-styles/concise-done.md` - Rendered output style file (CREATE)

## Implementation Plan

### Phase 1: Foundation
- Understand the output-styles directory structure
- Review existing instruction files in `.claude/commands/` to understand prose/instruction format
- Understand that output-style templates are static (no Jinja2 variables)

### Phase 2: Core Implementation
- Create the Jinja2 template with Markdown-formatted instructions
- Instructions should guide Claude to:
  - Use minimal output (brief confirmations)
  - Respond with "Done." or short status messages
  - Avoid verbose explanations unless specifically asked
  - Focus on reducing token consumption
- Render the template to `.claude/output-styles/concise-done.md`

### Phase 3: Integration
- Ensure both files are created in correct locations
- Verify the template renders correctly (no Jinja2 errors)
- Validate file permissions and git staging

## Step by Step Tasks

### Task 1: Create the Jinja2 template
- Create file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2`
- Write Markdown prose instructions that:
  - Explain the purpose of the concise-done output style
  - Provide clear guidance on minimal responses
  - Use natural language Claude understands
  - Keep instructions focused and actionable
- Template should be static (no Jinja2 variables like `{{ config.* }}`)

### Task 2: Render the template to .claude/
- Create file: `.claude/output-styles/concise-done.md`
- Content should be identical to the template (since no variable substitution)
- This file serves as the distributed reference copy for agents to read

### Task 3: Validate creation
- Verify both files exist and are readable
- Check that template has no syntax errors
- Confirm content is appropriate Markdown with clear instruction prose
- Ensure file permissions allow reading by the project

## Testing Strategy

### Content Validation
- Verify template file contains valid Markdown syntax
- Confirm prose instructions are clear and actionable
- Check that both files have identical content (no variables)

### Integration Validation
- Verify files can be read from their respective locations
- Check that Jinja2 rendering produces valid output (no errors)
- Ensure git can track and display the files

### Edge Cases
- Template rendering should be idempotent (static content)
- File permissions should allow reading by all project participants

## Acceptance Criteria
- [ ] Jinja2 template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2`
- [ ] Rendered file created at `.claude/output-styles/concise-done.md`
- [ ] Both files contain clear, actionable Markdown instructions for minimal responses
- [ ] Template contains no Jinja2 variables
- [ ] Files are valid Markdown with proper formatting
- [ ] Content explains the concise-done output style clearly
- [ ] Files are readable and correctly staged in git

## Validation Commands
Run these commands to validate with zero regressions:

- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 && echo "Template file exists"` - Verify template creation
- `test -f .claude/output-styles/concise-done.md && echo "Rendered file exists"` - Verify rendered file
- `diff tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 .claude/output-styles/concise-done.md || echo "Files differ (expected for static content)"` - Verify content consistency
- `file tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 | grep -q text && echo "Template is text file"` - Verify file type
- `wc -l tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Verify template is populated

## Notes

### Key Considerations
- Output-style templates are static instruction files, not configuration templates
- The `.j2` extension is used for consistency with the templating system, but no variable substitution occurs
- These files serve as system prompts/instructions for Claude behavior
- The rendered copy in `.claude/` allows agents to read the actual output style without running the generator

### Future Enhancements
- If additional output styles are needed (e.g., verbose, structured, etc.), follow this same pattern
- If test infrastructure is added for templates, tests can be added retroactively
- Consider creating a registry of available output styles once multiple styles exist

### Context
- This is part of TAC Bootstrap Task 9, which implements output-styles infrastructure
- Follows the pattern established by previous output-style creation (e.g., previous tasks in this feature)
- Templates in `tac_bootstrap_cli/` are sources; rendered files in `.claude/` are distributions
