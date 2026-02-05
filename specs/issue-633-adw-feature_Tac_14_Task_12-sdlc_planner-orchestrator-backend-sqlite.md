# Feature: Orchestrator Backend con SQLite

## Metadata
issue_number: `633`
adw_id: `feature_Tac_14_Task_12`
issue_json: `{"number": 633, "title": "Implementar Orchestrator Backend con SQLite (BASE + TEMPLATES)", "body": "..."}`

## Feature Description
Implementar backend FastAPI para orquestación de agentes usando SQLite via DatabaseManager existente. Backend expone endpoints REST/CQRS para CRUD de orchestrator_agents, runtime agents, prompts, y logs, más WebSocket para actualizaciones en tiempo real.

## User Story
As a TAC Bootstrap user
I want a FastAPI backend that manages orchestrator agents with SQLite persistence
So that I can orchestrate ADW workflows via web UI with zero database configuration

## Problem Statement
TAC-14 requiere backend de orquestación con persistencia. Necesitamos FastAPI app que use DatabaseManager (ya implementado en adw_database.py) para servir datos a Web UI. Sin backend, no hay forma de crear/listar orchestrator agents, monitorear ejecuciones, o recibir actualizaciones en tiempo real.

## Solution Statement
Crear `orchestrator_web/` FastAPI app con:
- Lifecycle manager conectando DatabaseManager en startup
- Endpoints CQRS: `/api/agents` (GET/POST), `/api/agents/{id}` (GET/PUT/DELETE)
- WebSocket `/ws/agent-status` para streaming de estado
- CORS habilitado para frontend local (port 5173)
- Environment vars: DATABASE_PATH, WEBSOCKET_PORT, WEB_UI_PORT
- Templates Jinja2 para generación de proyectos

## Relevant Files

### Existing
- `adws/adw_modules/adw_database.py` - DatabaseManager con schema auto-load
- `adws/schema/schema_orchestrator.sql` - SQLite schema (5 tablas)
- `ai_docs/doc/plan_tasks_Tac_14_v2_SQLITE.md` - Task 12 spec con código FastAPI

### New Files
- `orchestrator_web/main.py` - FastAPI app con lifespan manager
- `orchestrator_web/routers/agents.py` - Endpoints CQRS para orchestrator_agents
- `orchestrator_web/routers/runtime.py` - Endpoints para runtime agents/prompts
- `orchestrator_web/routers/websocket.py` - WebSocket handler
- `orchestrator_web/.env.sample` - Environment variables template
- `orchestrator_web/dependencies.py` - FastAPI dependencies
- Templates equivalentes en `tac_bootstrap_cli/tac_bootstrap/templates/orchestrator_web/`

## Implementation Plan

### Phase 1: Foundation
- Crear estructura `orchestrator_web/` con `__init__.py`
- Setup FastAPI app con DatabaseManager lifespan
- Configurar CORS para Web UI
- Crear `.env.sample` con DATABASE_PATH, WEBSOCKET_PORT, WEB_UI_PORT

### Phase 2: Core Implementation
- Implementar `/api/agents` endpoints (CQRS pattern)
- Implementar `/api/runtime` endpoints para agents/prompts
- Implementar WebSocket handler para real-time status
- Crear dependency injection para db_manager

### Phase 3: Integration
- Registrar routers en main.py
- Crear templates Jinja2 en CLI
- Actualizar scaffold_service.py para renderizar orchestrator_web
- Add `uvicorn` dependency to pyproject.toml

## Step by Step Tasks

### Task 1: Crear estructura orchestrator_web
- `mkdir orchestrator_web orchestrator_web/routers`
- Crear `orchestrator_web/__init__.py` vacío
- Crear `orchestrator_web/.env.sample` con DATABASE_PATH, WEBSOCKET_PORT, WEB_UI_PORT
- Crear `orchestrator_web/dependencies.py` con get_db_manager()

### Task 2: Implementar main.py con lifespan
- Crear `orchestrator_web/main.py` con FastAPI app
- Implementar @asynccontextmanager lifespan: connect DatabaseManager en startup, close en shutdown
- Configurar CORS: allow_origins=["http://localhost:5173"], allow_methods=["*"]
- Global db_manager instance

