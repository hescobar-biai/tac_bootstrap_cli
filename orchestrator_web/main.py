"""Orchestrator Web Backend - FastAPI Application.

Zero-configuration FastAPI server for orchestrating ADW workflows with SQLite.
Provides REST API (CQRS) + WebSocket for real-time agent status updates.
"""

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path for adw_modules import
sys.path.insert(0, str(Path(__file__).parent.parent))

from adw_modules.adw_database import DatabaseManager
import dependencies
from routers import agents, runtime, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager - connects DatabaseManager on startup.
    
    Startup:
        - Initialize DatabaseManager with DATABASE_PATH env var
        - Connect to SQLite (auto-creates schema on first run)
        - Store in global dependencies.db_manager
    
    Shutdown:
        - Close DatabaseManager connection
        - Cleanup resources
    """
    # Startup
    db_path = dependencies.get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[Orchestrator] Connecting to database: {db_path}")
    dependencies.db_manager = DatabaseManager(str(db_path))
    await dependencies.db_manager.connect()
    print("[Orchestrator] Database connected successfully")
    
    yield
    
    # Shutdown
    print("[Orchestrator] Closing database connection")
    await dependencies.db_manager.close()
    print("[Orchestrator] Shutdown complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Orchestrator Web Backend",
    description="FastAPI backend for TAC Bootstrap agent orchestration",
    version="0.8.0",
    lifespan=lifespan,
)

# Configure CORS for Web UI
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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
    return {
        "service": "orchestrator-web",
        "version": "0.8.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Detailed health check with database status."""
    db_manager = dependencies.get_db_manager()
    return {
        "status": "healthy",
        "database": "connected" if db_manager.conn else "disconnected",
        "database_path": str(dependencies.get_database_path())
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("WEBSOCKET_PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
