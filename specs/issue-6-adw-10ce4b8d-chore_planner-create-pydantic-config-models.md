# Chore: Create Pydantic Configuration Models

## Metadata
issue_number: `6`
adw_id: `10ce4b8d`
issue_json: `{"number":6,"title":"chore: #5 - Create Pydantic config models","body":"## Summary\n\nThis PR addresses issue #5: Create Pydantic config models for TAC Bootstrap configuration.\n\n### Implementation Plan\n\nRelated to: /Volumes/MAc1/Celes/tac_bootstrap/specs/issue-5-adw-e80a5f17-sdlc_planner-create-pydantic-config-models.md\n\n### Changes\n\n- Updated MCP configuration files (.mcp.json and playwright-mcp-config.json)\n\n### ADW Tracking\n\nADW ID: e80a5f17\n\n### Checklist\n\n- [x] MCP configuration updated\n- [ ] Pydantic models created (tac_bootstrap/domain/models.py)\n- [ ] Enums defined for Language, Framework, Architecture, etc.\n- [ ] Helper functions implemented\n- [ ] Validation logic added\n\n### Notes\n\nThis PR contains the initial configuration changes. The main Pydantic models implementation appears to be incomplete and will need to be added to fully address the issue requirements.\n\nCloses #5"}`

## Chore Description

Complete the implementation of Pydantic v2 configuration models in `tac_bootstrap/domain/models.py` for TAC Bootstrap. This chore finishes issue #5 by implementing the remaining unchecked items from the PR checklist.

The implementation includes:
- Comprehensive Pydantic models covering project, commands, permissions, and hooks configuration
- Enums for Language, Framework, Architecture, PermissionLevel, and HookEvent
- Helper methods for YAML/JSON loading, serialization, and default config generation
- Validation logic for framework-language compatibility and path existence
- Support for both YAML (primary) and JSON config formats
- Sensible defaults throughout all models

This builds upon the MCP configuration changes already completed in the PR and follows the detailed implementation plan from issue #5.

## Relevant Files

### Existing Files to Reference

- `specs/issue-5-adw-e80a5f17-sdlc_planner-create-pydantic-config-models.md` - Original implementation plan with complete requirements
- `config.yml` - Current TAC Bootstrap configuration structure that models must represent
- `tac_bootstrap_cli/pyproject.toml` - Verify Pydantic 2.5.0+ dependency availability
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - Domain package location
- `.claude/settings.json` - Claude settings structure for reference

### New Files to Create

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Complete Pydantic models implementation (main deliverable)
- `tac_bootstrap_cli/tac_bootstrap/domain/exceptions.py` - Custom TACConfigError exception class

## Step by Step Tasks

IMPORTANTE: This chore completes the work from issue #5. Follow the original plan strictly.

### Task 1: Create All Required Enums

Create enum classes in `tac_bootstrap/domain/models.py`:
- `Language` - PYTHON, JAVASCRIPT, TYPESCRIPT, GO, RUST, JAVA
- `Framework` - FASTAPI, DJANGO, FLASK, EXPRESS, NEXTJS, REACT, etc.
- `Architecture` - DDD, LAYERED, HEXAGONAL, CLEAN, SIMPLE
- `PackageManager` - UV, POETRY, PIP, PNPM, NPM, YARN, GO_MOD, CARGO
- `ProjectMode` - NEW, EXISTING
- `AgenticProvider` - CLAUDE_CODE
- `RunIdStrategy` - UUID, TIMESTAMP
- `DefaultWorkflow` - SDLC_ISO, PATCH_ISO, PLAN_IMPLEMENT
- `PermissionLevel` - ALLOW, DENY, ASK
- `HookEvent` - PRE_COMMIT, POST_COMMIT, PRE_TEST, POST_TEST

All enums inherit from `str, Enum` for JSON serialization.

### Task 2: Create Configuration Sub-Models

Implement Pydantic BaseModel classes for each section:
- `ProjectSpec` - name, mode, language, framework, architecture, package_manager, description
  - Add field_validator for `name` to sanitize project names
