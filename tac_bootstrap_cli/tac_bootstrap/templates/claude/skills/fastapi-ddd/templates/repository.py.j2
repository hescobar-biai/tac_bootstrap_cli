"""Repository Pattern - DDD Lite (Sync SQLAlchemy)

This template provides the BaseRepository pattern from Celes DDD Lite.
Uses synchronous SQLAlchemy Session (not async).

Usage:
    Replace 'EntityName' with your actual entity name.
    Replace 'entity_name' with the snake_case version.
    Place interface in: src/{capability}/domain/aggregates/
    Place impl in: src/{capability}/infrastructure/persistence/

Conventions:
    - BaseRepository provides generic CRUD: create, get_by_id, get_by_code,
      get_all, update, delete, soft_delete, activate, deactivate
    - Uses sync SQLAlchemy Session (default for DDD Lite)
    - Repository implementations named {Entity}RepositoryImpl
    - Abstract interface named {Entity}Repository
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

# Type variable for generic repository
T = TypeVar("T")


# ===========================================================================
# Abstract Repository Interface (domain layer)
# ===========================================================================


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository with standard CRUD operations.

    Provides the contract for all repository implementations.
    Place in: src/{capability}/domain/aggregates/{entity_name}_repository.py
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        ...

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[T]:
        ...

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        ...

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        ...

    @abstractmethod
    def soft_delete(self, entity_id: int) -> Optional[T]:
        ...

    @abstractmethod
    def activate(self, entity_id: int) -> Optional[T]:
        ...

    @abstractmethod
    def deactivate(self, entity_id: int) -> Optional[T]:
        ...


# ===========================================================================
# SQLAlchemy ORM Model (infrastructure/persistence/entity_name_model.py)
# ===========================================================================
#
# from sqlalchemy import Column, Integer, String, DateTime, func
# from sqlalchemy.orm import DeclarativeBase
#
# class Base(DeclarativeBase):
#     pass
#
# class EntityNameModel(Base):
#     __tablename__ = "entity_names"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     code = Column(String(50), unique=True, nullable=True)
#     name = Column(String(255), nullable=False)
#     state = Column(Integer, default=1)  # EntityState.ACTIVE
#     created_by = Column(String(100), nullable=True)
#     updated_by = Column(String(100), nullable=True)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ===========================================================================
# Concrete Repository Implementation (infrastructure/persistence/)
# ===========================================================================


class EntityNameRepositoryImpl(BaseRepository):
    """Sync SQLAlchemy implementation of EntityName repository.

    Uses the DDD Lite convention: {Entity}RepositoryImpl naming.
    Place in: src/{capability}/infrastructure/persistence/entity_name_repository.py

    Args:
        session: A synchronous SQLAlchemy session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, entity) -> object:
        model = EntityNameModel(
            code=entity.code,
            name=entity.name,
            state=entity.state,
            created_by=entity.created_by,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return model

    def get_by_id(self, entity_id: int) -> object | None:
        return self._session.get(EntityNameModel, entity_id)

    def get_by_code(self, code: str) -> object | None:
        stmt = select(EntityNameModel).where(EntityNameModel.code == code)
        return self._session.execute(stmt).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list:
        stmt = (
            select(EntityNameModel)
            .where(EntityNameModel.state != 2)  # Exclude DELETED
            .offset(skip)
            .limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def update(self, entity_id: int, entity) -> object | None:
        model = self._session.get(EntityNameModel, entity_id)
        if model is None:
            return None
        model.name = entity.name
        model.code = entity.code
        model.state = entity.state
        model.updated_by = entity.updated_by
        self._session.flush()
        self._session.refresh(model)
        return model

    def delete(self, entity_id: int) -> bool:
        model = self._session.get(EntityNameModel, entity_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.flush()
        return True

    def soft_delete(self, entity_id: int) -> object | None:
        model = self._session.get(EntityNameModel, entity_id)
        if model is None:
            return None
        model.state = 2  # EntityState.DELETED
        self._session.flush()
        return model

    def activate(self, entity_id: int) -> object | None:
        model = self._session.get(EntityNameModel, entity_id)
        if model is None:
            return None
        model.state = 1  # EntityState.ACTIVE
        self._session.flush()
        return model

    def deactivate(self, entity_id: int) -> object | None:
        model = self._session.get(EntityNameModel, entity_id)
        if model is None:
            return None
        model.state = 0  # EntityState.INACTIVE
        self._session.flush()
        return model
