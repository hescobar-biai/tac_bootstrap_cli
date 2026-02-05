# Feature: Implementar Database Operations con sqlite3/aiosqlite

## Metadata
issue_number: `629`
adw_id: `feature_Tac_14_Task_8`
issue_json: `{"number": 629, "title": "Implementar Database Operations con sqlite3/aiosqlite (BASE + TEMPLATES)", "body": "file: ddd_lite.md \nfile: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_8`\n\n**Cambios principales**:\n```diff\n\n+ aiosqlite para SQLite asíncrono\n+ Connection pooling simple con aiosqlite\n+ SQLite queries (? placeholders)\n+ SELECT last_insert_rowid() (SQLite)\n```"}`

## Feature Description
Implementar DatabaseManager como módulo standalone de infraestructura (`adws/adw_database.py`) con aiosqlite para operaciones SQLite asíncronas. Este módulo proporciona CRUD operations para las tablas del orchestrator (orchestrator_agents y agents) siguiendo los principios de DDD Lite Infrastructure layer.

La implementación utiliza SQLite como base de datos zero-configuration para TAC-14 v0.8.0, permitiendo desarrollo local sin barreras de entrada. El módulo soporta tanto context manager pattern como explicit connect/close para flexibilidad en diferentes workflows.

## User Story
As a TAC Bootstrap orchestrator workflow developer
I want to persist orchestrator agent state and execution logs to a SQLite database
So that I can track multi-agent orchestration history, retrieve agent states, and enable the orchestrator web application

## Problem Statement
TAC-14 Class 3 (Orchestrator Agent) requiere persistencia de estado para:
- Tracking de orchestrator agents (definiciones de agentes especializados)
- Runtime agent instances (ejecuciones concretas con session_id)
- Execution logs y metrics para observabilidad
- Real-time updates via WebSocket (requiere estado compartido)

El plan original TAC-14 v1 proponía PostgreSQL, pero presenta barreras de entrada (instalación, configuración, credenciales). TAC-14 v2 adopta SQLite first approach para maximizar adopción mientras mantiene todas las features de Class 3.

## Solution Statement
Implementar DatabaseManager en `adws/adw_database.py` con:

1. **Async SQLite operations** usando aiosqlite para compatibilidad con orchestrator workflows asíncronos
2. **Single connection pattern** con soporte para context manager (`async with`) y explicit connect/close
3. **CRUD operations** para orchestrator_agents y agents tables (foundation para prompts, logs en tareas futuras)
4. **Schema initialization** automática desde `adws/schema/schema_orchestrator.sqlite`
5. **Error propagation** limpia (dejar que aiosqlite exceptions se propaguen para debugging)
6. **Zero configuration** - database en `data/orchestrator.db` (configurable via ORCHESTRATOR_DB_PATH)

Arquitectura DDD Lite Infrastructure layer:
- DatabaseManager como cross-cutting concern para orchestrator workflows
- Standalone module reutilizable desde adw_sdlc_zte_iso.py y otros ADWs
- Defer connection pooling y migrations (YAGNI - suficiente para v0.8.0)

## Relevant Files
Archivos necesarios para implementar la feature:

### Existing Files
- `adws/schema/schema_orchestrator.sqlite` - Schema SQL (creado en Tarea 6)
  - Define 5 tablas: orchestrator_agents, agents, prompts, agent_logs, system_logs
  - Tipos SQLite nativos (TEXT para UUIDs, INTEGER, REAL)
- `adws/adw_modules/orch_database_models.py` - Pydantic models (creado en Tarea 7)
  - OrchestratorAgent, Agent, Prompt, AgentLog, SystemLog
  - Validators para UUID/datetime serialization
- `ai_docs/doc/ddd_lite.md` - DDD Lite architecture guide
  - Infrastructure layer principles
  - Repository patterns y base classes
- `plan_tasks_Tac_14_v2_SQLITE.md` - SQLite adaptation specifications
  - Tarea 8 detailed requirements
  - CRUD code examples

