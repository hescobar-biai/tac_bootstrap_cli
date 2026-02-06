"""Orchestrator configuration management.

Loads configuration from config.yml (orchestrator section).
Environment variables can override any value.

Priority: env var > config.yml > hardcoded default
"""

import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
BACKEND_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Load config.yml
# ---------------------------------------------------------------------------

_config_yml: dict = {}

try:
    import yaml

    _config_path = BASE_DIR / "config.yml"
    if _config_path.exists():
        with open(_config_path, "r") as f:
            _config_yml = yaml.safe_load(f) or {}
except ImportError:
    print("[config] Warning: pyyaml not installed, using defaults", file=sys.stderr)
except Exception as e:
    print(f"[config] Warning: Could not load config.yml: {e}", file=sys.stderr)

_orch: dict = _config_yml.get("orchestrator", {})

# ---------------------------------------------------------------------------
# Configuration values: env var > config.yml > hardcoded default
# ---------------------------------------------------------------------------

# Database (SQLite - zero config)
_db_url = _orch.get("database_url", "sqlite:///data/orchestrator.db")
_db_path_from_yml = _db_url.replace("sqlite:///", "") if _db_url.startswith("sqlite:///") else "data/orchestrator.db"
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / _db_path_from_yml))

# Server
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", str(_orch.get("websocket_port", 8000))))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", str(_orch.get("frontend_port", 5173))))

# API URLs
API_BASE_URL = os.getenv("API_BASE_URL", _orch.get("api_base_url", "http://localhost:8000"))
WS_BASE_URL = os.getenv("WS_BASE_URL", _orch.get("ws_base_url", "ws://localhost:8000"))

# WebSocket
WS_HEARTBEAT_INTERVAL = int(os.getenv("WS_HEARTBEAT_INTERVAL", "30"))
WS_MAX_CONNECTIONS = int(os.getenv("WS_MAX_CONNECTIONS", "50"))
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", str(_orch.get("polling_interval", 5000))))

# CORS - auto-generate from frontend port
_default_cors = (
    f"http://localhost:{FRONTEND_PORT},"
    f"http://127.0.0.1:{FRONTEND_PORT},"
    f"http://localhost:5175,"
    f"http://127.0.0.1:5175"
)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", _default_cors).split(",")

# Models
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5-20250929")

# Logging
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    _config_yml.get("agentic", {}).get("logging", {}).get("level", "INFO"),
)
LOG_DIR = os.getenv("LOG_DIR", str(BASE_DIR / "logs"))

# Orchestrator enabled flag
ENABLED = _orch.get("enabled", False)
