"""FastAPI backend for orchestrator web UI.

Provides REST API and WebSocket endpoints for managing orchestrator agents,
runtime agents, prompts, and logs with SQLite persistence.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adws.adw_modules.adw_database import DatabaseManager
from orchestrator_web.dependencies import set_db_manager
from orchestrator_web.routers import agents, runtime, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI lifecycle: connect/disconnect DatabaseManager."""
    # Startup: Initialize DatabaseManager
    db_path = os.getenv("DATABASE_PATH", "orchestrator.db")
    db_manager = DatabaseManager(db_path)
    await db_manager.connect()
    set_db_manager(db_manager)

    print(f"✓ DatabaseManager connected to {db_path}")

    yield

    # Shutdown: Close DatabaseManager
    await db_manager.close()
    print("✓ DatabaseManager closed")


app = FastAPI(
    title="Orchestrator Backend",
    description="Backend API for ADW orchestration with SQLite persistence",
    version="0.8.0",
    lifespan=lifespan
)

# Configure CORS for Web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(runtime.router, prefix="/api", tags=["Runtime"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "orchestrator-backend", "version": "0.8.0"}
