# Changelog

All notable changes to TAC Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.11.2] - 2026-02-10

### Added - 3-Tier Runtime Model Configuration System

**Core Model Configuration:**
- **`get_model_id(model_type)` function** in `adw_modules/workflow_ops.py` - Implements 3-tier resolution hierarchy:
  1. Environment variables (`ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`)
  2. Configuration file (`config.yml: agentic.model_policy.{opus,sonnet,haiku}_model`)
  3. Hardcoded defaults (Opus: `claude-opus-4-5-20251101`, Sonnet: `claude-sonnet-4-5-20250929`, Haiku: `claude-haiku-4-5-20251001`)

**Configuration Schema Extension:**
- `config.yml` - Added optional fields to `agentic.model_policy`:
  - `opus_model: Optional[str]` - Override Opus model ID
  - `sonnet_model: Optional[str]` - Override Sonnet model ID
  - `haiku_model: Optional[str]` - Override Haiku model ID
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Extended Pydantic `ModelPolicy` with three new optional fields

**Dynamic Model Resolution Functions:**
- `get_resolved_model_opus()`, `get_resolved_model_sonnet()`, `get_resolved_model_haiku()` in `adw_agent_sdk.py`
- `get_model_fallback_chain()` in `agent.py` - Returns dynamic fallback mapping with resolved model IDs
- `get_fallback_model(current_model)` in `agent.py` - Retrieves fallback model for any given model
- `get_fast_model()` in `adw_summarizer.py` - Returns Haiku model ID for fast operations

**Orchestrator Updates:**
- `adw_sdlc_zte_iso.py` - Updated 6 phases (plan, build, test, review, document, ship) to use `get_model_id("sonnet")`
- `adw_sdlc_iso.py` - Updated 5 phases (plan, build, test, review, document) to use dynamic model resolution
- `adw_ship_iso.py` - Updated ship phase orchestrator

**Workflow Updates:**
- `adw_plan_build_review.py` - Updated model parameter initialization to use `get_model_id("opus")`
- `adw_plan_build_review_fix.py` - Updated plan, build, review, and fix models to use dynamic resolution

**Template Synchronization:**
- 11 Jinja2 templates synchronized with source implementations:
  - `adws/adw_modules/workflow_ops.py.j2`
  - `adws/adw_modules/agent.py.j2`
  - `adws/adw_modules/adw_summarizer.py.j2`
  - `adws/adw_modules/adw_agent_sdk.py.j2`
  - `adws/adw_sdlc_zte_iso.py.j2`, `adws/adw_sdlc_iso.py.j2`, `adws/adw_ship_iso.py.j2`
  - `adws/adw_workflows/adw_plan_build_review.py.j2`
  - `adws/adw_workflows/adw_plan_build_review_fix.py.j2`
  - `config/config.yml.j2` (with conditional Jinja2 rendering)

**Environment Variable Documentation:**
- `.env.example` - Added optional section documenting 3 new environment variables for model configuration

**Comprehensive Testing & Documentation:**
- `adws/tests/test_model_configuration.py` - 23-test suite covering:
  - 3-tier resolution hierarchy verification
  - Environment variable override validation
  - Configuration file loading
  - Model fallback chain logic
  - Fast model resolution
  - Edge cases and error handling
- `MODEL_CONFIGURATION.md` - Complete documentation with:
  - Usage examples for all three configuration methods
  - API reference for all resolver functions
  - Architecture details and implementation flow
  - Migration guide for existing projects
  - Troubleshooting section
  - Future enhancement ideas

