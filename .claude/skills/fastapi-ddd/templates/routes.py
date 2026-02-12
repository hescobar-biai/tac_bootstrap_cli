"""Presentation Layer (API Routes) - DDD Lite

This template provides the FastAPI router pattern from Celes DDD Lite.
Routes are thin: validate input, delegate to use case, format output.

Usage:
    Replace 'EntityName' with your actual entity name.
    Replace 'entity_name' with the snake_case version.
    Replace 'entity-names' with the kebab-case plural for URL paths.
    Place in: src/{capability}/presentation/api/entity_name_router.py

Conventions:
    - Routes live in the presentation layer (not interfaces)
    - Dependency injection via FastAPI Depends()
    - Sync SQLAlchemy session (default for DDD Lite)
    - Standard CRUD + activate/deactivate/soft-delete endpoints
    - Use cases live in application/use_cases/ or application/commands/
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    pass

# ===========================================================================
# Router
# ===========================================================================

router = APIRouter(
    prefix="/entity-names",
    tags=["EntityNames"],
)


# ===========================================================================
# Dependency Injection
# ===========================================================================


def get_db() -> Session:
    """Provide a sync database session.

    Replace with your actual session factory:
        from src.shared.infrastructure.database import SessionLocal
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    """
    raise NotImplementedError("Replace with your actual database session provider")


def get_repository(db: Session = Depends(get_db)):
    """Provide the repository implementation."""
    # from src.{capability}.infrastructure.persistence.entity_name_repository import EntityNameRepositoryImpl
    # return EntityNameRepositoryImpl(db)
    raise NotImplementedError("Replace with your actual repository")


def get_use_case(repository=Depends(get_repository)):
    """Provide the use case / service."""
    # from src.{capability}.application.use_cases.entity_name_use_case import EntityNameUseCase
    # return EntityNameUseCase(repository)
    raise NotImplementedError("Replace with your actual use case")


# ===========================================================================
# CRUD Endpoints
# ===========================================================================


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new EntityName",
)
def create_entity_name(
    payload: "EntityNameCreate",
    use_case=Depends(get_use_case),
):
    """Create a new EntityName via the create use case."""
    try:
        entity = use_case.create(payload)
        return entity
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e


@router.get(
    "/",
    summary="List all EntityNames",
)
def list_entity_names(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    use_case=Depends(get_use_case),
):
    """List EntityNames with pagination."""
    return use_case.get_all(skip=skip, limit=limit)


@router.get(
    "/{entity_id}",
    summary="Get EntityName by ID",
)
def get_entity_name(
    entity_id: int,
    use_case=Depends(get_use_case),
):
    """Get a single EntityName by its ID."""
    entity = use_case.get_by_id(entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )
    return entity


@router.put(
    "/{entity_id}",
    summary="Update EntityName",
)
def update_entity_name(
    entity_id: int,
    payload: "EntityNameUpdate",
    use_case=Depends(get_use_case),
):
    """Update an existing EntityName (partial update)."""
    entity = use_case.update(entity_id, payload)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )
    return entity


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete EntityName",
)
def delete_entity_name(
    entity_id: int,
    use_case=Depends(get_use_case),
):
    """Hard delete an EntityName."""
    deleted = use_case.delete(entity_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )


# ===========================================================================
# Lifecycle Endpoints (DDD Lite pattern)
# ===========================================================================


@router.post(
    "/{entity_id}/activate",
    summary="Activate EntityName",
)
def activate_entity_name(
    entity_id: int,
    use_case=Depends(get_use_case),
):
    """Transition EntityName to ACTIVE state."""
    entity = use_case.activate(entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )
    return entity


@router.post(
    "/{entity_id}/deactivate",
    summary="Deactivate EntityName",
)
def deactivate_entity_name(
    entity_id: int,
    use_case=Depends(get_use_case),
):
    """Transition EntityName to INACTIVE state."""
    entity = use_case.deactivate(entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )
    return entity


@router.delete(
    "/{entity_id}/soft",
    summary="Soft delete EntityName",
)
def soft_delete_entity_name(
    entity_id: int,
    use_case=Depends(get_use_case),
):
    """Mark EntityName as DELETED (soft delete)."""
    entity = use_case.soft_delete(entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityName with id {entity_id} not found",
        )
    return entity


# ===========================================================================
# Router Registration
# ===========================================================================
#
# In your main.py:
#   from src.{capability}.presentation.api.entity_name_router import router
#   app.include_router(router, prefix="/api/v1")
#
# Endpoints:
#   POST   /api/v1/entity-names/
#   GET    /api/v1/entity-names/
#   GET    /api/v1/entity-names/{entity_id}
#   PUT    /api/v1/entity-names/{entity_id}
#   DELETE /api/v1/entity-names/{entity_id}
#   POST   /api/v1/entity-names/{entity_id}/activate
#   POST   /api/v1/entity-names/{entity_id}/deactivate
#   DELETE /api/v1/entity-names/{entity_id}/soft
