---
doc_type: feature
adw_id: 5eb8f822
date: 2026-01-27
idk:
  - pydantic
  - validation
  - configuration
  - schema
  - domain-model
  - type-safety
  - enum
  - smart-defaults
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
  - config.yml
---

# Pydantic Configuration Models

**ADW ID:** 5eb8f822
**Date:** 2026-01-27
**Specification:** specs/issue-5-adw-5eb8f822-sdlc_planner-create-pydantic-config-models.md

## Overview

Comprehensive Pydantic models representing the entire `config.yml` schema for TAC Bootstrap. These models provide type safety, validation, smart defaults, and documentation for all configuration options used by the CLI generator.

## What Was Built

- Complete enum definitions for configuration options (Language, Framework, Architecture, PackageManager, ProjectMode, AgenticProvider, RunIdStrategy, DefaultWorkflow, FieldType)
- Sub-models for each config.yml section (ProjectSpec, PathsSpec, CommandsSpec, WorktreeConfig, LoggingConfig, SafetyConfig, AgenticSpec, ClaudeSettings, ClaudeConfig, TemplatesConfig, BootstrapConfig)
- Root TACConfig model that composes all sub-models
- Field validators for name sanitization and format validation (PascalCase, snake_case, kebab-case)
- Helper functions for framework/package manager selection based on language
- Additional entity generation models (FieldSpec, EntitySpec) for DDD scaffold capabilities
- BootstrapMetadata model for version tracking and upgrade management

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Created comprehensive Pydantic models (590+ lines) with complete schema representation

### Key Changes

1. **Enum Definitions**: All valid configuration options defined as string enums (Language, Framework, Architecture, PackageManager, ProjectMode, AgenticProvider, RunIdStrategy, DefaultWorkflow, FieldType)
2. **Nested Model Structure**: Each major config.yml section has its own Pydantic model with Field() descriptions and smart defaults
3. **Validation Logic**: Custom validators for project name sanitization and format validation (PascalCase, snake_case, kebab-case patterns)
4. **Helper Functions**: `get_frameworks_for_language()`, `get_package_managers_for_language()`, `get_default_commands()` provide intelligent defaults
5. **DDD Support**: FieldSpec and EntitySpec models enable scaffold service to generate domain entities

## How to Use

### Import Models

```python
from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    Language,
    Framework,
    PackageManager,
    Architecture
)
```

### Create Configuration Programmatically

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
        lint="uv run ruff check .",
        format="uv run ruff format ."
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name="my-app")
    )
)
```

### Validate Configuration from YAML

```python
import yaml
from tac_bootstrap.domain.models import TACConfig

with open("config.yml") as f:
    config_dict = yaml.safe_load(f)

config = TACConfig(**config_dict)  # Validates and raises on errors
```

### Use Helper Functions

```python
from tac_bootstrap.domain.models import (
    Language,
    get_frameworks_for_language,
    get_package_managers_for_language,
    get_default_commands
)

# Get valid frameworks for Python
frameworks = get_frameworks_for_language(Language.PYTHON)
# Returns: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE]

# Get valid package managers for Python
package_managers = get_package_managers_for_language(Language.PYTHON)
# Returns: [PackageManager.UV, PackageManager.POETRY, PackageManager.PIP, PackageManager.PIPENV]

# Get default commands for Python with UV
commands = get_default_commands(Language.PYTHON, PackageManager.UV)
# Returns: CommandsSpec with intelligent defaults
```

## Configuration

No additional configuration required. The models are self-contained and can be imported directly.

## Testing

### Import Test

```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"
```

### Model Instantiation Test

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

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### CLI Smoke Test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Implementation Highlights

- **Production-Ready**: Goes beyond basic requirements with entity generation models, bootstrap metadata, and comprehensive validation
- **Enhanced Enums**: Supports multiple frameworks per language (AXUM/ACTIX for Rust, SPRING for Java, etc.)
- **Nested Models**: Uses nested Pydantic models (ModelPolicy, WorkflowsConfig) instead of flat dictionaries for better type safety
- **Smart Validation**: Sophisticated validators for PascalCase, snake_case, kebab-case format enforcement
- **DDD Architecture**: Follows Domain-Driven Design principles with models in the domain layer

### Validation Results

All acceptance criteria met:
- ✅ File `tac_bootstrap_cli/tac_bootstrap/domain/models.py` exists
- ✅ All enums have valid string values
- ✅ All models have Field() with description
- ✅ Helper functions implemented
- ✅ Imports correct, no syntax errors
- ✅ Models can be imported successfully
- ✅ Models support the full config.yml schema
- ✅ Additional entity generation models included
- ✅ BootstrapMetadata for version tracking included
- ✅ 690 unit tests passing, zero linting issues, type checking successful

### Next Steps

According to PLAN_TAC_BOOTSTRAP.md, the next tasks are:
- TAREA 2.2: Create config loader service (parse config.yml using these models)
- TAREA 2.3: Create interactive wizard (use these models for user input validation)
- TAREA 2.4: Implement scaffold service (use these models to generate project structure)