**Additional Templates:**
- `.claude/commands/create-gh-issue.md` - Command template for creating GitHub issues from task files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py.j2` - ScaffoldService template for project generation

**CLI Roadmap:**
- `CLI_ROADMAP_100PERCENT.md` - Comprehensive analysis of 20 features needed for 100% CLI completeness:
  - 3 Tier 1 CRITICAL features (11h effort)
  - 7 Tier 2 IMPORTANT features (18h effort)
  - 10 Tier 3 NICE-TO-HAVE features (20h effort)
  - 4-6 week implementation timeline with effort estimates

### Changed
- All orchestrators and workflows now dynamically resolve model IDs at runtime
- `MODEL_FALLBACK_CHAIN` refactored from static dict to `get_model_fallback_chain()` function
- `FAST_MODEL` now calls `get_fast_model()` for dynamic resolution
- New projects inherit complete model configuration system through template synchronization

### Benefits
- 🔄 **Runtime Configuration** - Change Claude models without code modifications
- 💰 **Cost Optimization** - Use cheaper models (Haiku) for testing, premium models (Opus) for production
- 🌍 **Environment Flexibility** - Different models for dev, staging, production
- 🔒 **Vendor Stability** - Pin to specific model versions for reproducibility
- ✅ **Zero Breaking Changes** - 100% backward compatible with existing projects

## [0.10.4] - 2026-02-09

### Fixed
- **Complete scaffolding overhaul for `upgrade --with-orchestrator`**: Consolidated fixes from 0.10.1-0.10.3 and verified end-to-end upgrade succeeds
- **`apps/` bulk directory copy**: `_add_orchestrator_apps()` now walks `templates/apps/` recursively with `os.walk()`, copying all ~207 source files instead of listing ~60 individually
- **53 previously unregistered templates**: All triggers, workflows, tests, commands, experts, output styles, and scripts now registered in scaffold plan
- **`FileAction.CREATE` during upgrades**: Orchestrator files use `OVERWRITE` when `existing_repo=True`
- **`add-agentic --with-orchestrator` wizard**: Parameter now propagated through wizard to `OrchestratorConfig`
- **Removed non-existent template references**: `frontend/.env.j2`, `frontend/tsconfig.json`, `playwright.config.ts.j2` and 7 other phantom files that caused upgrade rollback

### Changed
- `scaffold_service.py` - Replaced `_add_orchestrator_database()`, `_add_orchestrator_backend()`, `_add_orchestrator_frontend()` with single `_add_orchestrator_apps()` using `os.walk()`
- `scaffold_service.py` - 100% template registration coverage across all categories
- `wizard.py` - `run_add_agentic_wizard()` accepts `with_orchestrator: bool`
- `cli.py` - `add_agentic()` passes `with_orchestrator` to wizard
- `upgrade_service.py` - Preview includes both `orchestrator_3_stream` and `orchestrator_db`
- Excludes build artifacts: `.venv`, `node_modules`, `__pycache__`, `.mypy_cache`, `.pytest_cache`, `logs`

## [0.10.3] - 2026-02-09

### Fixed
- **`apps/` templates not fully copied during upgrade**: `_add_orchestrator_frontend()`, `_add_orchestrator_backend()`, and `_add_orchestrator_database()` listed files individually, missing ~140 files (`.claude/`, `app_docs/`, `specs/`, root configs). Replaced with bulk `_add_orchestrator_apps()` that walks `templates/apps/` recursively
- **Non-existent template references causing upgrade failure**: `frontend/.env.j2`, `frontend/tsconfig.json`, `frontend/env.d.ts`, `playwright.config.ts.j2`, and 6 Playwright test files were referenced but did not exist on disk, causing `upgrade --with-orchestrator` to fail and rollback

### Changed
- `scaffold_service.py` - Replaced `_add_orchestrator_database()`, `_add_orchestrator_backend()`, `_add_orchestrator_frontend()` with single `_add_orchestrator_apps()` that uses `os.walk()` to copy entire `apps/orchestrator_db/` and `apps/orchestrator_3_stream/` directories
- `scaffold_service.py` - Removed Playwright test references from `_add_test_files()` (now handled by bulk app copy)
- Excludes build artifacts: `.venv`, `node_modules`, `__pycache__`, `.mypy_cache`, `.pytest_cache`, `logs`

## [0.10.2] - 2026-02-08

### Fixed
- **53 unregistered templates in `scaffold_service.py`**: Templates existed on disk but were not registered in the scaffold plan, so they were silently excluded from generated projects during `init`, `add-agentic`, and `upgrade`

### Added
- **ADW Triggers (2)**: `adw_manual_trigger.py`, `adw_scripts.py` registered in `_add_adw_files()`
- **ADW Root Workflow (1)**: `adw_database.py` added to workflows list
- **ADW Tests (8 + 1 submodule)**: `__init__.py`, `health_check.py`, `sandbox_poc.py`, `test_agents.py`, `test_model_selection.py`, `test_r2_uploader.py`, `test_webhook_simplified.py`, `adw_tests/adw_modules/adw_agent_sdk.py` registered in `_add_test_files()`
- **Schema Migration (1)**: `migrations/001_initial.sql` registered in `_add_schema_files()`
- **Commands (6)**: `/fix`, `/ping`, `/prime_nile`, `/prime_specific_docs`, `/question-w-mermaid-diagrams`, `/start_nile` added to commands list
- **Expert Commands (10 + 2 expertise files)**: `database/{question,self-improve}`, `websocket/{question,self-improve,plan,plan_build_improve}`, `adw/{plan,plan_build_improve}` commands and `database/expertise.yaml`, `websocket/expertise.yaml` seed files
- **Expert Directories (2)**: `.claude/commands/experts/database`, `.claude/commands/experts/websocket` added to `_add_directories()`
- **Output Styles (11)**: `bullet-points`, `genui`, `html-structured`, `markdown-focused`, `observable-tools-diffs-tts`, `observable-tools-diffs`, `table-based`, `tts-summary-base`, `tts-summary`, `ultra-concise`, `yaml-structured`
- **Scripts (15)**: `kill_trigger_webhook.sh`, `aea_server_start.sh`, `aea_server_reset.sh`, `clear_issue_comments.sh`, `copy_dot_env.sh`, `check_ports.sh`, `copy_claude.py`, `delete_pr.sh`, `dev_build.sh`, `dev_lint.sh`, `dev_start.sh`, `dev_test.sh`, `expose_webhook.sh`, `reset_db.sh`, `stop_apps.sh`

### Changed
- `scaffold_service.py` - All template categories now have 100% registration coverage matching templates on disk

## [0.10.1] - 2026-02-08

### Fixed
- **`apps/orchestrator_db/` not copied on `upgrade --with-orchestrator`**: `_add_orchestrator_database()` and `_add_orchestrator_backend()` used `FileAction.CREATE` (skip if exists) even during upgrades. Changed to `FileAction.OVERWRITE` when `existing_repo=True` so files are properly created/updated
- **`add-agentic --with-orchestrator` ignored in interactive mode**: `run_add_agentic_wizard()` did not accept `with_orchestrator` parameter, so orchestrator was never enabled when using the interactive wizard. Added parameter and propagated to `OrchestratorConfig`
- **`cli.py` did not pass `with_orchestrator` to wizard**: `add_agentic` command in interactive mode called `run_add_agentic_wizard(repo_path, detected)` without the flag
- **Upgrade preview missing `orchestrator_db`**: `get_changes_preview()` only showed `apps/orchestrator_3_stream/` but not `apps/orchestrator_db/`. Now shows both directories
- **Silent error swallowing in orchestrator scaffolding**: All 5 orchestrator template-reading loops used `except Exception: continue` which hid file-not-found errors. Changed to `except FileNotFoundError` with warning output

### Changed
- `scaffold_service.py` - `_add_orchestrator_database()` and `_add_orchestrator_backend()` use `OVERWRITE` for existing repos
- `wizard.py` - `run_add_agentic_wizard()` accepts `with_orchestrator: bool` parameter
- `cli.py` - `add_agentic()` passes `with_orchestrator` to wizard; updated `--with-orchestrator` help text to mention `orchestrator_db`
- `upgrade_service.py` - `get_changes_preview()` includes `orchestrator_db` directory status

## [0.10.0] - 2026-02-08

### Added - PostgreSQL Migration & Orchestrator Production-Ready

**PostgreSQL Database Layer (`apps/orchestrator_db/`):**
- Migrated orchestrator from SQLite to PostgreSQL for production-grade concurrency and scalability
- 11 SQL migration files with incremental schema evolution (0-10):
  - `0_orchestrator_agents.sql` - Core orchestrator agents table
  - `1_agents.sql` - Runtime agents with status tracking
  - `2_prompts.sql` - Prompt versioning and storage
  - `3_agent_logs.sql` - Structured agent execution logs
  - `4_system_logs.sql` - System-level event logging
  - `5_indexes.sql` - Performance indexes for all tables
  - `6_functions.sql` - PostgreSQL functions (updated_at triggers)
  - `7_triggers.sql` - Automatic timestamp triggers
  - `8_orchestrator_chat.sql` - Chat/conversation persistence
  - `9_ai_developer_workflows.sql` - ADW workflow state tracking
  - `10_adw_orchestrator_agent.sql` - ADW-orchestrator agent linking
- `run_migrations.py` - Migration runner with version tracking and rollback support
- `models.py` - Pydantic models for all PostgreSQL tables
- `sync_models.py` - Model-to-schema synchronization utility
- `drop_table.py` - Safe table drop with dependency awareness
- `git_utils.py` - Git integration utilities for DB operations

**Orchestrator Backend Modularization (`apps/orchestrator_3_stream/backend/modules/`):**
- `database.py` - PostgreSQL async database manager (replaces SQLite aiosqlite)
- `agent_manager.py` - Agent lifecycle management with state machine
- `autocomplete_agent.py` - AI-powered autocomplete with expert system prompts
- `autocomplete_models.py` - Pydantic models for autocomplete sessions
- `autocomplete_service.py` - Autocomplete session orchestration
- `command_agent_hooks.py` - Hook system for command-level agent execution
- `config.py` - Centralized configuration with PostgreSQL connection settings
- `event_summarizer.py` - AI event summarization for log reduction
- `file_tracker.py` - File change tracking and visualization
- `hooks.py` - Orchestrator hook management system
- `logger.py` - Structured logging with PostgreSQL persistence
- `orch_database_models.py` - Database models for orchestrator tables
- `orchestrator_hooks.py` - Orchestrator-specific lifecycle hooks
- `orchestrator_service.py` - Core orchestrator business logic
- `single_agent_prompt.py` - Single agent prompt execution
- `slash_command_parser.py` - Slash command discovery and parsing
- `subagent_loader.py` - Dynamic subagent loading from command definitions
- `subagent_models.py` - Pydantic models for subagent configurations
- `websocket_manager.py` - WebSocket connection manager for real-time updates

**Backend Tests (`apps/orchestrator_3_stream/backend/tests/`):**
- `test_database.py` - PostgreSQL connection and CRUD tests
- `test_agent_events.py` - Agent event lifecycle tests
- `test_autocomplete_agent.py` - Autocomplete AI agent tests
- `test_autocomplete_endpoints.py` - Autocomplete API endpoint tests
- `test_display.py` - Display rendering tests
- `test_slash_command_discovery.py` - Slash command parsing tests
- `test_websocket_raw.py` - WebSocket raw connection tests

**New Agent Experts:**
- Database Expert (`experts/database/`) - expertise.yaml, question, self-improve commands
- WebSocket Expert (`experts/websocket/`) - expertise.yaml, plan, plan_build_improve, question, self-improve commands
- ADW Expert enhancements - plan and plan_build_improve commands

**New Commands:**
- `/fix` - Fix issues identified in code review reports
- `/ping` - Simple connectivity check
- `/prime_nile` - Prime agents with Nile adaptive shopping app context
- `/prime_specific_docs` - Load specific documentation from ai_docs
- `/question-w-mermaid-diagrams` - Q&A with Mermaid diagram visualization
- `/start_nile` - Start Nile backend (port 8000) and frontend (port 5173)

**New Output Styles (11 presets):**
- `bullet-points.md` - Bullet point format
- `genui.md` - Generative UI format
- `html-structured.md` - HTML structured output
- `markdown-focused.md` - Markdown-first format
- `observable-tools-diffs.md` - Tool diffs with observability
- `observable-tools-diffs-tts.md` - Tool diffs with TTS support
- `table-based.md` - Table-based output
- `tts-summary-base.md` - TTS summary base format
- `tts-summary.md` - TTS summary with details
- `ultra-concise.md` - Ultra concise format
- `yaml-structured.md` - YAML structured output

**New Scripts:**
- `scripts/copy_claude.py` - Copy `.claude/` configuration between projects
- Templates for: `check_ports.sh`, `delete_pr.sh`, `dev_build.sh`, `dev_lint.sh`, `dev_start.sh`, `dev_test.sh`, `expose_webhook.sh`, `reset_db.sh`, `stop_apps.sh`

**New ADW Components:**
- `adw_summarizer.py` - AI-powered event and log summarization module
- `adw_manual_trigger.py` - Manual trigger for ADW workflows
- `adw_scripts.py` - ADW utility scripts
- `adw_tests/adw_modules/adw_agent_sdk.py` - Agent SDK test suite

**Orchestrator App Documentation (`app_docs/`):**
- 30+ documentation files covering backend architecture, frontend structure, autocomplete system, responsive UI, and database schema
- Backend quick start guide and module reference
- Swimlane and scout reports for architecture analysis

**Orchestrator App Specs:**
- Agent file tracking visualization spec
- Global command input bar spec
- Responsive UI plan
- Orchestrator chat width toggle spec

### Changed

**PostgreSQL Migration (SQLite → PostgreSQL):**
- `adw_database.py` - Rewritten for PostgreSQL with asyncpg/psycopg2 support
- `adw_db_bridge.py` - Updated database bridge for PostgreSQL connections
- `adw_logging.py` - Structured logging now persists to PostgreSQL
- `adw_websockets.py` - WebSocket manager updated for PostgreSQL event sourcing
- `orch_database_models.py` - Models updated for PostgreSQL data types (UUID, JSONB, TIMESTAMPTZ)
- `backend/main.py` - Consolidated FastAPI app with PostgreSQL lifespan management
- `backend/.env.sample` - Updated with PostgreSQL connection variables

**Backend Architecture Refactor:**
- Removed legacy router-based architecture (`routers/agents.py`, `routers/runtime.py`, `routers/websocket.py`, `routers/compat.py`)
- Replaced with modular service architecture (19 modules in `backend/modules/`)
- Removed legacy `backend/config.py`, `backend/dependencies.py`, `backend/logger.py`, `backend/__init__.py`

**Consolidated ADW Workflows (Database-Backed):**
- `adw_plan_build.py` - Major rewrite with PostgreSQL logging integration
- `adw_plan_build_review.py` - Enhanced with PostgreSQL-backed review tracking
- `adw_plan_build_review_fix.py` - Self-healing workflow with PostgreSQL state persistence

**Template Synchronization:**
- All base files synced to Jinja2 templates (100% coverage maintained)
- New `apps/orchestrator_3_stream/` template with full `.claude/` configuration
- New `apps/orchestrator_db/` template with migration system
- Removed obsolete `schema/schema_orchestrator.sql` (replaced by migration system)
- Removed legacy Playwright tests and config (replaced by backend test suite)
- Removed `frontend/package-lock.json`, `frontend/.env.example`, `frontend/env.d.ts`, `frontend/tsconfig.json`

**Scaffold Service:**
- Extended to generate PostgreSQL orchestrator database structure
- Updated app templates for new modular backend architecture

**Makefile:**
- Updated orchestrator targets for PostgreSQL (connection string, migrations)

### Removed
- `schema/schema_orchestrator.sql` - Replaced by incremental migration system in `apps/orchestrator_db/migrations/`
- Legacy router files (`routers/__init__.py`, `routers/agents.py`, `routers/compat.py`, `routers/runtime.py`, `routers/websocket.py`)
- Legacy backend config files (`backend/config.py`, `backend/dependencies.py`, `backend/logger.py`, `backend/__init__.py`, `backend/README.md`)
- Playwright test suite and config (replaced by pytest backend tests)
- Frontend build artifacts (`package-lock.json`, `env.d.ts`, `tsconfig.json`, `.env.example`)

## [0.9.9] - 2026-02-06

### Fixed
- **`ValueError: Invalid format specifier` in `workflow_ops.py`**: JSON examples inside f-strings had unescaped `{` and `}` braces (in `clarify_issue()` and `resolve_clarifications()` functions). Fixed to `{{` and `}}` in both the base file and the Jinja2 template (`{% raw %}` blocks now output double-braces)

## [0.9.8] - 2026-02-06

### Fixed
- **`adw_plan_iso.py` UnboundLocalError**: `worktree_path` was referenced before assignment when `validate_worktree()` returned invalid. Added `worktree_path = None` initialization
- **Version references in test templates**: `test_database.py.j2` and `test_websockets.py.j2` had hardcoded `0.9.5` instead of `0.8.0`; `adw_database.py.j2` referenced `v0.9.5+` instead of `v0.9.0+`
- **Typer dependency version**: `pyproject.toml` had `typer>=0.9.5` (linter artifact) instead of `typer>=0.9.4`
- **Missing `setup_worktree.sh` in generated projects**: `adw_plan_iso.py` calls `scripts/setup_worktree.sh` but the scaffold service didn't include it. Workflows failed with `No such file or directory`. Added to `_add_script_files()` in `scaffold_service.py`
- **Wrong `database_url` default in `OrchestratorConfig`**: Pydantic model default was `sqlite:///orchestrator.db` instead of `sqlite:///data/orchestrator.db`, causing generated `config.yml` to point to wrong DB path
- **Makefile and `setup_database.sh` not updated on upgrade**: Both used `FileAction.CREATE` (skip if exists), so `tac-bootstrap upgrade` never refreshed them. Changed to `OVERWRITE` for existing repos

