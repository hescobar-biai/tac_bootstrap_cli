# Feature: Create Pydantic Configuration Models

## Metadata
issue_number: `5`
adw_id: `11ee57c0`
issue_json: `{"number":5,"title":"TAREA 2.1: Crear modelos Pydantic para configuracion","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap usa un archivo `config.yml` como fuente de verdad declarativa. Necesitamos\nmodelos Pydantic que representen este schema y permitan validar la configuracion.\n\nEl config.yml tiene esta estructura:\n- project: nombre, modo (new/existing), lenguaje, framework, arquitectura, package manager\n- paths: rutas de app, agentic layer, prompts, adws, specs, logs, scripts, worktrees\n- commands: start, build, test, lint, typecheck, format\n- agentic: provider, model_policy, worktrees config, logging, safety, workflows\n- claude: settings para .claude/settings.json, comandos slash\n- templates: rutas a templates de prompts\n- bootstrap: opciones para proyecto nuevo (git, license, readme)\n\n## Objetivo\nCrear modelos Pydantic completos en `domain/models.py` que representen todo el schema\nde `config.yml` con validacion, defaults inteligentes y documentacion."}`

## Feature Description
This feature implements the foundational data models for TAC Bootstrap CLI using Pydantic. These models represent the complete schema of the `config.yml` configuration file, providing validation, smart defaults, and comprehensive documentation for all configuration options. The models follow Domain-Driven Design (DDD) principles and serve as the single source of truth for configuration structure throughout the CLI application.

## User Story
As a TAC Bootstrap CLI developer
I want strongly-typed Pydantic models for the config.yml schema
So that I can validate user configuration, provide intelligent defaults, and ensure type safety throughout the application

## Problem Statement
The TAC Bootstrap CLI requires a declarative configuration file (`config.yml`) that defines project settings, paths, commands, agentic layer configuration, and more. Without proper data models:
- Configuration validation is difficult or impossible
- No type safety when accessing configuration values
- Difficult to provide intelligent defaults
- No clear documentation of expected configuration structure
- Risk of runtime errors from invalid or missing configuration

## Solution Statement
Create comprehensive Pydantic models in `tac_bootstrap/domain/models.py` that:
1. Define all configuration sections as typed models with validation
2. Provide smart defaults based on language and package manager
3. Include clear documentation via Field descriptions
4. Implement validation rules for critical fields
5. Expose helper functions for language-specific defaults
6. Follow DDD principles by placing models in the domain layer

## Relevant Files
Files necessary for implementing this feature:

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Main models file to create (contains all Pydantic models)
- `config.yml` - Reference for understanding the schema structure
- `PLAN_TAC_BOOTSTRAP.md` - Contains the detailed specification for this task
- `CLAUDE.md` - Project guidelines and DDD architecture reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Complete Pydantic models with enums, sub-models, root model, and helper functions

## Implementation Plan

### Phase 1: Foundation
1. Create the domain directory structure if it doesn't exist
2. Set up the base models.py file with proper imports
3. Define all enum classes (Language, Framework, Architecture, PackageManager, etc.)

### Phase 2: Core Implementation
1. Implement sub-models for each configuration section:
   - ProjectSpec
   - PathsSpec
   - CommandsSpec
   - WorktreeConfig
   - LoggingConfig
   - SafetyConfig
   - AgenticSpec
   - ClaudeSettings
   - ClaudeCommandsConfig
   - ClaudeConfig
   - TemplatesConfig
   - BootstrapConfig
2. Implement the root TACConfig model that composes all sub-models
3. Add field validators where needed (e.g., project name validation)

### Phase 3: Integration
1. Implement helper functions:
   - `get_frameworks_for_language()`
   - `get_package_managers_for_language()`
   - `get_default_commands()`
2. Add comprehensive docstrings to all models and functions
3. Verify imports and syntax

## Step by Step Tasks

