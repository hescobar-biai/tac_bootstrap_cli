---
doc_type: feature
adw_id: feature_Tac_14_Task_8
date: 2026-02-05
idk:
  - database
  - sqlite
  - aiosqlite
  - async
  - repository
  - orm
  - crud
  - orchestrator
tags:
  - feature
  - infrastructure
  - database
related_code:
  - adws/adw_modules/adw_database.py
  - adws/adw_database.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2
  - data/.gitignore
---

# SQLite Database Operations for Orchestrator Persistence

**ADW ID:** feature_Tac_14_Task_8
**Date:** 2026-02-05
**Specification:** specs/issue-629-adw-feature_Tac_14_Task_8-sdlc_planner-database-operations.md

## Overview

Implemented a zero-configuration SQLite database manager for TAC Bootstrap orchestrator system using aiosqlite. This module provides async CRUD operations for five core tables (orchestrator_agents, agents, prompts, agent_logs, system_logs) enabling orchestrator workflows to persist agent state, execution logs, and metrics without requiring external database servers.

## What Was Built

- **DatabaseManager Class**: Async context manager for SQLite operations with WAL mode
- **Complete CRUD Operations**: Full create/read/update/delete methods for all 5 orchestrator tables
- **Auto-Schema Initialization**: Reads and applies schema from `adws/schema/schema_orchestrator.sql` on first connection
- **Zero Configuration**: Single-file database in `data/orchestrator.db` with auto-directory creation
- **Template Support**: Jinja2 template for bootstrapped projects in `tac_bootstrap_cli/templates/`
- **Environment Configuration**: Support for `ORCHESTRATOR_DB_PATH` to customize database location

## Technical Implementation

### Files Modified

- `adws/adw_modules/adw_database.py`: Core DatabaseManager implementation (1012 lines) with PEP 723 dependencies
- `adws/adw_database.py`: Standalone convenience wrapper for direct usage in ADWs
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2`: Template version for project generation
- `data/.gitignore`: Exclude `*.db` files from version control
- `adws/adw_build_iso.py`, `adws/adw_plan_iso.py`, `adws/adw_review_iso.py`: Updated to use DatabaseManager for persistence

### Key Changes

1. **Async SQLite Interface**: Uses `aiosqlite` for non-blocking database operations compatible with async orchestrator workflows
2. **Context Manager Pattern**: Supports both `async with DatabaseManager()` and explicit `connect()`/`close()` lifecycle
3. **Row Factory**: Configured with `aiosqlite.Row` for dict-like access to query results (`dict(row)`)
4. **WAL Mode**: Write-Ahead Logging enabled for concurrent reads with single writer
5. **Comprehensive CRUD**:
   - orchestrator_agents: create, get, list, update, delete
   - agents: create, get, list (with session filtering), update, delete
   - prompts: create, get, list (by agent), update, delete
   - agent_logs: create, get (filtered by agent/level/date), list recent
   - system_logs: create, get (filtered by level/component/date), list recent

### Architecture Highlights

**DDD Lite Infrastructure Layer**:
- DatabaseManager as cross-cutting concern (infrastructure layer)
- No business logic - pure data access
- Clean abstraction enabling future PostgreSQL migration
- Pydantic models in `orch_database_models.py` for type safety

**SQLite Implementation Details**:
- UUIDs stored as TEXT: `"550e8400-e29b-41d4-a716-446655440000"`
- Timestamps as TEXT (ISO 8601): `"2026-02-04T10:30:00.000000"`
- JSON metadata as TEXT: `json.dumps()` for storage, `json.loads()` for retrieval
- Placeholders: `?` syntax (SQLite) vs PostgreSQL `$1, $2`
- Last insert ID: `cursor.lastrowid` (SQLite) vs PostgreSQL `RETURNING id`

## How to Use

### Basic Context Manager Pattern (Recommended)

```python
import asyncio
from adws.adw_database import DatabaseManager

async def example():
    # Auto-connects, initializes schema, and closes on exit
    async with DatabaseManager("data/orchestrator.db") as db:
        # Create orchestrator agent definition
        agent_id = await db.create_orchestrator_agent(
            name="scout-report-suggest",
            description="Scouts codebase and suggests fixes",
            agent_type="utility",
            capabilities="codebase_exploration,issue_detection",
            default_model="claude-sonnet-3.5"
        )

        # Create runtime agent instance
        runtime_id = await db.create_agent(
            orchestrator_agent_id=agent_id,
            session_id="550e8400-e29b-41d4-a716-446655440000",
            status="executing"
        )

        # Log agent activity
        await db.create_agent_log(
            agent_id=runtime_id,
            log_level="INFO",
            log_type="state_change",
            message="Agent started execution",
            details={"phase": "exploration"}
        )

        # Query agent state
        agent = await db.get_agent(runtime_id)
        print(f"Agent status: {agent['status']}")

asyncio.run(example())
```

### Explicit Connection Management

```python
async def explicit_example():
    db = DatabaseManager("data/orchestrator.db")
    try:
        await db.connect()

        agents = await db.list_orchestrator_agents()
        for agent in agents:
            print(f"{agent['name']}: {agent['description']}")
    finally:
        await db.close()
```

### Integration in ADW Workflows

```python
# In adws/adw_sdlc_zte_iso.py or similar orchestrator ADW
from adws.adw_database import DatabaseManager

