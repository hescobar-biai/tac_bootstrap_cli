---
doc_type: feature
adw_id: feature_Tac_14_Task_9
date: 2026-02-05
idk:
  - database-logging
  - aiosqlite
  - async-operations
  - error-handling
  - json-serialization
  - repository-pattern
tags:
  - feature
  - database
  - logging
related_code:
  - adws/adw_modules/adw_database.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2
  - adws/schema/schema_orchestrator.sql
---

# Database Logging with SQLite

**ADW ID:** feature_Tac_14_Task_9
**Date:** 2026-02-05
**Specification:** specs/issue-630-adw-feature_Tac_14_Task_9-sdlc_planner-database-logging.md

## Overview

Extended the DatabaseManager class with enhanced logging capabilities and flexible query methods for the agent_logs table. This feature implements async database logging infrastructure to support orchestrator agent monitoring, debugging, and observability with graceful error handling that ensures logging failures never crash orchestrator agents.

## What Was Built

- **log_agent_event()**: High-level convenience method for logging agent events with graceful error handling
- **get_agent_logs_by_type()**: Query logs filtered by both agent_id and log_type
- **get_logs_by_type()**: Query logs by type across all agents
- **get_recent_logs()**: Alias method for querying recent activity across all agents
- **cleanup_old_logs()**: Utility method for manual log retention (not auto-executed)
- Updated module docstrings with usage examples demonstrating error-resilient logging patterns
- Jinja2 template synchronization for generated projects

## Technical Implementation

### Files Modified

- `adws/adw_modules/adw_database.py`: Added 5 new logging methods (245 lines) to DatabaseManager class with comprehensive docstrings and error handling
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2`: Updated Jinja2 template to match BASE implementation for generated projects

### Key Changes

1. **Error-Resilient Logging**: log_agent_event() wraps create_agent_log() with try/except catching aiosqlite.Error and generic exceptions, logging warnings to stderr instead of raising exceptions
2. **JSON Metadata Handling**: All query methods deserialize the TEXT details field using json.loads() with JSONDecodeError protection
3. **Flexible Querying**: Three query methods support different filtering patterns - by agent+type, by type globally, and recent activity dashboards
4. **Manual Retention**: cleanup_old_logs() uses datetime.timedelta to calculate cutoff timestamps and returns deleted row count
5. **Consistent Patterns**: All methods follow existing repository pattern with async/await, proper error logging, and descriptive docstrings with examples

## How to Use

### Logging Agent Events (Error-Resilient)

```python
from adws.adw_modules.adw_database import DatabaseManager

async def agent_workflow():
    db = DatabaseManager("orchestrator.db")
    await db.initialize()

    # High-level logging - never raises exceptions
    await db.log_agent_event(
        agent_id="550e8400-e29b-41d4-a716-446655440000",
        log_type="milestone",
        message="Starting code analysis",
        metadata={"files_queued": 42}
    )

    # Even if database fails, this won't crash your agent
    # Errors logged to stderr instead
    await db.close()
```

### Querying Logs by Type

```python
# Get all error logs across all agents
all_errors = await db.get_logs_by_type("error", limit=50)
print(f"System has {len(all_errors)} error logs")

# Get errors for specific agent
agent_errors = await db.get_agent_logs_by_type(
    agent_id="550e8400-e29b-41d4-a716-446655440000",
    log_type="error",
    limit=10
)

# Get recent activity dashboard
recent = await db.get_recent_logs(limit=100)
for log in recent[:10]:
    print(f"{log['created_at']}: {log['message']}")
```

### Manual Log Cleanup

```python
# Delete logs older than 90 days (not auto-executed)
deleted = await db.cleanup_old_logs(days=90)
print(f"Deleted {deleted} old logs")
```

## Configuration

### Supported Log Types

The log_type parameter accepts values constrained by schema CHECK:
- `state_change`: Agent state transitions
- `milestone`: Significant progress points
- `error`: Error events
- `performance`: Performance metrics
- `tool_call`: Tool execution tracking
- `cost_update`: Cost/token tracking

### Supported Log Levels

The log_level parameter (defaults to 'INFO'):
- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

### Database Schema

Uses existing `agent_logs` table from schema_orchestrator.sql:
- PRIMARY KEY: INTEGER AUTOINCREMENT (not UUID)
- FOREIGN KEY: agent_id references agents(id)
- Indexed on: agent_id (idx_agent_logs_agent)
- metadata stored as TEXT (JSON serialized)

## Testing

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Test Error Resilience

```python
# This should log to stderr but NOT raise exception
async def test_graceful_degradation():
    db = DatabaseManager("nonexistent.db")
    # Don't initialize - database not ready

    # Should return None and log warning, not crash
    result = await db.log_agent_event(
        agent_id="test-id",
        log_type="milestone",
        message="This will fail gracefully"
    )
    assert result is None  # Returns None on error
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Run Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**Error Handling Philosophy:**
- Logging is supporting infrastructure - NEVER crash orchestrator agents
- All database errors caught and logged to stderr
- Methods return None or empty list on error instead of raising exceptions
- Documented clearly in docstrings with "never raises exceptions" guarantees

**Performance Considerations:**
- agent_logs table has index on agent_id (idx_agent_logs_agent) for fast agent-specific queries
- SQLite WAL mode (from Task 8) supports concurrent writes from multiple agents
- Limit parameters prevent unbounded result sets (default: 100)

**Dual-Location Pattern:**
- BASE: `adws/adw_modules/adw_database.py` (functional code in this repository)
- TEMPLATES: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2` (for generated projects)
- Both files must stay synchronized - logging methods have no Jinja2 variables

**No Auto-Retention:**
- cleanup_old_logs() is utility method for MANUAL cleanup only
- Not auto-executed - call manually or schedule via cron/systemd timer
- Example cron: `0 2 * * * cd /path/to/project && python -c "import asyncio; from adw_database import DatabaseManager; asyncio.run(DatabaseManager('orchestrator.db').cleanup_old_logs(30))"`

**Future PostgreSQL Migration:**
- Methods are backend-agnostic (only SQL syntax would change)
- PostgreSQL version would use asyncpg with same interface
- Placeholder migration: `?` → `$1, $2, $3` for asyncpg
