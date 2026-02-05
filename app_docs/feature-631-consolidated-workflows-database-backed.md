---
doc_type: feature
adw_id: feature_Tac_14_Task_10
date: 2026-02-05
idk:
  - consolidated-workflows
  - database-backed
  - agent-orchestration
  - sqlite-logging
  - multi-agent-coordination
  - workflow-templates
  - agent-sdk-control
tags:
  - feature
  - workflows
  - database
  - orchestration
related_code:
  - adws/adw_workflows/adw_plan_build.py
  - adws/adw_workflows/adw_plan_build_review.py
  - adws/adw_workflows/adw_plan_build_review_fix.py
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review_fix.py.j2
---

# Consolidated Workflows with Database-Backed Orchestration

**ADW ID:** feature_Tac_14_Task_10
**Date:** 2026-02-05
**Specification:** specs/issue-631-adw-feature_Tac_14_Task_10-sdlc_planner-consolidated-workflows.md

## Overview

This feature implements three progressive database-backed orchestration workflows that coordinate Plan, Build, Review, and Fix agents with SQLite persistence. These consolidated workflows replace JSON state file chaining with centralized database tracking, enabling real-time monitoring, resume capability, and historical analysis.

## What Was Built

- **adw_plan_build.py**: Basic two-step workflow (Plan → Build) with database logging
- **adw_plan_build_review.py**: Three-step workflow (Plan → Build → Review) with quality gates
- **adw_plan_build_review_fix.py**: Four-step workflow (Plan → Build → Review → Fix) with self-healing iterations
- **Jinja2 Templates**: Three .j2 templates exposing configuration variables for project generation
- **Scaffold Service Integration**: Registration in scaffold_service.py for automated project scaffolding

## Technical Implementation

### Files Created

**BASE Workflows (adws/adw_workflows/)**:
- `adws/adw_workflows/adw_plan_build.py`: 393 lines - Foundation workflow with Plan + Build steps
- `adws/adw_workflows/adw_plan_build_review.py`: 487 lines - Adds Review validation after Build
- `adws/adw_workflows/adw_plan_build_review_fix.py`: 596 lines - Adds iterative Fix loop (max 3 attempts)

**Templates (tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/)**:
- `adw_plan_build.py.j2`: Jinja2 template with config variables
- `adw_plan_build_review.py.j2`: Jinja2 template with config variables
- `adw_plan_build_review_fix.py.j2`: Jinja2 template with config variables

**Modified**:
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added `_add_adw_workflow_files()` method (lines 745-777)

### Key Changes

1. **PEP 723 Dependency Headers**: All workflows include inline script metadata with dependencies for `aiosqlite`, `anthropic`, `pydantic`, `python-dotenv`, and `rich`

2. **Argparse CLI**: Each workflow accepts `--adw-id` (required), `--prompt`, and `--working-dir` flags for database tracking and agent configuration

3. **DatabaseManager Integration**: Workflows use `async with DatabaseManager() as db:` context managers for automatic connection lifecycle and CRUD operations

4. **Milestone Logging**: All workflow phases log to SQLite via `db.create_agent_log()` with structured metadata:
   - Workflow start/completion
   - Step transitions (Plan, Build, Review, Fix)
   - Error details with tracebacks
   - Step duration and model usage

5. **Progressive Enhancement Pattern**:
   - adw_plan_build: Foundation (Plan → Build)
   - adw_plan_build_review: Adds quality gate (+ Review)
   - adw_plan_build_review_fix: Adds self-healing (+ Fix loop with max 3 iterations)

6. **Jinja2 Variable Substitution**: Templates expose `{{ config.project.name }}`, `{{ config.database.path }}`, `{{ config.agent_sdk.model }}`, `{{ config.logging.level }}`

