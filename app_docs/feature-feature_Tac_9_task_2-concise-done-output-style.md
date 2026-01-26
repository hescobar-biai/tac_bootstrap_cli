---
doc_type: feature
adw_id: feature_Tac_9_task_2
date: 2026-01-25
idk:
  - output-styles
  - jinja2-templates
  - token-efficiency
  - claude-instructions
  - concise-responses
tags:
  - feature
  - output-styles
  - templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2
  - .claude/output-styles/concise-done.md
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
---

# Add Concise-Done Output Style Template

**ADW ID:** feature_Tac_9_task_2
**Date:** 2026-01-25
**Specification:** specs/issue-233-adw-feature_Tac_9_task_2-sdlc_planner-concise-done-output-style.md

## Overview

This feature creates a Jinja2 template for the "concise-done" output style that instructs Claude to minimize output by responding with brief confirmations. The output style reduces token consumption significantly in agentic workflows while maintaining effective communication of task completion.

## What Was Built

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Jinja2 template for concise-done output style instructions
- `.claude/output-styles/concise-done.md` - Rendered output style file for project distribution
- Updated ADW agent templates to refactor retry logic (removed model fallback chain)
- Removed unused fallback model configuration from domain models

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` (new): Static Markdown template with clear instructions for minimal response output
- `.claude/output-styles/concise-done.md` (new): Rendered reference copy identical to template
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`: Refactored `prompt_claude_code_with_retry()` function, removed `is_quota_exhausted_error()` and `get_fallback_model()` helper functions, removed model fallback chain logic
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`: Updated related imports
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Removed unused `fallback` field from `ModelPolicy` configuration class

### Key Changes

1. **Static Output Style Template**: Created a Markdown file with Jinja2 extension that contains no variable substitution - serves as static instruction content for Claude behavior

2. **Response Guidelines**: Template clearly instructs Claude to:
   - Use minimal confirmations ("Done." or brief status updates)
   - Avoid verbose explanations unless requested
   - Reduce token consumption through concise responses
   - Use one-line confirmations when possible
   - Only provide details on errors or issues

3. **Usage Context**: Template explains when to apply concise-done style:
   - Repetitive tasks needing confirmation but not explanation
   - Multiple sequential operations where verbosity is wasteful
   - Agentic workflows prioritizing token efficiency
   - Tasks not requiring detailed reasoning

4. **Refactored Agent Retry Logic**: Simplified `prompt_claude_code_with_retry()` by:
   - Removing model fallback chain (opus → sonnet → haiku)
   - Removing quota exhaustion detection logic
   - Removing unused fallback model field from configuration
   - Maintaining core retry logic with exponential backoff

5. **Two-File Strategy**: Template exists in both locations:
   - Template source in `tac_bootstrap_cli/tac_bootstrap/templates/` for scaffolding
   - Rendered copy in `.claude/` for agent distribution and reference

## How to Use

The concise-done output style is designed to be included in Claude Code settings and instruction files:

1. **Enable in Settings**: Add `concise-done` to the project's output style configuration
2. **Reference in Instructions**: Include the output style in `.claude/settings.json` or Claude Code configuration
3. **Apply to Workflows**: Use in agentic workflows that perform repetitive tasks requiring confirmation but not verbose explanation
4. **Token Optimization**: Apply when running multiple sequential operations where token efficiency is critical

Example usage in instructions:

```
Load the concise-done output style from .claude/output-styles/concise-done.md
Apply this style to minimize Claude's responses to brief confirmations
```

## Configuration

The output style is static Markdown content with no configuration required. It works with any Claude Code project that includes the `.claude/output-styles/` directory.

## Testing

Verify the feature implementation with these commands:

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 && echo "✓ Template file exists"
```

```bash
test -f .claude/output-styles/concise-done.md && echo "✓ Rendered file exists"
```

```bash
diff tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 .claude/output-styles/concise-done.md && echo "✓ Files match (expected for static content)"
```

```bash
wc -l tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2 .claude/output-styles/concise-done.md
```

Verify content includes expected sections:

```bash
grep -q "Response Guidelines" .claude/output-styles/concise-done.md && echo "✓ Response Guidelines section present"
```

```bash
grep -q "Example Responses" .claude/output-styles/concise-done.md && echo "✓ Example Responses section present"
```

## Notes

### Key Considerations

- Output-style templates are static instruction files that don't use Jinja2 variable substitution
- The `.j2` extension maintains consistency with the templating system even though no variable substitution occurs
- These files serve as system prompts that communicate behavior expectations to Claude
- The rendered copy in `.claude/` allows agents to read output styles without running the generator

### Integration with Agent System

The concise-done output style works alongside the refactored retry logic in `agent.py.j2`:
- Retry logic now focuses on core exponential backoff and connection handling
- Model fallback complexity was removed to simplify maintenance
- Output style provides instruction-level guidance on response minimization
- Token efficiency is achieved through both response style and retry simplification

### Related Output Styles

This feature establishes the pattern for output styles in TAC Bootstrap:
- Static Markdown instruction files
- Jinja2 template naming for consistency
- Dual-location strategy (template source + rendered reference)
- Clear use case guidance in content

### Future Enhancements

- Additional output styles (verbose, structured, debug) following this pattern
- Output style registry documenting available styles and use cases
- Integration with `.claude/settings.json` for automatic style loading
- Template validation tests for output style Markdown syntax
