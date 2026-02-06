"""Orchestrator configuration management.

Centralized configuration for the orchestrator backend.
All settings can be overridden via environment variables.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent

# Database (SQLite - zero config)
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "orchestrator.db"))

# Server
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5173"))

# WebSocket
WS_HEARTBEAT_INTERVAL = int(os.getenv("WS_HEARTBEAT_INTERVAL", "30"))
WS_MAX_CONNECTIONS = int(os.getenv("WS_MAX_CONNECTIONS", "50"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", f"http://localhost:{FRONTEND_PORT}").split(",")

# Models
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5-20250929")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", str(BASE_DIR / "logs"))
