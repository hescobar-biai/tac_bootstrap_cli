# Scripts and Configuration Templates

**ADW ID:** feff53ac
**Date:** 2026-01-20
**Specification:** specs/issue-18-adw-feff53ac-sdlc_planner-create-scripts-config-templates.md

## Overview

Created comprehensive Jinja2 templates for generating development scripts, configuration files, and documentation structure in projects bootstrapped by TAC Bootstrap CLI. These templates enable automated generation of bash scripts (start, test, lint, build), configuration files (config.yml, .mcp.json, .gitignore), and README documentation for key directories.

## What Was Built

This implementation added 10 new Jinja2 templates organized in three categories:

- **4 Bash Script Templates** - Executable development scripts with dynamic configuration
- **3 Configuration File Templates** - Project configuration files (YAML, JSON, gitignore patterns)
- **3 Documentation Templates** - README files for documentation directories

## Technical Implementation

### Files Modified

All files created in `tac_bootstrap_cli/tac_bootstrap/templates/`:

**Scripts (templates/scripts/):**
- `scripts/start.sh.j2`: Template for starting the application with dynamic start command
- `scripts/test.sh.j2`: Template for running tests with dynamic test command
- `scripts/lint.sh.j2`: Template for running linter with conditional lint command
- `scripts/build.sh.j2`: Template for building the project with conditional build command

**Configuration (templates/config/):**
- `config/config.yml.j2`: Comprehensive YAML configuration template with all TACConfig fields
- `config/.mcp.json.j2`: MCP server configuration template for Playwright integration
- `config/.gitignore.j2`: Dynamic gitignore with project-specific paths and standard patterns

**Documentation Structure (templates/structure/):**
- `structure/specs/README.md.j2`: Documentation for specifications directory
- `structure/app_docs/README.md.j2`: Documentation for application documentation directory
- `structure/ai_docs/README.md.j2`: Documentation for AI-generated documentation directory

### Key Changes

- **Conditional Rendering**: Templates use Jinja2 conditionals (`{% if config.commands.lint %}`) to handle optional commands and features gracefully
- **Enum Handling**: Templates properly access enum values using `.value` accessor (e.g., `{{ config.project.language.value }}`)
- **Boolean Formatting**: YAML booleans use `| lower` filter to ensure proper lowercase formatting in generated files
- **Dynamic Paths**: Templates use config.paths variables for directory references, making them adapt to project structure
- **Comprehensive Coverage**: config.yml.j2 template includes all sections from TACConfig model including project, paths, commands, agentic, claude, templates, and bootstrap configurations

## How to Use

### 1. Templates are Used Automatically

When running `tac-bootstrap init`, these templates are automatically rendered with your project configuration:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap init my-project --language python --framework fastapi
```

### 2. Template Rendering with TemplateRepository

Templates can be rendered programmatically using the TemplateRepository:

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(
        name='my-app',
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
        framework=Framework.FASTAPI
    ),
    commands=CommandsSpec(
        start='uv run python -m app',
        test='uv run pytest',
        lint='uv run ruff check .'
    )
)

# Render config.yml template
result = repo.render('config/config.yml.j2', {'config': config})
print(result)
```

### 3. Generated Files Location

Templates generate files in these locations within target projects:

- `scripts/start.sh`, `scripts/test.sh`, `scripts/lint.sh`, `scripts/build.sh`
- `config.yml`
- `.mcp.json`
- `.gitignore`
- `specs/README.md`
- `app_docs/README.md`
- `ai_docs/README.md`

## Configuration

### Available Template Variables

Templates have access to the `config` object (TACConfig instance) with these sections:

**Project Configuration:**
- `config.project.name` - Project name
- `config.project.language` - Programming language (enum)
- `config.project.framework` - Framework (optional enum)
- `config.project.package_manager` - Package manager (enum)
- `config.project.architecture` - Architecture pattern (enum)

**Paths:**
- `config.paths.app_root` - Application root directory
- `config.paths.agentic_root` - Agentic layer root
- `config.paths.logs_dir` - Logs directory
- `config.paths.worktrees_dir` - Git worktrees directory
- `config.paths.specs_dir` - Specifications directory

**Commands:**
- `config.commands.start` - Start command (required)
- `config.commands.test` - Test command (required)
- `config.commands.lint` - Lint command (optional)
- `config.commands.build` - Build command (optional)
- `config.commands.typecheck` - Type checking command (optional)
- `config.commands.format` - Code formatting command (optional)

**Agentic Configuration:**
- `config.agentic.provider` - AI provider (enum)
- `config.agentic.model_policy` - Model selection policy
- `config.agentic.worktrees` - Worktree configuration
- `config.agentic.logging` - Logging configuration
- `config.agentic.safety` - Safety constraints

**Claude Configuration:**
- `config.claude.settings` - Claude-specific settings
- `config.claude.commands` - Slash command definitions

### Template Conventions

1. **Enums**: Always use `.value` to access enum string value
   ```jinja2
   language: "{{ config.project.language.value }}"
   ```

2. **Booleans in YAML**: Use `| lower` filter for proper formatting
   ```jinja2
   enabled: {{ config.agentic.worktrees.enabled | lower }}
   ```

3. **Conditionals**: Check existence before rendering optional fields
   ```jinja2
   {% if config.commands.lint -%}
   lint: "{{ config.commands.lint }}"
   {% endif -%}
   ```

4. **Lists**: Use for loops for arrays
   ```jinja2
   {% for workflow in config.agentic.workflows.available -%}
   - "{{ workflow.value }}"
   {% endfor -%}
   ```

## Testing

### Manual Template Rendering Test

Test template rendering with sample configuration:

```bash
cd tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(
        name='test-app',
        language=Language.PYTHON,
        package_manager=PackageManager.UV
    ),
    commands=CommandsSpec(
        start='uv run python main.py',
        test='uv run pytest'
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name='test-app')
    )
)

result = repo.render('config/config.yml.j2', {'config': config})
print(result)
"
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "template"
```

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

### Design Decisions

- **Conditional Commands**: Lint and build scripts check if commands are configured before executing, preventing errors in projects that don't use these tools
- **Fail-Fast Scripts**: All bash scripts use `set -e` to exit immediately on error, ensuring robust execution
- **Dynamic .gitignore**: Gitignore template uses config.paths variables for directories like logs_dir and worktrees_dir, ensuring patterns match actual project structure
- **Comprehensive config.yml**: Template includes all TACConfig fields, providing complete configuration reference for generated projects

### Future Enhancements

- Add templates for additional script types (deploy.sh, migrate.sh)
- Create language-specific .gitignore sections based on config.project.language
- Add conditional MCP server configurations based on project requirements
- Generate IDE-specific configuration files (.vscode/settings.json, .idea/*)

### Related Files

- Model definitions: tac_bootstrap_cli/tac_bootstrap/domain/models.py:408
- Template repository: tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py
- Reference implementations: config.yml, .mcp.json, .gitignore, scripts/dev_*.sh