### Added
- **9 missing ADW templates**: Synced base `adws/` files to templates that had no `.j2` counterpart:
  - `adw_database.py.j2` - Top-level database initialization script
  - `adw_tests/__init__.py.j2`, `health_check.py.j2`, `sandbox_poc.py.j2` - Test infrastructure
  - `adw_tests/test_agents.py.j2`, `test_model_selection.py.j2`, `test_r2_uploader.py.j2`, `test_webhook_simplified.py.j2` - Test suites
  - `schema/migrations/001_initial.sql.j2` - Initial DB migration
- **5 missing skill templates**: Created `.j2` templates for `meta-skill` and `start-orchestrator` skills
- **`.claude/hooks/utils/__init__.py`** in base directory

### Changed
- **`adw_plan_iso.py.j2`**: Major sync with base - early worktree creation before docs loading, cached branch name support, `setup_worktree.sh` integration
- **`adw_test_iso.py.j2`**: Synced `.ports.env` auto-detection documentation
- **Skill templates consolidated**: Moved from `templates/.claude/skills/` to `templates/claude/skills/` for consistency; updated `scaffold_service.py` references
- Deleted 3 residual `.bak` files from `templates/claude/commands/`

## [0.9.5] - 2026-02-06

### Fixed
- **Database path mismatch in `setup_database.sh`**: Default `DB_PATH` was `orchestrator.db` (project root) but `adw_db_bridge.py` reads from `data/orchestrator.db`. Fixed default to `data/orchestrator.db`
- **Missing context bundle functions in `workflow_ops.py.j2`**: Template was missing 4 functions required by ADW workflows: `get_context_bundle_path`, `create_context_bundle`, `update_context_bundle_decisions`, `load_context_bundle`. Caused `ImportError` when running `adw_sdlc_iso.py`

