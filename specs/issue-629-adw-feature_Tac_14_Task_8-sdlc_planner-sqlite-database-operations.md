# Feature: SQLite Database Operations with aiosqlite (BASE + TEMPLATES)

## Metadata
issue_number: `629`
adw_id: `feature_Tac_14_Task_8`
issue_json: `{"number": 629, "title": "Implementar Database Operations con sqlite3/aiosqlite (BASE + TEMPLATES)", "body": "file: ddd_lite.md \nfile: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_8`\n\n**Cambios principales**:\n```diff\n\n+ aiosqlite para SQLite asíncrono\n+ Connection pooling simple con aiosqlite\n+ SQLite queries (? placeholders)\n+ SELECT last_insert_rowid() (SQLite)\n```"}`

## Feature Description
Implement a complete async DatabaseManager class using aiosqlite for SQLite operations with full CRUD capabilities for all 5 orchestrator schema tables. The manager will provide a zero-configuration, single-connection interface for orchestrator state persistence following the "zero configuration, maximum portability" philosophy from TAC-14 v2 SQLite approach.

## User Story
As a TAC Bootstrap developer
I want to persist orchestrator agent state to SQLite with async operations
So that orchestrator workflows can track execution history, costs, and logs with zero setup requirements while maintaining upgrade path to PostgreSQL

## Problem Statement
The orchestrator system (Class 3) requires persistent state management to track:
- Agent definitions (orchestrator_agents table)
- Runtime agent instances (agents table)
- Prompt/response interactions (prompts table)
- Agent execution logs (agent_logs table)
- System-wide events (system_logs table)

PostgreSQL would require complex setup and configuration, creating barriers to adoption. SQLite provides zero-configuration persistence while maintaining all required features.

## Solution Statement
Create `adw_database.py` module with:
1. **DatabaseManager class** - Async context manager with single connection (WAL mode enabled)
2. **Full CRUD operations** - Create, Read, Update, Delete for all 5 tables
3. **Schema initialization** - Auto-create tables from schema_orchestrator.sql on first connect()
4. **Explicit transactions** - Manual commit() after write operations for control
5. **Structured error handling** - Clear error messages with fail-fast behavior
6. **Configurable paths** - Default to 'orchestrator.db' with env var override support

## Relevant Files
Files necessary for implementing the feature:

### Existing Files (Dependencies)
- `adws/schema/schema_orchestrator.sql` - SQLite schema with 5 tables, triggers, and indexes
- `adws/adw_modules/orch_database_models.py` - Pydantic models for all 5 tables with UUID/datetime validation
- `ai_docs/doc/plan_tasks_Tac_14_v2_SQLITE.md` - SQLite implementation requirements and philosophy
- `ai_docs/doc/ddd_lite.md` - DDD patterns for domain separation and repository interfaces