7. **Scaffold Service Registration**: New `_add_adw_workflow_files()` method registers 3 workflow templates with FileAction.CREATE (idempotent - only creates if file doesn't exist)

## How to Use

### Running Workflows in BASE Repository

Execute workflows directly with `uv run` for immediate orchestration:

```bash
# Basic Plan + Build workflow
uv run adws/adw_workflows/adw_plan_build.py \
  --adw-id workflow_001 \
  --prompt "Add user authentication feature" \
  --working-dir /path/to/project

# Plan + Build + Review workflow with validation
uv run adws/adw_workflows/adw_plan_build_review.py \
  --adw-id workflow_002 \
  --prompt "Refactor payment processing module" \
  --working-dir /path/to/project

# Plan + Build + Review + Fix workflow with self-healing
uv run adws/adw_workflows/adw_plan_build_review_fix.py \
  --adw-id workflow_003 \
  --prompt "Implement user dashboard with tests" \
  --working-dir /path/to/project
```

### Generating Workflows in New Projects

Use `tac-bootstrap` CLI to scaffold workflows in generated projects:

```bash
# Generate project with consolidated workflows
cd tac_bootstrap_cli
uv run tac-bootstrap scaffold /path/to/new/project \
  --config config.yaml

# Workflows will be created in:
# /path/to/new/project/adws/adw_workflows/adw_plan_build.py
# /path/to/new/project/adws/adw_workflows/adw_plan_build_review.py
# /path/to/new/project/adws/adw_workflows/adw_plan_build_review_fix.py
```

### Inspecting Workflow Execution

Query SQLite database to inspect workflow execution history:

```bash
# View all workflow executions
sqlite3 orchestrator.db "SELECT adw_id, agent_name, step_name, created_at FROM agent_logs ORDER BY created_at DESC LIMIT 20;"

# View specific workflow logs
sqlite3 orchestrator.db "SELECT * FROM agent_logs WHERE adw_id = 'workflow_001';"

# View error logs
sqlite3 orchestrator.db "SELECT adw_id, message, details FROM agent_logs WHERE log_level = 'ERROR';"
```

## Configuration

### Environment Variables

Workflows read configuration from `.env` file:

```bash
# Database path (relative or absolute)
DATABASE_PATH=orchestrator.db

# Anthropic API key for Agent SDK
ANTHROPIC_API_KEY=sk-ant-...

# Model selection (optional, defaults to claude-sonnet-4.5)
AGENT_MODEL=claude-sonnet-4.5

# Logging level (optional, defaults to INFO)
LOG_LEVEL=INFO
```

### Template Configuration (Generated Projects)

In generated projects, Jinja2 templates substitute variables from `config.yaml`:

```yaml
project:
  name: my_project

database:
  path: data/orchestrator.db

agent_sdk:
  model: claude-sonnet-4.5

logging:
  level: INFO
```

### Workflow Arguments

All workflows accept these CLI arguments:

- `--adw-id` (required): Unique identifier for database tracking and resume capability
- `--prompt` (required): Task description to pass to Plan agent
- `--working-dir` (required): Directory where agents execute (must exist)
- `--model` (optional): Override model selection (defaults to claude-sonnet-4.5)

## Testing

### Manual Workflow Execution

Test workflows with sample prompts:

```bash
# Test Plan + Build workflow
uv run adws/adw_workflows/adw_plan_build.py \
  --adw-id test_plan_build \
  --prompt "Create a simple calculator function" \
  --working-dir .
```

Expected output: Rich console panels showing workflow progress with step timing and database logging confirmation.

### Database Verification

Verify database logging after workflow execution:

```bash
# Check if workflow logs were created
sqlite3 orchestrator.db "SELECT COUNT(*) FROM agent_logs WHERE adw_id = 'test_plan_build';"

# Verify milestone logs exist
sqlite3 orchestrator.db "SELECT step_name, log_type FROM agent_logs WHERE adw_id = 'test_plan_build' AND log_type = 'milestone';"
```

### Template Rendering Test

Test Jinja2 template rendering:

```bash
# Run scaffold service unit tests
cd tac_bootstrap_cli
uv run pytest tests/application/test_scaffold_service.py -v -k workflow
```

### Integration Test

Test complete workflow in generated project:

```bash
# Generate test project
cd tac_bootstrap_cli
uv run tac-bootstrap scaffold /tmp/test_project --config examples/basic_config.yaml

# Run workflow in generated project
cd /tmp/test_project
uv run adws/adw_workflows/adw_plan_build.py \
  --adw-id integration_test \
  --prompt "Add README file" \
  --working-dir .

# Verify execution
sqlite3 orchestrator.db "SELECT * FROM agent_logs WHERE adw_id = 'integration_test';"
```

## Notes

### Progressive Enhancement Design

Each workflow builds on the previous with incremental complexity:

1. **adw_plan_build.py**: Foundation workflow demonstrating Plan → Build orchestration with database logging
2. **adw_plan_build_review.py**: Adds quality gate by running Review agent after Build completes
3. **adw_plan_build_review_fix.py**: Adds self-healing by detecting test failures in Review output and iteratively invoking Fix agent (max 3 attempts)

This pattern allows users to choose the appropriate workflow complexity for their use case.

### Database-Backed Architecture Benefits

- **Execution Visibility**: All agent activity logged to SQLite with timestamps, step names, and metadata
- **Resume Capability**: Future versions can resume workflows from checkpoints using adw_id
- **Historical Analysis**: Query past executions for debugging, cost tracking, and performance analysis
- **Real-time Monitoring**: Orchestrator Web App (Task 12) can query database for live progress updates
- **Cost Tracking**: Log token usage and API costs for budget management

### Agent SDK Integration

Current implementation uses subprocess execution for agents (following existing ADW patterns). Full programmatic Agent SDK control is planned for future iterations with:
- Direct Python API calls to Anthropic SDK
- In-process agent execution without subprocess overhead
- Streaming token consumption and real-time cost tracking

### Migration Path

SQLite implementation targets v0.8.0. PostgreSQL migration planned for v0.9.0 requires minimal changes due to DatabaseManager abstraction layer.

### Dependencies

This feature depends on:
- Task 5: adw_agent_sdk.py (Agent SDK models)
- Task 8: adw_database.py (DatabaseManager with async CRUD)
- Task 9: adw_logging.py (async logging functions)

### Future Enhancements

- **Resume Capability**: Read checkpoint data from database to resume interrupted workflows
- **Parallel Execution**: Run multiple workflows concurrently with separate adw_ids
- **Web UI Integration**: Real-time progress visualization via Orchestrator Web App (Task 12)
- **Cost Analytics**: Aggregate token usage and costs across workflows
- **Notification Hooks**: Trigger webhooks on workflow completion or failure
