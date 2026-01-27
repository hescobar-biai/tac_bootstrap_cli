---
doc_type: feature
adw_id: feature_Tac_9_task_30
date: 2026-01-26
idk:
  - jinja2-template
  - claude-code-hooks
  - expert-workflow
  - yaml-frontmatter
  - hook-implementation
  - settings-integration
  - validation-testing
tags:
  - feature
  - template
  - hooks
  - expert-command
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2
---

# Claude Code Hook Expert Build Template

**ADW ID:** feature_Tac_9_task_30
**Date:** 2026-01-26
**Specification:** specs/issue-271-adw-feature_Tac_9_task_30-sdlc_planner-cc-hook-expert-build-template.md

## Overview

Created a Jinja2 template for the `cc_hook_expert_build` expert command that guides AI agents through implementing Claude Code hooks. This is the second phase in the Plan-Build-Improve workflow cycle, focused on executing implementation plans, writing hook code, integrating with settings.json, and validating functionality.

## What Was Built

- **Jinja2 Template**: Complete expert command template with YAML frontmatter and comprehensive implementation guidance
- **4-Phase Workflow**: Structured workflow covering Review Plan → Implement Hook → Validate Implementation → Troubleshoot Issues
- **Implementation Patterns**: Code examples for hook structure, settings.json integration, error handling, and logging
- **Quality Checks**: Validation checklist covering code quality, integration, functionality, and testing
- **Troubleshooting Guide**: Common errors and debugging steps for hook implementation issues

## Technical Implementation

### Files Created

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2`: Expert build command template (520 lines)

### Key Changes

- **YAML Frontmatter**: Configured with implementation-focused tools (Read, Write, Edit, Bash, TodoWrite, Glob, Grep), description, and sonnet model
- **Variables Section**: Defined BUILD_CONTEXT ($ARGUMENTS), PROJECT_NAME ({{ config.project.name }}), TEST_COMMAND ({{ config.commands.test }})
- **Phase 1 - Review Plan**: Instructions for locating plan documents, parsing key decisions, setting up TodoWrite tasks, and identifying files to create/modify
- **Phase 2 - Implement Hook**: Step-by-step guidance for writing hook scripts, implementing JSON parsing, hook logic, exit code strategy, error handling, and settings.json integration
- **Phase 3 - Validate Implementation**: Validation steps including tests, linting, type checking, manual smoke tests, and settings.json verification
- **Phase 4 - Troubleshoot Issues**: Debugging guidance for test failures, hooks not triggering, incorrect blocking, JSON parsing errors, import errors, and settings.json syntax issues
- **Implementation Patterns**: Code examples for hook structure, settings.json integration, error handling patterns, and session-based logging
- **Quality Checks**: Comprehensive checklist covering code quality, integration, functionality, testing, and documentation
- **Report Format**: Structured output format for implementation completion and validation results

## How to Use

### Generate Projects with Build Expert Command

1. Create or update TAC Bootstrap configuration for your project
2. Run TAC Bootstrap CLI to generate project structure:
   ```bash
   cd tac_bootstrap_cli
   uv run tac-bootstrap init /path/to/output
   ```
3. The generated project will include `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`

### Use Build Command in Generated Projects

After planning phase is complete:

```bash
# Search for plan automatically
/cc_hook_expert_build

# Reference specific plan
/cc_hook_expert_build specs/hook-validation-plan.md

# Provide build context
/cc_hook_expert_build "implement validation hook from plan"
```

### Workflow Integration

This command is the second step in the expert workflow:
- **Plan** (cc_hook_expert_plan) → **Build** (cc_hook_expert_build) → Improve (cc_hook_expert_improve)

## Configuration

The template uses minimal Jinja2 variables for project-specific configuration:

- `{{ config.project.name }}`: Project name for context
- `{{ config.commands.test }}`: Project-specific test command (e.g., `pytest`, `npm test`)

All expert guidance is static content, ensuring consistency across generated projects while allowing project-specific commands through configuration.

## Testing

### Validation Commands

Ensure template integrates correctly with CLI generator:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Validation

1. Generate a test project with TAC Bootstrap CLI
2. Verify `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md` renders correctly
3. Test the expert command workflow in Claude Code
4. Verify Jinja2 variables are correctly substituted
5. Validate YAML frontmatter is parsed correctly by Claude Code

## Notes

- The template creates workflow continuity with the planning phase (cc_hook_expert_plan.md.j2)
- Implementation patterns provide concrete code examples for common hook scenarios
- Troubleshooting guidance enables autonomous issue resolution during implementation
- Quality checks ensure hooks are validated before completion
- Exit code strategy (0=allow, 1=warn, 2=block) is central to hook behavior
- Settings.json integration pattern uses `$CLAUDE_PROJECT_DIR` and `|| true` for graceful failures
- Template follows established expert command patterns with YAML frontmatter and structured workflow sections
- Minimal Jinja2 variables reduce template complexity while providing necessary project context
