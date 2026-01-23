# Base Repository Template

Generic CRUD repository for SQLAlchemy. Place at `src/shared/infrastructure/base_repository.py`.

## Template

```python
"""
IDK: repository, data-access, crud-operations

Module: base_repository

Responsibility:
- Provide generic CRUD operations for all repositories
- Abstract database access patterns
- Support pagination, filtering, and sorting

Key Components:
- BaseRepository: Generic repository with CRUD operations

Invariants:
- All queries use SQLAlchemy ORM
- Soft delete operations set state=2
- Pagination is 1-indexed

Related Docs:
- docs/shared/infrastructure/base-repository.md
"""

from typing import TypeVar, Generic, Type, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import datetime, UTC

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    IDK: repository, orm-abstraction, crud-operations

    Responsibility:
    - Provide CRUD operations for ORM models
    - Abstract SQLAlchemy session management
    - Support filtering, sorting, and pagination

    Invariants:
    - All operations use single db session
    - Pagination pages are 1-indexed
    - Filters only apply to existing model attributes
    - Soft delete sets state=2

    Collaborators:
    - Session: SQLAlchemy database session
    - ORM Model: entity-specific model class

    Failure Modes:
    - SQLAlchemyError: database operation failures
    - AttributeError: invalid filter/sort fields

    Related Docs:
    - docs/shared/infrastructure/base-repository.md
    """

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, entity: T) -> T:
        """
        IDK: entity-creation, persistence, transaction

        Responsibility:
        - Persist new entity to database
        - Commit transaction
        - Refresh entity with generated values

        Invariants:
        - Entity added to session and committed
        - Entity refreshed with database-generated fields

        Inputs:
        - entity (T): ORM model instance to persist

        Outputs:
        - T: persisted entity with generated fields

        Failure Modes:
        - IntegrityError: constraint violations
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, entity_id: str) -> T | None:
        """
        IDK: entity-retrieval, query, primary-key

        Responsibility:
        - Retrieve single entity by primary key

        Invariants:
        - Returns None if not found
        - Returns first match (should be unique)

        Inputs:
        - entity_id (str): unique identifier

        Outputs:
        - T | None: entity or None

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> Tuple[list[T], int]:
        """
        IDK: pagination, filtering, query-builder

        Responsibility:
        - Retrieve paginated entity list
        - Apply dynamic filters and sorting
        - Return total count for pagination

        Invariants:
        - Page is 1-indexed
        - Filters only apply to existing attributes
        - Returns (items, total) tuple

        Inputs:
        - page (int): page number (1-indexed)
        - page_size (int): items per page
        - filters (dict | None): field:value filter pairs
        - sort_by (str | None): field to sort by
        - sort_order (str): 'asc' or 'desc'

        Outputs:
        - Tuple[list[T], int]: (items, total_count)

        Failure Modes:
        - AttributeError: invalid filter/sort field

        Related Docs:
        - docs/shared/infrastructure/pagination.md
        """
        query = self.db.query(self.model)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        # Get total count before pagination
        total = query.count()

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

        # Apply pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    def update(self, entity_id: str, data: dict) -> T | None:
        """
        IDK: entity-update, persistence, partial-update

        Responsibility:
        - Update entity fields from dictionary
        - Auto-update audit trail (updated_at, version)
        - Persist changes to database

        Invariants:
        - Only updates existing attributes
        - updated_at set to current UTC
        - version incremented automatically
        - Returns None if entity not found

        Inputs:
        - entity_id (str): entity identifier
        - data (dict): field:value pairs to update

        Outputs:
        - T | None: updated entity or None

        Failure Modes:
        - EntityNotFound: entity_id doesn't exist
        - SQLAlchemyError: database failures

        Related Docs:
        - docs/shared/infrastructure/crud-operations.md
        """
        entity = self.get_by_id(entity_id)
        if not entity:
            return None

        # Update fields
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        # Update modified timestamp and version
        entity.updated_at = datetime.now(UTC)
        entity.version = entity.version + 1

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, persistence, permanent-removal

        Responsibility:
        - Permanently remove entity from database
        - Not recoverable after commit

        Invariants:
        - Returns False if entity not found
        - Returns True if deleted successfully
        - Changes committed immediately

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - bool: True if deleted, False if not found

        Failure Modes:
        - SQLAlchemyError: database failures
        - IntegrityError: foreign key constraints

        Related Docs:
        - docs/shared/infrastructure/delete-operations.md
        """
        entity = self.get_by_id(entity_id)
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()
        return True

    def soft_delete(self, entity_id: str) -> T | None:
        """
        IDK: soft-delete, state-transition, recoverable

        Responsibility:
        - Mark entity as deleted (state=2)
        - Preserve data for recovery
        - Update audit trail

        Invariants:
        - Sets state to 2 (DELETED)
        - Data remains in database
        - Returns None if not found

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - T | None: updated entity or None

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        return self.update(entity_id, {"state": 2})

    def exists(self, entity_id: str) -> bool:
        """
        IDK: existence-check, query, predicate

        Responsibility:
        - Check if entity exists in database
        - Fast check without loading entity

        Invariants:
        - Returns boolean
        - Does not load full entity

        Inputs:
        - entity_id (str): entity identifier

        Outputs:
        - bool: True if exists, False otherwise

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        return self.db.query(self.model).filter(self.model.id == entity_id).count() > 0

    def get_by_code(self, code: str) -> T | None:
        """
        IDK: business-key-lookup, query, unique-code

        Responsibility:
        - Retrieve entity by business code
        - Support code-based lookups

        Invariants:
        - Returns None if not found
        - Code should be unique per entity type

        Inputs:
        - code (str): business identifier

        Outputs:
        - T | None: entity or None

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        return self.db.query(self.model).filter(self.model.code == code).first()

    def count(self, filters: dict | None = None) -> int:
        """
        IDK: aggregation, count-query, filtering

        Responsibility:
        - Count entities with optional filters
        - Support filtered counting

        Invariants:
        - Returns non-negative integer
        - Filters only apply to existing attributes

        Inputs:
        - filters (dict | None): field:value filter pairs

        Outputs:
        - int: count of matching entities

        Failure Modes:
        - AttributeError: invalid filter field

        Related Docs:
        - docs/shared/infrastructure/query-patterns.md
        """
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        return query.count()
```

## Directory Setup

```
src/
└── shared/
    └── infrastructure/
        ├── __init__.py
        ├── database.py
        └── base_repository.py  # <-- This file
```

**`src/shared/infrastructure/__init__.py`**:
```python
"""Shared infrastructure components."""
from .database import Base, get_db, init_db
from .base_repository import BaseRepository

__all__ = ["Base", "get_db", "init_db", "BaseRepository"]
```
