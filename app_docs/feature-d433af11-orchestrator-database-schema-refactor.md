---
doc_type: feature
adw_id: d433af11
date: 2026-02-08
idk:
  - database schema
  - SQLite
  - orchestrator
  - orch_database_models
  - WAL mode
  - Pydantic validation
  - template synchronization
tags:
  - feature
  - database
  - orchestrator
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/modules/database.py
  - adws/adw_modules/orch_database_models.py
  - tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/modules/orch_database_models.py
---

# Orchestrator Database Schema Refactor (SQLite Migration)

**ADW ID:** d433af11
**Date:** 2026-02-08
**Specification:** issue-657-adw-d433af11-chore_planner-orchestrator_test_3_verification.md

## Overview

Migrated orchestrator database from PostgreSQL to SQLite with comprehensive schema refactoring, updated Pydantic models, and template synchronization across the codebase.

## What Was Built

- **SQLite Schema Template** - New `schema_orchestrator.sql.j2` template with WAL mode, 5+ tables, and proper constraints
- **Database Models Refactor** - Updated `orch_database_models.py` with SQLite compatibility and improved Pydantic validation
- **Template Sync** - Synchronized database models and templates across `adws/` and CLI template directories
- **Type Annotations** - Enhanced type safety with proper type hints across database modules
- **Database Operations** - Refactored async database operations for SQLite (aiosqlite instead of asyncpg)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2`: New SQLite schema template with 5 tables (orchestrator_agents, agents, prompts, agent_logs, system_logs)
- `adws/adw_modules/orch_database_models.py`: Updated Pydantic models for SQLite with validation and UUID handling
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/modules/orch_database_models.py`: Synchronized copy for CLI templates
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/modules/database.py`: Refactored async operations with type hints

### Key Changes

- **Database Migration**: Transitioned from PostgreSQL (`asyncpg`) to SQLite (`aiosqlite`)
- **Schema Design**: 5-table schema with foreign keys, check constraints, and WAL mode for concurrency
- **Pydantic Models**: Updated with Union types for UUID/string handling, proper validators, and field defaults
- **Type Safety**: Added comprehensive type annotations (`Dict[str, Any]`, proper return types)
- **Model Definitions**: Refactored OrchestratorAgent, Agent, Prompt, AgentLog, SystemLog with SQLite field mappings

## How to Use

### 1. Initialize Database

```bash
# Create SQLite database from schema
cd tac_bootstrap_cli
uv run tac-bootstrap init my-app --with-orchestrator
```

### 2. Run Migrations (if needed)

```bash
# Using the template
python apps/orchestrator_db/run_migrations.py
```

### 3. Access Models in Code

```python
from orch_database_models import Agent, OrchestratorAgent, Prompt

# Automatic UUID handling
agent = Agent(**row_dict)
print(agent.id)  # Works with both UUID and string
```

## Configuration

- **WAL Mode**: Enabled by default for better concurrency (multiple readers + single writer)
- **Foreign Keys**: Enforced via PRAGMA
- **Database File**: Located at configured path (default: `orchestrator.db`)

## Testing

```bash
# Run database tests
cd tac_bootstrap_cli
uv run pytest tests/test_database.py -v

# Validate models
uv run pytest tests/test_orch_database_models.py -v

# Type checking
uv run ruff check tac_bootstrap/
```

## Notes

- SQLite provides zero-configuration setup (no separate server needed)
- Models are source of truth for schema structure
- Both `adws/` and CLI templates maintain synchronized copies
- Automatic UUID/string conversion for compatibility
- WAL mode improves concurrent access patterns
