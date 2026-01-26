# Feature: Add concise-ultra.md.j2 Output Style Template

## Metadata
issue_number: `234`
adw_id: `feature_Tac_9_task_3`
issue_json: `{"number":234,"title":"Add concise-ultra.md.j2 output style template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_3\n\n**Description:**\nCreate Jinja2 template for the \"concise-ultra\" output style. This style limits responses to under 50 tokens for maximum efficiency.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/output-styles/concise-ultra.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/output-styles/concise-ultra.md` (CREATE - rendered)\n\n"}`

## Feature Description

Create a Jinja2 template for the "concise-ultra" output style that enforces maximum response brevity (targeting under 50 tokens). This style extends the proven "concise-done" pattern with more aggressive constraints on response length, making it ideal for high-frequency repetitive operations, batch processing, and agentic workflows where token efficiency is critical.

The concise-ultra style represents an elevation of concise-done: where concise-done uses brief confirmations with minimal detail, concise-ultra uses single-word or single-phrase responses with zero explanation unless critical. This style includes intelligent exception handling for errors and security-critical information that legitimately require exceeding the 50-token target.

## User Story

As a **TAC Bootstrap developer**
I want to **provide a concise-ultra output style template for generated projects**
So that **agents can operate at maximum efficiency when performing batch operations, repetitive tasks, and high-frequency interactions that prioritize token consumption over detailed explanations**

## Problem Statement

The TAC Bootstrap CLI currently provides only the "concise-done" output style, which aims for brevity but doesn't explicitly target extreme efficiency. Projects requiring the most aggressive token optimization lack guidance on response patterns for ultra-condensed communication. The absence of a concise-ultra style prevents users from leveraging the maximum efficiency available in agentic workflows where every token matters.

Additionally, agents need clear guidance on when ultra-brief responses are appropriate versus when they must exceed the 50-token limit (e.g., error explanations, security information, critical context). Without explicit exception handling documented, agents may either truncate important information or respond more verbosely than necessary.

## Solution Statement

Implement a new "concise-ultra" output style template that:

1. **Follows the established pattern** of static Jinja2 templates (`.md.j2` extension) without variable substitution, maintaining consistency with concise-done
2. **Extends the concise-done structure** (Response Guidelines → When to Use → Examples → Important Notes) while escalating the brevity constraints
3. **Provides explicit 50-token soft guidance** rather than hard constraints, allowing intelligent behavior
4. **Demonstrates single-word/phrase responses** through examples showing minimal confirmations: "Done.", "Created.", "Fixed.", "Error: X"
5. **Includes intelligent exception carve-outs** for errors, security information, critical context, and clarification questions
6. **Clarifies use cases** emphasizing batch operations, polling loops, and repetitive workflows where speed matters most
7. **Creates both files** as per the two-file strategy:
   - Source template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2`
   - Rendered reference: `.claude/output-styles/concise-ultra.md`

## Relevant Files

### Existing Reference Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Pattern reference for template structure
- `.claude/output-styles/concise-done.md` - Rendered output style reference
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering engine
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that deploys templates
- `specs/issue-233-adw-feature_Tac_9_task_2-sdlc_planner-concise-done-output-style.md` - Previous task documentation

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2` - Template source
- `.claude/output-styles/concise-ultra.md` - Rendered reference copy

## Implementation Plan

### Phase 1: Foundation
Review existing concise-done template and understand the output style pattern. This ensures consistency and identifies the exact structure, tone, and format to replicate for concise-ultra.

### Phase 2: Core Implementation
Create the concise-ultra template with escalated brevity constraints while maintaining structural consistency. Content emphasizes single-word responses, explicit token limits as soft guidelines, and intelligent exception handling.

### Phase 3: Validation
Create the rendered reference copy in `.claude/output-styles/` and verify both files are consistent. Run validation commands to ensure no regressions and proper integration with the CLI.

## Step by Step Tasks

