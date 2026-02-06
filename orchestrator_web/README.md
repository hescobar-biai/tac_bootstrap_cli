# Orchestrator Web Backend

FastAPI backend for TAC Bootstrap agent orchestration with SQLite persistence and real-time WebSocket updates.

## Architecture

```
orchestrator_web/
├── main.py            # FastAPI app with lifespan manager
├── dependencies.py    # Dependency injection (DatabaseManager)
├── .env.sample        # Environment variables template
└── routers/
    ├── agents.py      # CQRS endpoints for orchestrator_agents
    ├── runtime.py     # Runtime agents, prompts, logs
    └── websocket.py   # Real-time agent status updates
```

## Quick Start

```bash
# 1. Install dependencies
pip install fastapi uvicorn[standard] aiosqlite pydantic

# 2. Initialize database
./scripts/setup_database.sh

# 3. Start server
cd orchestrator_web
uvicorn main:app --reload --port 8000
```

Or using the Makefile:
```bash
make install-backend
make setup-db
make dev-backend
```

## API Endpoints

### Health
| Method | Path      | Description              |
|--------|-----------|--------------------------|
| GET    | /         | Basic health check       |
| GET    | /health   | Detailed health + DB     |

### Orchestrator Agents (CQRS)
| Method | Path                   | Description             |
|--------|------------------------|-------------------------|
| GET    | /api/agents            | List all agents         |
| POST   | /api/agents            | Create new agent        |
| GET    | /api/agents/{id}       | Get agent by ID         |
| PUT    | /api/agents/{id}       | Update agent            |
| DELETE | /api/agents/{id}       | Delete agent            |

### Runtime
| Method | Path                           | Description                    |
|--------|--------------------------------|--------------------------------|
| GET    | /api/runtime/agents            | List runtime agent instances   |
| POST   | /api/runtime/agents            | Create runtime agent           |
| GET    | /api/runtime/agents/{id}       | Get runtime agent by ID        |
| GET    | /api/runtime/prompts           | List prompts (filter by agent) |
| GET    | /api/runtime/logs              | Recent logs (filter by level)  |
| GET    | /api/runtime/logs/agent/{id}   | Agent-specific logs            |

### WebSocket
| Protocol  | Path                  | Description                    |
|-----------|-----------------------|--------------------------------|
| WebSocket | /ws/agent-status      | Real-time agent status updates |

## Database

Uses SQLite with zero-config auto-initialization. Schema at `adws/schema/schema_orchestrator.sql`.

**Tables:** orchestrator_agents, agents, prompts, agent_logs, system_logs

**Features:**
- WAL mode for concurrent reads
- Foreign key constraints
- Auto-updated timestamps via triggers
- 6 performance indexes

## Environment Variables

| Variable        | Default                                      | Description              |
|-----------------|----------------------------------------------|--------------------------|
| DATABASE_PATH   | ./data/orchestrator.db                       | SQLite database path     |
| WEBSOCKET_PORT  | 8000                                         | Server port              |
| CORS_ORIGINS    | http://localhost:5173,http://127.0.0.1:5173  | Allowed CORS origins     |

## Interactive API Docs

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
