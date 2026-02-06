# Start Orchestrator

Launch the Orchestrator 3 Stream backend and frontend services.

## Usage

```
/start-orchestrator [--session SESSION_ID] [--cwd WORKING_DIR]
```

## What it does

1. Starts the FastAPI backend (port 8000) with SQLite persistence
2. Starts the Vue 3 frontend dev server (port 5173)
3. Opens the dashboard in the default browser

## Prerequisites

- Python 3.10+ with uvicorn installed
- Node.js 18+ with npm
- SQLite database initialized (`make orch-setup-db`)

## Quick Start

### Using Makefile (recommended)

```bash
# First time setup
make orch-install          # Install backend dependencies
make orch-install-frontend # Install frontend dependencies
make orch-setup-db         # Initialize SQLite database

# Start services
make orch-dev              # Backend (port 8000, hot reload)
make orch-dev-frontend     # Frontend (port 5173) - separate terminal
```

### Manual Start

```bash
# Backend
cd orchestrator_web
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd apps/orchestrator_3_stream/frontend
npm run dev
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| http://localhost:8000 | Backend health check |
| http://localhost:8000/docs | Swagger API documentation |
| http://localhost:8000/redoc | ReDoc API documentation |
| http://localhost:5173 | Frontend dashboard |
| ws://localhost:8000/ws/agent-status | WebSocket real-time updates |

## Architecture

```
User Browser (5173) → Vue 3 Frontend → FastAPI Backend (8000) → SQLite DB
                                      ↕ WebSocket (real-time agent status)
```

## Database

- **Type**: SQLite 3.35+ (WAL mode)
- **Location**: `orchestrator.db` (project root)
- **Tables**: 7 (orchestrator_agents, agents, prompts, agent_logs, system_logs, orchestrator_chat, ai_developer_workflows)
- **Schema**: `adws/schema/schema_orchestrator.sql`

## Troubleshooting

- **Port in use**: Check with `lsof -i :8000` or `lsof -i :5173`
- **DB not found**: Run `make orch-setup-db` to initialize
- **Import errors**: Ensure you're running from the project root
- **CORS issues**: Backend allows localhost origins by default
