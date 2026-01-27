---
doc_type: feature
adw_id: feature_Tac_10_task_2
date: 2026-01-26
idk:
  - meta-prompt
  - prompt-generation
  - template-generator
  - jinja2
  - workflow
  - tac-framework
  - level-6-abstraction
tags:
  - feature
  - meta-prompt
  - template
related_code:
  - .claude/commands/t_metaprompt_workflow.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2
---

# Meta-Prompt Workflow Template

**ADW ID:** feature_Tac_10_task_2
**Date:** 2026-01-26
**Specification:** specs/issue-307-adw-feature_Tac_10_task_2-sdlc_planner-metaprompt-workflow-template.md

## Overview

Created a Level 6 meta-prompt generator that produces new prompts following TAC framework standards. The `t_metaprompt_workflow` command takes a high-level description and generates complete, well-structured prompts with frontmatter, variables, workflow steps, and report formats.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2` - Source template for TAC Bootstrap CLI generator
- **Rendered Command**: `.claude/commands/t_metaprompt_workflow.md` - Fully rendered version for direct use (dogfooding)
- **Documentation**: Comprehensive specification and checklist in `specs/` directory
- **Integration**: Template follows TAC framework standards with frontmatter, variables, workflow, and report sections

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2`: New Jinja2 template for the meta-prompt generator (301 lines)
- `.claude/commands/t_metaprompt_workflow.md`: New rendered command file for direct use (301 lines)
- `specs/issue-307-adw-feature_Tac_10_task_2-sdlc_planner-metaprompt-workflow-template.md`: Feature specification (177 lines)
- `specs/issue-307-adw-feature_Tac_10_task_2-sdlc_planner-metaprompt-workflow-template-checklist.md`: Implementation checklist (48 lines)

### Key Changes

- **Level 6 Meta-Prompt**: Implements TAC-10 abstraction hierarchy level 6 - a prompt that generates other prompts
- **Frontmatter Configuration**: Minimal frontmatter with `allowed-tools` (Write, Edit, WebFetch, Task) for prompt generation capabilities
- **Variable Definition**: Single `HIGH_LEVEL_PROMPT` variable capturing `$ARGUMENTS` for flexible input
- **Specified Format Template**: Comprehensive 4-section structure guide (Metadata, Variables, Workflow, Report) with guidelines for each section
- **Documentation Links**: References to 6 local command files demonstrating TAC patterns
- **Working Example**: Complete docstring validation prompt example showing the full generation process
- **Dual Nature**: Both Jinja2 template (.j2) for code generation and rendered file (.md) for direct usage

## How to Use

1. **Invoke the meta-prompt with your requirements:**
   ```bash
   /t_metaprompt_workflow Create a prompt for running E2E tests and reporting failures
   ```

2. **The agent will analyze your description and generate a complete prompt** following TAC standards with:
   - Appropriate frontmatter and allowed tools
   - Defined variables using `$1`, `$2`, or `$ARGUMENTS` syntax
   - 3-7 workflow steps with clear actions
   - Structured report format

3. **Review the generated prompt** which will be production-ready and follow the Specified Format Template.

4. **Save or integrate** the generated prompt into your `.claude/commands/` directory.

## Configuration

The meta-prompt uses minimal configuration:

- **Allowed Tools**: Write, Edit, WebFetch, Task
- **Input Variable**: `HIGH_LEVEL_PROMPT` = `$ARGUMENTS`
- **No Project Variables**: Template is generic and doesn't use project-specific Jinja2 variables

Template includes references to these local documentation files:
- `.claude/commands/feature.md`
- `.claude/commands/implement.md`
- `.claude/commands/test.md`
- `.claude/commands/review.md`
- `.claude/commands/commit.md`
- `.claude/commands/parallel_subagents.md`

## Testing

**Validate template syntax:**

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

**Check code quality:**

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

**Type checking:**

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

**Smoke test CLI:**

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

**Manual test (generate a sample prompt):**

```bash
# From repository root
/t_metaprompt_workflow Create a simple prompt for code formatting validation
```

## Notes

- **Meta-Prompt Concept**: A prompt whose output is another prompt, codifying best practices into a reusable generator
- **Level 6 TAC-10**: Highest abstraction level in the TAC framework for prompt generation
- **Dogfooding Pattern**: Both `.j2` template for generation and `.md` file for direct use in this repository
- **Specified Format Template**: Provides structure without being overly prescriptive, allowing flexibility
- **Generic Design**: No hard-coded project variables, making it reusable across different contexts
- **Simple Example**: Docstring validation example illustrates full format without overwhelming complexity
- **Naming Convention**: `t_` prefix indicates template generator command
- **Dual Purpose**: Serves as both reference documentation and functional code generator