async with DatabaseManager() as db:  # Uses default data/orchestrator.db
    # Track orchestrator agent execution
    session_id = str(uuid.uuid4())

    # Create agent instances for SDLC workflow
    planner_id = await db.create_agent(
        orchestrator_agent_id="...",
        session_id=session_id,
        status="pending"
    )

    # Update status as workflow progresses
    await db.update_agent(planner_id, status="executing", started_at=now_iso())

    # Log activities
    await db.create_agent_log(
        agent_id=planner_id,
        log_level="INFO",
        log_type="execution",
        message="Plan phase completed",
        details={"files_created": 5}
    )
```

## Configuration

### Environment Variables

- `ORCHESTRATOR_DB_PATH`: Override default database location
  ```bash
  export ORCHESTRATOR_DB_PATH=/custom/path/orchestrator.db
  ```

### Default Locations

- Database file: `data/orchestrator.db` (relative to project root)
- Schema file: `adws/schema/schema_orchestrator.sql` (required for initialization)
- Data directory: Auto-created with `parents=True, exist_ok=True`

### SQLite Settings

Automatically configured on connection:
- WAL mode: `PRAGMA journal_mode=WAL`
- Foreign keys: `PRAGMA foreign_keys=ON`
- Synchronous: `PRAGMA synchronous=NORMAL` (performance vs safety balance)

## Testing

### Manual Smoke Test

```bash
# Create test script
cat > test_db_smoke.py << 'EOF'
import asyncio
from adws.adw_database import DatabaseManager

async def test():
    async with DatabaseManager() as db:
        # Create orchestrator agent
        agent_id = await db.create_orchestrator_agent(
            name="test-agent",
            description="Test description"
        )
        print(f"✓ Created agent: {agent_id}")

        # Retrieve
        agent = await db.get_orchestrator_agent(agent_id)
        assert agent["name"] == "test-agent"
        print(f"✓ Retrieved agent: {agent['name']}")

        # List all
        agents = await db.list_orchestrator_agents()
        print(f"✓ Total agents: {len(agents)}")

asyncio.run(test())
EOF

# Run smoke test
uv run python test_db_smoke.py
```

### Verify Database Schema

```bash
# Inspect database structure
sqlite3 data/orchestrator.db ".schema"

# View orchestrator agents
sqlite3 data/orchestrator.db "SELECT id, name, agent_type FROM orchestrator_agents;"

# View agent logs
sqlite3 data/orchestrator.db "SELECT agent_id, log_level, message FROM agent_logs ORDER BY created_at DESC LIMIT 10;"
```

### Import Validation

```bash
# Test module import
uv run python -c "from adws.adw_database import DatabaseManager; print('✓ Import successful')"
```

### Linting Check

```bash
# Verify code quality
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

### SQLite vs PostgreSQL Trade-offs

**Advantages of SQLite for TAC v0.8.0:**
- Zero installation and configuration required
- Single-file portability (copy `.db` file to backup/share)
- Perfect for local development and testing
- Sufficient for orchestrator use case (single workflow process)

**Limitations (Documented):**
- Single writer (concurrent writes are serialized)
- Not suitable for high-concurrency production (>10 concurrent users)
- No built-in replication or distributed transactions

**Migration Path to PostgreSQL (v0.9.0+):**
- Use `pgloader` for data migration: `pgloader orchestrator.db postgresql://...`
- DatabaseManager interface remains identical (abstraction layer)
- Swap implementation: `asyncpg` instead of `aiosqlite`
- Connection pooling with `asyncpg.create_pool()`

### Design Decisions

**Why Single Connection (No Pooling)?**
- Orchestrator workflows are sequential (one workflow at a time per process)
- SQLite's single-writer constraint makes pooling redundant
- WAL mode provides concurrent reads without connection pool overhead
- YAGNI principle: Add pooling if concurrent workflow execution is needed

**Why Explicit commit()?**
- Transaction control visible in application code
- Enables batch operations without intermediate commits
- Fail-fast on errors before data is persisted
- Matches PostgreSQL mental model for easier migration

**Why Dict Return Types?**
- Flexible schema evolution (add columns without breaking code)
- JSON-serializable for API responses
- Can be mapped to Pydantic models at domain layer
- Avoids ORM complexity for simple CRUD operations

### Future Enhancements

Deferred to later TAC versions:
- **Connection Pooling**: Add `asyncpg.create_pool()` when PostgreSQL support added
- **Migrations**: Use Alembic for schema versioning (v0.9.0 when schema stabilizes)
- **Transaction Context Manager**: `async with db.transaction()` for complex multi-table operations
- **Soft Deletes**: Add `deleted_at` column if audit trail required
- **Pagination**: Add `offset`/`limit` parameters to `list_*` methods
- **Query Builder**: Consider SQLAlchemy Core for complex dynamic queries

### Dependencies

**Runtime Dependencies** (PEP 723):
- `aiosqlite>=0.19.0`: Async SQLite driver

**Schema Dependencies**:
- `adws/schema/schema_orchestrator.sql`: Must exist or `FileNotFoundError` raised

**Related Modules**:
- `adws/adw_modules/orch_database_models.py`: Pydantic models for type hints (optional)
- `adws/adw_modules/workflow_ops.py`: Orchestrator workflow utilities

### Concurrency Model

**SQLite Limitations**:
- Single writer at a time (writes are serialized)
- Concurrent reads allowed with WAL mode
- Recommended: One DatabaseManager instance per process

**Best Practices**:
- Use connection pooling at application level, not database level
- For high-concurrency, migrate to PostgreSQL
- Document single-instance pattern in orchestrator ADWs
