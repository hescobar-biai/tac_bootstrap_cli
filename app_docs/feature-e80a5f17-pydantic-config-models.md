# Pydantic Configuration Models

**ADW ID:** e80a5f17
**Date:** 2026-01-20
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/specs/issue-5-adw-e80a5f17-sdlc_planner-create-pydantic-config-models.md

## Overview

Created comprehensive Pydantic v2 models representing the entire TAC Bootstrap configuration schema. These models provide type safety, validation, smart defaults, and documentation for all configuration sections in `config.yml`, serving as the foundation for configuration management throughout the CLI.

## What Was Built

- **8 Configuration Enums** - Type-safe options for languages, frameworks, architectures, package managers, and workflow settings
- **13 Pydantic BaseModel Classes** - Sub-models for each configuration section (project, paths, commands, agentic, claude, templates, bootstrap)
- **1 Root Configuration Model** - `TACConfig` that combines all sub-models with schema versioning
- **3 Helper Functions** - Utility functions for getting context-aware defaults based on language and package manager combinations
- **Field Validation** - Project name sanitization validator to ensure safe directory/package naming

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Created new file with 679 lines of comprehensive Pydantic models

### Key Changes

- **Enums for Type Safety**: Created `Language`, `Framework`, `Architecture`, `PackageManager`, `ProjectMode`, `AgenticProvider`, `RunIdStrategy`, and `DefaultWorkflow` enums, all inheriting from `str, Enum` for proper serialization
- **Hierarchical Model Structure**: Implemented 13 BaseModel classes (`ProjectSpec`, `PathsSpec`, `CommandsSpec`, `WorktreeConfig`, `LoggingConfig`, `SafetyConfig`, `AgenticSpec`, `ClaudeSettings`, `ClaudeCommandsConfig`, `ClaudeConfig`, `TemplatesConfig`, `BootstrapConfig`, and root `TACConfig`) matching the exact structure of `config.yml`
- **Smart Validation**: Added `@field_validator` for `ProjectSpec.name` that sanitizes project names by stripping whitespace, converting to lowercase, and replacing spaces with hyphens
- **Helper Functions**: Implemented `get_frameworks_for_language()`, `get_package_managers_for_language()`, and `get_default_commands()` to provide context-aware defaults for the interactive wizard
- **Comprehensive Documentation**: All models and fields include detailed docstrings with `Field()` descriptions for IDE autocomplete and generated documentation

## How to Use

### Importing Models

```python
from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    Language,
    PackageManager,
    Framework,
    Architecture
)
```

### Creating a Configuration Instance

```python
config = TACConfig(
    project=ProjectSpec(
        name="my-app",
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
        framework=Framework.FASTAPI,
        architecture=Architecture.DDD
    ),
    commands=CommandsSpec(
        start="uv run python -m app",
        test="uv run pytest",
        build="uv build"
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name="my-app")
    )
)
```

### Using Helper Functions

```python
from tac_bootstrap.domain.models import (
    get_frameworks_for_language,
    get_package_managers_for_language,
    get_default_commands,
    Language,
    PackageManager
)

# Get valid frameworks for Python
frameworks = get_frameworks_for_language(Language.PYTHON)
# Returns: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE]

# Get valid package managers for TypeScript
pkg_managers = get_package_managers_for_language(Language.TYPESCRIPT)
# Returns: [PackageManager.PNPM, PackageManager.NPM, PackageManager.YARN, PackageManager.BUN]

# Get default commands for Python with uv
commands = get_default_commands(Language.PYTHON, PackageManager.UV)
# Returns: {"start": "uv run python -m app", "test": "uv run pytest", ...}
```

### Serialization

```python
# Export to dict
config_dict = config.model_dump()

# Export to JSON
config_json = config.model_dump_json(indent=2)

# Parse from dict
config = TACConfig.model_validate(config_dict)
```

## Configuration

### Model Schema Sections

The `TACConfig` root model includes these sections:

- **version** (int): Schema version number for compatibility tracking
- **project** (`ProjectSpec`): Project metadata (name, language, framework, architecture, package manager, mode)
- **paths** (`PathsSpec`): Directory structure (app_root, agentic_root, prompts_dir, adws_dir, specs_dir, logs_dir, scripts_dir, worktrees_dir)
- **commands** (`CommandsSpec`): Shell commands (start, build, test, lint, typecheck, format)
- **agentic** (`AgenticSpec`): Agentic layer configuration (provider, model_policy, worktrees, logging, safety, workflows)
- **claude** (`ClaudeConfig`): Claude Code settings (settings, commands for slash command mappings)
- **templates** (`TemplatesConfig`): Template file paths (plan_template, chore_template, feature_template, bug_template, patch_template)
- **bootstrap** (`BootstrapConfig`): Bootstrap options for new projects (create_git_repo, initial_commit, license, readme)

### Validation Rules

- **Project Name**: Automatically sanitized (stripped, lowercased, spaces replaced with hyphens)
- **Extra Fields**: Forbidden via `extra = "forbid"` to catch configuration errors early
- **Required Fields**: Marked with `...` in Field definitions
- **Smart Defaults**: Provided for most fields based on language/framework combinations

## Testing

### Verify Model Import

```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"
```

### Test Model Instantiation

```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import *; config = TACConfig(project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV), commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'), claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))); print(config.model_dump_json(indent=2))"
```

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Linting Validation

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### CLI Smoke Test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

- **Pydantic V2 Syntax**: Uses modern Pydantic 2.5.0+ features (`Field()`, `field_validator`, `model_dump_json()`)
- **Schema Alignment**: Models exactly match the structure in the existing `config.yml` to ensure validation compatibility
- **No Test Files**: Per specification, model tests will be created in a future task
- **No Scaffolding Logic**: Models only define the schema; generation/scaffolding logic will be implemented separately
- **String Enums**: All enums inherit from `(str, Enum)` for proper YAML/JSON serialization

### Future Integration Points

These models will be used by:
1. **Interactive Wizard** (Task 2.2) - For capturing user input with validation
2. **Config Generator** (Task 2.3) - For creating validated `config.yml` files
3. **Template Renderer** (Task 3.x) - For passing configuration to Jinja2 templates
4. **CLI Commands** - For loading and validating existing configurations

### Dependencies

All required dependencies are already installed per `pyproject.toml`:
- pydantic>=2.5.0
- pyyaml>=6.0.1
- typing-extensions (for Python <3.10 compatibility)

### File Location

`tac_bootstrap_cli/tac_bootstrap/domain/models.py` (679 lines)
