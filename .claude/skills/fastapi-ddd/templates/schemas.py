"""Pydantic Schemas (DTOs) - DDD Lite

This template provides the schema pattern from Celes DDD Lite.
Uses BaseCreate, BaseUpdate, BaseResponse, and PaginatedResponse.

Usage:
    Replace 'EntityName' with your actual entity name.
    Place in: src/{capability}/application/dtos/entity_name_schemas.py

Conventions:
    - BaseCreate: fields for creation (no id, no timestamps)
    - BaseUpdate: all fields optional for partial updates
    - BaseResponse: includes id, state, timestamps
    - PaginatedResponse: wraps list + total for paginated endpoints
    - Uses Pydantic v2 with model_config
"""

from __future__ import annotations

from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


# ===========================================================================
# Base Schema Classes (shared across all entities)
# ===========================================================================


class BaseCreate(BaseModel):
    """Base schema for entity creation requests.

    Subclass this and add entity-specific fields.
    Does NOT include id, state, or timestamps (server-generated).
    """

    code: Optional[str] = Field(default=None, description="Business-friendly unique code")
    name: str = Field(..., min_length=1, max_length=255, description="Entity name")


class BaseUpdate(BaseModel):
    """Base schema for entity update requests.

    All fields optional to support partial updates.
    """

    code: Optional[str] = Field(default=None, description="Updated code")
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="Updated name")


class BaseResponse(BaseModel):
    """Base schema for entity responses.

    Includes all server-generated fields.
    """

    id: int = Field(..., description="Auto-generated primary key")
    code: Optional[str] = Field(default=None, description="Business-friendly unique code")
    name: str = Field(..., description="Entity name")
    state: int = Field(..., description="Entity state: 0=INACTIVE, 1=ACTIVE, 2=DELETED")
    created_by: Optional[str] = Field(default=None, description="Creator")
    updated_by: Optional[str] = Field(default=None, description="Last updater")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.

    Usage:
        PaginatedResponse[EntityNameResponse]
    """

    items: List[T] = Field(..., description="List of items in current page")
    total: int = Field(..., ge=0, description="Total number of matching items")
    skip: int = Field(default=0, ge=0, description="Offset")
    limit: int = Field(default=20, ge=1, le=100, description="Page size")


# ===========================================================================
# Concrete Entity Schemas (replace EntityName)
# ===========================================================================


class EntityNameCreate(BaseCreate):
    """Schema for creating a new EntityName.

    Place in: src/{capability}/application/dtos/entity_name_schemas.py
    """

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional description",
    )

    # Add entity-specific creation fields:
    # tenant_id: str = Field(..., description="Multi-tenant identifier")
    # category: Optional[str] = None


class EntityNameUpdate(BaseUpdate):
    """Schema for updating an existing EntityName."""

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Updated description",
    )

    # Add entity-specific update fields:
    # category: Optional[str] = None


class EntityNameResponse(BaseResponse):
    """Schema for returning an EntityName."""

    description: Optional[str] = Field(default=None, description="Entity description")

    # Add entity-specific response fields:
    # category: Optional[str] = None
