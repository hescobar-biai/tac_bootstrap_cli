# ScaffoldService build_plan() Implementation

**ADW ID:** c9d3ab60
**Date:** 2026-01-20
**Specification:** specs/issue-28-adw-c9d3ab60-sdlc_planner-implement-scaffold-service-build-plan.md

## Overview

Implemented the central `ScaffoldService` in the application layer that builds comprehensive scaffolding plans from user configuration and applies them to generate complete Agentic Layer structures. This service orchestrates the creation of ~50+ files and ~16 directories, handling idempotency, template rendering, and different file actions based on whether scaffolding into new or existing repositories.

## What Was Built

- **ApplyResult Dataclass**: Result tracking for scaffold plan application with statistics (directories created, files created/skipped/overwritten) and error handling
- **ScaffoldService Class**: Core service with dependency injection for TemplateRepository
- **build_plan() Method**: Orchestrates plan construction by delegating to specialized methods for different file categories
- **_add_directories()**: Adds 16 core directories using dynamic paths from TACConfig
- **_add_claude_files()**: Adds .claude/ configuration (settings.json, 18 slash commands, 3 hooks, 2 hook utils)
- **_add_adw_files()**: Adds ADW workflows (README, 5 modules, 2 workflows, 2 triggers)
- **_add_script_files()**: Adds utility scripts (start.sh, test.sh, lint.sh, build.sh)
- **_add_config_files()**: Adds configuration files (config.yml, .mcp.json, .gitignore) with smart action selection
- **_add_structure_files()**: Adds README documentation for directory structure
- **apply_plan() Method**: Executes scaffold plan to create physical directory/file structure with resilient error handling
- **CLI Integration**: Updated cli.py to use new ScaffoldPlan API (directories/files lists instead of operations)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: New service module with complete scaffolding logic (395 lines)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Updated to use new ScaffoldPlan API in init, add_agentic, and render commands
- `specs/issue-28-adw-c9d3ab60-sdlc_planner-implement-scaffold-service-build-plan.md`: Feature specification document
- `.mcp.json`: Minor config update
- `playwright-mcp-config.json`: Minor config update

### Key Changes

**1. ScaffoldService Architecture**
- Follows DDD clean architecture: application layer service orchestrates domain models (ScaffoldPlan) and infrastructure (TemplateRepository, FileSystem)
- Dependency injection pattern with optional TemplateRepository constructor parameter
- Separation of concerns: build_plan() (in-memory plan construction) vs apply_plan() (filesystem execution)

**2. build_plan() Logic**
- Accepts TACConfig and existing_repo boolean flag
- Delegates to 6 specialized private methods for different file categories
- Each category determines FileAction based on existing_repo flag (CREATE for new, SKIP for existing)
- Special handling: config.yml always OVERWRITE, .gitignore PATCH in existing repos

**3. File Organization Strategy**
- **18 slash commands**: prime, start, build, test, lint, feature, bug, chore, patch, implement, commit, pull_request, review, document, health_check, prepare_app, install, track_agentic_kpis
- **3 executable hooks**: pre_tool_use.py, post_tool_use.py, stop.py
- **5 ADW modules**: __init__.py, agent.py, state.py, git_ops.py, workflow_ops.py
- **2 executable workflows**: adw_sdlc_iso.py, adw_patch_iso.py
- **4 executable scripts**: start.sh, test.sh, lint.sh, build.sh

**4. apply_plan() Execution**
- Lazy import of FileSystem (implemented in TAREA 5.2)
- Two-phase execution: directories first, then files
- Resilient error handling: try/catch per operation, collect errors without aborting
- Force flag support: overrides CREATE actions when files exist
- Template rendering with {"config": config} context
- Executable permission handling for scripts/hooks/workflows

**5. CLI Integration Updates**
- Changed from plan.operations iteration to plan.directories and plan.files separate lists
- Updated result field names: dirs_created → directories_created, files_modified → files_overwritten
- Enhanced dry-run preview to show directory operations explicitly

## How to Use

### Building a Scaffold Plan

```python
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

# Create service
service = ScaffoldService()

# Build config
config = TACConfig(
    project=ProjectSpec(
        name='my-project',
        language=Language.PYTHON,
        package_manager=PackageManager.UV
    ),
    commands=CommandsSpec(
        start='uv run python -m app',
        test='uv run pytest'
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name='my-project')
    )
)

# Build plan for new project
plan = service.build_plan(config, existing_repo=False)

# Build plan for existing project (different file actions)
plan_existing = service.build_plan(config, existing_repo=True)

# Preview plan
print(plan.summary)
print(f'Directories: {plan.total_directories}')
print(f'Files: {plan.total_files}')
```

### Applying a Scaffold Plan

```python
from pathlib import Path

# Apply plan to create actual files
result = service.apply_plan(
    plan=plan,
    output_dir=Path('/path/to/target'),
    config=config,
    force=False  # Set True to overwrite existing files
)

# Check results
if result.success:
    print(f'✓ Created {result.directories_created} directories')
    print(f'✓ Created {result.files_created} files')
    print(f'⊘ Skipped {result.files_skipped} files')
else:
    print(f'✗ {result.error}')
    for error in result.errors:
        print(f'  - {error}')
```

