# Install Template for TAC Bootstrap CLI

**ADW ID:** issue-44-adw-d450b40b
**Date:** 2026-01-20
**Specification:** specs/issue-44-adw-d450b40b-sdlc_planner-create-install-template.md

## Overview

Created a new Jinja2 template for the `/install` slash command that enables Claude agents to install project dependencies using the appropriate package manager. This template is part of the TAC Bootstrap CLI system that generates agentic layers for target projects.

## What Was Built

- Jinja2 template for the `/install` command (`install.md.j2`)
- Support for 12 different package managers with correct install commands
- Error handling instructions for common installation issues
- Post-installation verification workflow
- Specification document detailing requirements and implementation plan

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2`: New template file created with conditional logic for package manager detection and corresponding install commands

### Key Changes

- Implemented conditional Jinja2 blocks mapping each `PackageManager` enum value to its specific install command
- Added comprehensive error handling guidance for network errors, permission issues, version conflicts, and missing lock files
- Included post-installation verification instructions to ensure dependencies were installed correctly
- Used `{{ config.project.package_manager }}` variable to detect the project's package manager at render time
- Followed the same structure and format as existing command templates (test.md.j2, build.md.j2, lint.md.j2)

### Package Manager Mappings

The template supports the following package managers:

| Package Manager | Install Command |
|----------------|----------------|
| uv | `uv sync` |
| poetry | `poetry install` |
| pip | `pip install -r requirements.txt` |
| pipenv | `pipenv install` |
| npm | `npm install` |
| pnpm | `pnpm install` |
| yarn | `yarn install` |
| bun | `bun install` |
| go | `go mod download` |
| cargo | `cargo build` |
| maven | `mvn install` |
| gradle | `gradle build` |

## How to Use

### For TAC Bootstrap Users

When you initialize a new project or add agentic capabilities to an existing project using TAC Bootstrap CLI, the `/install` command will be automatically generated in your project's `.claude/commands/` directory based on this template.

1. The template will be rendered with your project's specific configuration
2. The resulting `install.md` file will contain the correct install command for your package manager
3. Claude agents in your project can use `/install` to install dependencies

### For TAC Bootstrap Developers

This template is part of the templates system and will be automatically used by the `TemplateRepository` when generating agentic layers:

1. Template location: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2`
2. Rendered by: `TemplateRepository.render_template()` method
3. Variables passed: `config` object containing `project.package_manager` and other project metadata

## Configuration

The template uses the following configuration variables from the `config` object:

- `{{ config.project.package_manager }}` - The package manager for the target project (from PackageManager enum)
- `$ARGUMENTS` - Optional command-line arguments passed to the install command

## Testing

Since this is a template file, testing is done through:

1. **Syntax validation**: Ensure Jinja2 template renders without errors
2. **Structure validation**: Compare with reference templates (test.md.j2, build.md.j2, lint.md.j2)
3. **Coverage validation**: Verify all PackageManager enum values are handled

To run the validation commands:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2
```

## Notes

- This template is a markdown instruction file that Claude agents read, not executable code
- The actual dependency installation happens in the target project, not in TAC Bootstrap itself
- The template includes safeguards to prevent agents from modifying code files during installation
- Some package managers (cargo, gradle) combine build and dependency installation in a single command
- This is part of FASE 3 (Templates System) in the TAC Bootstrap implementation roadmap
- The template follows the established pattern of having Variables, Instructions, and Report sections
