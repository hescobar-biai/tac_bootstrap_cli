# Feature: Implementar WebSockets module (BASE + TEMPLATES)

## Metadata
issue_number: `632`
adw_id: `feature_Tac_14_Task_11`
issue_json: `{"number": 632, "title": "Implementar WebSockets module (BASE + TEMPLATES)", "body": "file: ddd_lite.md\nfile: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md\n\n- **Descripción**:\nCrear adw_websockets.py para comunicación real-time en BASE y templates.\n\n**Pasos técnicos**:\n\n**BASE**:\n1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_websockets.py`\n2. Implementar WebSocket connection manager\n3. Implementar broadcast de agent events\n4. Implementar connection pooling\n5. Implementar heartbeat/ping-pong\n6. Agregar PEP 723 dependency: websockets>=12.0\n7. Integrar con adw_logging.py\n\n**TEMPLATES**:\n8. Copiar a template .j2\n9. Agregar variable {{ config.websocket_port }}\n10. Registrar en scaffold_service.py\n\n**Criterios de aceptación**:\n- WebSocket server implementado\n- Connection management robusto\n- Event broadcasting funcional\n- Template creado con variables\n\n**Rutas impactadas**:\n\n**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):\n```\nadws/adw_modules/adw_websockets.py  [CREAR]\n```\n\n**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):\n```\nadws/adw_modules/adw_websockets.py.j2  [CREAR]\n```\n\n**CLI**:\n```\napplication/scaffold_service.py  [MODIFICAR]\n```\n\n**Metadata**:\n- Categoría: WebSockets\n- Prioridad: Alta\n- Estimación: 3h\n- Dependencias: Tarea 9\n\n**Keywords**: websockets, real-time, event-streaming, connection-pooling, class-3\n\n**ADW Metadata**:\n- Tipo: `/feature`\n- Workflow: `/adw_sdlc_zte_iso`\n- ID: `/adw_id: feature_Tac_14_Task_11`"}`

## Feature Description
Implement a standalone async WebSocket server module (`adw_websockets.py`) for real-time communication between ADW orchestrator workflows and monitoring clients. The server broadcasts agent lifecycle events (started, completed, errors), prompt executions, and system events to connected WebSocket clients for live monitoring dashboards.

This is Task 11 of the TAC-14 implementation plan, enabling Class 3 (Orchestrator) real-time observability. The module integrates with the existing SQLite-backed logging system (Task 9) to provide event streaming capabilities.

## User Story
As an ADW orchestrator workflow developer
I want to broadcast real-time agent events over WebSockets
So that monitoring dashboards can display live agent activity, prompt executions, and system status without polling

## Problem Statement
The current TAC Bootstrap SQLite-backed orchestrator (Tasks 6-9) stores agent events in the database, but there's no real-time notification mechanism for monitoring clients. Polling the database for updates creates unnecessary load and introduces latency.

For effective orchestrator monitoring, we need:
1. Push-based real-time event delivery to multiple connected clients
2. Robust connection management that handles client disconnects gracefully
3. Heartbeat mechanism to detect dead connections
4. Event broadcasting that matches the adw_logging.py schema for consistency
5. Localhost-only binding with optional token authentication for security

## Solution Statement
Implement a pure async WebSocket server using the `websockets>=12.0` library that:
- Runs as a standalone server controlled by ADW orchestrator workflows (start/stop functions)
- Maintains an in-memory connection registry (100 max connections, 60s idle timeout)
- Broadcasts events that match the adw_logging.py schema (agent_started, agent_completed, prompt_sent, etc.)
- Implements 30s ping/pong keepalive with 3-strike disconnect policy
- Binds to localhost (127.0.0.1) with optional connection token for minimal auth
- Gracefully removes failed connections from the pool without crashing

The solution provides a Jinja2 template with `{{ config.websocket_port }}` variable for project generation.

## Relevant Files
Files necessary for implementing the feature:

### Existing Files (for reference)
- `adws/adw_modules/adw_database.py` - SQLite database manager with async operations (Task 8)
  - Provides database connection pattern to reference
  - Uses `aiosqlite>=0.19.0` for async operations
  - Implements clean context manager pattern

- `adws/adw_modules/orch_database_models.py` - Pydantic models for database (Task 7)
  - Defines AgentLog, SystemLog models that WebSocket events should match
  - Shows log_type enum values: "step_start", "step_end", "event"
  - Defines log_level values: "info", "warning", "error"

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registration
  - Contains `_add_adw_modules()` method (around line 500-600)
  - Pattern for registering new module templates
  - Shows how to handle .j2 templates with variables

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model
  - May need to add `websocket_port` field to ProjectConfig
  - Current config structure to understand

