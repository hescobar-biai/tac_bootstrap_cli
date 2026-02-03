# Changelog

All notable changes to TAC Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
