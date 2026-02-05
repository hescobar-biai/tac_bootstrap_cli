# Feature: Implementar Database Logging con SQLite (BASE + TEMPLATES)

## Metadata
issue_number: `630`
adw_id: `feature_Tac_14_Task_9`
issue_json: `{"number": 630, "title": "Implementar Database Logging con SQLite (BASE + TEMPLATES)", "body": "file: ddd_lite.md\nfile: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md\n\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_9`\n**Cambios**:\n```diff\n+ Logging asíncrono con aiosqlite\n\n+ JSON serialization con TEXT field\n```\n\n**Ejemplo de logging adaptado**:\n```python\nimport json\nfrom datetime import datetime\nimport uuid\n\nasync def log_agent_event(\n    db: DatabaseManager,\n    agent_id: str,\n    log_type: str,\n    message: str,\n    metadata: Optional[dict] = None\n):\n    \"\"\"Log agent event to database.\"\"\"\n    log_id = str(uuid.uuid4())\n    now = datetime.utcnow().isoformat()\n    metadata_json = json.dumps(metadata) if metadata else None\n\n    await db.conn.execute(\n        \"\"\"\n        INSERT INTO agent_logs (id, agent_id, log_type, message, metadata, created_at)\n        VALUES (?, ?, ?, ?, ?, ?)\n        \"\"\",\n        (log_id, agent_id, log_type, message, metadata_json, now)\n    )\n    await db.conn.commit()"}`

## Feature Description

Extend the existing DatabaseManager from Task 8 (adws/adw_modules/adw_database.py) with enhanced logging capabilities and query methods for the agent_logs table. This feature implements async database logging infrastructure to support orchestrator agent monitoring, debugging, and observability.

The logging methods integrate seamlessly with the existing SQLite-based DatabaseManager, using the agent_logs table schema already defined in schema_orchestrator.sql. All operations use aiosqlite for async execution with proper error handling.

## User Story

As an orchestrator agent developer
I want to log agent events to the database with flexible querying capabilities
So that I can monitor agent execution, debug issues, and analyze agent behavior patterns without exceptions disrupting agent workflows

## Problem Statement

The current DatabaseManager (Task 8) provides CRUD operations for orchestrator_agents, agents, prompts, and basic agent_logs operations. However, it lacks:

1. **Convenience logging methods**: No high-level log_agent_event() function for common logging patterns
2. **Flexible queries**: Limited query methods to retrieve logs by type, recency, or agent
3. **Error resilience**: No graceful degradation when logging fails (would crash orchestrator agents)
4. **Retention utilities**: No cleanup mechanism for old logs (though not auto-executed)

This limits visibility into agent execution and risks orchestrator crashes if logging encounters errors.

## Solution Statement

Extend DatabaseManager with 4 new methods:

1. **log_agent_event(agent_id, log_type, message, metadata)**: High-level logging method with error handling
2. **get_agent_logs(agent_id, limit)**: Query logs for a specific agent with limit
3. **get_logs_by_type(log_type, limit)**: Query logs by type (e.g., 'error', 'milestone')
4. **get_recent_logs(limit)**: Query recent logs across all agents
5. **cleanup_old_logs(days)**: Utility method for manual log retention (not auto-executed)

All methods:
- Use async/await with aiosqlite
- Follow repository pattern from Task 8
- Implement try/except with stderr warnings (no exceptions)
- Support JSON metadata serialization/deserialization
- Leverage existing agent_logs table and indexes

## Relevant Files

### Existing Files (to extend)
- `adws/adw_modules/adw_database.py` - DatabaseManager class with existing create_agent_log() method (line 750-792)
- `adws/schema/schema_orchestrator.sql` - Schema with agent_logs table (line 87-98) and idx_agent_logs_agent index (line 136)

### Template Files (to update)
- `tac_bootstrap_cli/infrastructure/templates/adws/adw_modules/adw_database.py.j2` - Template for DatabaseManager
- `tac_bootstrap_cli/infrastructure/templates/adws/schema/schema_orchestrator.sql.j2` - Template for schema (if not exists)

### New Files
None - all changes extend existing files

## Implementation Plan