### Task 1: Create concise-ultra.md.j2 Template
Create the source template file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2` with the following structure:

1. **Header**: "# Concise Ultra Output Style" with brief introduction explaining the style targets under 50 tokens
2. **Response Guidelines section**:
   - Emphasize single-word or single-phrase responses (e.g., "Done.", "Created.", "Fixed.")
   - Explain that explanations are deferred to follow-up queries
   - Guide on achieving brevity: minimal confirmations, one-word responses where safe
   - Include note that correctness trumps brevity when needed
3. **When to Use This Style section**:
   - High-frequency repetitive operations
   - Batch processing and polling loops
   - Agentic workflows prioritizing token efficiency
   - Tasks where confirmation matters more than detail
4. **Example Responses section**:
   - Show good examples under 50 tokens: "Done.", "Created: file.txt", "Fixed.", "Error: X"
   - Show avoid examples: verbose alternatives explaining what was done
5. **Important Notes section**:
   - Explicit 50-token soft guideline (not hard constraint)
   - Exception carve-outs for errors, security info, critical context, clarification
   - Note about agentic workflow optimization
   - Clarify this affects output only, not thinking/analysis

- File structure and content must match concise-done pattern (static Markdown, no variable substitution)
- Total expected length: 40-50 lines (slightly longer than concise-done to accommodate ultra-specific guidance)
- Use same formatting as concise-done (headers, bullet points, examples with ✓ and ✗ markers)

### Task 2: Create .claude/output-styles/concise-ultra.md Rendered Copy
Create the rendered reference file at `.claude/output-styles/concise-ultra.md`:

1. Copy the exact content from the template created in Task 1
2. File should be identical to the `.j2` template (since no variable substitution occurs)
3. Verify both files match exactly

### Task 3: Validate Files and Integration
Execute validation to confirm proper integration:

1. Verify both files exist and contain identical content
2. Confirm file naming follows kebab-case convention (concise-ultra, not concise_ultra)
3. Verify no Jinja2 template syntax errors in `.j2` file
4. Run lint and type checks on related Python files (if any changes to scaffold_service.py)
5. Execute smoke test to ensure CLI still functions

**Validation Commands:**
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2` - Verify template created
- `ls -la .claude/output-styles/concise-ultra.md` - Verify rendered file created
- `diff tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2 .claude/output-styles/concise-ultra.md` - Verify files match
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Lint check
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI

## Testing Strategy

### Unit Tests
Existing test suite should continue passing. No new tests required since this is a static template file without code logic.

### Edge Cases
- Template file exists and is readable
- Rendered file content matches template exactly
- Markdown formatting is valid
- No Jinja2 syntax errors in template
- File permissions are appropriate (readable, not executable)

## Acceptance Criteria

- [ ] `concise-ultra.md.j2` template created in `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/`
- [ ] File contains all required sections: header, Response Guidelines, When to Use This Style, Example Responses, Important Notes
- [ ] Template follows established pattern from concise-done (static Markdown, no variable substitution)
- [ ] Content emphasizes single-word/phrase responses and explicit 50-token soft guideline
- [ ] Intelligent exception handling documented for errors, security info, and critical context
- [ ] `.claude/output-styles/concise-ultra.md` rendered copy created with identical content
- [ ] Both files match exactly (verified via diff)
- [ ] File naming uses kebab-case (concise-ultra)
- [ ] All validation commands pass with zero regressions
- [ ] `tac-bootstrap --help` executes successfully (smoke test)

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Verify files created
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2
ls -la .claude/output-styles/concise-ultra.md

# Verify files match
diff tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2 .claude/output-styles/concise-ultra.md

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

- **Template Pattern**: This is a static Markdown template using `.j2` extension for consistency with the templating system, even though no variable substitution occurs. This matches the pattern established by concise-done.
- **Two-File Strategy**: The template in `tac_bootstrap_cli/templates/` is the source of truth; the rendered copy in `.claude/output-styles/` is a distributed reference for agents to read without running the generator.
- **No Code Changes Required**: This feature only adds new template files. No modifications to Python code (scaffold_service.py, template_repo.py, etc.) are necessary.
- **Future Integration**: Once this template exists, it can be integrated into scaffold_service.py to automatically deploy concise-ultra to generated projects (separate task).
- **Content Guidance**: The auto-resolved clarifications provided detailed specifications for concise-ultra content, including 50-token soft limit, exception carve-outs, and emphasis on batch/repetitive operations. Follow these specifications closely.
- **Consistency**: Mirror the structure and formatting of concise-done.md.j2 to maintain visual and organizational consistency across output styles.
