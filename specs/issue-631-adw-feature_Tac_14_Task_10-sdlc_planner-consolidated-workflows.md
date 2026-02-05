# Feature: Implementar Consolidated Workflows (BASE + TEMPLATES)

## Metadata
issue_number: `631`
adw_id: `feature_Tac_14_Task_10`
issue_json: `{"number": 631, "title": "Implementar Consolidated Workflows (BASE + TEMPLATES)", "body": "file: ddd_lite.md\nfile: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md\n\n**Descripción**:\nCrear 3 workflows database-backed con Agent SDK en BASE y templates.\n\n**Pasos técnicos**:\n\n**BASE**:\n1. Crear directorio `adws/adw_workflows/`\n2. Copiar `adw_plan_build.py` desde `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_workflows/`\n3. Copiar `adw_plan_build_review.py`\n4. Copiar `adw_plan_build_review_fix.py`\n5. Adaptar imports\n6. Implementar CLI arg parsing (--adw-id)\n7. Integrar con adw_database.py\n8. Integrar con adw_agent_sdk.py\n9. Integrar con adw_logging.py\n10. Agregar PEP 723 dependencies\n\n**TEMPLATES**:\n11. Copiar 3 workflows a templates .j2\n12. Registrar en scaffold_service.py\n\n**Criterios de aceptación**:\n- 3 workflows creados en BASE\n- Database integration funcional\n- Agent SDK control implementado\n- Templates creados\n\n**Rutas impactadas**:\n\n**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):\n```\nadws/adw_workflows/                               [CREAR]\nadws/adw_workflows/adw_plan_build.py              [CREAR]\nadws/adw_workflows/adw_plan_build_review.py       [CREAR]\nadws/adw_workflows/adw_plan_build_review_fix.py   [CREAR]\n```\n\n**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):\n```\nadws/adw_workflows/adw_plan_build.py.j2              [CREAR]\nadws/adw_workflows/adw_plan_build_review.py.j2       [CREAR]\nadws/adw_workflows/adw_plan_build_review_fix.py.j2   [CREAR]\n```\n\n**CLI**:\n```\napplication/scaffold_service.py  [MODIFICAR]\n```\n\n**Metadata**:\n- Categoría: Workflows\n- Prioridad: Alta\n- Estimación: 4h\n- Dependencias: Tarea 5, Tarea 8, Tarea 9\n\n**Keywords**: consolidated-workflows, database-backed, agent-sdk-control, orchestration\n\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_10`"}`

## Feature Description

Create three progressive database-backed orchestration workflows that use the Agent SDK to coordinate Plan, Build, Review, and Fix agents with SQLite persistence. These workflows represent a consolidated approach to multi-agent orchestration with full execution tracking and state management.

The workflows follow a progressive enhancement pattern:
1. **adw_plan_build.py**: Basic Plan → Build orchestration
2. **adw_plan_build_review.py**: Adds Review agent after Build
3. **adw_plan_build_review_fix.py**: Adds iterative Fix loop for test failures

All workflows integrate with the existing SQLite database infrastructure (Tasks 6-9) for execution logging, share the same ADW module patterns, and are exposed as Jinja2 templates for project generation.

## User Story

As a TAC Bootstrap user
I want to use consolidated multi-agent workflows that persist their execution state to a database
So that I can orchestrate complex development tasks with full visibility, resume capability, and historical tracking

## Problem Statement

The current ADW system (adw_sdlc_iso.py, adw_patch_iso.py) chains separate isolated workflows via JSON state files. While functional, this approach lacks:
- **Execution visibility**: No central database tracking of agent activity
- **Resume capability**: Cannot resume failed workflows from checkpoints
- **Historical analysis**: No queryable log of past executions
- **Cost tracking**: Limited ability to track token usage and costs across workflows
- **Real-time monitoring**: No infrastructure for web UI or external tools to monitor progress

TAC-14 Task 10 addresses this by creating consolidated workflows that integrate Agent SDK control with SQLite persistence, enabling the Orchestrator Web App (Task 12) to provide real-time monitoring and historical analysis.

## Solution Statement

Implement three database-backed workflows in `adws/adw_workflows/` that:

1. **Use argparse** for CLI with required `--adw-id` flag for database tracking
2. **Integrate DatabaseManager** (from adw_database.py) via async context managers
3. **Use Agent SDK wrappers** to invoke Plan, Build, Review, and Fix agents programmatically
4. **Log all milestones** to SQLite via async logging methods
5. **Follow existing ADW patterns**: PEP 723 dependencies, standalone+importable structure
6. **Generate Jinja2 templates** exposing config variables for project-specific customization
7. **Register in scaffold_service.py** to make workflows available in generated projects

The workflows will attempt to read source files from `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_workflows/` but fall back to creating implementations based on existing codebase patterns (adw_sdlc_iso.py, adw_patch_iso.py) if unavailable.

## Relevant Files

Files necessary for implementing the feature:

### Existing ADW Workflows (Reference Patterns)
- `adws/adw_sdlc_iso.py` - Multi-phase SDLC workflow with argparse CLI
- `adws/adw_patch_iso.py` - Simple patch workflow with state management
- Both demonstrate: PEP 723 headers, argparse patterns, state handling, agent invocation

