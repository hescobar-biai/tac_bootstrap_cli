# Claude Configuration Templates for TAC Bootstrap

**ADW ID:** d30e0391
**Date:** 2026-01-20
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/d30e0391/specs/issue-12-adw-d30e0391-chore_planner-create-claude-templates.md

## Overview

Created a comprehensive set of Jinja2 templates that generate Claude Code configuration files (`.claude/settings.json` and slash commands) for projects initialized with TAC Bootstrap CLI. These templates are parametrized with TACConfig variables, enabling customized Claude integration based on each project's technology stack, architecture, and tooling.

## What Was Built

- **Settings Template**: Parametrized `settings.json.j2` with permissions and hooks configuration
- **14 Command Templates**: Slash commands covering complete SDLC workflow:
  - Project context: `/prime`, `/start`
  - Testing and building: `/test`, `/build`
  - Planning: `/feature`, `/bug`, `/chore`, `/patch`
  - Execution: `/implement`, `/commit`, `/pull_request`
  - Validation: `/review`, `/health_check`
  - Documentation: `/document`

## Technical Implementation

### Files Created

All templates created in `tac_bootstrap_cli/tac_bootstrap/templates/claude/`:

- `settings.json.j2` - Main Claude Code configuration with permissions/hooks
- `commands/prime.md.j2` - Initialize agent with project context
- `commands/start.md.j2` - Start the application
- `commands/test.md.j2` - Run test suite
- `commands/build.md.j2` - Build the project
- `commands/feature.md.j2` - Plan new feature implementation
- `commands/bug.md.j2` - Plan bug fix
- `commands/chore.md.j2` - Plan maintenance tasks
- `commands/patch.md.j2` - Quick patch workflow
- `commands/implement.md.j2` - Execute a plan file
- `commands/commit.md.j2` - Create git commit with conventions
- `commands/pull_request.md.j2` - Create pull request
- `commands/review.md.j2` - Review implementation against spec
- `commands/document.md.j2` - Generate feature documentation
- `commands/health_check.md.j2` - Validate project setup

### Key Template Features

1. **Dynamic Permissions** (`settings.json.j2`):
   - Package manager-specific permissions (e.g., `uv`, `npm`, `pip`)
   - Safe defaults with explicit deny list for destructive operations
   - Hook integration for lifecycle events

2. **Context-Aware Commands**:
   - Project-specific paths via `{{ config.paths.* }}`
   - Technology stack awareness via `{{ config.project.language.value }}`
   - Architecture pattern enforcement via `{{ config.project.architecture.value }}`
   - Command customization via `{{ config.commands.* }}`

3. **Conditional Rendering**:
   - Optional commands (lint, build, typecheck) only shown if configured
   - Framework-specific guidance when framework is specified
   - Safety rules customized per project's forbidden paths

4. **Variable Interpolation**:
   - `{{ config.project.package_manager.value }}` - npm, uv, pip, etc.
   - `{{ config.commands.start }}` - Project start command
   - `{{ config.paths.specs_dir }}` - Specification directory path
   - `{{ config.agentic.safety.forbidden_paths | join(', ') }}` - Protected paths

### Template Syntax Examples

**Settings.json.j2** - Package manager parameterization:
```jinja2
"Bash({{ config.project.package_manager.value }}:*)",
...
"command": "{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
```

**Prime.md.j2** - Conditional rendering:
```jinja2
{% if config.commands.lint %}
   - Lint: `{{ config.commands.lint }}`
{% endif %}
```

**Feature.md.j2** - Path and architecture interpolation:
```jinja2
Write a plan file to `{{ config.paths.specs_dir }}/` with:
...
- [ ] Code follows {{ config.project.architecture.value }} patterns
```

## How to Use

### For TAC Bootstrap Development

These templates will be used by the generator when running:
```bash
tac-bootstrap init <project_name>
```

### Template Rendering Test

Verify templates render correctly:
```bash
cd tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()

# Create test config
config = TACConfig(
    project=ProjectSpec(
        name='test',
        language=Language.PYTHON,
        package_manager=PackageManager.UV
    ),
    commands=CommandsSpec(
        start='uv run python -m app',
        test='uv run pytest',
        lint='uv run ruff check .'
    ),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

# Render settings.json
result = repo.render('claude/settings.json.j2', {'config': config})
print('=== settings.json ===')
print(result[:500])

# Render a command
result = repo.render('claude/commands/prime.md.j2', {'config': config})
print('\\n=== prime.md ===')
print(result[:500])
"
```

### In Generated Projects

After TAC Bootstrap generates a project, users will have:
- `.claude/settings.json` with their tool-specific permissions
- `.claude/commands/*.md` with 14 slash commands customized to their stack

Example usage in a generated project:
```bash
# Initialize Claude agent with project context
/prime

# Plan a new feature
/feature "Add user authentication"

# Execute the plan
/implement specs/feature-auth.md

# Run tests
/test

# Create commit
/commit

# Create pull request
/pull_request
```

## Configuration

### TACConfig Variables Used

Templates consume these configuration sections:

**Project Spec** (`config.project.*`):
- `name` - Project name
- `language.value` - python, typescript, go, etc.
- `framework.value` - fastapi, nextjs, gin, etc. (optional)
- `architecture.value` - simple, ddd, clean, hexagonal
- `package_manager.value` - uv, npm, pip, go, cargo

**Paths** (`config.paths.*`):
- `app_root` - Application source code directory
- `specs_dir` - Specification/plan files directory
- `adws_dir` - AI Developer Workflows directory
- `scripts_dir` - Utility scripts directory

**Commands** (`config.commands.*`):
- `start` - Application start command (required)
- `test` - Test suite command (required)
- `lint` - Linting command (optional)
- `build` - Build command (optional)
- `typecheck` - Type checking command (optional)

**Safety** (`config.agentic.safety.*`):
- `forbidden_paths` - List of paths agents must not modify

### Command Template Variables

Each command template accepts:
- `$ARGUMENTS` - User-provided arguments to the command
- `$1, $2, ...` - Positional parameters for specific commands

## Testing

### Verify Template Structure

Check all files exist:
```bash
cd tac_bootstrap_cli
ls -la tac_bootstrap/templates/claude/
ls -la tac_bootstrap/templates/claude/commands/
```

Expected output:
- 1 `settings.json.j2` file
- 14 command `.md.j2` files

### Run Unit Tests

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli
uv run ruff check .
```

### Smoke Test CLI

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

## Notes

### Added Commands Beyond Original Spec

The original issue specified 12 commands, but 14 were created to ensure completeness:
- `/build` - Build command for compiled/bundled projects
- `/patch` - Quick patch workflow for small fixes
- `/pull_request` - GitHub PR creation workflow

These additions align with existing `.claude/commands/` in the TAC Bootstrap repository base.

### Template Design Principles

1. **Minimal assumptions**: Templates only require essential TACConfig fields
2. **Graceful degradation**: Optional features use `{% if %}` conditionals
3. **DRY**: Common patterns abstracted into config variables
4. **Safe defaults**: Permissions whitelist approach with explicit deny rules
5. **User guidance**: Each command includes clear instructions and expected output format

### Future Enhancements

Potential improvements for future iterations:
- Hook templates (TAREA 3.3 in plan)
- ADW workflow templates (future tasks)
- Custom filter functions for complex formatting
- Multi-language command variations
- Environment-specific settings overrides

### Related Tasks

- **Prerequisite**: TAREA 3.1 - Jinja2 Template Infrastructure (completed, ADW d2f77c7a)
- **Next**: TAREA 3.3 - Create hook templates
- **Next**: TAREA 3.4 - Create ADW workflow templates