## [0.9.4] - 2026-02-06

### Fixed
- **Missing orchestrator frontend files**: `tsconfig.node.json`, `env.d.ts`, `start.sh`, and `public/favicon.svg` were absent from scaffold templates, causing Vite build errors (`ENOENT: tsconfig.node.json`)

### Added
- Templates: `tsconfig.node.json`, `env.d.ts`, `start.sh`, `public/favicon.svg` for orchestrator frontend
- `scaffold_service.py`: New `frontend_root_files` block for static root-level frontend files

## [0.9.3] - 2026-02-06

### Fixed
- **Orchestrator frontend `.j2` files not rendered**: `scaffold_service.py` wrote output files as `.env.j2` and `vite.config.ts.j2` instead of `.env` and `vite.config.ts`. Templates were rendered correctly but output paths kept the `.j2` suffix.

## [0.9.2] - 2026-02-06

### Fixed
- **Jinja2 template render error in `adw_db_bridge.py.j2`**: Python f-string escaped braces `{{` were interpreted as Jinja2 print statements, causing `expected token 'end of print statement', got ':'` during scaffold/upgrade. Wrapped template in `{% raw %}` block.
- **Upgrade error reporting**: `perform_upgrade()` now prints individual file failure details before restoring from backup, instead of only showing generic "N error(s) occurred"

## [0.9.1] - 2026-02-06

### Fixed
- **`--with-orchestrator` ignored in interactive mode**: Flag was not passed from CLI to `run_init_wizard()`, causing `config.orchestrator.enabled` to always default to `false` in interactive mode
- **Wizard missing `OrchestratorConfig`**: `run_init_wizard()` did not accept or propagate orchestrator setting to `TACConfig`

### Added
- **`tac-bootstrap upgrade --with-orchestrator`**: New flag to add orchestrator to existing projects during upgrade
  - Enables `config.orchestrator.enabled = true` before re-scaffolding
  - Shows orchestrator changes in `--dry-run` preview
  - Allows upgrade even when versions match (treats flag as a reason to upgrade)

### Changed
- `wizard.py` - Added `with_orchestrator` parameter and `OrchestratorConfig` import
- `cli.py` - Pass `with_orchestrator` to wizard in interactive mode; added flag to `upgrade` command
- `upgrade_service.py` - `perform_upgrade()` and `get_changes_preview()` accept `with_orchestrator` parameter

## [0.9.0] - 2026-02-05

### Added - TAC-14: Codebase Singularity & Orchestrator

**Database Layer (SQLite Zero-Config):**
- SQLite orchestrator database schema with 5 tables: `orchestrator_agents`, `agents`, `prompts`, `agent_logs`, `system_logs`
- Schema with WAL mode, foreign keys, triggers, and 6 performance indexes
- `adw_database.py` - Async CRUD operations with aiosqlite (DatabaseManager)
- `orch_database_models.py` - Pydantic models mapping to schema tables
- `setup_database.sh` - SQLite initialization script with schema verification

**Structured Logging & WebSockets:**
- `adw_logging.py` - Structured database logging for ADW workflows (init, log_step_start/end, log_agent_event, log_system_event)
- `adw_websockets.py` - WebSocket server for real-time event broadcasting to frontend

