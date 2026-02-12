"""Domain Entity - DDD Lite (Screaming Architecture)

This template provides the Entity base class pattern from Celes DDD Lite.
Entities use Pydantic BaseModel (not dataclasses) with EntityState lifecycle.

Usage:
    Replace 'EntityName' with your actual entity name.
    Place in: src/{capability}/domain/aggregates/{entity_name}.py

Conventions:
    - Entities inherit from a Pydantic base Entity class
    - EntityState enum: INACTIVE=0, ACTIVE=1, DELETED=2
    - All entities have: id, code, name, state, created_by, updated_by, timestamps
    - Value objects are frozen dataclasses
    - Aggregate roots enforce invariants
"""

from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# EntityState (shared across all entities)
# ---------------------------------------------------------------------------


class EntityState(IntEnum):
    """Lifecycle states for all entities in DDD Lite."""

    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2


# ---------------------------------------------------------------------------
# Base Entity (inherit from this in all domain entities)
# ---------------------------------------------------------------------------


class Entity(BaseModel):
    """Base Entity class following DDD Lite pattern.

    All domain entities inherit from this class. Provides:
    - Identity (id, code)
    - Lifecycle (state with EntityState enum)
    - Audit fields (created_by, updated_by, timestamps)

    Note: Uses Pydantic BaseModel, not dataclasses.
    Sync SQLAlchemy Session is the default (not async).
    """

    id: Optional[int] = Field(default=None, description="Auto-generated primary key")
    code: Optional[str] = Field(default=None, description="Business-friendly unique code")
    name: str = Field(..., description="Human-readable name")
    state: EntityState = Field(default=EntityState.ACTIVE, description="Entity lifecycle state")
    created_by: Optional[str] = Field(default=None, description="User who created this entity")
    updated_by: Optional[str] = Field(default=None, description="User who last updated this entity")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Value Objects (frozen dataclasses for immutable domain concepts)
# ---------------------------------------------------------------------------

# from dataclasses import dataclass
#
# @dataclass(frozen=True)
# class Money:
#     amount: float
#     currency: str = "USD"


# ---------------------------------------------------------------------------
# Concrete Entity (replace EntityName with your entity)
# ---------------------------------------------------------------------------


class EntityName(Entity):
    """Domain entity for EntityName.

    Inherits id, code, name, state, created_by, updated_by, timestamps
    from Entity base class. Add domain-specific fields below.

    Place in: src/{capability}/domain/aggregates/entity_name.py
    """

    # --- Domain-specific fields ---
    description: Optional[str] = Field(default=None, description="Entity description")

    # Add your domain fields here, for example:
    # tenant_id: str = Field(..., description="Multi-tenant identifier")
    # category: Optional[str] = None
    # quantity: int = Field(default=0, ge=0)

    # --- Business logic methods ---

    def activate(self) -> None:
        """Transition entity to ACTIVE state."""
        if self.state == EntityState.DELETED:
            raise ValueError("Cannot activate a deleted entity")
        self.state = EntityState.ACTIVE

    def deactivate(self) -> None:
        """Transition entity to INACTIVE state."""
        if self.state != EntityState.ACTIVE:
            raise ValueError(f"Can only deactivate active entities, current: {self.state.name}")
        self.state = EntityState.INACTIVE

    def soft_delete(self) -> None:
        """Mark entity as deleted (soft delete)."""
        self.state = EntityState.DELETED