### New Files
- `adws/adw_modules/adw_websockets.py` - Core WebSocket server implementation (BASE)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_websockets.py.j2` - Jinja2 template

## Implementation Plan

### Phase 1: Foundation
**Check for source file and create core WebSocket module structure**

1. Check if source file exists at `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_websockets.py`
   - If accessible, use as reference for implementation patterns
   - If not accessible, implement from scratch using requirements

2. Create `adws/adw_modules/adw_websockets.py` with:
   - PEP 723 dependency header: `# dependencies = ["websockets>=12.0"]`
   - Module docstring documenting: purpose, architecture, usage example, SQLite integration
   - Import statements: `asyncio`, `websockets`, `json`, `datetime`, `typing`, `dataclasses`

3. Define event schema dataclass:
   ```python
   @dataclass
   class WebSocketEvent:
       event_type: str  # "agent_started", "agent_completed", "prompt_sent", etc.
       agent_id: str
       message: str
       metadata: dict
       timestamp: str  # ISO 8601
   ```

### Phase 2: Core Implementation
**Implement connection manager and WebSocket server**

4. Implement `ConnectionManager` class with:
   - `connections: set[websockets.WebSocketServerProtocol]` - Active connections registry
   - `MAX_CONNECTIONS = 100` - Connection limit
   - `IDLE_TIMEOUT = 60` - Seconds before timeout
   - `async def register(websocket)` - Add connection, enforce max
   - `async def unregister(websocket)` - Remove connection
   - `async def broadcast(event: WebSocketEvent)` - Send to all, remove dead connections
   - `async def keepalive(websocket)` - 30s ping, 10s pong timeout, 3-strike disconnect

5. Implement server functions:
   - `async def start_server(host: str = "127.0.0.1", port: int = 8765, token: str | None = None)`
     - Creates ConnectionManager instance
     - Starts websockets.serve() with handler
     - Returns server task for orchestrator control
   - `async def stop_server(server_task)` - Graceful shutdown
   - `async def _handle_client(websocket, manager, token)` - Connection handler with auth check

6. Implement event emission:
   - `async def broadcast_agent_event(manager: ConnectionManager, agent_id: str, event_type: str, message: str, metadata: dict = None)`
     - Creates WebSocketEvent from parameters
     - Serializes to JSON
     - Calls manager.broadcast()
     - Logs failures to stderr (never crashes)

### Phase 3: Integration
**Integrate with existing systems and create template**

7. Add integration helpers:
   - `def map_log_to_event(log: dict) -> WebSocketEvent` - Converts adw_logging schema to WebSocket event
   - Document in module docstring how to use with adw_database.py queries

