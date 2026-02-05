---
doc_type: feature
adw_id: Tac_14_Task_12
date: 2026-02-05
idk:
  - fastapi
  - sqlite
  - websocket
  - cqrs
  - orchestrator
  - rest-api
  - lifespan-manager
tags:
  - feature
  - backend
  - orchestration
related_code:
  - orchestrator_web/main.py
  - orchestrator_web/routers/agents.py
  - orchestrator_web/routers/runtime.py
  - orchestrator_web/routers/websocket.py
  - orchestrator_web/dependencies.py
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
---

# Orchestrator Backend with SQLite

**ADW ID:** Tac_14_Task_12
**Date:** 2026-02-05
**Specification:** specs/issue-633-adw-feature_Tac_14_Task_12-sdlc_planner-orchestrator-backend-sqlite.md

## Overview

FastAPI backend for orchestrating ADW workflows with SQLite persistence. Provides REST API (CQRS pattern) and WebSocket endpoints for managing orchestrator agents, runtime instances, prompts, and logs with zero-configuration database setup.

## What Was Built

- **FastAPI Application** with lifespan manager for DatabaseManager initialization
- **CQRS REST Endpoints** for orchestrator agents (GET/POST/PUT/DELETE)
- **Runtime Endpoints** for agent instances, prompts, and logs
- **WebSocket Server** for real-time agent status updates
- **Template System** with Jinja2 templates for CLI code generation
- **Scaffold Service Integration** to generate orchestrator_web in new projects

## Technical Implementation

### Files Created

#### Base Implementation (orchestrator_web/)
- `orchestrator_web/main.py`: FastAPI app with lifespan manager, CORS configuration, health endpoints
- `orchestrator_web/dependencies.py`: Dependency injection for DatabaseManager singleton
- `orchestrator_web/routers/agents.py`: CQRS endpoints for orchestrator_agents CRUD
- `orchestrator_web/routers/runtime.py`: Endpoints for runtime agents, prompts, logs with filtering
- `orchestrator_web/routers/websocket.py`: WebSocket handler broadcasting agent status every 2s
- `orchestrator_web/.env.sample`: Environment variables (DATABASE_PATH, WEBSOCKET_PORT, CORS_ORIGINS)

#### CLI Templates (tac_bootstrap_cli/)
- `tac_bootstrap/templates/orchestrator_web/*.j2`: Jinja2 templates mirroring base implementation
- `tac_bootstrap/application/scaffold_service.py`: Added `_add_orchestrator_web()` method (lines 1035-1102)
- `tac_bootstrap/domain/models.py`: Added TokenOptimizationConfig for ADW workflow token limits

### Key Changes

- **Lifespan Manager**: FastAPI @asynccontextmanager connects DatabaseManager on startup, closes on shutdown
- **CQRS Pattern**: Separate command (POST/PUT/DELETE) and query (GET) endpoints for agents
- **Dependency Injection**: Global db_manager singleton accessed via get_db_manager() FastAPI dependency
- **WebSocket Polling**: Simple 2-second polling loop detecting agent state changes, broadcasting JSON updates
- **Zero Config**: DATABASE_PATH auto-creates SQLite file, schema auto-loads via DatabaseManager.connect()

## How to Use

### 1. Start Backend Server

```bash
cd orchestrator_web
uv run uvicorn main:app --reload --port 8000
```

Backend starts on http://localhost:8000 with API docs at http://localhost:8000/docs

### 2. Create Orchestrator Agent

```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "feature-planner",
    "description": "Plans feature implementation",
    "agent_type": "skill",
    "capabilities": "planning,analysis",
    "default_model": "claude-sonnet-3.5"
  }'
```

### 3. List Agents

```bash
curl http://localhost:8000/api/agents
```

### 4. Connect WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/agent-status');
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  console.log('Agent update:', msg.data);
};
```

### 5. Generate in New Project

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap new my-project --language python --framework fastapi
```

Orchestrator backend automatically generated in `my-project/orchestrator_web/`

## Configuration

Environment variables (copy `.env.sample` to `.env`):

- `DATABASE_PATH`: SQLite database file path (default: `./data/orchestrator.db`)
- `WEBSOCKET_PORT`: Backend server port (default: `8000`)
- `WEB_UI_PORT`: Frontend port for CORS (default: `5173`)
- `CORS_ORIGINS`: Comma-separated allowed origins (default: `http://localhost:5173,http://127.0.0.1:5173`)

## Testing

### Smoke Test Backend

```bash
cd orchestrator_web
uv run uvicorn main:app --port 8000
```

Verify http://localhost:8000/health returns `{"status": "healthy", "database": "connected"}`

### Run Unit Tests

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

### Lint Check

```bash
cd tac_bootstrap_cli
uv run ruff check .
```

### Type Check

```bash
cd tac_bootstrap_cli
uv run mypy tac_bootstrap/
```

## Notes

- Uses existing DatabaseManager from `adws/adw_modules/adw_database.py` (no new DB layer)
- Schema auto-loads from `adws/schema/schema_orchestrator.sql` on first connect
- SQLite stores UUIDs as TEXT, metadata as JSON strings
- WebSocket uses simple polling (2s interval) - sufficient for v0.8.0, can optimize later with triggers
- CORS pre-configured for Vite dev server (port 5173)
- Templates follow dual-strategy pattern: base implementation + Jinja2 templates for generation
- Future enhancements: Pydantic request/response schemas, authentication/authorization, WebSocket optimization