**Orchestrator Web Backend (FastAPI):**
- `orchestrator_web/main.py` - FastAPI app with lifespan manager, CORS, health endpoints
- `orchestrator_web/dependencies.py` - Dependency injection for DatabaseManager
- `orchestrator_web/routers/agents.py` - CQRS endpoints for orchestrator_agents (GET/POST/PUT/DELETE)
- `orchestrator_web/routers/runtime.py` - Runtime agents, prompts, and logs endpoints
- `orchestrator_web/routers/websocket.py` - WebSocket endpoint for real-time agent status updates
- `.env.sample` - Environment variables template

**Orchestrator Frontend (Vue 3 + TypeScript):**
- `apps/orchestrator_3_stream/frontend/` - Vue 3 SPA with Pinia state management
- Swimlane board visualization for agent status tracking
- Command palette overlay with keyboard shortcuts
- WebSocket client for real-time updates
- Tailwind CSS styling

**Skills System:**
- Meta-skill for creating new agent skills following best practices
- Skills documentation (complete guide, architecture overview, design principles)
- Progressive disclosure pattern (metadata -> instructions -> resources)

**Orchestrator Commands:**
- `/orch_plan_w_scouts_build_review` - Complete workflow: scout, plan, build, review
- `/orch_scout_and_build` - Simplified workflow: scout and direct build
- `/orch_one_shot_agent` - Single specialized agent execution pattern

**Consolidated Workflows (Database-Backed):**
- `adw_plan_build.py` - Plan + Build with database logging
- `adw_plan_build_review.py` - Plan + Build + Review with database logging
- `adw_plan_build_review_fix.py` - Plan + Build + Review + Fix with self-healing

**Test Suites:**
- `adws/adw_tests/` - Pytest tests for database, workflows, agent SDK, websockets
- `apps/orchestrator_3_stream/playwright-tests/` - 6 Playwright E2E tests
- Playwright configuration for frontend testing

**CLI Enhancements:**
- `--with-orchestrator` flag for `init` and `add-agentic` commands
- `OrchestratorConfig` with `enabled`, `websocket_port`, `database_url` fields
- Conditional orchestrator generation in scaffold service

**Build & Operations:**
- Root `Makefile` with orchestrator commands (install, setup-db, dev, start, test, health)
- CLI `Makefile` extended with `orch-*` targets
- Makefile template for generated projects

**Documentation:**
- `ai_docs/doc/Tac-14_complete_guide.md` - Complete architecture guide with Mermaid diagrams
- `ai_docs/doc/Tac-14_skills_guide.md` - Skills system guide with examples
- TAC-14 section in CLI README with 12-component table

### Fixed
- **TAC-13 Validation Error**: Added missing expert system slash commands to `SlashCommand` Literal type in `data_types.py`
- **Model fallback chain**: Changed haiku->None to haiku->haiku for retry loop continuation
- **worktree_path bug**: Fixed None passed as working_dir in adw_plan_iso.py
- **Missing pyyaml**: Added dependency to adw_test_iso.py and adw_ship_iso.py

### Changed
- Version bump from 0.8.0 to 0.9.0
- scaffold_service.py extended with conditional orchestrator generation
- All TAC-14 components include both BASE files and Jinja2 templates

## [0.8.0] - 2026-02-03

### Added - TAC-13: Agent Experts

**Core Capabilities:**
- Agent experts with self-improving expertise files (Act → Learn → Reuse loop)
- Self-improving template metaprompts for domain specialization
- Mental model pattern: expertise.yaml files that validate against codebase
- Question prompts: Answer domain questions by reading expertise + validating against code
- Self-improve prompts: 7-phase workflow (check diff → validate → update → enforce limits)

**Agent Experts Included:**
- CLI Expert: tac-bootstrap CLI, templates, scaffold service
- ADW Expert: AI Developer Workflows, state management, GitHub integration
- Commands Expert: Slash command structure, variables, workflows

**Meta-Agentics:**
- `/meta-prompt`: Generate new slash commands from descriptions
- `/meta-agent`: Generate new agent definitions from descriptions
- Meta-skill pattern documentation (progressive disclosure)

**Orchestration:**
- `/expert-orchestrate`: Plan → Build → Improve workflow for agent experts
- `/expert-parallel`: Scale experts in parallel (3-10 instances) for high-confidence results

**Documentation:**
- Comprehensive TAC-13 guide in ai_docs/doc/
- Expertise file structure documentation
- Meta-skill pattern guide
- Auto-detection keywords for TAC-13 docs

**Templates:**
- CLI expert templates (question, self-improve, expertise seed)
- Meta-prompt template
- Meta-agent template
- Expert orchestration templates

### Changed
- Updated README with Agent Experts section and usage examples
- Enhanced AI docs auto-detection with TAC-13 keywords
- Extended scaffold service to include expert templates and expertise files

## [0.7.1] - 2026-02-03

### Added

#### Token Optimization (TAC-9)
- **Automatic Documentation Summarization**: New `summarize_doc_content()` function using haiku model
  - Reduces documentation token consumption by 70-80% while preserving essential information
  - Targets 300 tokens per summary (configurable per phase)
  - Automatic fallback to original content if summarization fails
  - Logs reduction percentages for monitoring
- **Phase-Aware Documentation Limits**:
  - Planning phase: Max 3 documents with 300 token summaries
  - Build phase: Reuses summarized context from planning (no reload)
  - Estimated 85% token reduction in planning, 58% overall workflow savings
- **Documentation Keywords**: Added detection support for:
  - `ddd_lite`: Domain-Driven Design lightweight patterns
  - `solid`: SOLID principles
  - `fractal_docs`: Fractal documentation structure

#### Agent Configuration
- Added `doc_summarizer` to read-only agents (eliminates working_dir warnings)

### Changed

#### State Management (TAC-9)
- **Enhanced ADWState Persistence**: Added `ai_docs_context` and `loaded_docs_topic` fields
  - Documentation now persists across workflow phases (plan → build → test → review)
  - Prevents redundant documentation reloading in build/implementation phases
  - Updated in `update()`, `save()`, and `to_stdout()` methods
- **ADWStateData Model**: Extended with optional documentation context fields
  - `ai_docs_context: Optional[str]` - Summarized documentation content
  - `loaded_docs_topic: Optional[str]` - Comma-separated list of loaded topics

#### Documentation Loading (TAC-9)
- **Path Correction**: `/load_ai_docs` command now searches in `ai_docs/` instead of `ai_docs/doc/`
  - Aligns with `detect_relevant_docs()` which already scanned full directory
  - Enables loading of root-level documentation files (ddd_lite.md, solid.md, design_patterns.md, etc.)
  - Updated all examples and documentation to reflect correct path
