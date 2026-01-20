# Chore: Create Pydantic Configuration Models

## Metadata
issue_number: `5`
adw_id: `e80a5f17`
issue_json: `{"number":5,"title":"TAREA 2.1: Crear modelos Pydantic para configuracion","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap usa un archivo `config.yml` como fuente de verdad declarativa. Necesitamos\nmodelos Pydantic que representen este schema y permitan validar la configuracion.\n\nEl config.yml tiene esta estructura:\n- project: nombre, modo (new/existing), lenguaje, framework, arquitectura, package manager\n- paths: rutas de app, agentic layer, prompts, adws, specs, logs, scripts, worktrees\n- commands: start, build, test, lint, typecheck, format\n- agentic: provider, model_policy, worktrees config, logging, safety, workflows\n- claude: settings para .claude/settings.json, comandos slash\n- templates: rutas a templates de prompts\n- bootstrap: opciones para proyecto nuevo (git, license, readme)\n\n## Objetivo\nCrear modelos Pydantic completos en `domain/models.py` que representen todo el schema\nde `config.yml` con validacion, defaults inteligentes y documentacion."}`

## Chore Description

Create comprehensive Pydantic models in `tac_bootstrap/domain/models.py` that represent the entire `config.yml` schema. These models will serve as the foundation for configuration validation, type safety, and documentation throughout the TAC Bootstrap CLI.

The models must:
- Represent all configuration sections from `config.yml`
- Provide smart defaults based on language/framework combinations
- Include field validation (e.g., project name sanitization)
- Support both "new" and "existing" project modes
- Include comprehensive documentation for all fields
- Implement helper functions for framework/package manager selection

## Relevant Files

### Existing Files to Read
- `/Volumes/MAc1/Celes/tac_bootstrap/config.yml` - Current configuration structure that models must represent
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml` - Verify Pydantic dependency is available (>=2.5.0)
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - Ensure domain package exists

### New Files to Create
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Complete Pydantic models (main deliverable)

## Step by Step Tasks

### Task 1: Create Enums for Configuration Options
Create all enum classes that define valid configuration values:
- `Language` - Supported programming languages (Python, TypeScript, JavaScript, Go, Rust, Java)
- `Framework` - Frameworks per language (FastAPI, Django, Next.js, Express, etc.)
- `Architecture` - Software patterns (simple, layered, DDD, clean, hexagonal)
- `PackageManager` - Package managers per language (uv, poetry, pip, pnpm, npm, etc.)
- `ProjectMode` - Initialization mode (new, existing)
- `AgenticProvider` - Agentic provider options (claude_code)
- `RunIdStrategy` - Run ID generation (uuid, timestamp)
- `DefaultWorkflow` - Available workflows (sdlc_iso, patch_iso, plan_implement)

All enums should inherit from `str, Enum` for proper serialization.

### Task 2: Create Sub-Models for Configuration Sections
Implement Pydantic BaseModel classes for each configuration section:
- `ProjectSpec` - Project metadata (name, mode, language, framework, architecture, package_manager)
  - Include field validator for `name` to sanitize project names
- `PathsSpec` - Directory structure (app_root, agentic_root, prompts_dir, etc.)
- `CommandsSpec` - Shell commands (start, build, test, lint, typecheck, format)
- `WorktreeConfig` - Git worktree settings (enabled, max_parallel, naming)
- `LoggingConfig` - Logging configuration (level, capture_agent_transcript, run_id_strategy)
- `SafetyConfig` - Safety constraints (require_tests_pass, allowed_paths, forbidden_paths)
- `AgenticSpec` - Agentic layer config (provider, model_policy, worktrees, logging, safety, workflows)
- `ClaudeSettings` - Claude Code settings (project_name, preferred_style, allow_shell)
- `ClaudeCommandsConfig` - Slash command mappings (prime, start, build, test, review, ship)
- `ClaudeConfig` - Claude configuration wrapper (settings, commands)
- `TemplatesConfig` - Template paths (plan_template, chore_template, feature_template, etc.)
- `BootstrapConfig` - Bootstrap options (create_git_repo, initial_commit, license, readme)

All fields must use `Field()` with comprehensive descriptions.

### Task 3: Create Root Configuration Model
Implement the `TACConfig` class that combines all sub-models:
- Include all section models as fields
- Set `version: int = Field(1, ...)` for schema versioning
- Configure `extra = "forbid"` to catch unknown fields
- Add comprehensive docstring with usage example

### Task 4: Implement Helper Functions
Create utility functions for smart defaults:
- `get_frameworks_for_language(language: Language) -> List[Framework]` - Return valid frameworks for a language
- `get_package_managers_for_language(language: Language) -> List[PackageManager]` - Return valid package managers for a language
- `get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]` - Return default command mappings for language/package manager combinations

These functions will be used by the interactive wizard to provide context-aware defaults.

### Task 5: Verify Import and Model Instantiation
Test that the models can be imported and instantiated correctly:
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"`
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import *; config = TACConfig(project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV), commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'), claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))); print(config.model_dump_json(indent=2))"`

### Task 6: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- Run unit tests: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run linting: `cd tac_bootstrap_cli && uv run ruff check .`
- Run smoke test: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Important Implementation Details
1. **No Test Files Yet** - Per issue instructions, do not create test files for models at this stage
2. **No Scaffolding Logic** - Only create the models, do not implement any scaffolding/generation logic
3. **Schema Alignment** - The models must exactly match the structure in `config.yml` at `/Volumes/MAc1/Celes/tac_bootstrap/config.yml`
4. **Pydantic V2** - Use Pydantic 2.5.0+ syntax (Field, field_validator, model_dump_json)
5. **Type Safety** - Use proper type hints (Optional, List, Dict) from typing module

### Configuration Schema Notes
The `config.yml` has a nested structure that differs slightly from the issue body:
- `agentic.workflows` is an object with `default` and `available` keys, not a flat list
- Models should match the actual `config.yml` structure for validation to work correctly

### Dependencies Already Available
Per `pyproject.toml`, these dependencies are already installed:
- pydantic>=2.5.0
- pyyaml>=6.0.1
- typer>=0.9.0
- rich>=13.7.0

### Model Validation Strategy
The `ProjectSpec.name` validator should:
- Check for non-empty strings
- Strip whitespace
- Convert to lowercase
- Replace spaces with hyphens for safe directory/package naming
