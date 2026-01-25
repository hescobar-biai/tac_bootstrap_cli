# Changelog

All notable changes to TAC Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