- **Detection-Loading Alignment**: Fixed inconsistency where docs were detected but not loaded
  - Detection searched `ai_docs/` (os.walk)
  - Loading only searched `ai_docs/doc/`
  - Now both search full `ai_docs/` directory tree

### Fixed

- **State Persistence Bug**: Documentation context was being discarded after planning phase
  - Root cause: `ai_docs_context` not in `core_fields` whitelist
  - Impact: Build phase reloaded full documentation (6.6x more tokens than planner)
  - Resolution: Added fields to state management in 5 locations
- **Documentation Path Mismatch**: Auto-detected docs failed to load due to path inconsistency
  - Files like `ddd_lite.md` detected but not found during loading
  - Marked as "failed to load" despite existing in `ai_docs/`
- **Working Directory Warnings**: Eliminated spurious warnings for read-only agents
  - `doc_summarizer` now recognized as read-only (no file creation)

### Performance

#### Token Usage Improvements
- **Before Optimization** (Issue #574):
  - Planning: 325k tokens
  - Build: 2.1M tokens (docs reloaded without summaries)
  - Total: 2.49M tokens, $1.53
- **After Optimization** (Estimated):
  - Planning: 325k tokens (3 docs × 300 tokens = 900 tokens for docs)
  - Build: ~800k tokens (reuses summarized docs from state)
  - Total: ~1.1M tokens, $0.65 (58% cost reduction)

#### Token Reduction Breakdown
- **Documentation Summarization**: 40% average reduction observed
  - TAC-13_dual_strategy_summary: 2130 → 1331 chars (37.5%)
  - TAC-13_implementation_status: 2620 → 1423 chars (45.7%)
  - Tac-1: 1576 → 1023 chars (35.1%)
- **Phase Limiting**: 7 docs → 3 docs in planning (57% reduction)
- **State Reuse**: Eliminates redundant documentation loading in subsequent phases

### Technical

#### Files Modified
**Core Implementation:**
- `adws/adw_modules/workflow_ops.py` - Added summarization function and updated keywords
- `adws/adw_modules/state.py` - Extended with documentation context fields (3 methods)
- `adws/adw_modules/data_types.py` - Updated ADWStateData model
- `adws/adw_modules/agent.py` - Added doc_summarizer to read_only_agents
- `adws/adw_plan_iso.py` - Integrated summarization in planning workflow
- `.claude/commands/load_ai_docs.md` - Corrected documentation path

**Templates (for generated projects):**
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/state.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`

## [0.7.0] - 2026-02-02

### Added

#### New Commands (TAC-12 Wave 1)
- `/all_tools` - List all available built-in tools for the current session
- `/build` - Sequential plan implementation with step-by-step file writing
- `/build_in_parallel` - Parallel plan implementation delegating file creation to build-agents for cost optimization
- `/find_and_summarize` - Advanced codebase search with AI-powered summarization of results
- `/load_ai_docs` - Load and process AI documentation with specialized sub-agents
- `/load_bundle` - Recover previous agent context from saved context bundles
- `/parallel_subagents` - TAC-10 Level 4 delegation pattern for launching parallel specialized agents
- `/plan` - Create implementation plans with simple file exploration workflow
- `/plan_w_docs` - Enhanced planning with documentation exploration using scout agents
- `/plan_w_scouters` - Enhanced planning with parallel scout-based codebase exploration (3 base + 5 fast agents)
- `/prime_3` - Deep context loading with comprehensive codebase understanding
- `/prime_cc` - Claude Code-specific context priming with perplexity optimization
- `/scout_plan_build` - End-to-end workflow orchestrating scout, plan, and build phases

#### New Agents (TAC-12 Wave 2)
- `build-agent` - Specialist for implementing one specific file based on detailed instructions and context
- `playwright-validator` - E2E validation and browser automation specialist for Playwright tests
- `scout-report-suggest` - Read-only analysis and reporting for codebase issues with resolution suggestions
- `scout-report-suggest-fast` - Fast variant of scout-report-suggest optimized for speed using haiku model
- `docs-scraper` - Documentation fetching and processing for AI knowledge integration
- `meta-agent` - Generates new agent definition files (.md) and Jinja2 templates from specifications

#### New Hooks (TAC-12 Wave 3)
- `send_event` - Emit structured events for observability and analytics (usage, errors, performance)
- `session_start` - Execute at session initialization with environment and context setup
- `pre_tool_use` - Pre-execution validation and monitoring for any tool invocation
- `post_tool_use` - Post-execution analysis and result processing for tools
- `notification` - Send alerts and notifications based on events and conditions
- `stop` - Graceful shutdown and cleanup handler
- `subagent_stop` - Handle subagent termination and result collection
- `pre_compact` - Pre-compaction logging for context analysis and optimization
- `user_prompt_submit` - Handle user input submissions and prompt processing

#### Hook Utilities (TAC-12 Wave 4)
- `summarizer.py` - Text summarization utility for reducing token usage
- `model_extractor.py` - LLM model information extraction and validation
- `constants.py` - Shared constants and configuration values
- `llm/` subdirectory - LLM provider utilities (Anthropic, OpenAI, Ollama)
- `tts/` subdirectory - Text-to-speech provider utilities (ElevenLabs, OpenAI, pyttsx3)

#### Observability Infrastructure
- Event emission system via `send_event` hook for tracking usage patterns, errors, and performance metrics
- Pre/post tool use hooks for detailed operation monitoring and result analysis
- Session lifecycle management with `session_start`, `stop`, and `subagent_stop` hooks
- Pre-compaction logging via `pre_compact` hook for context analysis and optimization
- Structured event logging for analytics and system health monitoring

#### Status Line Feature
- Dynamic status line configuration via `status_line_main.py` in `.claude/status_lines/`
- Real-time status display during agent execution
- Customizable status line templates for different contexts

### Changed

#### background.md Improvements
- Enhanced with TAC-12 model selection via `$MODEL` variable
- Structured reporting format with automatic progress tracking
- Auto-rename on completion/failure (`.complete.md` / `.failed.md` suffixes)
- Uses claude CLI directly with `--dangerously-skip-permissions` for streamlined execution
- Support for background task queuing and status monitoring

#### quick-plan.md Improvements
- Integrated 8 parallel scout subagents (3 base + 5 fast variants) for comprehensive exploration
- Task type classification support (chore|feature|refactor|fix|enhancement)
- Complexity level detection (simple|medium|complex)
- Conditional plan formats based on task characteristics
- Automatic plan format selection for different task types

### Technical Details

#### Multi-Agent Orchestration Patterns
- **Parallel Scout Exploration (Level 4 Delegation)**: Launch 2-10 parallel Explore agents with different search strategies (file patterns, content search, architecture analysis, dependency mapping, tests, configs, types, docs) to identify relevant files. Results aggregated with frequency scoring and saved to `agents/scout_files/` directory.
- **Build Agent Delegation**: Delegate file creation tasks to specialized build-agents for reduced context usage and cost optimization
- **Haiku-based Cost Optimization**: Use Haiku model agents for parallel subagent work to reduce token costs while maintaining quality
- **Conditional Agent Selection**: Route tasks to specialized agents based on task type and complexity

#### Hook-Based Observability Architecture
- **Event Emission**: `send_event` hook emits structured events (usage, errors, performance) to observability systems
- **Tool Lifecycle Tracking**: `pre_tool_use` and `post_tool_use` hooks provide comprehensive tool execution monitoring
- **Session Management**: `session_start`, `stop`, and `subagent_stop` hooks handle session lifecycle and agent termination
- **Pre-Compaction Analysis**: `pre_compact` hook logs context state before compaction for optimization analysis
- **User Input Processing**: `user_prompt_submit` hook processes and enriches user submissions before agent execution

#### Jinja2 Template Integration
- All new features include Jinja2 templates for seamless integration in generated projects
- Templates support dynamic configuration via `config` variable
- Agent definitions are template files (.md) for easy customization

#### TAC-10 Level Patterns
- Level 1: Single agent execution
- Level 2: Sequential delegation
- Level 3: Error handling and retry
- Level 4: Parallel delegation with aggregation (scout exploration)
- Level 5: Conditional routing
- Level 6: Metaprompt generation
- Level 7: Self-improvement loops

## [0.6.1] - 2026-01-27

### Added

- Trigger: `adws/adw_triggers/trigger_plan_parallel.py` - Execute tasks from plan markdown files in parallel
- Parses `#### Task N` format with support for task groups (P1, P2, etc.) and task types (FEATURE, CHORE, BUG)
- Options: `--group`, `--tasks`, `--max-concurrent`, `--workflow`, `--dry-run`, `--verbose`
- Template: `trigger_plan_parallel.py.j2`

#### Documentation Scripts with Dual Provider Support
- `scripts/gen_docs_fractal.py` - Now supports `--provider claude` (default) and `--provider api`
- `scripts/gen_docstring_jsdocs.py` - Same dual provider support
- Claude provider uses CLI directly (no API key needed)
- Options: `--claude-model` (sonnet, opus, haiku), `--claude-path`

#### E2E Test Commands
- New command templates in `.claude/commands/e2e/` (7 test examples)

#### Base Commands
- Added `build.md` and `lint.md` to base `.claude/commands/`

### Changed
- Documentation scripts default to Claude Code CLI provider (no API key required)
- Removed `openai` dependency when using Claude provider
- Updated README with new trigger and scripts documentation

## [0.6.0] - 2026-01-27

### Added

#### Security Features (TAC-11)
- Security hook: `dangerous_command_blocker.py` - Pre-execution validation for Bash commands that blocks destructive operations (rm -rf, dd to devices, mkfs, chmod -R 777, etc.) with safer alternative suggestions and audit trail logging
- Directory: `agents/security_logs/` - Audit trail for blocked dangerous commands (JSON lines format)
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2` - Hook template for generated projects

#### New Commands (TAC-11)
- `/scout` command - Multi-model parallel codebase exploration using TAC-10 Level 4 delegation pattern. Launches 2-10 parallel Explore agents with different search strategies (file patterns, content search, architecture analysis, dependency mapping, tests, configs, types, docs) to identify relevant files for a task. Produces frequency-scored aggregated reports saved to `agents/scout_files/`
- `/question` command - Read-only Q&A mode for answering questions about project structure, architecture, and documentation using git ls-files exploration and Read tool
- Directory: `agents/scout_files/` - Storage for scout exploration reports with timestamps
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2` - Scout command template for generated projects
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` - Question command template for generated projects
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2` - Scout files directory template

#### Parallel Workflow Execution (TAC-11)
- Trigger: `adws/adw_triggers/trigger_issue_parallel.py` - Parallel ADW trigger that processes multiple GitHub issues simultaneously using ThreadPoolExecutor. Unlike sequential `trigger_issue_chain.py`, this trigger launches workflows concurrently for all open assigned issues, with configurable max concurrent workers (default: 5) and polling interval (default: 20s). Includes graceful shutdown, thread-safe tracking, and `--once` flag for single-cycle testing
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_parallel.py.j2` - Parallel trigger template for generated projects

### Changed
- settings.json now includes dangerous_command_blocker.py in hooks configuration with blockIfNonzeroExit behavior
- Scaffold service creates `agents/security_logs/` and `agents/scout_files/` directories with .gitkeep files
- Extended ADW trigger capabilities from sequential-only to concurrent parallel processing

### Technical Details
All TAC-11 features follow established patterns:
- Security hook uses pre-execution blocking (exit code 2) with comprehensive pattern matching
- Scout command implements TAC-10 Level 4 delegation with Haiku agents for cost efficiency
- Parallel trigger uses thread-safe tracking with locks for concurrent workflow management
- All features include Jinja2 templates for seamless integration in generated projects

## [0.5.1] - 2026-01-26

### Added
- Nuevo template `parallel_subagents.md.j2` para delegación multi-agente (TAC-10 Level 4)
- Nuevo template `t_metaprompt_workflow.md.j2` para generación de prompts (TAC-10 Level 6)
- Nuevo template `cc_hook_expert_improve.md.j2` para self-improvement (TAC-10 Level 7)
- Nuevo template `build_w_report.md.j2` con reporte YAML estructurado
- Hooks adicionales: UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd
- Integración de universal_hook_logger en todos los hooks
- Directorios `agents/hook_logs/` y `agents/context_bundles/` en scaffold

### Changed
- settings.json.j2 actualizado con configuración completa de hooks
- scaffold_service.py ahora crea estructura de directorios agents/

## [0.5.0] - 2026-01-25

### Added
- Output style presets for token control (concise-done, concise-ultra, concise-tts, verbose-bullet-points, verbose-yaml-structured)
- LLM utility wrappers for Anthropic, OpenAI, and Ollama
- TTS utility wrappers for ElevenLabs, OpenAI, and pyttsx3
- Context bundle builder hook for session tracking and recovery
- Universal hook logger for comprehensive event logging
- `/background` command for out-loop agent delegation
- `/load_bundle` command for context recovery
- `/load_ai_docs` command for documentation loading via sub-agents
- `/prime_cc` command for Claude Code-specific context priming
- `/quick-plan` command for rapid implementation planning
- Agent definitions: docs-scraper, meta-agent, research-docs-fetcher
- Expert agent pattern: cc_hook_expert (plan/build/improve)
- Local settings override template for output style configuration

### Changed
- Extended `.claude/` directory structure with new subdirectories (output-styles, agents, hooks/utils/llm, hooks/utils/tts, commands/experts)

## [0.4.0] - 2026-01-25

### Added
- `--once` flag in `adws/adw_triggers/trigger_cron.py` for single execution cycle
- `--once` flag in `adws/adw_triggers/trigger_issue_chain.py` for single execution cycle
- Documentation for `trigger_issue_chain.py` in `adws/README.md`
- Trigger polling configuration section in `adws/README.md`
- Complete docstring in `adws/adw_triggers/__init__.py` with all available triggers

### Fixed
- `config.yml` structure aligned with `TACConfig` schema
- Moved `allowed_paths` and `forbidden_paths` into `agentic.safety` section
- Restructured `workflows` configuration under `agentic.workflows`
- Added missing `claude` configuration section

### Changed
- N/A

## [0.4.1] - 2026-01-25

### Added
- User assignment validation in all ADW triggers (cron, webhook, issue_chain)
- Functions `get_current_gh_user()`, `is_issue_assigned_to_me()`, `assign_issue_to_me()` in `github.py`
- Template `trigger_webhook.py.j2` for webhook trigger generation
- Polling interval documentation in README

### Changed
- Triggers now only process issues assigned to the authenticated GitHub user
- Triggers display current user at startup for visibility
- Synchronized `trigger_cron.py.j2` template with root (user validation)
- Synchronized `trigger_issue_chain.py.j2` template with root (user validation)
- Synchronized `github.py.j2` template with root (user validation functions)

## [0.3.0] - 2026-01-25

### Added

#### Entity Generation (Fase 2)
- New command `tac-bootstrap generate entity <name>` for CRUD entity generation
- Interactive wizard for defining entity fields
- Support for field types: str, int, float, bool, datetime, uuid, text, decimal, json
- `--authorized` flag for row-level security templates
- `--async` flag for async repository generation
- `--with-events` flag for domain events
- Vertical slice architecture: domain, application, infrastructure, api layers

#### Shared Base Classes (Fase 1)
- `base_entity.py` - Entity base with audit trail, soft delete, state management, optimistic locking
- `base_schema.py` - BaseCreate, BaseUpdate, BaseResponse DTOs
- `base_service.py` - Generic typed CRUD service with soft delete
- `base_repository.py` - Generic SQLAlchemy sync repository
- `base_repository_async.py` - Generic async repository with bulk operations
- `database.py` - SQLAlchemy session management (sync/async)
- `exceptions.py` - Typed exceptions with FastAPI HTTP handlers
- `responses.py` - PaginatedResponse, SuccessResponse, ErrorResponse
- `dependencies.py` - FastAPI dependency injection factories
- `health.py` - Health check endpoint with DB connectivity check
- Auto-included when `--architecture ddd|clean|hexagonal` and `--framework fastapi`

#### Fractal Documentation (Fase 6)
- `scripts/gen_docstring_jsdocs.py` - Automatic IDK-first docstring generation
- `scripts/gen_docs_fractal.py` - Fractal documentation tree generator
- `scripts/run_generators.sh` - Orchestrator script
- Slash command `/generate_fractal_docs` for Claude Code integration
- `canonical_idk.yml` - Domain-specific keyword vocabulary
- Bottom-up documentation: one markdown per folder in `docs/`
- Support for Python and TypeScript

#### Document Workflow Improvements (Fase 7)
- IDK frontmatter in generated feature documentation
- Fractal docs integration in `adw_document_iso.py`
- Automatic conditional_docs.md updates for new documentation

#### Multi-layer Validation (Fase 4)
- ValidationService with 5 validation layers
- Framework/language compatibility rules
- Template existence verification
- Filesystem permission and conflict checks
- Git state warnings
- All errors reported at once with fix suggestions

#### Audit Trail (Fase 3)
- `bootstrap` section in config.yml with generation metadata
- Tracks: generated_at, generated_by, last_upgrade, schema_version
- Automatic timestamp recording on init and upgrade

#### Code Quality (Fase 5)
- Value Objects: ProjectName, TemplatePath, SemanticVersion
- IDK-first docstrings on all application and infrastructure modules

#### Documentation and Release (Fase 8)
- Comprehensive README with entity generation guides and workflow documentation
- CHANGELOG.md following Keep a Changelog format
- Entity generation command usage examples
- Fractal documentation workflow guide
- Complete feature documentation

### Changed
- `conditional_docs.md` template includes fractal documentation rules
- `document.md` template generates docs with IDK frontmatter
- `adw_document_iso.py` template includes fractal docs step (non-blocking)
- `config.yml` template includes bootstrap metadata section
- Scaffold service includes shared base classes for DDD projects
- Scaffold service includes fractal documentation scripts

### Fixed
- (none in this release)

## [0.2.2] - 2026-01-22

### Fixed
- `tac-bootstrap upgrade` now works with projects using legacy `tac_version` field
- Config field normalized from `tac_version` to `version` for consistency

### Changed
- Template `config.yml.j2` now generates `version` instead of `tac_version`
- Upgrade service normalizes legacy field names automatically

## [0.2.1] - 2026-01-22

### Added
- `resolve_clarifications()` function for auto-resolving ambiguity questions
- ADW workflows now auto-resolve clarifications instead of pausing

### Changed
- Workflows continue automatically with AI-generated decisions
- Clarification responses posted to GitHub issues for transparency

### Removed
- Port management from ADW workflows (not applicable to all app types)
- `--clarify-continue` flag (replaced by auto-resolution)
- `backend_port` and `frontend_port` from state management

### Technical
- Updated `workflow_ops.py` and `workflow_ops.py.j2`
- Updated `adw_plan_iso.py` and `adw_plan_iso.py.j2`
- Removed port functions from `worktree_ops.py`
- Cleaned up `data_types.py` and `state.py`

## [0.2.0] - 2026-01-22

### Added
- `tac-bootstrap upgrade` command for updating existing projects
- Version tracking in `config.yml`
- `target_branch` configuration in `config.yml`
- `--version` flag for CLI

### Changed
- All ADW templates synchronized with latest modules
- Improved worktree port management
- Enhanced agent retry logic with rate limiting

### Fixed
- Jinja2 template escaping for JSON examples
- Template synchronization issues

### Upgrade Notes
Projects created with v0.1.0 can upgrade using:
```bash
tac-bootstrap upgrade
```

This will update adws/, .claude/, and scripts/ while preserving your code.

## [0.1.0] - 2026-01-20

### Added
- Initial TAC Bootstrap CLI
- Project scaffolding for Python and TypeScript
- ADW workflow templates
- Claude Code integration