8. Create Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_websockets.py.j2`:
   - Copy entire BASE implementation
   - Replace hardcoded port `8765` with `{{ config.websocket_port }}`
   - Add template comment at top: `{# WebSocket Server Module - TAC-14 Task 11 #}`
   - Preserve all PEP 723 headers and docstrings

9. Register template in `scaffold_service.py`:
   - Locate `_add_adw_modules()` method (around line 500-600)
   - Add entry for `adw_websockets.py.j2` template
   - Follow existing pattern from `adw_database.py` registration
   - Ensure template variables are passed correctly

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Check source file and create module structure
- Check if `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_websockets.py` exists and is readable
- If accessible, read it for reference patterns
- Create `adws/adw_modules/adw_websockets.py` with PEP 723 header, imports, and module docstring
- Define `WebSocketEvent` dataclass matching adw_logging.py schema

### Task 2: Implement ConnectionManager class
- Create `ConnectionManager` class with connection registry (set)
- Implement `register()`, `unregister()`, `broadcast()` methods
- Implement `keepalive()` with 30s ping, 10s pong timeout, 3-strike policy
- Add connection limit enforcement (100 max)
- Handle failed broadcasts by removing dead connections

### Task 3: Implement server control functions
- Create `start_server()` function returning server task
- Create `stop_server()` function for graceful shutdown
- Create `_handle_client()` function with optional token auth
- Bind to localhost (127.0.0.1) only for security
- Add error handling and logging to stderr

### Task 4: Implement event broadcasting functions
- Create `broadcast_agent_event()` helper function
- Add `map_log_to_event()` to convert adw_logging schema
- Document integration pattern in module docstring
- Ensure errors never crash (log to stderr instead)

### Task 5: Create Jinja2 template
- Create template directory structure if needed
- Copy BASE implementation to `.j2` template
- Replace hardcoded port with `{{ config.websocket_port }}` variable
- Add template header comment
- Verify all functionality preserved

### Task 6: Register template in scaffold_service.py
- Read existing `_add_adw_modules()` method to understand pattern
- Add `adw_websockets.py.j2` template entry
- Pass config variables correctly
- Test template rendering logic

### Task 7: Validation
- Run validation commands (see below)
- Verify no import errors
- Check PEP 723 dependency syntax
- Ensure template renders correctly with sample config

## Testing Strategy

### Unit Tests
**Note**: Unit tests would be added in Task 15 (Test Suites). For this task, focus on manual validation.

Manual validation tests:
1. Import test: `python -c "from adws.adw_modules import adw_websockets"`
2. Connection manager: Create manager, register 3 mock connections, broadcast event
3. Server lifecycle: Start server on port 9999, connect client, send event, stop server
4. Keepalive: Connect client, wait 35 seconds, verify ping/pong messages
5. Max connections: Try to connect 101 clients, verify 101st is rejected
6. Template rendering: Run scaffold_service with test config, verify generated file has correct port

### Edge Cases
1. **Port already in use**: Server start should fail gracefully with clear error
2. **Client disconnects mid-broadcast**: Dead connection removed without crashing
3. **Invalid token**: Client connection rejected if token doesn't match
4. **Empty connections set**: Broadcast should succeed silently (no clients)
5. **Event serialization failure**: Log error to stderr, don't crash server
6. **Very large metadata dict**: Ensure JSON serialization handles large payloads
7. **Concurrent broadcasts**: Multiple agents broadcasting simultaneously should work
8. **Source file not found**: Implementation should succeed from scratch using requirements

## Acceptance Criteria
- [ ] `adw_websockets.py` created in BASE with PEP 723 header
- [ ] WebSocket server implements localhost-only binding (127.0.0.1)
- [ ] ConnectionManager maintains max 100 connections with 60s timeout
- [ ] Keepalive implements 30s ping, 10s pong timeout, 3-strike disconnect
- [ ] Event broadcasting matches adw_logging.py schema (log_type, log_level)
- [ ] Failed broadcasts remove dead connections without crashing
- [ ] `start_server()` and `stop_server()` functions for orchestrator control
- [ ] Optional token authentication in connection query params
- [ ] Template `.j2` created with `{{ config.websocket_port }}` variable
- [ ] Template registered in `scaffold_service.py` `_add_adw_modules()` method
- [ ] Module docstring documents usage, architecture, SQLite integration
- [ ] Import test passes: `python -c "from adws.adw_modules import adw_websockets"`
- [ ] No syntax errors, all validation commands pass

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `python -c "from adws.adw_modules import adw_websockets"` - Import test
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios (if tests exist)
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Implementation Notes
- **Zero-config philosophy**: Server works out-of-box, optional token for hardening
- **In-memory only**: No state persistence, clients auto-reconnect on restart
- **Separation of concerns**: adw_logging.py handles persistence, adw_websockets.py handles distribution
- **Pub-sub pattern**: Logging is source of truth, WebSocket is notification channel
- **Graceful degradation**: Broadcast failures clean up connections, never crash workflows
- **Standard keepalive**: 30s ping interval is industry standard, balances detection vs chattiness

### SQLite v2 Context (from plan_tasks_Tac_14_v2_SQLITE.md)
- This task integrates with SQLite-backed orchestrator (not PostgreSQL)
- Database schema: 5 tables (orchestrator_agents, agents, prompts, agent_logs, system_logs)
- Event types: "step_start", "step_end", "event" (from agent_logs.log_type)
- Log levels: "info", "warning", "error" (from system_logs.log_level)
- Use `aiosqlite>=0.19.0` pattern from adw_database.py for async operations

### DDD Lite Alignment
- **Domain layer**: WebSocketEvent dataclass (pure data)
- **Infrastructure layer**: ConnectionManager, server functions (external I/O)
- **No framework coupling**: Pure websockets library, no FastAPI/Starlette dependency
- **Clean abstraction**: Orchestrator workflows control lifecycle (start/stop)

### Future Enhancements (not in scope)
- Persistent connections across server restarts (requires state persistence)
- Per-client subscriptions (filter events by agent_id, log_type)
- Backpressure handling for slow clients (requires buffering)
- SSL/TLS for production deployments (currently localhost-only)
- Migration to ASGI WebSocket when FastAPI orchestrator API is added (Task 12)

### Dependencies on Other Tasks
- **Task 9 (adw_logging.py)**: Event schema compatibility required
  - Must match log_type enum values
  - Must match log_level values
  - Must handle metadata dict structure
- **Task 8 (adw_database.py)**: Connection pattern reference
  - Context manager pattern
  - Async operation patterns
  - Error handling approach
- **Task 12 (Orchestrator Backend)**: Will integrate WebSocket endpoint
  - FastAPI will expose WebSocket route
  - This module provides underlying server

### Path to PostgreSQL Migration (v0.9.0+)
When migrating to PostgreSQL in v0.9.0:
- WebSocket module unchanged (no database dependency)
- Only adw_database.py changes (swap aiosqlite for asyncpg)
- Event schema remains consistent across backends
- Connection management logic identical

### References
- WebSocket RFC 6455: https://tools.ietf.org/html/rfc6455
- Python websockets library: https://websockets.readthedocs.io/
- TAC-14 plan: plan_tasks_Tac_14_v2_SQLITE.md (Task 11)
- SQLite schema: adws/schema/schema_orchestrator.sql (Task 6)
- Logging module: adws/adw_modules/adw_logging.py (Task 9)