### New Files
- `adws/adw_modules/adw_database.py` - DatabaseManager class with full CRUD operations (BASE)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2` - Jinja2 template (TEMPLATES)

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Register template for adw_database.py.j2

## Implementation Plan

### Phase 1: Foundation
1. Add PEP 723 dependency metadata for aiosqlite>=0.19.0
2. Create DatabaseManager class skeleton with __init__, connect(), close() methods
3. Implement async context manager protocol (__aenter__, __aexit__)
4. Add WAL mode configuration for better concurrency

### Phase 2: Core Implementation
1. Implement _init_schema() - Auto-execute schema_orchestrator.sql on connect()
2. Implement CRUD for orchestrator_agents table (5 methods)
3. Implement CRUD for agents table (5 methods)
4. Implement CRUD for prompts table (5 methods)
5. Implement CRUD for agent_logs table (4 methods - append-only)
6. Implement CRUD for system_logs table (4 methods - append-only)
7. Add error handling with contextual error messages

### Phase 3: Integration
1. Create Jinja2 template (.j2) with configurable db_path variable
2. Register template in scaffold_service.py
3. Add docstrings with usage examples and architecture notes
4. Document zero-configuration philosophy in module docstring

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create DatabaseManager skeleton with connection lifecycle
- Create `adws/adw_modules/adw_database.py` with PEP 723 header
- Add module docstring explaining SQLite approach, zero-configuration philosophy
- Implement `__init__(self, db_path: str = "orchestrator.db")`
- Implement async `connect()` - open connection, set row_factory, enable WAL mode
- Implement async `close()` - close connection safely
- Implement `__aenter__` and `__aexit__` for context manager protocol
- Add type hints: `self.conn: Optional[aiosqlite.Connection] = None`

### Task 2: Implement schema initialization
- Implement `_init_schema()` method
- Open and read `adws/schema/schema_orchestrator.sql` file
- Execute schema using `conn.executescript()`
- Add error handling for missing schema file with clear error message
- Add error handling for invalid SQL with descriptive context
- Call `_init_schema()` at end of `connect()` method

### Task 3: Implement CRUD for orchestrator_agents table
- Implement `create_orchestrator_agent(name: str, description: Optional[str], agent_type: str, ...) -> str`
  - Generate UUID, create ISO timestamp
  - INSERT with ? placeholders
  - Explicit commit()
  - Return agent_id
- Implement `get_orchestrator_agent(agent_id: str) -> Optional[dict]`
  - SELECT with WHERE id = ?
  - Convert Row to dict if found
- Implement `list_orchestrator_agents() -> List[dict]`
  - SELECT * ORDER BY created_at DESC
  - Convert all Rows to dicts
- Implement `update_orchestrator_agent(agent_id: str, **kwargs) -> bool`
  - Dynamic UPDATE based on kwargs
  - Update updated_at timestamp
  - Return True if rowcount > 0
- Implement `delete_orchestrator_agent(agent_id: str) -> bool`
  - DELETE WHERE id = ?
  - Return True if rowcount > 0

### Task 4: Implement CRUD for agents table
- Implement `create_agent(orchestrator_agent_id: str, session_id: str, ...) -> str`
- Implement `get_agent(agent_id: str) -> Optional[dict]`
- Implement `list_agents(session_id: Optional[str] = None) -> List[dict]`
  - Optional filtering by session_id
- Implement `update_agent(agent_id: str, **kwargs) -> bool`
  - Support status updates, completion timestamps, cost tracking
- Implement `delete_agent(agent_id: str) -> bool`

### Task 5: Implement CRUD for prompts table
- Implement `create_prompt(agent_id: str, prompt_type: str, prompt_text: str, ...) -> str`
- Implement `get_prompt(prompt_id: str) -> Optional[dict]`
- Implement `list_prompts(agent_id: str) -> List[dict]`
  - Filter by agent_id
- Implement `update_prompt(prompt_id: str, **kwargs) -> bool`
  - Support response updates, token counts, cost, completion timestamp
- Implement `delete_prompt(prompt_id: str) -> bool`

### Task 6: Implement CRUD for agent_logs table
- Implement `create_agent_log(agent_id: str, log_level: str, log_type: str, message: str, details: Optional[dict]) -> int`
  - Serialize details dict to JSON TEXT
  - Use AUTOINCREMENT id (INTEGER PRIMARY KEY)
  - Return last_rowid
- Implement `get_agent_logs(agent_id: str, log_level: Optional[str] = None) -> List[dict]`
  - Filter by agent_id, optional log_level filter
  - Deserialize JSON details
- Implement `list_recent_agent_logs(limit: int = 100) -> List[dict]`
  - ORDER BY created_at DESC LIMIT ?
- Note: No update/delete methods (append-only log)

### Task 7: Implement CRUD for system_logs table
- Implement `create_system_log(log_level: str, component: str, message: str, details: Optional[dict]) -> int`
  - Serialize details dict to JSON TEXT
  - Return last_rowid
- Implement `get_system_logs(log_level: Optional[str] = None, component: Optional[str] = None) -> List[dict]`
  - Optional filters for log_level and component
- Implement `list_recent_system_logs(limit: int = 100) -> List[dict]`
  - ORDER BY created_at DESC LIMIT ?
- Note: No update/delete methods (append-only log)

### Task 8: Add comprehensive error handling and logging
- Wrap all database operations in try/except blocks
- Catch `aiosqlite.Error` and re-raise with context (table name, operation type)
- Add DEBUG-level logging for successful operations with query context
- Add ERROR-level logging for failures with full error details
- Document error scenarios in module docstring

### Task 9: Create Jinja2 template and register
- Copy `adws/adw_modules/adw_database.py` to `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_database.py.j2`
- Add Jinja2 variable for db_path: `{{ config.database.path | default('orchestrator.db') }}`
- Update `scaffold_service.py`:
  - Import template registration utilities
  - Add `adw_database.py.j2` to template list
  - Configure rendering with database config variables
- Ensure template preserves PEP 723 dependency header

### Task 10: Add documentation and usage examples
- Add comprehensive module docstring with:
  - Architecture overview (async context manager, single connection, WAL mode)
  - Zero-configuration philosophy explanation
  - Full usage example with context manager
  - Database lifecycle management notes
  - Upgrade path to PostgreSQL mention
- Add method docstrings with parameter descriptions and return types
- Document SQLite-specific patterns (? placeholders, TEXT storage for UUID/datetime)

### Task 11: Validation - Run all validation commands
- Execute validation commands to ensure zero regressions

## Testing Strategy

### Unit Tests
Create `adws/adw_tests/test_adw_database.py` with:
- `test_database_manager_context_manager()` - Verify async context manager protocol
- `test_schema_initialization()` - Verify tables created from schema_orchestrator.sql
- `test_orchestrator_agents_crud()` - Full CRUD cycle for orchestrator_agents
- `test_agents_crud()` - Full CRUD cycle for agents table
- `test_prompts_crud()` - Full CRUD cycle for prompts table
- `test_agent_logs_append_only()` - Verify append-only behavior, JSON serialization
- `test_system_logs_append_only()` - Verify append-only behavior
- `test_concurrent_reads()` - Verify WAL mode allows concurrent reads
- `test_missing_schema_file()` - Verify clear error on missing schema
- `test_invalid_sql()` - Verify error handling for schema execution failures
- `test_uuid_validation()` - Verify UUID format validation via Pydantic models
- `test_json_metadata_serialization()` - Verify dict → JSON TEXT → dict roundtrip

### Edge Cases
- Empty database (first run) - schema auto-creates
- Missing schema file - raises clear error with path
- Invalid UUID format - caught by Pydantic validation
- Invalid SQL in schema - caught with descriptive error
- Null/optional fields - handled correctly (description, timestamps, metadata)
- Large JSON metadata - serialization works for agent/system logs
- Concurrent reads - multiple connections can read simultaneously (WAL mode)
- Connection already closed - graceful handling in __aexit__

## Acceptance Criteria
1. DatabaseManager implements async context manager protocol (__aenter__, __aexit__)
2. Single connection per instance, WAL mode enabled for concurrency
3. Schema auto-initializes from schema_orchestrator.sql on first connect()
4. Full CRUD operations for all 5 tables with correct SQLite syntax (? placeholders)
5. UUID stored/retrieved as TEXT, datetime as ISO 8601 TEXT
6. JSON metadata serialized to TEXT for logs, deserialized on retrieval
7. Explicit commit() after all write operations (no autocommit)
8. Clear error messages on failures (missing schema, invalid SQL, connection errors)
9. DEBUG logging for operations, ERROR logging for failures
10. Jinja2 template created with {{ config.database.path }} variable
11. Template registered in scaffold_service.py
12. Zero external dependencies beyond aiosqlite (no ORM, no migrations)
13. All unit tests passing with >90% coverage
14. Module docstring documents zero-configuration philosophy and upgrade path

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### SQLite-Specific Implementation Details
- **UUIDs as TEXT**: Stored as "550e8400-e29b-41d4-a716-446655440000" (validated by Pydantic)
- **Timestamps as TEXT**: Stored as "2026-02-04T10:30:00.000000" (ISO 8601 format)
- **JSON as TEXT**: Dicts serialized with `json.dumps()`, deserialized with `json.loads()`
- **WAL mode**: Enabled via `PRAGMA journal_mode=WAL` for concurrent reads
- **Row factory**: `aiosqlite.Row` for dict-like access to query results
- **Placeholders**: Use `?` (not `$1`, `$2` like PostgreSQL)
- **Last insert ID**: Use `cursor.lastrowid` (not `RETURNING id`)

### Zero-Configuration Philosophy
- No external database server required
- No connection strings or credentials
- No migrations (schema auto-creates)
- Single .db file in project root (git-ignored)
- Works immediately after `uv run` with no setup

### Abstraction Layer
- DatabaseManager provides same interface regardless of backend
- Future PostgreSQL support: swap implementation, keep interface
- Repository pattern (DDD) - domain layer never knows about SQLite
- Pydantic models bridge domain ↔ infrastructure layers

### Future Considerations (v0.9.0+)
- Connection pooling for multi-process scenarios
- Database migrations with alembic if schema evolves
- PostgreSQL adapter following same interface
- Cleanup policies for old logs (VACUUM, retention)
- Performance monitoring and query optimization