- `CommandsSpec` - start, test, build, lint, typecheck, format
- `PermissionsSpec` - file_operations, network, subprocess (PermissionLevel)
- `HooksSpec` - pre_commit, post_commit, on_test (lists of shell commands)
- `PathsSpec` - app_root, agentic_root, prompts_dir, etc.
- `WorktreeConfig` - enabled, max_parallel, naming
- `LoggingConfig` - level, capture_agent_transcript, run_id_strategy
- `SafetyConfig` - require_tests_pass, allowed_paths, forbidden_paths
- `AgenticSpec` - provider, model_policy, worktrees, logging, safety, workflows
- `ClaudeSettings` - project_name, preferred_style, allow_shell
- `ClaudeCommandsConfig` - prime, start, build, test, review, ship
- `ClaudeConfig` - settings, commands
- `TemplatesConfig` - plan_template, chore_template, feature_template, etc.
- `BootstrapConfig` - create_git_repo, initial_commit, license, readme

Use `Field()` with defaults and descriptions throughout.

### Task 3: Create Root TACConfig Model

Implement the main configuration model:
- Combine all sub-models as fields
- Add `version: int = Field(1, ...)` for schema versioning
- Configure `model_config = ConfigDict(extra="forbid")`
- Add comprehensive docstring

### Task 4: Implement Cross-Field Validation

Add framework-language compatibility validation:
- Use `@model_validator(mode='after')` on `ProjectSpec`
- Validate framework matches language constraints:
  - FASTAPI/DJANGO/FLASK only with PYTHON
  - EXPRESS/NEXTJS only with JAVASCRIPT/TYPESCRIPT
  - Add other language-framework rules

### Task 5: Implement Helper Methods

Add class methods to `TACConfig`:
- `from_yaml(cls, path: Path) -> TACConfig` - Load from YAML file
- `from_json(cls, path: Path) -> TACConfig` - Load from JSON file
- `to_dict(self) -> dict` - Serialize to dict
- `to_yaml(self, path: Path) -> None` - Save to YAML file
- `to_json(self, path: Path) -> None` - Save to JSON file
- `get_default_config(cls, **overrides) -> TACConfig` - Factory for defaults

Add utility functions:
- `get_frameworks_for_language(language: Language) -> List[Framework]`
- `get_package_managers_for_language(language: Language) -> List[PackageManager]`
- `get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]`

### Task 6: Create Custom Exception

Create `tac_bootstrap/domain/exceptions.py`:
- Define `TACConfigError(Exception)` for domain validation errors
- Import and use in models.py for business logic validation

### Task 7: Verify Import and Instantiation

Test model functionality:
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('Import OK')"`
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.models import TACConfig; config = TACConfig.get_default_config(); print(config.model_dump_json(indent=2))"`
- Verify framework-language validation works correctly

### Task 8: Run All Validation Commands

Execute validation suite to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Implementation Context

This chore completes PR #6 which addresses issue #5. The MCP configuration changes mentioned in the PR body are already complete. This implementation focuses on the remaining unchecked checklist items:
- Pydantic models creation
- Enums definition
- Helper functions
- Validation logic

### Following Original Plan

The detailed implementation plan from `issue-5-adw-e80a5f17-sdlc_planner-create-pydantic-config-models.md` should be followed as the authoritative source. This chore plan summarizes the key requirements.

### Auto-Resolved Clarifications Applied

The auto-resolved clarifications provide critical context:
- Models are independent of MCP configs (those are for Claude's environment)
- Assume no models exist yet - build everything from scratch
- Use Pydantic v2 syntax throughout
- YAML is primary format, JSON is secondary
- Framework-language compatibility is the main cross-field validation
- Let Pydantic ValidationError bubble up, use TACConfigError for domain logic

### No Over-Engineering

Keep implementations focused:
- Only validate essential business rules (framework-language compatibility)
- Don't add speculative validation
- Defaults should be practical and minimal
- Helper functions cover only stated use cases

### Schema Alignment Critical

The models MUST match the actual `config.yml` structure in the repository. Read `config.yml` carefully before implementing to ensure exact alignment.
