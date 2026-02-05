---
doc_type: feature
adw_id: feature_Tac_14_Task_6
date: 2026-02-04
idk:
  - sqlite-schema
  - database-orchestrator
  - zero-config
  - wal-mode
  - migration-versioning
  - dual-validation
  - cascade-integrity
  - jinja2-templates
tags:
  - feature
  - database
  - orchestrator
  - infrastructure
related_code:
  - adws/schema/schema_orchestrator.sql
  - adws/schema/README.md
  - adws/schema/migrations/001_initial.sql
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2
---

# SQLite Schema Implementation for Orchestrator Database

**ADW ID:** feature_Tac_14_Task_6
**Date:** 2026-02-04
**Specification:** specs/issue-627-adw-feature_Tac_14_Task_6-sdlc_planner-sqlite-schema.md

## Overview

Implemented a complete SQLite database schema for TAC Bootstrap's orchestrator system, providing persistent state tracking for agent workflows, prompts, and execution logs. The implementation follows a dual-location pattern (BASE functional + TEMPLATES Jinja2) with zero-config auto-initialization, WAL mode for concurrency, and defensive integrity constraints.

This feature enables full observability into agent orchestration, supporting the TAC-14 goal of transforming tac_bootstrap into a Class 3 Orchestrator with persistent state management.

## What Was Built

### Core Database Schema (5 Tables)

- **orchestrator_agents**: Agent type definitions/templates (~10-50 records)
- **agents**: Runtime agent instances per workflow (100s-1000s records)
- **prompts**: Individual LLM prompt executions (1000s-10000s records)
- **agent_logs**: Agent lifecycle events (1000s-10000s records)
- **system_logs**: System-wide logging (1000s-10000s records)

### Database Files Created

**BASE (Functional Implementation)**:
- `adws/schema/schema_orchestrator.sql` - Complete schema with tables, triggers, indexes
- `adws/schema/README.md` - Comprehensive documentation (9 sections)
- `adws/schema/migrations/001_initial.sql` - Initial versioned migration
- `adws/schema/migrations/.gitkeep` - Preserve directory in git

**TEMPLATES (Jinja2 for CLI Generation)**:
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/.gitkeep`

### Integration with Scaffold Service

- Added `_add_schema_files()` method to ScaffoldService (scaffold_service.py:740-773)
- Registered schema templates in build_plan() pipeline after ADW files
- Renders 3 files: schema SQL, README, migrations/.gitkeep

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added schema file registration (38 new lines)
  - New method `_add_schema_files()` following existing pattern
  - Integration point at line 93 in `build_plan()`

### Key Changes

1. **SQLite-Native Schema Design**:
   - TEXT for UUIDs (instead of PostgreSQL UUID type)
   - TEXT for timestamps with ISO 8601 format (instead of TIMESTAMPTZ)
   - REAL for cost tracking (instead of DECIMAL)
   - TEXT for JSON storage (instead of JSONB)
   - Preserved all 5 core tables from PostgreSQL v1 design

2. **Defensive Integrity Constraints**:
   - CHECK constraints for enums (status, log_level, log_type, agent_type)
   - FOREIGN KEY constraints with ON DELETE CASCADE for cleanup
   - DEFAULT values for timestamps using `datetime('now')`
   - Trigger `update_orchestrator_agents_updated_at` for auto-update timestamps

3. **Performance Optimization**:
   - 6 strategic indexes for common query patterns:
     - `idx_agents_session` on agents(session_id)
     - `idx_agents_orch` on agents(orchestrator_agent_id)
     - `idx_prompts_agent` on prompts(agent_id)
     - `idx_prompts_status` on prompts(status)
     - `idx_agent_logs_agent` on agent_logs(agent_id)
     - `idx_system_logs_level` on system_logs(log_level)

4. **Concurrency Support**:
   - WAL mode enabled via `PRAGMA journal_mode=WAL`
   - Foreign key constraints enabled via `PRAGMA foreign_keys=ON`
   - Supports multiple readers + single writer pattern

5. **Zero-Config Philosophy**:
   - Database auto-creates at `adws/schema/orchestrator.db`
   - Override via `TAC_ORCHESTRATOR_DB` environment variable
   - No manual setup required (implementation in future Task 8: adw_database.py)

## How to Use

### For TAC Bootstrap Development

1. **View the schema**:
   ```bash
   cat adws/schema/schema_orchestrator.sql
   ```

2. **Read documentation**:
   ```bash
   cat adws/schema/README.md
   ```

3. **Validate SQL syntax**:
   ```bash
   sqlite3 :memory: < adws/schema/schema_orchestrator.sql
   ```

### For Generated Projects

When using `tac-bootstrap init` to create a new project, the schema files will be automatically copied:

1. Schema SQL template renders to `adws/schema/schema_orchestrator.sql`
2. README renders to `adws/schema/README.md`
3. Migrations directory created with `.gitkeep`

### Inspect Database (Future)

Once database operations are implemented (Task 8):

```bash
# Connect to database
sqlite3 adws/schema/orchestrator.db

