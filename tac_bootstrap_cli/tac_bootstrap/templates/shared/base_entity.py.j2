"""
IDK: domain-entity, base-model, audit-trail

Module: base_entity

Responsibility:
- Provide foundation for all domain entities
- Enforce common entity structure and behavior
- Support audit trail and versioning patterns

Key Components:
- EntityState: State enumeration (inactive, active, deleted)
- Entity: Base class with identity, audit, and lifecycle management

Invariants:
- All entities have unique id (UUID)
- All entities track creation and modification metadata
- State transitions follow 0 (inactive) -> 1 (active) -> 2 (deleted)

Related Docs:
- docs/shared/domain/base-entity.md
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from uuid import uuid4
from datetime import datetime, UTC
from typing import Any
from enum import IntEnum


class EntityState(IntEnum):
    """
    IDK: state-machine, entity-lifecycle, soft-delete

    Responsibility:
    - Define valid entity state values
    - Enable state-based filtering and transitions

    Invariants:
    - Only three states allowed: INACTIVE (0), ACTIVE (1), DELETED (2)
    - State values are immutable integers

    State:
    - 0: INACTIVE - Entity is deactivated but can be reactivated
    - 1: ACTIVE - Entity is active and operational
    - 2: DELETED - Entity is soft-deleted (archived)

    Related Docs:
    - docs/shared/domain/entity-state.md
    """
    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2


class Entity(BaseModel):
    """
    IDK: domain-entity, aggregate-root, audit-trail

    Responsibility:
    - Serve as base class for all domain entities
    - Provide identity, audit trail, and lifecycle management
    - Enable multi-tenancy and versioning support

    Invariants:
    - id is unique and immutable (UUID v4)
    - code is required and serves as business identifier
    - created_at/updated_at always set to UTC
    - state must be 0, 1, or 2 (INACTIVE, ACTIVE, DELETED)
    - version increments on each update

    Collaborators:
    - Pydantic BaseModel: validation and serialization
    - EntityState: state enumeration

    Failure Modes:
    - ValidationError: invalid field values
    - ValueError: constraint violations

    Related Docs:
    - docs/shared/domain/base-entity.md
    """

    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        use_enum_values=True,
        json_schema_extra={
            "description": "Base entity with audit and metadata fields"
        }
    )

    # Core Identity Fields
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier (UUID v4)",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )

    code: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Business code/reference (e.g., SKU, employee ID)",
        examples=["PROD-001", "EMP-2024-001"]
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable name",
        examples=["Product Name", "John Doe"]
    )

    # Business Metadata
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Detailed description"
    )

    type: str | None = Field(
        default=None,
        max_length=50,
        description="Entity type discriminator",
        examples=["product", "user", "supplier"]
    )

    # Audit Trail - Creation
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of creation"
    )

    created_by: str | None = Field(
        default=None,
        max_length=255,
        description="User ID or username who created this entity"
    )

    # Audit Trail - Modification
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of last update"
    )

    updated_by: str | None = Field(
        default=None,
        max_length=255,
        description="User ID or username who last updated this entity"
    )

    # State Management
    state: int = Field(
        default=EntityState.ACTIVE,
        ge=0,
        le=2,
        description="Entity state: 0=inactive, 1=active, 2=deleted",
        examples=[0, 1, 2]
    )

    status: str | None = Field(
        default=None,
        max_length=50,
        description="Business status (domain-specific)",
        examples=["pending", "approved", "completed", "draft"]
    )

    version: int = Field(
        default=1,
        ge=1,
        description="Version number for optimistic locking"
    )

    # Multi-tenancy & Organization
    organization_id: str | None = Field(
        default=None,
        max_length=100,
        description="Organization/tenant identifier"
    )

    project_id: str | None = Field(
        default=None,
        max_length=100,
        description="Project identifier"
    )

    owner: str | None = Field(
        default=None,
        max_length=255,
        description="Owner user ID (for access control)"
    )

    @field_validator('updated_at', mode='before')
    @classmethod
    def sync_updated_at(cls, v: Any, info) -> datetime:
        """
        IDK: audit-trail, timestamp-sync, validation

        Responsibility:
        - Ensure updated_at reflects current time on modification

        Invariants:
        - Always returns UTC datetime
        - Overrides any manually provided value

        Inputs:
        - v (Any): provided value (ignored)
        - info: validator context

        Outputs:
        - datetime: current UTC timestamp

        Related Docs:
        - docs/shared/domain/audit-trail.md
        """
        return datetime.now(UTC)

    def mark_updated(self, user_id: str | None = None) -> None:
        """
        IDK: audit-trail, versioning, mutation

        Responsibility:
        - Update audit trail on entity modification
        - Increment version for optimistic locking

        Invariants:
        - updated_at set to current UTC time
        - version always incremented
        - updated_by set only if user_id provided

        Inputs:
        - user_id (str | None): user making the update

        Outputs:
        - None (mutates self)

        Related Docs:
        - docs/shared/domain/audit-trail.md
        """
        self.updated_at = datetime.now(UTC)
        if user_id:
            self.updated_by = user_id
        self.version += 1

    def deactivate(self, user_id: str | None = None) -> None:
        """
        IDK: state-transition, lifecycle, deactivation

        Responsibility:
        - Transition entity to INACTIVE state
        - Update audit trail

        Invariants:
        - State set to 0 (INACTIVE)
        - Audit trail updated

        Inputs:
        - user_id (str | None): user performing deactivation

        Outputs:
        - None (mutates self)

        Related Docs:
        - docs/shared/domain/entity-lifecycle.md
        """
        self.state = EntityState.INACTIVE
        self.mark_updated(user_id)

    def activate(self, user_id: str | None = None) -> None:
        """
        IDK: state-transition, lifecycle, activation

        Responsibility:
        - Transition entity to ACTIVE state
        - Update audit trail

        Invariants:
        - State set to 1 (ACTIVE)
        - Audit trail updated

        Inputs:
        - user_id (str | None): user performing activation

        Outputs:
        - None (mutates self)

        Related Docs:
        - docs/shared/domain/entity-lifecycle.md
        """
        self.state = EntityState.ACTIVE
        self.mark_updated(user_id)

    def delete(self, user_id: str | None = None) -> None:
        """
        IDK: soft-delete, state-transition, lifecycle

        Responsibility:
        - Soft delete entity (state = DELETED)
        - Update audit trail
        - Preserve data for recovery

        Invariants:
        - State set to 2 (DELETED)
        - Data remains in database
        - Audit trail updated

        Inputs:
        - user_id (str | None): user performing deletion

        Outputs:
        - None (mutates self)

        Related Docs:
        - docs/shared/domain/soft-delete.md
        """
        self.state = EntityState.DELETED
        self.mark_updated(user_id)

    def is_active(self) -> bool:
        """
        IDK: state-check, query-method, predicate

        Responsibility:
        - Check if entity is in ACTIVE state

        Invariants:
        - Returns true only if state == 1

        Inputs:
        - None

        Outputs:
        - bool: True if active, False otherwise

        Related Docs:
        - docs/shared/domain/entity-lifecycle.md
        """
        return self.state == EntityState.ACTIVE

    def is_deleted(self) -> bool:
        """
        IDK: state-check, query-method, predicate

        Responsibility:
        - Check if entity is soft-deleted

        Invariants:
        - Returns true only if state == 2

        Inputs:
        - None

        Outputs:
        - bool: True if deleted, False otherwise

        Related Docs:
        - docs/shared/domain/soft-delete.md
        """
        return self.state == EntityState.DELETED

    def is_inactive(self) -> bool:
        """
        IDK: state-check, query-method, predicate

        Responsibility:
        - Check if entity is in INACTIVE state

        Invariants:
        - Returns true only if state == 0

        Inputs:
        - None

        Outputs:
        - bool: True if inactive, False otherwise

        Related Docs:
        - docs/shared/domain/entity-lifecycle.md
        """
        return self.state == EntityState.INACTIVE

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, code={self.code}, name={self.name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id}', code='{self.code}', name='{self.name}', type='{self.type}')"