### Task 1: Create domain directory and base file structure
- Create `tac_bootstrap_cli/tac_bootstrap/domain/` directory if not exists
- Create `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` (empty)
- Create `tac_bootstrap_cli/tac_bootstrap/domain/models.py` with module docstring and imports

### Task 2: Define all enum classes
- Implement Language enum with python, typescript, javascript, go, rust, java
- Implement Framework enum with framework options per language
- Implement Architecture enum with simple, layered, ddd, clean, hexagonal
- Implement PackageManager enum with package managers per language
- Implement ProjectMode enum with new/existing
- Implement AgenticProvider enum (claude_code)
- Implement RunIdStrategy enum (uuid/timestamp)
- Implement DefaultWorkflow enum

### Task 3: Implement configuration sub-models
- Create ProjectSpec with name, mode, repo_root, language, framework, architecture, package_manager
- Create PathsSpec with all directory paths (app_root, agentic_root, prompts_dir, etc.)
- Create CommandsSpec with start, build, test, lint, typecheck, format commands
- Create WorktreeConfig with enabled, max_parallel, naming
- Create LoggingConfig with level, capture_agent_transcript, run_id_strategy
- Create SafetyConfig with require_tests_pass, require_review_artifacts, allowed_paths, forbidden_paths
- Create AgenticSpec composing worktrees, logging, safety configs

### Task 4: Implement Claude-specific models
- Create ClaudeSettings with project_name, preferred_style, allow_shell
- Create ClaudeCommandsConfig mapping slash commands to prompt files
- Create ClaudeConfig composing settings and commands
- Create TemplatesConfig with template paths
- Create BootstrapConfig with git/license/readme options

### Task 5: Implement root TACConfig model
- Create TACConfig composing all sub-models
- Add version field with default value 1
- Configure Pydantic to forbid extra fields
- Add comprehensive docstring with usage example

### Task 6: Add field validators
- Implement name validator in ProjectSpec to sanitize project names
- Ensure validation for integer constraints (e.g., max_parallel ge=1, le=20)

### Task 7: Implement helper functions
- Create get_frameworks_for_language() mapping languages to available frameworks
- Create get_package_managers_for_language() mapping languages to package managers
- Create get_default_commands() providing smart defaults per language/package manager combination
- Include Python (uv/poetry), TypeScript (pnpm/npm), and Go defaults

### Task 8: Verify implementation
- Check all imports are correct
- Verify no syntax errors
- Run verification commands to test model imports and instantiation
- Execute validation commands (see below)

## Testing Strategy

### Unit Tests
No unit tests required for this task (specified in issue: "No crear archivos de test aun")

### Edge Cases
- Empty or whitespace project names (handled by validator)
- Invalid language/framework/package manager combinations
- Missing required fields
- Extra unknown fields (rejected by Pydantic config)

## Acceptance Criteria
- [x] File `tac_bootstrap_cli/tac_bootstrap/domain/models.py` created with all models
- [x] All enums have valid string values
- [x] All models have Field() with description parameter
- [x] Helper functions implemented (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- [x] Imports are correct with no syntax errors
- [x] Models can be imported successfully
- [x] TACConfig can be instantiated with valid data
- [x] Model serialization to JSON works correctly

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Test model imports
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"

# Test model instantiation and serialization
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.models import *
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)
print(config.model_dump_json(indent=2))
"

# Run linting (if ruff is configured)
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/domain/ || echo "Ruff not configured yet"

# Run type checking (if mypy is configured)
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/domain/ || echo "Mypy not configured yet"
```

## Notes
- This is Phase 2, Task 2.1 from PLAN_TAC_BOOTSTRAP.md
- Following DDD architecture: models go in domain/ layer
- Models serve as foundation for subsequent tasks (interactive wizard, YAML loader, etc.)
- No test files should be created yet (per task specification)
- No scaffold logic should be implemented yet
- The complete model code is provided in the issue body and should be used as-is
- Smart defaults are crucial for good UX in the interactive wizard (future task)
- Helper functions will be used by the wizard to show relevant options based on user selections