### Phase 1: Foundation
1. Read existing DatabaseManager implementation to understand patterns
2. Verify agent_logs schema and existing create_agent_log() method
3. Identify insertion point for new logging methods (after existing agent_logs CRUD)

### Phase 2: Core Implementation
4. Implement log_agent_event() with error handling and stderr fallback
5. Implement get_agent_logs() query method with limit parameter
6. Implement get_logs_by_type() query method
7. Implement get_recent_logs() query method
8. Implement cleanup_old_logs() utility method
9. Add comprehensive docstrings with log_type examples

### Phase 3: Integration
10. Update template at tac_bootstrap_cli/infrastructure/templates/adws/adw_modules/adw_database.py.j2
11. Verify template matches BASE implementation
12. Update scaffold_service.py if template registration needed (likely already registered from Task 8)

## Step by Step Tasks

### Task 1: Read and understand existing implementation
- Read adws/adw_modules/adw_database.py focusing on create_agent_log() method (lines 750-792)
- Read adws/schema/schema_orchestrator.sql agent_logs table definition (lines 87-98)
- Understand existing error handling patterns in DatabaseManager
- Identify common log_type values from schema CHECK constraint (line 97)

### Task 2: Implement log_agent_event() convenience method
- Add log_agent_event() method after create_agent_log() in DatabaseManager class
- Parameters: agent_id (str), log_type (str), message (str), metadata (Optional[dict])
- Return type: Optional[int] (log_id or None on error)
- Implement try/except wrapper calling create_agent_log()
- Add stderr warning with fallback to print() if database write fails
- Document common log_type values in docstring: 'state_change', 'milestone', 'error', 'performance', 'tool_call', 'cost_update'
- Example signature:
  ```python
  async def log_agent_event(
      self,
      agent_id: str,
      log_type: str,
      message: str,
      metadata: Optional[Dict[str, Any]] = None
  ) -> Optional[int]:
  ```

### Task 3: Implement get_agent_logs() query method
- Add get_agent_logs() method in agent_logs section of DatabaseManager
- Parameters: agent_id (str), limit (int = 100)
- Return type: List[Dict[str, Any]]
- Query agent_logs WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?
- Deserialize JSON metadata field using json.loads()
- Add error handling with aiosqlite.Error
- Use existing pattern from get_agent_logs() at line 794 as reference

### Task 4: Implement get_logs_by_type() query method
- Add get_logs_by_type() method after get_agent_logs()
- Parameters: log_type (str), limit (int = 100)
- Return type: List[Dict[str, Any]]
- Query agent_logs WHERE log_type = ? ORDER BY created_at DESC LIMIT ?
- Deserialize JSON metadata field
- Add error handling
- Document example: useful for finding all 'error' logs across agents

### Task 5: Implement get_recent_logs() query method
- Add get_recent_logs() method after get_logs_by_type()
- Parameters: limit (int = 100)
- Return type: List[Dict[str, Any]]
- Query agent_logs ORDER BY created_at DESC LIMIT ?
- Deserialize JSON metadata field
- Add error handling
- Document example: dashboard view of recent activity

### Task 6: Implement cleanup_old_logs() utility method
- Add cleanup_old_logs() method at end of agent_logs section
- Parameters: days (int = 30)
- Return type: int (number of deleted logs)
- Calculate cutoff timestamp: datetime.utcnow() - timedelta(days=days)
- DELETE FROM agent_logs WHERE created_at < cutoff
- Add docstring warning: "Manual cleanup only - not auto-executed"
- Add error handling
- Return rowcount

### Task 7: Update BASE file docstring and examples
- Update module docstring at top of adw_database.py
- Add usage example showing log_agent_event() with error handling
- Add usage example showing query methods
- Document that logging never raises exceptions (graceful degradation)

### Task 8: Update template file
- Read tac_bootstrap_cli/infrastructure/templates/adws/adw_modules/adw_database.py.j2
- Copy all new methods from BASE to template
- Verify Jinja2 variables are preserved (if any)
- Ensure docstrings and error handling match BASE exactly
- Note: No Jinja2 variables expected in logging methods (config-agnostic)

### Task 9: Verify template registration
- Check tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
- Verify adw_database.py.j2 is already registered from Task 8
- If not registered, add registration for adw_modules/adw_database.py.j2
- Note: Likely already registered, this is verification only

