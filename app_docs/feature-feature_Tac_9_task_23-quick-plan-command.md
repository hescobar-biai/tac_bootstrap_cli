---
doc_type: feature
adw_id: feature_Tac_9_task_23
date: 2026-01-26
idk:
  - jinja2-template
  - slash-command
  - architect-pattern
  - implementation-planning
  - static-template
  - cli-generation
tags:
  - feature
  - command-template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2
  - .claude/commands/quick-plan.md
---

# Quick-Plan Command Template

**ADW ID:** feature_Tac_9_task_23
**Date:** 2026-01-26
**Specification:** specs/issue-264-adw-feature_Tac_9_task_23-sdlc_planner-quick-plan-command-template.md

## Overview

Created a Jinja2 template for the `/quick-plan` slash command that enables rapid implementation planning using an architect pattern. This command provides a streamlined version of planning workflows, allowing developers to quickly create concise implementation plans without extensive ceremony.

## What Was Built

- Static Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- Rendered command file at `.claude/commands/quick-plan.md` for immediate use in this repository
- Integration with existing TAC Bootstrap template generation system

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`: Created static Jinja2 template (no variable substitution)
- `.claude/commands/quick-plan.md`: Rendered version of the command for dogfooding in this repository
- `specs/issue-264-adw-feature_Tac_9_task_23-sdlc_planner-quick-plan-command-template.md`: Specification document
- `specs/issue-264-adw-feature_Tac_9_task_23-sdlc_planner-quick-plan-command-template-checklist.md`: Checklist document

### Key Changes

- **Static Template Pattern**: Following the `prime_cc.md.j2` pattern, this template contains no Jinja2 variables and is a pure passthrough template
- **Command Structure**: Includes YAML frontmatter with allowed tools (`Read, Write, Edit, Glob, Grep`), description, and model specification (`claude-opus-4-1-20250805`)
- **Architect Pattern**: The command guides the agent through requirement analysis, implementation planning, and structured documentation creation
- **Output Format**: Plans are saved to `specs/<descriptive-name>.md` with standardized sections including problem statement, technical approach, implementation guide, testing strategy, and success criteria
- **Dual Purpose**: Template serves both as a generator template for new projects and as an immediately usable command in this repository

### Command Workflow

The `/quick-plan` command follows this workflow:
1. Accepts user requirements through `$ARGUMENTS` variable
2. Analyzes requirements and determines best implementation approach
3. Creates comprehensive implementation plan with:
   - Problem statement and objectives
   - Technical approach and architecture decisions
   - Step-by-step implementation guide
   - Potential challenges and solutions
   - Testing strategy and success criteria
4. Generates kebab-case filename based on plan topic
5. Saves plan to `specs/` directory
6. Provides structured report with file location and key components

## How to Use

### In This Repository

1. Use the slash command with your requirements:
```bash
/quick-plan Implement user authentication with JWT tokens
```

2. The agent will create a detailed implementation plan and save it to `specs/<descriptive-name>.md`

3. Review the generated plan which includes:
   - Clear problem statement
   - Technical architecture decisions
   - Step-by-step implementation tasks
   - Testing and validation strategy

### In Generated Projects

When TAC Bootstrap generates a new project, the `quick-plan.md.j2` template will be rendered to `.claude/commands/quick-plan.md`, making the command immediately available in the generated project's Claude Code environment.

## Configuration

This is a static template with no configuration variables. The command uses these default settings:

- **Allowed Tools**: `Read, Write, Edit, Glob, Grep`
- **Model**: `claude-opus-4-1-20250805` (Opus 4 for high-quality planning)
- **Output Directory**: `specs/` (configurable via PLAN_OUTPUT_DIRECTORY variable)

## Testing

### Verify Template Exists

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2 && echo "Template exists" || echo "ERROR: Template missing"
```

### Verify Rendered File Exists

```bash
test -f .claude/commands/quick-plan.md && echo "Rendered file exists" || echo "ERROR: Rendered file missing"
```

### Compare Files (Should Be Identical)

```bash
diff tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2 .claude/commands/quick-plan.md && echo "Files identical (expected for static template)" || echo "Files differ"
```

### Run Full Validation Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing

Test the command by using it in Claude Code:
```bash
/quick-plan Create a REST API endpoint for user profile management
```

## Notes

### Design Decisions

- **Static Over Dynamic**: Chose to make this a static template (no Jinja2 variables) following the `prime_cc.md.j2` pattern, ensuring consistency across all generated projects
- **Opus Model Selection**: Uses Opus 4 instead of Sonnet to ensure high-quality architectural planning and comprehensive analysis
- **Limited Tool Access**: Restricts to read/write/search tools only, preventing the planning agent from executing code or making system changes
- **Architect Pattern**: Emphasizes deep thinking and structured planning over rapid implementation, providing a foundation for quality development work

### Comparison to Other Commands

- **vs /feature**: Quick-plan is more lightweight, requiring minimal ceremony and focusing on rapid plan creation
- **vs /bug**: Similar lightweight approach but for any type of implementation, not just bug fixes
- **vs /prime_cc**: Both are static templates, but quick-plan is focused on implementation planning while prime_cc is for codebase priming

### Future Considerations

If project-specific customization is needed, potential variables could include:
- `{{ config.paths.specs_dir }}` - Customizable output directory
- `{{ config.project.name }}` - Project context in generated plans
- `{{ config.planning.model }}` - Configurable model selection

### Integration with TAC Bootstrap

This template is part of Phase 9 (TAC_9) which focuses on creating command templates for the generator CLI. When `tac-bootstrap init` is run, this template will be rendered into the target project's `.claude/commands/` directory, making the quick-plan workflow immediately available to developers.