### Database Infrastructure (Dependencies)
- `adws/adw_modules/adw_database.py` - SQLite DatabaseManager with async CRUD
- `adws/adw_modules/orch_database_models.py` - Pydantic models for database tables
- `adws/schema/schema_orchestrator.sql` - SQLite schema with 5 tables + 6 indexes
- These provide: connection management, CRUD operations, schema initialization

### Agent SDK Integration (Dependencies)
- `adws/adw_modules/adw_agent_sdk.py` - Pydantic models for Agent SDK configuration
- Provides: ModelName enum, AgentConfig models, typed SDK control layer

### Template Registration (Modification Target)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registry
- Will add: `_add_adw_workflow_files()` method to register 3 workflow templates

### New Files
- `adws/adw_workflows/adw_plan_build.py` - Basic Plan+Build workflow
- `adws/adw_workflows/adw_plan_build_review.py` - Plan+Build+Review workflow
- `adws/adw_workflows/adw_plan_build_review_fix.py` - Plan+Build+Review+Fix workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/*.j2` - Jinja2 templates for all 3

## Implementation Plan

### Phase 1: Directory Structure & Source Analysis
Create `adws/adw_workflows/` directory and attempt to read source files from tac-14 reference codebase. If unavailable, prepare to synthesize implementations from existing patterns.

### Phase 2: Core Workflow Implementation (BASE)
Create the three workflows with database integration, Agent SDK control, and CLI argument parsing. Follow existing ADW patterns for structure and dependencies.

### Phase 3: Template Generation & Registration
Convert workflows to Jinja2 templates, expose configuration variables, and register in scaffold_service.py for project generation.

## Step by Step Tasks

### Task 1: Create adw_workflows directory and check source files
- Create `adws/adw_workflows/` directory
- Attempt to read source files from `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_workflows/adw_plan_build.py`
- Attempt to read `adw_plan_build_review.py` and `adw_plan_build_review_fix.py`
- Document availability of source files for next task

### Task 2: Implement adw_plan_build.py (BASE)
- Create `adws/adw_workflows/adw_plan_build.py` with PEP 723 header:
  ```python
  # /// script
  # dependencies = ["anthropic>=0.40.0", "aiosqlite>=0.19.0", "pydantic>=2.0.0"]
  # ///
  ```
- Add argparse CLI with required `--adw-id` flag (follow adw_sdlc_iso.py pattern)
- Import DatabaseManager: `from adw_modules.adw_database import DatabaseManager`
- Implement async main() using `async with DatabaseManager() as db:`
- Log workflow start: `await db.create_agent_log(agent_id, "INFO", "milestone", "Plan+Build workflow started")`
- Invoke Plan agent (using Agent SDK or subprocess pattern from existing ADWs)
- Invoke Build agent
- Log workflow completion with metadata
- Add `if __name__ == '__main__':` block for standalone execution

### Task 3: Implement adw_plan_build_review.py (BASE)
- Copy structure from adw_plan_build.py
- Update PEP 723 header and docstring (describe Plan+Build+Review)
- Add Review agent invocation after Build completes
- Log Review phase milestone: `await db.create_agent_log(agent_id, "INFO", "milestone", "Review phase started")`
- Capture Review agent output for logging
- Update final completion log with Review results

### Task 4: Implement adw_plan_build_review_fix.py (BASE)
- Copy structure from adw_plan_build_review.py
- Update PEP 723 header and docstring (describe Plan+Build+Review+Fix)
- Add Fix loop after Review:
  - Check Review output for test failures
  - If failures exist, invoke Fix agent with failure details
  - Re-run Build and Review
  - Limit iterations to 3 attempts
- Log Fix attempts: `await db.create_agent_log(agent_id, "INFO", "milestone", f"Fix attempt {iteration}/3")`
- Update final completion log with Fix iteration count

### Task 5: Adapt imports and ensure async patterns
- Verify all workflows use proper relative imports: `from adw_modules.adw_database import DatabaseManager`
- Ensure async/await consistency across all database calls
- Add error handling with try/except around database operations
- Log errors to database: `await db.create_agent_log(agent_id, "ERROR", "error", error_message, details={"traceback": str(e)})`

### Task 6: Test workflows in BASE with real adw-id
- Run `uv run adws/adw_workflows/adw_plan_build.py --adw-id test_workflow_001`
- Verify database logging: Check `orchestrator.db` for agent_logs entries
- Test argparse error handling: Run without `--adw-id` flag and verify error message
- Repeat for adw_plan_build_review.py and adw_plan_build_review_fix.py

### Task 7: Create Jinja2 template for adw_plan_build.py
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/` directory
- Copy `adw_plan_build.py` to `adw_plan_build.py.j2`
- Add Jinja2 variable substitutions:
  - `{{ config.project.name }}` in docstring
  - `{{ config.database.path }}` for DatabaseManager initialization
  - `{{ config.agent_sdk.model }}` for agent model configuration
  - `{{ config.logging.level }}` for log level
- Preserve PEP 723 header and Python syntax (no variables in code structure)

### Task 8: Create Jinja2 templates for remaining workflows
- Copy `adw_plan_build_review.py` to `adw_plan_build_review.py.j2` with same variable substitutions
- Copy `adw_plan_build_review_fix.py` to `adw_plan_build_review_fix.py.j2` with same variable substitutions
- Verify all templates have consistent variable usage

### Task 9: Register workflows in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Find `_add_adw_files()` method (around line 400-500)
- Add new method `_add_adw_workflow_files()` after `_add_adw_files()`:
  ```python
  def _add_adw_workflow_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
      """Add consolidated workflow templates to plan."""
      workflows = [
          ("adws/adw_workflows/adw_plan_build.py.j2", "adws/adw_workflows/adw_plan_build.py"),
          ("adws/adw_workflows/adw_plan_build_review.py.j2", "adws/adw_workflows/adw_plan_build_review.py"),
          ("adws/adw_workflows/adw_plan_build_review_fix.py.j2", "adws/adw_workflows/adw_plan_build_review_fix.py"),
      ]
      for template_path, output_path in workflows:
          if existing_repo and Path(output_path).exists():
              continue
          plan.add_file(
              output_path,
              self.template_repo.render_template(template_path, config.model_dump()),
              description=f"Consolidated workflow: {Path(output_path).stem}"
          )
  ```
- Call `_add_adw_workflow_files(plan, config, existing_repo)` in `build_plan()` after `_add_adw_files()`

### Task 10: Validate template rendering
- Create test config with all required variables:
  ```python
  config = TACConfig(
      project=ProjectConfig(name="test_project"),
      database={"path": "test.db"},
      agent_sdk={"model": "claude-sonnet-3.5"},
      logging={"level": "INFO"}
  )
  ```
- Render each template and verify Jinja2 variables are substituted
- Check that PEP 723 headers remain intact after rendering

### Task 11: Run validation commands
Execute all validation commands to verify zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Testing Strategy

### Unit Tests
- **DatabaseManager integration**: Mock DatabaseManager and verify async context manager usage
- **Argparse validation**: Test CLI with/without `--adw-id` flag
- **Agent SDK invocation**: Mock agent executions and verify logging
- **Template rendering**: Test Jinja2 variable substitution with sample configs

### Edge Cases
- **Missing source files**: Verify workflows can be created from codebase patterns if tac-14 source unavailable
- **Database connection failure**: Test graceful error handling with logging to stderr
- **Agent execution failure**: Verify error logging and workflow termination
- **Missing --adw-id**: Verify argparse raises clear error message

## Acceptance Criteria

1. **Directory Structure**: `adws/adw_workflows/` directory exists with 3 workflow files
2. **PEP 723 Compliance**: All workflows have valid PEP 723 dependency headers
3. **Database Integration**: Workflows use DatabaseManager with async context managers
4. **Agent SDK Control**: Workflows invoke agents programmatically (not just subprocess)
5. **CLI Arguments**: All workflows accept `--adw-id` flag via argparse (required)
6. **Logging**: Workflows log milestones, errors, and completion to SQLite via DatabaseManager
7. **Progressive Enhancement**: adw_plan_build < adw_plan_build_review < adw_plan_build_review_fix in complexity
8. **Templates Created**: 3 Jinja2 templates in `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/`
9. **Template Variables**: Templates expose config.project.name, config.database.path, config.agent_sdk.model, config.logging.level
10. **Scaffold Registration**: `scaffold_service.py` includes `_add_adw_workflow_files()` method
11. **Standalone Execution**: Workflows can run via `uv run adws/adw_workflows/adw_*.py --adw-id test`
12. **Importable**: Workflows can be imported as modules for orchestrator integration

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- **Source File Strategy**: Task 1 attempts to read source files from `/Volumes/MAc1/Celes/TAC/tac-14/`. If unavailable, Task 2-4 synthesize implementations using existing ADW patterns (adw_sdlc_iso.py, adw_patch_iso.py) as references.
- **Async Context Manager**: All database operations use `async with DatabaseManager() as db:` pattern for automatic connection lifecycle.
- **Error Resilience**: Database logging failures should not crash workflows - errors are logged to stderr instead.
- **Agent SDK Note**: Current implementation may use subprocess for agent invocation (like existing ADWs). Full Agent SDK programmatic control is aspirational for future iterations.
- **Progressive Enhancement**: Each workflow builds on the previous:
  - adw_plan_build: Foundation (Plan → Build)
  - adw_plan_build_review: Adds quality gate (+ Review)
  - adw_plan_build_review_fix: Adds self-healing (+ Fix loop)
- **Template Variables**: Using `config.*` pattern consistent with CLAUDE.md conventions
- **Dependencies**: This task depends on completion of:
  - Task 5: adw_agent_sdk.py (Agent SDK models)
  - Task 8: adw_database.py (DatabaseManager with async CRUD)
  - Task 9: adw_logging.py (async logging functions)
- **Migration Path**: SQLite-based implementation (v0.8.0). PostgreSQL migration planned for v0.9.0 requires minimal changes due to DatabaseManager abstraction.
