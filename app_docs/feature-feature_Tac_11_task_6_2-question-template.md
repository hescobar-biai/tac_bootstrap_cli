---
doc_type: feature
adw_id: feature_Tac_11_task_6_2
date: 2026-01-27
idk:
  - jinja2
  - template
  - command
  - read-only
  - codebase-exploration
  - slash-command
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2
---

# Question Command Template for Generated Projects

**ADW ID:** feature_Tac_11_task_6_2
**Date:** 2026-01-27
**Specification:** specs/issue-341-adw-feature_Tac_11_task_6_2-sdlc_planner-question-template.md

## Overview

Created a Jinja2 template version of the `/question` slash command that enables generated projects to have a structured, read-only Q&A capability for exploring and understanding project structure, architecture, and documentation without file modifications.

## What Was Built

- Jinja2 template file for the `/question` command
- Read-only exploration workflow with 5-step structured process
- Comprehensive report formatting guidelines
- Safety constraints through instructional guidance

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`: New Jinja2 template created (91 lines) that mirrors the original `.claude/commands/question.md` implementation from Task 5 (PR #336)

### Key Changes

- Created fully static Jinja2 template with no dynamic variables (the command is generic and framework-agnostic)
- Preserved complete 5-step workflow:
  1. Analyze the Question - Scope determination
  2. Explore Project Structure - Git ls-files exploration
  3. Read Project Overview - Documentation files (README.md, CLAUDE.md, PLAN_*.md)
  4. Read Relevant Files - Configuration, source code, tests
  5. Synthesize Information - Structured response with evidence
- Maintained structured report format with sections: Answer, Supporting Evidence, Documentation References, Conceptual Explanation, Limitations
- Included safety notes emphasizing read-only constraints and tool limits
- Followed naming convention consistent with other command templates (*.md.j2)

## How to Use

Once a project is generated with TAC Bootstrap CLI, end users can invoke the question command:

1. Run the command with a question about the project:
```bash
/question "What is the project structure?"
```

2. The agent will follow the structured 5-step workflow to explore the codebase

3. The agent provides a formatted response with:
   - Direct answer (2-4 sentences)
   - Supporting evidence from files
   - Documentation references
   - Conceptual explanations
   - Explicit limitations if applicable

## Configuration

No configuration required. The template is fully static and will work in any generated project regardless of framework or language.

The read-only behavior is enforced through instructional constraints in the template rather than technical permissions (those are managed separately in settings.json).

## Testing

Verify the template file exists and has valid format:

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2
```

Run linting to ensure code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Run full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify CLI smoke test:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This template is part of TAC Bootstrap Task 6.2, completing the question command template implementation
- The original `.claude/commands/question.md` was created in Task 5 (PR #336, commit 7525c80)
- Unlike some other command templates, this one requires NO Jinja2 variables because the Q&A workflow is universal across all project types
- Read-only constraints are communicated through instructions rather than technical restrictions, following the pattern from the original implementation
- The template follows the same minimalist approach as `scout.md.j2`, which is also a generic exploration command
- Future generated projects will automatically include this command, enabling users to explore their codebase structure through an AI-guided Q&A workflow
