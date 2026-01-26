---
doc_type: feature
adw_id: feature_Tac_9_task_3
date: 2026-01-25
idk:
  - output-styles
  - jinja2-templates
  - token-efficiency
  - agentic-workflows
  - template-pattern
  - batch-operations
  - concise-ultra
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2
  - .claude/output-styles/concise-ultra.md
  - .claude/output-styles/concise-done.md
  - tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Concise Ultra Output Style Template

**ADW ID:** feature_Tac_9_task_3
**Date:** 2026-01-25
**Specification:** /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_9_task_3/specs/issue-234-adw-feature_Tac_9_task_3-sdlc_planner-concise-ultra-output-style.md

## Overview

Created a Jinja2 template for the "concise-ultra" output style, extending the proven "concise-done" pattern with more aggressive brevity constraints. This style enforces responses targeting under 50 tokens for maximum efficiency in batch operations, polling loops, and high-frequency agentic workflows where token efficiency is critical.

## What Was Built

- **concise-ultra.md.j2 template**: Source template in `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/` following the established static Markdown pattern
- **concise-ultra.md rendered copy**: Reference distribution file in `.claude/output-styles/` for agents to read without running the generator
- **Intelligent exception handling**: Clear carve-outs for errors, security information, critical context, and clarification questions that legitimately exceed the 50-token target
- **Response pattern guidance**: Emphasis on single-word/phrase confirmations ("Done.", "Created.", "Fixed.", "Error: X") with zero explanation unless critical

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2`: Created as source template with 50-line structure mirroring concise-done pattern
- `.claude/output-styles/concise-ultra.md`: Created as rendered reference copy with identical content (static template, no variable substitution)

### Key Changes

- Escalated brevity constraints compared to concise-done while maintaining structural consistency
- Defined explicit 50-token soft guideline (not hard constraint) with intelligent exception carve-outs
- Provided concrete examples of ultra-condensed responses: single words, minimal confirmations, error indicators
- Documented use cases emphasizing high-frequency repetitive operations, batch processing, polling loops, and agentic workflows
- Maintained two-file strategy: template source in generator (`tac_bootstrap_cli/`) and rendered distribution in project root (`.claude/`)

## How to Use

### For Generated Projects

Once integrated into the scaffold service, projects will receive the `.claude/output-styles/concise-ultra.md` file during generation. Agents in those projects can reference it for response patterns:

1. Read `.claude/output-styles/concise-ultra.md` to understand the style requirements
2. Apply single-word/phrase responses in batch operations and polling scenarios
3. Use exception carve-outs when providing error details, security information, or critical context
4. Target under 50 tokens while prioritizing correctness and safety

### For Template Maintenance

The template source is located at `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2`:

1. Modify the `.j2` template file as needed (this is the source of truth)
2. Keep the `.claude/output-styles/concise-ultra.md` copy synchronized with template changes
3. Follow the established pattern: static Markdown with `.j2` extension, no variable substitution

## Configuration

No configuration needed. This is a static template file that gets deployed to generated projects through the scaffold service. The template uses kebab-case naming (`concise-ultra`) consistent with other output styles.

## Testing

Verify the implementation with the following commands:

```bash
# Verify both files exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2
ls -la .claude/output-styles/concise-ultra.md
```

Verify files match exactly:

```bash
diff tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2 .claude/output-styles/concise-ultra.md
```

Run unit tests to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Lint and type check:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Template Pattern**: Static Markdown template using `.j2` extension for consistency with the templating system, even though no variable substitution occurs. Mirrors the pattern established by concise-done.
- **Two-File Strategy**: The template in `tac_bootstrap_cli/templates/` is the source of truth; the rendered copy in `.claude/output-styles/` is a distributed reference.
- **No Code Changes**: Feature only adds new template files. No modifications to Python code (scaffold_service.py, template_repo.py) required.
- **Future Integration**: Template is ready for integration into scaffold_service.py to automatically deploy concise-ultra to generated projects.
- **Exception Handling**: The 50-token limit is a soft guideline—errors, security information, critical context, and clarification questions explicitly allow exceeding this target.
- **Use Cases**: Designed for batch operations, polling loops, high-frequency repetitive operations, and agentic workflows where token efficiency is paramount.
