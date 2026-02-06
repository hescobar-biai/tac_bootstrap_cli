"""FastAPI dependency injection for orchestrator web backend."""

import sys
from pathlib import Path

# Ensure adws directory is in path for adw_modules import
sys.path.insert(0, str(Path(__file__).parent.parent / "adws"))

from adw_modules.adw_database import DatabaseManager
from config import DATABASE_PATH

# Global DatabaseManager instance
db_manager: DatabaseManager | None = None


def get_db_manager() -> DatabaseManager:
    """Get the global DatabaseManager instance.
    
    Raises:
        RuntimeError: If DatabaseManager not initialized (lifespan not started).
    """
    if db_manager is None:
        raise RuntimeError(
            "DatabaseManager not initialized. "
            "Ensure FastAPI lifespan has executed startup."
        )
    return db_manager


def get_database_path() -> Path:
    """Get database path from config.yml (via config module)."""
    return Path(DATABASE_PATH)
