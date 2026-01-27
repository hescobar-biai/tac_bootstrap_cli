---
doc_type: feature
adw_id: 11ee57c0
date: 2026-01-27
idk:
  - pydantic
  - validation
  - configuration
  - domain-model
  - schema
  - ddd
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
  - tac_bootstrap_cli/tests/test_value_objects.py
---

# Pydantic Configuration Models

**ADW ID:** 11ee57c0
**Date:** 2026-01-27
**Specification:** specs/issue-5-adw-11ee57c0-sdlc_planner-create-pydantic-config-models.md

## Overview

This feature implements comprehensive Pydantic models that represent the complete schema of TAC Bootstrap's `config.yml` configuration file. The models provide type safety, validation, smart defaults, and serve as the foundation for all configuration-related operations in the CLI application.

## What Was Built

- **8 Configuration Enums**: Language, Framework, Architecture, PackageManager, ProjectMode, AgenticProvider, RunIdStrategy, DefaultWorkflow
- **13 Pydantic Models**: ProjectSpec, PathsSpec, CommandsSpec, WorktreeConfig, LoggingConfig, SafetyConfig, AgenticSpec, ClaudeSettings, ClaudeCommandsConfig, ClaudeConfig, TemplatesConfig, BootstrapConfig, TACConfig (root model)
- **3 Helper Functions**: Language-specific framework/package manager mappings and default command generators
- **Field Validators**: Project name sanitization and constraint validation
- **912 lines** of well-documented, type-safe configuration code

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Complete implementation of all Pydantic models (new file, 912 lines)
- `tac_bootstrap_cli/tests/test_value_objects.py`: Fixed semantic version comparison test
- `specs/issue-5-adw-11ee57c0-sdlc_planner-create-pydantic-config-models.md`: Feature specification
- `specs/issue-5-adw-11ee57c0-sdlc_planner-create-pydantic-config-models-checklist.md`: Validation checklist

### Key Changes

- **Domain-Driven Design Architecture**: Models placed in `domain/` layer following DDD principles
- **Comprehensive Type Safety**: All configuration fields are strongly typed with Pydantic validation
- **Smart Defaults**: Language and package manager-specific defaults for commands (Python with uv/poetry, TypeScript with pnpm/npm, Go)
- **Field Documentation**: Every model field includes detailed descriptions via `Field(description=...)`
- **Validation Rules**: Project name sanitization (whitespace trimming, lowercasing, replacing spaces/underscores with hyphens)
- **Helper Functions**: `get_frameworks_for_language()`, `get_package_managers_for_language()`, `get_default_commands()` provide intelligent mappings

## How to Use

### Import the Models

```python
from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    Language,
    PackageManager,
    Architecture,
    CommandsSpec,
    ClaudeConfig,
    ClaudeSettings
)
```

### Create a Configuration Instance

```python
config = TACConfig(
    project=ProjectSpec(
        name="my-app",
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
        architecture=Architecture.DDD
    ),
    commands=CommandsSpec(
        start="uv run python -m app",
        test="uv run pytest"
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name="my-app")
    )
)
```

### Use Helper Functions

```python
# Get available frameworks for a language
frameworks = get_frameworks_for_language(Language.PYTHON)
# Returns: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE]

# Get package managers for a language
pkg_managers = get_package_managers_for_language(Language.TYPESCRIPT)
# Returns: [PackageManager.PNPM, PackageManager.NPM, PackageManager.YARN, PackageManager.BUN]

# Get default commands
defaults = get_default_commands(Language.PYTHON, PackageManager.UV)
# Returns: CommandsSpec with uv-specific commands
```

### Serialize to JSON

```python
config_json = config.model_dump_json(indent=2)
print(config_json)
```

## Configuration

The models support the complete `config.yml` schema with these main sections:

- **project**: Project metadata (name, language, framework, architecture, package manager)
- **paths**: Directory paths (app_root, agentic_root, prompts_dir, adws_dir, specs_dir, etc.)
- **commands**: Build/test/lint commands
- **agentic**: Agentic layer configuration (worktrees, logging, safety, workflows)
- **claude**: Claude Code settings and slash commands
- **templates**: Template file paths
- **bootstrap**: New project initialization options

All fields include validation, defaults, and comprehensive documentation.

## Testing

### Test Model Imports

```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"
```

### Test Model Instantiation and Serialization

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.models import *
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)
print(config.model_dump_json(indent=2))
"
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/domain/
```

### Run Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/domain/
```

## Notes

- This is Phase 2, Task 2.1 from `PLAN_TAC_BOOTSTRAP.md`
- Models serve as the foundation for upcoming tasks: interactive configuration wizard (2.2), YAML loader (2.3), and scaffold generator (2.4)
- No unit test files were created per the task specification - testing will be added in a future phase
- The implementation forbids extra fields via Pydantic configuration to prevent invalid configuration keys
- Smart defaults enable a better UX in the interactive wizard by pre-populating sensible values
- Helper functions will be used by the wizard to dynamically show relevant options based on user selections
