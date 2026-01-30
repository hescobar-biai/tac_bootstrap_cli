---
doc_type: feature
adw_id: feature_Tac_12_task_5
date: 2026-01-30
idk:
  - slash-command
  - documentation-exploration
  - task-agent
  - jinja2-template
  - agentic-planning
  - explore-subagent
  - scaffold-service
tags:
  - feature
  - command
  - planning
related_code:
  - .claude/commands/plan_w_docs.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Plan with Documentation Exploration Command

**ADW ID:** feature_Tac_12_task_5
**Date:** 2026-01-30
**Specification:** specs/issue-457-adw-feature_Tac_12_task_5-sdlc_planner-plan-w-docs-command.md

## Overview

Created the `/plan_w_docs` slash command that enhances the planning process by exploring relevant documentation before generating implementation plans. The command uses the Task/Explore agent to discover and summarize documentation from local sources (ai_docs/, app_docs/, specs/) and optionally web-based library documentation, resulting in better-informed plans based on actual project context and architectural patterns.

## What Was Built

- New slash command `/plan_w_docs` in base repository
- Jinja2 template for CLI generation of the command
- Integration with scaffold service for automated command generation
- Documentation exploration workflow with 5-step process
- Support for graceful handling of missing documentation

## Technical Implementation

### Files Modified

- `.claude/commands/plan_w_docs.md`: New command file with YAML frontmatter (allowed-tools: Task, Read, Glob, Grep, WebFetch), documentation exploration workflow, and plan format template. Includes 5-step documentation exploration process and machine-parseable output format.

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2`: Jinja2 template version using `{{ config.project.name }}`, `{{ config.paths.specs_dir }}`, `{{ config.commands.* }}` variables for dynamic project configuration.

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:324`: Added "plan_w_docs" to commands list for automatic inclusion in generated projects.

### Key Changes

1. **Documentation Exploration Workflow**: Implements 5-step process:
   - Step 1: Search local docs (ai_docs/, app_docs/, specs/) using Task/Explore agent with medium thoroughness
   - Step 2: Optional web documentation via WebFetch for framework/library docs
   - Step 3: Summarize top 5-10 relevant documentation sources
   - Step 4: Identify documentation gaps
   - Step 5: Proceed with planning informed by documentation insights

2. **Graceful Degradation**: Command continues with planning even if documentation is missing or Task/Explore fails, logging warnings in Notes section rather than blocking execution.

3. **Plan Format Extension**: Adds "Documentation Exploration Summary" section to standard feature.md plan format, including "Relevant Documentation Found" and "Documentation Gaps" subsections.

4. **Template Variables**: Uses Jinja2 templating for project-specific configuration:
   - `{{ config.project.name }}` for project name
   - `{{ config.paths.specs_dir }}` for specs directory
   - `{{ config.commands.install }}`, `{{ config.commands.test }}`, etc. for project commands

5. **Machine-Parseable Output**: Strict output format requiring ONLY relative path (e.g., `specs/issue-37-adw-e4dc9574-sdlc_planner-feature-name.md`) with no explanations or formatting.

## How to Use

### In TAC Bootstrap Project

1. Run the command with issue metadata:
```bash
/plan_w_docs 457 feature_Tac_12_task_5 '{"number":457,"title":"Create plan_w_docs command","body":"Create a planning command that explores documentation before creating plans."}'
```

2. The command will:
   - Explore documentation in ai_docs/, app_docs/, specs/ using Task/Explore agent
   - Summarize top 5-10 relevant docs
   - Identify documentation gaps
   - Generate plan in specs/ directory with documentation insights

3. Output will be relative path only:
```
specs/issue-457-adw-feature_Tac_12_task_5-sdlc_planner-plan-w-docs-command.md
```

### In Generated Projects

1. Use tac-bootstrap CLI to generate project with plan_w_docs command included
2. Command file will be created at `.claude/commands/plan_w_docs.md`
3. Use same invocation pattern with project-specific paths from config.yml

## Configuration

### Command Frontmatter

```yaml
allowed-tools: Task, Read, Glob, Grep, WebFetch
description: Enhanced planning with documentation exploration
```

### Variables

- `issue_number` ($1): GitHub issue number or identifier
- `adw_id` ($2): ADW workflow identifier
- `issue_json` ($3): JSON string with issue metadata (number, title, body)

### Template Configuration

Uses Jinja2 variables from config object:
- `config.project.name`: Project name
- `config.paths.specs_dir`: Specifications directory path
- `config.paths.ai_docs`: AI documentation directory
- `config.commands.install`: Package installation command
- `config.commands.test`: Test execution command
- `config.commands.lint`: Linting command
- `config.commands.typecheck`: Type checking command

## Testing

### Manual Testing

Verify command file exists and has valid structure:

```bash
# Check command file exists in base repository
test -f .claude/commands/plan_w_docs.md && echo "✓ Command file exists"

# Check template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2 && echo "✓ Template exists"

# Verify YAML frontmatter is valid
head -n 3 .claude/commands/plan_w_docs.md | grep "allowed-tools"
```

Test command execution:

```bash
# Run command with test issue
/plan_w_docs 999 test_feature '{"number":999,"title":"Test Feature","body":"Test feature implementation"}'

# Verify output is relative path only (no explanations)
# Expected: specs/issue-999-adw-test_feature-sdlc_planner-*.md
```

### Validation Commands

Run all validation commands to ensure zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test - verify command is registered
cd tac_bootstrap_cli && uv run tac-bootstrap --help | grep -q "plan_w_docs" && echo "✓ Command registered"
```

### Edge Cases Tested

1. **Missing documentation directories**: Command proceeds with warning in Notes section
2. **Task/Explore agent timeout**: Command continues with planning, logs failure
3. **WebFetch unavailable**: Command works with local docs only
4. **Empty documentation directories**: Command notes lack of docs and proceeds
5. **Relative vs absolute path validation**: Command rejects absolute paths in output

## Notes

### Implementation Context

- Part of TAC-12 Wave 1 (New Commands), Task 5 of 49
- Follows patterns from existing commands (feature.md, quick-plan.md)
- Uses Task tool with Explore agent (medium thoroughness) for token efficiency
- Limits documentation summaries to top 5-10 docs to avoid context overflow
- Reference file `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_docs.md` was inaccessible, implementation based on feature.md and quick-plan.md patterns

### Cleanup Actions

- Removed deprecated commands: all_tools.md, build_in_parallel.md, find_and_summarize.md
- Removed corresponding templates and documentation
- Updated scaffold_service.py to remove deprecated commands from registration list
- Simplified adw_modules/github.py by removing deprecated functionality

### Architectural Decisions

1. **KISS Principle**: Uses standard config object, no custom configuration beyond config.paths
2. **Advisory Warnings**: Missing docs trigger warnings, not hard validation that blocks execution
3. **Subagent Instructions**: Task/Explore receives specific 3-step instructions: search → summarize → identify gaps
4. **Compatibility**: Output follows same format as feature.md for compatibility with existing ADW workflows (adw_sdlc_iso.py, adw_plan_iso.py)

### Future Enhancements

- Could add caching for documentation search results to improve performance on repeated searches
- Could integrate with fractal documentation system for automatic IDK keyword extraction
- Could add support for custom documentation directories via config
- Could add metrics tracking for documentation coverage and usefulness