### Task 3: Implementar router agents CQRS
- Crear `orchestrator_web/routers/agents.py`
- GET `/api/agents` → db_manager.list_orchestrator_agents()
- POST `/api/agents` → db_manager.create_orchestrator_agent(name, description, type, capabilities, model)
- GET `/api/agents/{id}` → db_manager.get_orchestrator_agent(id)
- PUT `/api/agents/{id}` → db_manager.update_orchestrator_agent()
- DELETE `/api/agents/{id}` → db_manager.delete_orchestrator_agent()

### Task 4: Implementar router runtime
- Crear `orchestrator_web/routers/runtime.py`
- GET `/api/runtime/agents` → db_manager.list_agents()
- POST `/api/runtime/agents` → db_manager.create_agent(orchestrator_agent_id, session_id)
- GET `/api/runtime/agents/{id}` → db_manager.get_agent(id)
- GET `/api/runtime/prompts` → db_manager.list_prompts()
- GET `/api/runtime/logs` → db_manager.get_recent_logs(limit=100)

### Task 5: Implementar WebSocket
- Crear `orchestrator_web/routers/websocket.py`
- WebSocket endpoint `/ws/agent-status`
- Accept connection, broadcast agent status changes (poll db every 2s)
- JSON format: {"type": "agent_update", "data": {...}}

### Task 6: Registrar routers en main.py
- app.include_router(agents.router, prefix="/api", tags=["Agents"])
- app.include_router(runtime.router, prefix="/api", tags=["Runtime"])
- app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])

### Task 7: Crear templates CLI
- Copiar orchestrator_web/ a tac_bootstrap_cli/tac_bootstrap/templates/
- Convertir main.py a main.py.j2 (sin variables por ahora)
- Copiar routers/ sin cambios (.py → .py.j2)
- .env.sample → .env.sample (sin extension .j2)

### Task 8: Actualizar scaffold_service.py
- Agregar método render_orchestrator_web()
- Copiar templates orchestrator_web/ con estructura completa
- Registrar en ScaffoldService.render_all()

### Task 9: Add uvicorn dependency
- `cd tac_bootstrap_cli && uv add uvicorn[standard]`
- Verificar pyproject.toml dependencies

### Task 10: Ejecutar validación
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd orchestrator_web && uv run uvicorn main:app --reload` (smoke test)

## Testing Strategy

### Unit Tests
- `tests/test_orchestrator_main.py`: Verificar lifespan connect/close DatabaseManager
- `tests/test_agents_router.py`: Mock db_manager, test CRUD endpoints retornan 200/201/404
- `tests/test_websocket.py`: Connect WebSocket, recibir JSON {"type": "agent_update"}

### Edge Cases
- DatabaseManager.connect() falla → FastAPI no inicia, log error
- GET /api/agents/{id} con UUID inválido → 404
- WebSocket disconnect durante broadcast → catch exception, continue
- DATABASE_PATH no existe → DatabaseManager crea archivo .db automáticamente

## Acceptance Criteria
- FastAPI app inicia con `uvicorn main:app` sin errores
- DatabaseManager.connect() ejecuta en lifespan startup
- GET /api/agents retorna lista de orchestrator_agents (puede ser [])
- POST /api/agents crea agent y retorna 201 + UUID
- WebSocket /ws/agent-status acepta conexión y envía JSON
- CORS permite requests desde http://localhost:5173
- Templates en tac_bootstrap_cli/tac_bootstrap/templates/orchestrator_web/ creados
- scaffold_service.py registra render_orchestrator_web()

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd orchestrator_web && uv run uvicorn main:app --reload --port 8000` - Backend smoke test

## Notes
- DatabaseManager ya implementa todos los métodos CRUD necesarios
- Schema auto-load en connect() - no requiere migración manual
- SQLite usa TEXT para UUIDs, JSON serializado en metadata fields
- WebSocket polling simple (cada 2s) - suficiente para v0.8.0
- Futuro: Agregar Pydantic schemas para request/response validation
- Futuro: Implementar authentication/authorization
- Dependency: uvicorn[standard] requerido para FastAPI server
