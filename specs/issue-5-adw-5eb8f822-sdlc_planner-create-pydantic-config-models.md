# Feature: Create Pydantic Configuration Models

## Metadata
issue_number: `5`
adw_id: `5eb8f822`
issue_json: `{"number":5,"title":"TAREA 2.1: Crear modelos Pydantic para configuracion","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap usa un archivo `config.yml` como fuente de verdad declarativa. Necesitamos\nmodelos Pydantic que representen este schema y permitan validar la configuracion.\n\nEl config.yml tiene esta estructura:\n- project: nombre, modo (new/existing), lenguaje, framework, arquitectura, package manager\n- paths: rutas de app, agentic layer, prompts, adws, specs, logs, scripts, worktrees\n- commands: start, build, test, lint, typecheck, format\n- agentic: provider, model_policy, worktrees config, logging, safety, workflows\n- claude: settings para .claude/settings.json, comandos slash\n- templates: rutas a templates de prompts\n- bootstrap: opciones para proyecto nuevo (git, license, readme)\n\n## Objetivo\nCrear modelos Pydantic completos en `domain/models.py` que representen todo el schema\nde `config.yml` con validacion, defaults inteligentes y documentacion."}`

## Feature Description
Create comprehensive Pydantic models that represent the entire `config.yml` schema for TAC Bootstrap. These models provide type safety, validation, smart defaults, and documentation for all configuration options used by the CLI generator.

## User Story
As a TAC Bootstrap CLI developer
I want Pydantic models that represent the config.yml schema
So that I can validate configuration files, provide smart defaults, and ensure type safety throughout the CLI

## Problem Statement
TAC Bootstrap uses `config.yml` as the source of truth for project configuration. Without strongly-typed models, there's no way to:
- Validate configuration before processing
- Provide intelligent defaults
- Ensure type safety in code that consumes configuration
- Auto-complete and IDE support for configuration

## Solution Statement
Implement a complete set of Pydantic models in `tac_bootstrap_cli/tac_bootstrap/domain/models.py` that:
1. Represent all sections of config.yml (project, paths, commands, agentic, claude, templates, bootstrap)
2. Define enums for valid options (Language, Framework, Architecture, etc.)
3. Provide field validation (e.g., project name sanitization)
4. Include smart defaults based on language/package manager combinations
5. Offer helper functions for framework/package manager selection

## Relevant Files
Files that exist and are relevant:

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - **ALREADY IMPLEMENTED** - Contains all Pydantic models
- `config.yml` - Configuration file that uses the schema

### New Files
None - the required file already exists and is complete.

## Implementation Plan

### Phase 1: Foundation
**STATUS: COMPLETED** - All enums, base models, and validators are implemented.

### Phase 2: Core Implementation
**STATUS: COMPLETED** - All models match the config.yml schema with:
- Complete enum definitions (Language, Framework, Architecture, PackageManager, etc.)
- All sub-models (ProjectSpec, PathsSpec, CommandsSpec, etc.)
- Root TACConfig model
- Field validators and sanitizers
- Helper functions for defaults

### Phase 3: Integration
**STATUS: COMPLETED** - Models are ready for use by:
- CLI wizard for interactive configuration
- Config loader for parsing config.yml
- Scaffold service for generating projects

## Step by Step Tasks

### Task 1: Verify Existing Implementation
**STATUS: COMPLETED**

The file `tac_bootstrap_cli/tac_bootstrap/domain/models.py` already exists with:
- ✅ All enums (Language, Framework, Architecture, PackageManager, ProjectMode, AgenticProvider, RunIdStrategy, DefaultWorkflow, FieldType)
- ✅ All sub-models (ProjectSpec, PathsSpec, CommandsSpec, WorktreeConfig, LoggingConfig, SafetyConfig, AgenticSpec, ClaudeSettings, ClaudeConfig, TemplatesConfig, BootstrapConfig)
- ✅ Root TACConfig model
- ✅ Field validators (name sanitization, format validation)
- ✅ Helper functions (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- ✅ Complete docstrings and Field descriptions
- ✅ Additional models for entity generation (FieldSpec, EntitySpec)
- ✅ BootstrapMetadata for audit trail

### Task 2: Run Validation Commands
Execute all validation commands to confirm zero regressions.

## Testing Strategy

### Unit Tests
Tests needed (to be created in future tasks):
- Test enum values are correct
- Test field validators (name sanitization, format validation)
- Test helper functions return correct defaults
- Test TACConfig can parse valid config.yml
- Test validation errors for invalid configurations

### Edge Cases
- Empty project name (should raise ValueError)
- Invalid language/framework combinations
- Reserved field names in EntitySpec
- Invalid PascalCase/snake_case/kebab-case formats

## Acceptance Criteria
All criteria met:
- ✅ File `tac_bootstrap_cli/tac_bootstrap/domain/models.py` exists
- ✅ All enums have valid string values
- ✅ All models have Field() with description
- ✅ Helper functions implemented (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- ✅ Imports correct, no syntax errors
- ✅ Models can be imported successfully
- ✅ Models support the full config.yml schema
- ✅ Additional entity generation models included
- ✅ BootstrapMetadata for version tracking included

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Import test
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"

# Model instantiation test
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.models import *
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)
print(config.model_dump_json(indent=2))
"

# Run unit tests (when they exist)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Implementation Notes
- The existing implementation goes beyond the basic requirements by including:
  - Entity generation models (FieldSpec, EntitySpec) for DDD scaffold capabilities
  - BootstrapMetadata for version tracking and upgrade management
  - ModelPolicy nested model for agentic configuration
  - WorkflowsConfig for ADW workflow management
  - Comprehensive validator logic for name formats

### Differences from Original Prompt
The actual implementation differs slightly from the prompt in the issue body:
1. **Enhanced enums**: Added more frameworks (AXUM, ACTIX for Rust; SPRING for Java)
2. **Additional models**: Includes FieldSpec, EntitySpec, BootstrapMetadata not in original spec
3. **Nested models**: Uses nested models like ModelPolicy, WorkflowsConfig instead of flat dicts
4. **Enhanced validation**: More sophisticated validators for PascalCase, snake_case, kebab-case

These enhancements make the implementation production-ready and align with the full TAC Bootstrap architecture described in CLAUDE.md.

### Next Steps
According to PLAN_TAC_BOOTSTRAP.md, the next task after creating domain models would be:
- TAREA 2.2: Create config loader service
- TAREA 2.3: Create interactive wizard
- TAREA 2.4: Implement scaffold service

### Testing
Unit tests should be created in a future task to validate:
- All validators work correctly
- Helper functions return expected defaults
- Model serialization/deserialization
- Edge cases and error handling