### Task 10: Run validation commands
- Execute: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Execute: `cd tac_bootstrap_cli && uv run ruff check .`
- Execute: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Execute: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify all commands pass with zero regressions

## Testing Strategy

### Unit Tests
Create tests in adws/adw_tests/test_database.py (if exists, else document for later):

1. **test_log_agent_event_success**: Verify log_agent_event() creates log with metadata
2. **test_log_agent_event_error_handling**: Mock aiosqlite.Error, verify stderr warning, no exception
3. **test_get_agent_logs_with_limit**: Create 150 logs, query with limit=100, verify count
4. **test_get_logs_by_type**: Create logs with different types, verify filtering
5. **test_get_recent_logs**: Create logs for multiple agents, verify cross-agent query
6. **test_cleanup_old_logs**: Create old and recent logs, verify only old ones deleted
7. **test_json_metadata_deserialization**: Verify metadata dict survives round-trip

### Edge Cases
1. **Missing agent_id**: log_agent_event() with invalid agent_id - should log to stderr, return None
2. **Empty log_type**: Query with empty string - should return empty list
3. **Large metadata**: 10KB JSON metadata - should serialize/deserialize correctly
4. **Concurrent writes**: Multiple agents logging simultaneously - WAL mode should handle
5. **Database connection closed**: Call logging methods after close() - should raise clear error

## Acceptance Criteria

1. ✅ log_agent_event() method added to DatabaseManager with 4 parameters
2. ✅ log_agent_event() never raises exceptions - uses try/except with stderr warnings
3. ✅ get_agent_logs(agent_id, limit) returns list of dicts with deserialized metadata
4. ✅ get_logs_by_type(log_type, limit) filters by log_type correctly
5. ✅ get_recent_logs(limit) returns cross-agent logs ordered by recency
6. ✅ cleanup_old_logs(days) deletes logs older than threshold, returns count
7. ✅ All new methods use async/await with aiosqlite
8. ✅ JSON metadata field correctly serialized (dumps) and deserialized (loads)
9. ✅ Docstrings document common log_type values from schema
10. ✅ Template at tac_bootstrap_cli/infrastructure/templates/adws/adw_modules/adw_database.py.j2 matches BASE
11. ✅ All validation commands pass with zero regressions

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Run tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**Key Implementation Details:**
- The agent_logs table uses INTEGER PRIMARY KEY AUTOINCREMENT (line 88 of schema), not TEXT UUID
- Existing create_agent_log() method returns int (lastrowid), not UUID string
- log_type values are constrained by CHECK in schema: 'state_change', 'milestone', 'error', 'performance', 'tool_call', 'cost_update'
- metadata field is TEXT in database, requires json.dumps() for write, json.loads() for read
- Indexes already exist on agent_id (idx_agent_logs_agent) - queries will be performant

**Error Handling Philosophy:**
- Logging is supporting infrastructure - NEVER crash orchestrator agents
- Use try/except to catch aiosqlite.Error
- Log to stderr with sys.stderr.write() or logging.warning()
- Return None or empty list on error, document this in docstrings
- Example pattern:
  ```python
  try:
      # database operation
  except aiosqlite.Error as e:
      sys.stderr.write(f"WARNING: Database logging failed: {e}\n")
      return None
  ```

**Dual-Location Pattern:**
- BASE: adws/adw_modules/adw_database.py (functional code)
- TEMPLATES: tac_bootstrap_cli/infrastructure/templates/adws/adw_modules/adw_database.py.j2
- Both must be identical for logging methods (no Jinja2 variables in this section)

**No Auto-Retention:**
- cleanup_old_logs() is utility method for MANUAL cleanup
- Document in docstring: "Not auto-executed - call manually or via cron"
- Users can add to cron: `python -c "asyncio.run(db.cleanup_old_logs(30))"`

**Dependencies:**
- aiosqlite>=0.19.0 (already in PEP 723 header from Task 8)
- No new dependencies required

**Future PostgreSQL Migration:**
- These methods are backend-agnostic
- PostgreSQL version would use asyncpg with same interface
- Only change: SQL placeholders (? → $1, $2)