### Via CLI

```bash
# Initialize new project (uses build_plan with existing_repo=False)
cd tac_bootstrap_cli && uv run tac-bootstrap init my-project --dry-run

# Add Agentic Layer to existing project (uses build_plan with existing_repo=True)
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic --dry-run

# Render from config (uses build_plan based on existing structure)
cd tac_bootstrap_cli && uv run tac-bootstrap render config.yml --dry-run
```

## Configuration

### File Actions by Scenario

**New Repository (existing_repo=False):**
- .claude/ files → CREATE
- adws/ files → CREATE
- scripts/ → CREATE
- config.yml → CREATE
- .mcp.json → CREATE
- .gitignore → CREATE

**Existing Repository (existing_repo=True):**
- .claude/ files → SKIP (don't overwrite user's Claude configuration)
- adws/ files → SKIP (preserve custom workflows)
- scripts/ → SKIP (preserve custom scripts)
- config.yml → OVERWRITE (always capture latest user settings)
- .mcp.json → SKIP (preserve MCP configuration)
- .gitignore → PATCH (append TAC patterns to existing)

### Dynamic Paths from TACConfig

All paths are configurable via TACConfig.paths:
- `adws_dir`: Default "adws"
- `specs_dir`: Default "specs"
- `logs_dir`: Default "logs"
- `scripts_dir`: Default "scripts"
- `prompts_dir`: Default "prompts"
- `worktrees_dir`: Default "trees"

## Testing

### Manual Validation

```bash
cd tac_bootstrap_cli

# Verify module imports
uv run python -c "from tac_bootstrap.application.scaffold_service import ScaffoldService, ApplyResult; print('✓ Module imports successfully')"

# Test build_plan() generates correct plan
uv run python -c "
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

service = ScaffoldService()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

plan = service.build_plan(config)
print(f'Total Directories: {plan.total_directories}')
print(f'Total Files: {plan.total_files}')
assert plan.total_directories >= 16
assert plan.total_files >= 50
print('✓ Plan generation successful')
"

# Test existing_repo flag changes file actions
uv run python -c "
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

service = ScaffoldService()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

plan = service.build_plan(config, existing_repo=True)
config_yml_op = next(f for f in plan.files if f.path == 'config.yml')
assert config_yml_op.action.value == 'overwrite'
gitignore_op = next(f for f in plan.files if f.path == '.gitignore')
assert gitignore_op.action.value == 'patch'
print('✓ Existing repo plan generation successful')
"
```

### Type Checking & Linting

```bash
cd tac_bootstrap_cli

# Type checking
uv run mypy tac_bootstrap/application/scaffold_service.py

# Linting
uv run ruff check tac_bootstrap/application/scaffold_service.py

# Format check
uv run ruff format --check tac_bootstrap/application/scaffold_service.py
```

## Notes

### Implementation Context
- This is TAREA 5.1 from PLAN_TAC_BOOTSTRAP.md (FASE 5: Servicios de Scaffolding)
- Follows DDD architecture: application layer orchestrates domain models and infrastructure services
- Code provided in specification was implemented exactly as specified
- Templates exist in tac_bootstrap/templates/ directory (created in FASE 3)

### Design Decisions
1. **Separation of build vs apply**: build_plan() is fast in-memory operation, apply_plan() is I/O-bound filesystem execution
2. **Idempotency handling**: Different file actions (CREATE, SKIP, OVERWRITE, PATCH) based on existing_repo context
3. **Resilient execution**: Errors during apply_plan() don't abort entire process, collected for review
4. **Lazy FileSystem import**: apply_plan() imports FileSystem at runtime to avoid circular dependencies
5. **Template-first approach**: All file content generated via Jinja2 templates for consistency
6. **Executable flags**: Scripts, hooks, and workflows automatically marked executable

### Limitations
- apply_plan() depends on FileSystem service (implemented in TAREA 5.2)
- Template errors during rendering are caught in apply_plan() try/catch
- No rollback mechanism if apply_plan() partially fails (resilient but not transactional)
- File actions are determined at build_plan() time, not re-evaluated during apply_plan()

### Next Steps
- **TAREA 5.2**: Implement FileSystem service (fs.py) with ensure_directory(), write_file(), append_file(), make_executable()
- **TAREA 5.3**: Implement DetectService for auto-detection of existing project characteristics
- **TAREA 6.1**: Full CLI integration with init/add-agentic commands using ScaffoldService

### Dependencies
Already installed in pyproject.toml:
- jinja2: Template rendering via TemplateRepository
- pydantic: TACConfig validation
- pathlib: Path handling

### Performance Characteristics
- build_plan() is O(1) with ~50 file operations - very fast in-memory construction
- apply_plan() is I/O bound - scales linearly with number of files
- Template rendering is lazy (only during apply_plan() execution)
- Preview capability allows dry-run without filesystem writes