### New Files
- `adws/adw_database.py` - DatabaseManager implementation (BASE)
- `adws/adw_modules/adw_database.py.j2` - Jinja2 template (TEMPLATES)
- `data/.gitignore` - Exclude orchestrator.db from version control
- `tests/test_database.py` - Unit tests para DatabaseManager (defer to Tarea 15)

## Implementation Plan

### Phase 1: Foundation (Database File Setup)
1. Create `data/` directory for runtime database storage
2. Add `data/.gitignore` to exclude `*.db` files
3. Set ORCHESTRATOR_DB_PATH environment variable support

**Rationale**: Separate runtime data from code. Prevent accidental commits of database files. Allow test/prod separation via env vars.

### Phase 2: Core Implementation (DatabaseManager Class)
1. Create `adws/adw_database.py` with PEP 723 dependency header
2. Implement `DatabaseManager.__init__(db_path)` with default to `data/orchestrator.db`
3. Implement `async connect()` - initialize aiosqlite connection with Row factory
4. Implement `async close()` - cleanup connection
5. Implement `async _init_schema()` - read and execute schema_orchestrator.sqlite
6. Implement context manager protocol (`__aenter__`, `__aexit__`)

**Rationale**: Foundation para async database operations. Row factory enables dict-like access. Context manager ensures cleanup.

### Phase 3: CRUD Operations (orchestrator_agents)
1. Implement `async create_orchestrator_agent(name, description)` → agent_id
   - Generate UUID, current timestamp
   - INSERT with ? placeholders
   - Commit and return agent_id
2. Implement `async get_orchestrator_agent(agent_id)` → Optional[dict]
   - SELECT with WHERE id = ?
   - Return dict(row) or None
3. Implement `async list_orchestrator_agents()` → List[dict]
   - SELECT all, ORDER BY created_at DESC
   - Return list of dicts

**Rationale**: Establish CRUD pattern for remaining tables. orchestrator_agents es core entity del orchestrator.

### Phase 4: CRUD Operations (agents table)
1. Implement `async create_agent(orchestrator_agent_id, session_id)` → agent_id
   - Generate UUID, timestamp
   - INSERT with FOREIGN KEY to orchestrator_agents
   - Commit and return agent_id
2. Implement `async get_agent(agent_id)` → Optional[dict]
3. Implement `async list_agents_by_session(session_id)` → List[dict]
4. Implement `async update_agent_status(agent_id, status, timestamps)`

**Rationale**: agents table tracks runtime instances. Critical para orchestrator workflow execution tracking.

### Phase 5: Integration (Environment & Error Handling)
1. Read ORCHESTRATOR_DB_PATH from environment (default: data/orchestrator.db)
2. Create data/ directory if missing (pathlib.Path.mkdir(parents=True, exist_ok=True))
3. Add docstrings with error propagation documentation
4. Validate schema file exists before executescript (raise FileNotFoundError if missing)

**Rationale**: Production-ready configuration. Clear error messages for missing schema (fail fast). Document SQLite concurrency limitations.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Setup data directory and .gitignore
- Create `data/` directory in project root
- Create `data/.gitignore` with content: `*.db`
- Verify directory exists and .gitignore prevents tracking

### Task 2: Implement DatabaseManager foundation
- Create `adws/adw_database.py`
- Add PEP 723 header: `# /// script\n# dependencies = ["aiosqlite>=0.19.0"]\n# ///`
- Implement `DatabaseManager.__init__(self, db_path: str = "data/orchestrator.db")`
- Add imports: `import aiosqlite, json, uuid, os, pathlib`
- Add type hints: `from typing import Optional, List`
- Add datetime: `from datetime import datetime`

### Task 3: Implement connection lifecycle
- Implement `async def connect(self):`
  - Read `ORCHESTRATOR_DB_PATH` env var (fallback to constructor db_path)
  - Create parent directory if missing: `pathlib.Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)`
  - Connect: `self.conn = await aiosqlite.connect(self.db_path)`
  - Set row factory: `self.conn.row_factory = aiosqlite.Row`
  - Call `await self._init_schema()`