# List tables
.tables

# View schema
.schema orchestrator_agents

# Query agents
SELECT name, agent_type FROM orchestrator_agents;
```

## Configuration

### Environment Variables

- **TAC_ORCHESTRATOR_DB**: Override default database location
  - Default: `adws/schema/orchestrator.db`
  - Example: `export TAC_ORCHESTRATOR_DB=/tmp/test_orchestrator.db`

### Database Location

The database file is gitignored by default (`.gitignore` already includes `*.db` patterns at lines 37-39, 173-175).

### Migration Strategy

- Versioned SQL files in `adws/schema/migrations/`
- Naming convention: `NNN_description.sql` (e.g., `001_initial.sql`)
- Future migrations append to directory
- Migration runner to be implemented in Task 19 (utility scripts)

## Testing

### Validate SQL Schema Syntax

```bash
sqlite3 :memory: < adws/schema/schema_orchestrator.sql
echo "Exit code: $?"
```

Expected: Exit code 0 (success)

### Verify BASE Files Exist

```bash
ls -la adws/schema/schema_orchestrator.sql
ls -la adws/schema/README.md
ls -la adws/schema/migrations/001_initial.sql
```

Expected: All files exist with content

### Verify TEMPLATE Files Exist

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/.gitkeep
```

Expected: All template files present

### Validate .gitignore Patterns

```bash
grep -E "\*\.db|\*\.sqlite" .gitignore
```

Expected: Patterns already exist (lines 37-39, 173-175)

### Run CLI Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Expected: All tests pass

### Smoke Test CLI

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Expected: Help output displays without errors

## Notes

### SQLite vs PostgreSQL Type Mapping

| PostgreSQL (v1) | SQLite (v2) | Python Type | Notes |
|----------------|-------------|-------------|-------|
| UUID | TEXT | str | Store as string representation |
| TIMESTAMPTZ | TEXT | datetime | ISO 8601 format, use datetime('now') |
| VARCHAR | TEXT | str | SQLite has single TEXT type |
| INTEGER | INTEGER | int | Same in both |
| DECIMAL | REAL | float/Decimal | Use REAL for cost_usd |
| JSONB | TEXT | dict | Store JSON as TEXT |

### Design Decisions

1. **Zero-config auto-init**: Database file creates automatically on first access (future Task 8)
2. **WAL mode**: Enabled for concurrent reads + single writer pattern
3. **Defensive integrity**: Triggers + CASCADE prevent orphaned records
4. **Dual validation**: DB CHECK constraints + Pydantic models (future Task 7)
5. **Migration versioning**: Supports easy PostgreSQL upgrade path

### Dependencies

- SQLite 3.35+ (built-in Python 3.10+)
- aiosqlite >=0.19.0 (to be added in Task 8: adw_database.py)

### Related Tasks

- **Task 7** (next): Create orch_database_models.py with Pydantic models mapping to this schema
- **Task 8** (depends on 7): Create adw_database.py with CRUD operations and connection pooling
- **Task 15** (testing): Create test suites including test_database.py
- **Task 19** (utilities): Create setup_database.sh script

### Future Enhancements

- Automatic retention policies (Phase 10, Task 19)
- Query performance monitoring
- Database backup automation
- PostgreSQL migration tooling (pgloader)
- Audit trail for schema changes

### Migration from TAC-14 v1

This schema simplifies the original PostgreSQL version:
- Removed explicit UUID type → TEXT
- Removed TIMESTAMPTZ → TEXT with ISO format
- Removed JSONB → TEXT
- Simplified indexes (6 instead of 8)
- Preserved all 5 core tables
- Preserved referential integrity
- Preserved functional requirements
