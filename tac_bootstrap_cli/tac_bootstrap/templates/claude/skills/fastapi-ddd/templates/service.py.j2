"""Use Case / Service Layer - DDD Lite

This template provides the use case pattern from Celes DDD Lite.
In DDD Lite, use cases live in the application layer and orchestrate
domain operations via the repository.

Usage:
    Replace 'EntityName' with your actual entity name.
    Place in: src/{capability}/application/use_cases/entity_name_use_case.py

Conventions:
    - Use cases orchestrate: validate input -> call repository -> return result
    - One use case class per aggregate (or split into command/query handlers)
    - CQRS decision: simple CRUD = use case class, complex domain = separate commands/queries
    - Uses BaseRepository interface (not concrete implementation)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..dtos.entity_name_schemas import EntityNameCreate, EntityNameUpdate

logger = logging.getLogger(__name__)


# ===========================================================================
# Use Case (Application Layer)
# ===========================================================================


class EntityNameUseCase:
    """Use case for EntityName CRUD and lifecycle operations.

    Orchestrates domain operations through the repository.
    Place in: src/{capability}/application/use_cases/entity_name_use_case.py

    Args:
        repository: A BaseRepository implementation for EntityName.
    """

    def __init__(self, repository) -> None:
        self._repository = repository

    # ------------------------------------------------------------------
    # Commands (write operations)
    # ------------------------------------------------------------------

    def create(self, payload: EntityNameCreate) -> object:
        """Create a new EntityName.

        Args:
            payload: Creation DTO with validated fields.

        Returns:
            The created entity (ORM model or domain entity).
        """
        logger.info("Creating EntityName: name=%s", payload.name)

        # Build domain entity from DTO
        from ..domain.aggregates.entity_name import EntityName

        entity = EntityName(
            code=payload.code,
            name=payload.name,
            description=getattr(payload, "description", None),
        )

        result = self._repository.create(entity)
        logger.info("Created EntityName: id=%s", result.id)
        return result

    def update(self, entity_id: int, payload: EntityNameUpdate) -> Optional[object]:
        """Update an existing EntityName (partial update).

        Args:
            entity_id: ID of the entity to update.
            payload: Update DTO with optional fields.

        Returns:
            Updated entity or None if not found.
        """
        logger.info("Updating EntityName: id=%s", entity_id)

        existing = self._repository.get_by_id(entity_id)
        if existing is None:
            return None

        # Apply only provided fields
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(existing, field):
                setattr(existing, field, value)

        result = self._repository.update(entity_id, existing)
        logger.info("Updated EntityName: id=%s", entity_id)
        return result

    def delete(self, entity_id: int) -> bool:
        """Hard delete an EntityName.

        Args:
            entity_id: ID of the entity to delete.

        Returns:
            True if deleted, False if not found.
        """
        logger.info("Deleting EntityName: id=%s", entity_id)
        return self._repository.delete(entity_id)

    # ------------------------------------------------------------------
    # Lifecycle operations (DDD Lite pattern)
    # ------------------------------------------------------------------

    def activate(self, entity_id: int) -> Optional[object]:
        """Activate an EntityName (state -> ACTIVE)."""
        return self._repository.activate(entity_id)

    def deactivate(self, entity_id: int) -> Optional[object]:
        """Deactivate an EntityName (state -> INACTIVE)."""
        return self._repository.deactivate(entity_id)

    def soft_delete(self, entity_id: int) -> Optional[object]:
        """Soft delete an EntityName (state -> DELETED)."""
        return self._repository.soft_delete(entity_id)

    # ------------------------------------------------------------------
    # Queries (read operations)
    # ------------------------------------------------------------------

    def get_by_id(self, entity_id: int) -> Optional[object]:
        """Get a single EntityName by ID."""
        return self._repository.get_by_id(entity_id)

    def get_by_code(self, code: str) -> Optional[object]:
        """Get a single EntityName by business code."""
        return self._repository.get_by_code(code)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[object]:
        """List EntityNames with pagination (excludes DELETED)."""
        return self._repository.get_all(skip=skip, limit=limit)