- Implement `async def close(self):`
  - Check `if self.conn:` then `await self.conn.close()`
- Implement `async def _init_schema(self):`
  - Validate schema file: `schema_path = "adws/schema/schema_orchestrator.sqlite"`
  - Raise `FileNotFoundError` if not exists with clear message
  - Read schema: `with open(schema_path, "r") as f: schema = f.read()`
  - Execute: `await self.conn.executescript(schema)`
  - Commit: `await self.conn.commit()`

### Task 4: Implement context manager protocol
- Implement `async def __aenter__(self):`
  - Call `await self.connect()`
  - Return `self`
- Implement `async def __aexit__(self, exc_type, exc_val, exc_tb):`
  - Call `await self.close()`
  - Return `None` (propagate exceptions)

### Task 5: Implement orchestrator_agents CRUD
- Implement `async def create_orchestrator_agent(self, name: str, description: Optional[str] = None) -> str:`
  - Generate: `agent_id = str(uuid.uuid4())`
  - Timestamp: `now = datetime.utcnow().isoformat()`
  - Execute INSERT with ? placeholders (5 params)
  - Commit
  - Return agent_id
- Implement `async def get_orchestrator_agent(self, agent_id: str) -> Optional[dict]:`
  - Use `async with self.conn.execute(SELECT_SQL, (agent_id,)) as cursor:`
  - Fetch: `row = await cursor.fetchone()`
  - Return `dict(row) if row else None`
- Implement `async def list_orchestrator_agents(self) -> List[dict]:`
  - SELECT all ORDER BY created_at DESC
  - Return `[dict(row) for row in rows]`

### Task 6: Implement agents table CRUD
- Implement `async def create_agent(self, orchestrator_agent_id: str, session_id: str) -> str:`
  - Generate UUID and timestamp
  - INSERT with FOREIGN KEY
  - Commit and return agent_id
- Implement `async def get_agent(self, agent_id: str) -> Optional[dict]:`
  - SELECT with WHERE
  - Return dict or None
- Implement `async def list_agents_by_session(self, session_id: str) -> List[dict]:`
  - SELECT WHERE session_id = ?
  - Order by created_at
- Implement `async def update_agent_status(self, agent_id: str, status: str, started_at: Optional[str] = None, completed_at: Optional[str] = None) -> bool:`
  - UPDATE status, timestamps WHERE id = ?
  - Commit
  - Return True if updated (check cursor.rowcount)

### Task 7: Add comprehensive docstrings
- Add module-level docstring explaining DatabaseManager purpose
- Add class docstring with usage examples (both patterns)
- Add method docstrings with:
  - Args with types
  - Returns with types
  - Raises (FileNotFoundError for missing schema, propagated aiosqlite errors)
- Document SQLite concurrency limitations (single-instance-per-process)

### Task 8: Manual smoke test
- Create test script `test_manual_db.py`:
  ```python
  import asyncio
  from adws.adw_database import DatabaseManager

  async def test():
      async with DatabaseManager() as db:
          # Create orchestrator agent
          agent_id = await db.create_orchestrator_agent("test-agent", "Test description")
          print(f"Created: {agent_id}")

          # Retrieve
          agent = await db.get_orchestrator_agent(agent_id)
          print(f"Retrieved: {agent}")

          # List all
          agents = await db.list_orchestrator_agents()
          print(f"Total: {len(agents)}")

  asyncio.run(test())
  ```
- Run: `uv run python test_manual_db.py`
- Verify: Check `data/orchestrator.db` exists
- Verify: Inspect with `sqlite3 data/orchestrator.db ".schema"`
- Clean up test script after verification

### Task 9: Validation Commands
- Execute all validation commands:
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` (if tests exist)
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` (if configured)
  - Manual smoke test from Task 8

## Testing Strategy

