---
doc_type: feature
adw_id: feature_Tac_9_task_22
date: 2026-01-26
idk:
  - jinja2-template
  - slash-command
  - claude-code
  - context-priming
  - cli-workflow
  - automation-hooks
  - parameterization
tags:
  - feature
  - template
  - cli
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2
  - .claude/commands/prime_cc.md
---

# Prime Claude Code Command Template

**ADW ID:** feature_Tac_9_task_22
**Date:** 2026-01-26
**Specification:** specs/issue-263-adw-feature_Tac_9_task_22-sdlc_planner-prime-cc-command-template.md

## Overview

Created a Jinja2 template for the `/prime_cc` slash command that provides Claude Code-specific context priming. This command helps Claude Code agents quickly understand a project's structure, available tools, workflows, and conventions with optimizations for CLI-based development patterns unique to Claude Code.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Parameterized template for generating the prime_cc command
- **Rendered Command**: `.claude/commands/prime_cc.md` - Generated command for tac_bootstrap itself as validation
- **Specification Document**: Complete specification with implementation plan and acceptance criteria

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` (CREATE): 281-line Jinja2 template with parameterized configuration
- `.claude/commands/prime_cc.md` (CREATE): 247-line rendered command for tac_bootstrap project
- `specs/issue-263-adw-feature_Tac_9_task_22-sdlc_planner-prime-cc-command-template.md` (CREATE): Complete specification document
- `specs/issue-263-adw-feature_Tac_9_task_22-sdlc_planner-prime-cc-command-template-checklist.md` (CREATE): Validation checklist

### Key Changes

1. **Template Structure**: Built on proven pattern from `load_ai_docs.md.j2`, following established template conventions in tac_bootstrap
2. **Parameterization Strategy**: Used Jinja2 variables for project-specific values while keeping Claude Code-specific instructions static and universal:
   - `{{ config.project.name }}` - Project name
   - `{{ config.agentic.provider }}` - Claude provider
   - `{{ config.paths.* }}` - Directory paths (adws_dir, scripts_dir, app_root)
   - `{{ config.commands.* }}` - CLI commands (start, test, lint, typecheck, build)
3. **Command Sections**:
   - **Run**: Execute `/prime` first, then load Claude Code-specific configuration
   - **Read**: List key files including `.claude/commands/**`, `.claude/settings.json`, automation hooks, and ADW documentation
   - **Understand**: Provide structured overview of Claude Code environment, available commands, CLI workflows, and key directories
   - **Report**: Template for agents to summarize their understanding
4. **Claude Code Optimizations**: Emphasized tool usage (Read, Edit, Bash, Grep, Glob), CLI workflows, file navigation shortcuts, command discovery, and hook system awareness
5. **Conditional Rendering**: Used Jinja2 conditionals to include optional sections based on config availability (e.g., ADW directories, specific commands)

## How to Use

This template is used internally by the `tac-bootstrap` CLI when generating projects. It creates a `/prime_cc` command that agents can run to understand both the project and Claude Code-specific workflows.

1. **Template Generation**: When `tac-bootstrap init` or `tac-bootstrap upgrade` runs, the template is rendered with project-specific configuration
2. **Agent Usage**: In a generated project, agents run `/prime_cc` to:
   - Load general project context via `/prime`
   - Read Claude Code configuration files
   - Understand available slash commands and automation hooks
   - Learn CLI workflows and tool usage patterns

## Configuration

The template uses configuration values from `config.yml`:

**Project Settings:**
- `config.project.name` - Project identifier
- `config.agentic.provider` - Claude provider (e.g., AgenticProvider.CLAUDE_CODE)
- `config.project.repo_root` - Repository root directory

**Paths:**
- `config.paths.adws_dir` - AI Developer Workflows directory
- `config.paths.scripts_dir` - Utility scripts directory
- `config.paths.app_root` - Application source code root

**Commands:**
- `config.commands.start` - Start application command
- `config.commands.test` - Run tests command
- `config.commands.lint` - Linting command
- `config.commands.typecheck` - Type checking command
- `config.commands.build` - Build command

**Claude Settings:**
- `config.claude.commands.*` - Boolean flags for available commands

## Testing

Validate the template renders correctly and produces valid output:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify linting and type checking pass:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Test the rendered command in the current project:

```bash
cat .claude/commands/prime_cc.md
```

## Notes

### Design Decisions

1. **Extends /prime**: The command builds on the existing `/prime` command rather than replacing it, ensuring general context is loaded first
2. **Static Best Practices**: Claude Code-specific instructions remain static across all generated projects, ensuring consistency in tool usage and workflow patterns
3. **Conditional Sections**: Optional sections (ADW workflows, specific commands) are only rendered if the configuration includes those features
4. **Template Consistency**: Follows the same structure as other command templates in the system for maintainability

### Integration with TAC Bootstrap

This template is part of the broader TAC (Test-Assist-Context) Bootstrap system that generates "agentic layers" for projects. It complements other templates in the `.claude/commands/` directory and works with the ADW (AI Developer Workflows) system.

### Future Enhancements

- Add project-type specific priming (web app vs CLI vs library)
- Include automatic detection of testing frameworks and CI/CD setup
- Auto-discover project conventions from existing code patterns
- Add support for custom context builders in hooks
