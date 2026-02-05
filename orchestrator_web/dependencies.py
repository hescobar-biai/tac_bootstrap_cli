"""FastAPI dependencies for orchestrator web backend."""

from typing import AsyncGenerator
from adws.adw_modules.adw_database import DatabaseManager

# Global db_manager instance
_db_manager: DatabaseManager | None = None


def set_db_manager(db_manager: DatabaseManager) -> None:
    """Set the global database manager instance."""
    global _db_manager
    _db_manager = db_manager


async def get_db_manager() -> AsyncGenerator[DatabaseManager, None]:
    """Get the database manager instance as a FastAPI dependency."""
    if _db_manager is None:
        raise RuntimeError("Database manager not initialized")
    yield _db_manager