### Unit Tests (Deferred to Tarea 15)
Will be implemented in `adws/adw_tests/test_database.py`:
- Test connection lifecycle (connect/close)
- Test context manager pattern
- Test create_orchestrator_agent returns UUID
- Test get_orchestrator_agent with valid/invalid IDs
- Test list_orchestrator_agents ordering
- Test create_agent with FOREIGN KEY constraint
- Test update_agent_status
- Test missing schema file raises FileNotFoundError
- Test concurrent access (document limitations)

### Manual Integration Tests (This Task)
- Smoke test creating and retrieving agents
- Verify database file creation in data/
- Verify schema initialization
- Verify .gitignore prevents tracking

### Edge Cases
- Missing schema file → Clear FileNotFoundError
- Invalid UUID format in queries → Propagate aiosqlite error
- FOREIGN KEY violation (invalid orchestrator_agent_id) → Propagate aiosqlite IntegrityError
- Multiple DatabaseManager instances → Document single-instance recommendation
- Connection already closed → aiosqlite error (document)

## Acceptance Criteria
- [x] `adws/adw_database.py` exists with DatabaseManager class
- [x] PEP 723 dependency header includes aiosqlite>=0.19.0
- [x] `data/` directory exists with .gitignore excluding *.db
- [x] DatabaseManager supports both context manager and explicit connect/close patterns
- [x] CRUD operations implemented for orchestrator_agents (create, get, list)
- [x] CRUD operations implemented for agents (create, get, list, update_status)
- [x] Schema initialization from `adws/schema/schema_orchestrator.sqlite`
- [x] Environment variable ORCHESTRATOR_DB_PATH supported
- [x] Missing schema file raises clear FileNotFoundError
- [x] Comprehensive docstrings with usage examples
- [x] Manual smoke test passes (create, retrieve, list)
- [x] Database file created in data/orchestrator.db
- [x] Ruff linting passes with zero violations

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `uv run python test_manual_db.py` - Manual smoke test
- `sqlite3 data/orchestrator.db ".schema"` - Verify schema
- `sqlite3 data/orchestrator.db "SELECT * FROM orchestrator_agents;"` - Verify data
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `uv run python -c "from adws.adw_database import DatabaseManager; print('Import OK')"` - Import test

## Notes

### SQLite vs PostgreSQL Trade-offs
**Advantages of SQLite for v0.8.0:**
- Zero installation/configuration
- Portable single-file database
- Perfect for local development and testing
- Sufficient for orchestrator use case (single workflow process)

**Limitations (documented):**
- Single writer (sequential writes)
- Not suitable for high-concurrency production (>10 concurrent users)
- No built-in replication

**Migration path to PostgreSQL (v0.9.0):**
- Can use pgloader for SQLite → PostgreSQL migration
- DatabaseManager interface remains stable
- Only connection logic changes (asyncpg instead of aiosqlite)

### Deferred Features (YAGNI)
- **Connection pooling**: Single connection sufficient for orchestrator workflows. Add if concurrent access patterns emerge.
- **Migrations**: Schema evolving rapidly in TAC-14 development. Use alembic in v0.9.0 when stable.
- **Prompts/logs CRUD**: Defer to Tarea 9 (Database Logging). Establish pattern with orchestrator_agents first.

### Dependencies
- **PEP 723 inline dependency**: `aiosqlite>=0.19.0` (async SQLite driver)
- **Schema dependency**: Requires `adws/schema/schema_orchestrator.sqlite` from Tarea 6
- **Models dependency**: Uses `adws/adw_modules/orch_database_models.py` from Tarea 7 (for type hints in future)

### Future Enhancements
- Add `async def transaction()` context manager for explicit transaction boundaries
- Add `async def get_agents_by_orchestrator(orchestrator_agent_id)` helper query
- Add pagination support for `list_*` methods (offset, limit)
- Add soft delete pattern (state column) if needed
- Add connection retry logic with exponential backoff

### Architecture Notes
Following DDD Lite Infrastructure layer:
- DatabaseManager handles technical concern (database access)
- No business logic in this module (pure CRUD)
- Orchestrator ADWs (Application layer) will use DatabaseManager for persistence
- Future: Domain layer entities can map to/from database dicts via Pydantic models
