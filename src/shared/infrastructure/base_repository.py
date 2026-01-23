"""
IDK: repository-layer, data-access, orm-abstraction

Module: base_repository

Responsibility:
- Provide generic CRUD operations for all domain entities
- Abstract SQLAlchemy ORM complexity from service layer
- Enforce soft-delete transparency (exclude state=2 by default)
- Handle transaction management with automatic commit/rollback
- Support dynamic filtering, sorting, and pagination

Key Components:
- BaseRepository[TModel]: Generic repository with full CRUD operations
- Soft-delete enforcement: All queries exclude state=2 entities
- Transaction management: Each method handles commit/rollback
- Dynamic filtering: Apply equality filters from dict
- Pagination: offset/limit with total count

Invariants:
- All queries filter out state=2 (soft-deleted) entities by default
- Each mutation method commits on success, rollbacks on exception
- Pagination uses 1-indexed pages (page=1 is first page)
- sort_by field must exist in model (validated via hasattr)
- Filters apply equality (==) operator only
- delete() sets state=2 (soft delete), hard_delete() removes physically

Usage Examples:

```python
# Define entity-specific repository by inheriting BaseRepository
from src.shared.infrastructure.base_repository import BaseRepository
from src.products.infrastructure.models import ProductModel
from src.shared.infrastructure.database import get_db
from sqlalchemy.orm import Session

class ProductRepository(BaseRepository[ProductModel]):
    def __init__(self, session: Session):
        super().__init__(session, ProductModel)

# Use in service layer
from src.products.infrastructure.repositories import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product(self, product_id: str):
        # Returns None if product has state=2 (soft-deleted)
        return self.repository.get_by_id(product_id)

    def list_products(self, page: int, page_size: int, category: str | None = None):
        filters = {"category": category} if category else {}
        # Excludes products with state=2
        items, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by="created_at",
            sort_order="desc"
        )
        return items, total

    def soft_delete_product(self, product_id: str):
        # Sets state=2 instead of physical deletion
        return self.repository.delete(product_id)

    def permanent_delete_product(self, product_id: str):
        # Physical deletion from database
        return self.repository.hard_delete(product_id)

# Use with FastAPI dependency injection
from fastapi import Depends

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)

@router.get("/products/{product_id}")
def get_product(
    product_id: str,
    repository: ProductRepository = Depends(get_product_repository)
):
    product = repository.get_by_id(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product
```

Collaborators:
- SQLAlchemy Session: database connection and transaction management
- ORM Models: entity classes mapped to database tables
- Service Layer: orchestrates business logic using repository

Failure Modes:
- ValueError: invalid pagination inputs (page < 1, page_size < 1)
- ValueError: invalid sort_by field (not an attribute of model)
- ValueError: entity not found during update operation
- DatabaseError: constraint violations, connection errors (propagated after rollback)

Related Docs:
- docs/shared/infrastructure/base-repository.md
- ai_docs/doc/create-crud-entity/
"""

from typing import Generic, TypeVar, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

# Generic type variable for ORM models
TModel = TypeVar('TModel')


class BaseRepository(Generic[TModel]):
    """
    IDK: repository-pattern, crud-operations, soft-delete

    Responsibility:
    - Provide generic CRUD operations for domain entities
    - Abstract SQLAlchemy operations from service layer
    - Enforce soft-delete filtering (exclude state=2)
    - Manage database transactions (commit/rollback)
    - Support pagination, filtering, and sorting

    Invariants:
    - All queries exclude entities with state=2 (soft-deleted)
    - Each mutation commits on success, rollback on exception
    - Pagination is 1-indexed (page=1 is first page)
    - Filters use equality operator (==) only
    - sort_by field must be valid model attribute

    Generic Type Parameters:
    - TModel: ORM model class (e.g., ProductModel, UserModel)

    Usage Pattern:
    - Entity repositories inherit and specify model type
    - Session injected via constructor
    - Used by service layer for data access

    Example:

    ```python
    class ProductRepository(BaseRepository[ProductModel]):
        def __init__(self, session: Session):
            super().__init__(session, ProductModel)

        # Add entity-specific queries if needed
        def get_by_sku(self, sku: str) -> ProductModel | None:
            return self.session.query(self.model_class).filter(
                self.model_class.sku == sku,
                self.model_class.state != 2
            ).first()
    ```

    Collaborators:
    - SQLAlchemy Session: database connection
    - ORM Models: entity classes
    - Service Layer: business logic

    Failure Modes:
    - ValueError: invalid inputs (page < 1, invalid sort_by, entity not found)
    - DatabaseError: database errors (propagated after rollback)

    Related Docs:
    - docs/shared/infrastructure/repository-pattern.md
    """

    def __init__(self, session: Session, model_class: type[TModel]):
        """
        IDK: dependency-injection, constructor

        Responsibility:
        - Initialize repository with database session and model class
        - Enable testability via dependency injection

        Invariants:
        - session must be active SQLAlchemy session
        - model_class must be ORM-mapped model

        Inputs:
        - session: SQLAlchemy database session
        - model_class: ORM model type

        Outputs:
        - None (initializes instance)

        Related Docs:
        - docs/shared/infrastructure/dependency-injection.md
        """
        self.session = session
        self.model_class = model_class

    def get_by_id(self, entity_id: str) -> TModel | None:
        """
        IDK: read-operation, retrieval, soft-delete-filter

        Responsibility:
        - Retrieve single entity by ID
        - Exclude soft-deleted entities (state=2)
        - Return None if not found or deleted

        Invariants:
        - Returns None if entity.state == 2
        - Returns None if entity_id doesn't exist
        - No exception raised on missing entity

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - TModel | None: entity if found and not deleted, None otherwise

        Example:

        ```python
        product = repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        if product is None:
            # Not found or soft-deleted
            raise HTTPException(404, "Product not found")
        ```

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        return self.session.query(self.model_class).filter(
            self.model_class.id == entity_id,
            self.model_class.state != 2
        ).first()

    def get_all(
        self,
        page: int,
        page_size: int,
        filters: Dict[str, Any] | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> tuple[list[TModel], int]:
        """
        IDK: list-operation, pagination, filtering, sorting

        Responsibility:
        - Retrieve paginated list of entities
        - Apply dynamic filters with equality operator
        - Sort by specified field
        - Exclude soft-deleted entities (state=2)
        - Return items and total count

        Invariants:
        - Excludes entities with state=2
        - page must be >= 1
        - page_size must be >= 1
        - sort_by must be valid model attribute if provided
        - Offset calculated as (page - 1) * page_size
        - Total count reflects all matching entities (not just current page)

        Inputs:
        - page: page number (1-indexed)
        - page_size: number of items per page
        - filters: dict of field:value for equality filtering
        - sort_by: field name to sort by (None for no sorting)
        - sort_order: "asc" or "desc"

        Outputs:
        - tuple[list[TModel], int]: (items in current page, total count)

        Failure Modes:
        - ValueError: page < 1 or page_size < 1
        - ValueError: sort_by is not a valid model attribute

        Example:

        ```python
        # Get page 2 with 10 items, filter by category, sort by price descending
        items, total = repository.get_all(
            page=2,
            page_size=10,
            filters={"category": "Electronics", "status": "active"},
            sort_by="price",
            sort_order="desc"
        )
        # items = [product11, product12, ..., product20]
        # total = 150 (total matching entities across all pages)
        ```

        Related Docs:
        - docs/shared/infrastructure/pagination.md
        - docs/shared/infrastructure/filtering.md
        """
        # Validate inputs
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        # Validate sort_by field if provided
        if sort_by and not hasattr(self.model_class, sort_by):
            raise ValueError(f"Invalid sort field: {sort_by}")

        # Base query excludes soft-deleted entities
        query = self.session.query(self.model_class).filter(
            self.model_class.state != 2
        )

        # Apply filters (equality only)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)

        # Get total count before pagination
        total = query.count()

        # Apply sorting
        if sort_by:
            sort_column = getattr(self.model_class, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        # Apply pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total

    def create(self, model: TModel) -> TModel:
        """
        IDK: create-operation, persistence, transaction

        Responsibility:
        - Insert new entity into database
        - Commit transaction
        - Return persisted entity with generated fields

        Invariants:
        - Commits transaction on success
        - Rollback on exception
        - Returns entity with database-generated fields (id, timestamps)

        Inputs:
        - model: entity instance to persist

        Outputs:
        - TModel: persisted entity with database-generated values

        Failure Modes:
        - DatabaseError: constraint violation (unique, foreign key, etc.)
        - Exception triggers rollback

        Example:

        ```python
        new_product = ProductModel(
            code="PROD-001",
            name="Laptop",
            price=999.99,
            category="Electronics"
        )
        created = repository.create(new_product)
        # created.id is now set by database
        ```

        Related Docs:
        - docs/shared/infrastructure/create-operations.md
        """
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, model: TModel) -> TModel:
        """
        IDK: update-operation, persistence, transaction

        Responsibility:
        - Update existing entity in database
        - Validate entity exists and is not deleted (state != 2)
        - Commit transaction
        - Return updated entity

        Invariants:
        - Entity must exist in database
        - Entity must not be soft-deleted (state != 2)
        - Commits transaction on success
        - Rollback on exception
        - Raises ValueError if entity not found or deleted

        Inputs:
        - model: entity instance with updated fields

        Outputs:
        - TModel: updated entity

        Failure Modes:
        - ValueError: entity not found or soft-deleted
        - DatabaseError: constraint violation
        - Exception triggers rollback

        Example:

        ```python
        product = repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        if not product:
            raise ValueError("Product not found")

        product.price = 899.99
        product.mark_updated(user_id="user-123")
        updated = repository.update(product)
        ```

        Related Docs:
        - docs/shared/infrastructure/update-operations.md
        """
        try:
            # Validate entity exists and is not deleted
            existing = self.get_by_id(model.id)
            if not existing:
                raise ValueError(f"Entity with id {model.id} not found or is deleted")

            # Merge changes and commit
            self.session.merge(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, entity_id: str) -> bool:
        """
        IDK: soft-delete, state-transition, data-preservation

        Responsibility:
        - Soft delete entity by setting state=2
        - Preserve data in database for audit trail
        - Commit transaction
        - Return success status

        Invariants:
        - Sets state=2 instead of physical deletion
        - Data remains in database
        - Returns True if entity found and deleted
        - Returns False if entity not found or already deleted
        - Idempotent: deleting already-deleted entity returns False

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if deleted, False if not found or already deleted

        Example:

        ```python
        # Soft delete product
        success = repository.delete("550e8400-e29b-41d4-a716-446655440000")
        if not success:
            raise HTTPException(404, "Product not found")

        # Subsequent queries won't return this entity (state=2)
        product = repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        # product is None
        ```

        Related Docs:
        - docs/shared/infrastructure/soft-delete.md
        """
        try:
            entity = self.get_by_id(entity_id)
            if not entity:
                return False

            entity.state = 2
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def hard_delete(self, entity_id: str) -> bool:
        """
        IDK: hard-delete, physical-deletion, permanent-removal

        Responsibility:
        - Physically delete entity from database
        - Remove data permanently (no recovery)
        - Commit transaction
        - Return success status

        Invariants:
        - Performs physical DELETE from database
        - Data is permanently removed
        - Returns True if entity found and deleted
        - Returns False if entity not found

        WARNING: This operation is irreversible. Use with caution.
        Prefer soft delete (delete() method) for most use cases.

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if deleted, False if not found

        Example:

        ```python
        # Permanently delete product (admin operation)
        success = repository.hard_delete("550e8400-e29b-41d4-a716-446655440000")
        if not success:
            raise HTTPException(404, "Product not found")

        # Entity is completely removed from database
        ```

        Related Docs:
        - docs/shared/infrastructure/hard-delete.md
        """
        try:
            # Query without state filter for hard delete
            entity = self.session.query(self.model_class).filter(
                self.model_class.id == entity_id
            ).first()

            if not entity:
                return False

            self.session.delete(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def exists(self, entity_id: str) -> bool:
        """
        IDK: existence-check, query-method, soft-delete-filter

        Responsibility:
        - Check if entity exists in database
        - Exclude soft-deleted entities (state=2)
        - Return boolean result

        Invariants:
        - Returns False for soft-deleted entities (state=2)
        - Returns False for non-existent entities
        - Returns True only for active/inactive entities (state=0 or 1)

        Inputs:
        - entity_id: unique identifier of entity

        Outputs:
        - bool: True if exists and not deleted, False otherwise

        Example:

        ```python
        if repository.exists("550e8400-e29b-41d4-a716-446655440000"):
            # Entity exists and is not soft-deleted
            product = repository.get_by_id("550e8400-e29b-41d4-a716-446655440000")
        else:
            raise HTTPException(404, "Product not found")
        ```

        Related Docs:
        - docs/shared/infrastructure/query-methods.md
        """
        count = self.session.query(func.count(self.model_class.id)).filter(
            self.model_class.id == entity_id,
            self.model_class.state != 2
        ).scalar()
        return count > 0

    def count(self, filters: Dict[str, Any] | None = None) -> int:
        """
        IDK: count-operation, aggregation, soft-delete-filter

        Responsibility:
        - Count entities matching filters
        - Exclude soft-deleted entities (state=2)
        - Apply dynamic filters with equality operator
        - Return total count

        Invariants:
        - Excludes entities with state=2
        - Returns 0 if no matches
        - Filters use equality operator (==) only

        Inputs:
        - filters: dict of field:value for equality filtering

        Outputs:
        - int: count of matching entities

        Example:

        ```python
        # Count all active products in Electronics category
        total = repository.count({"category": "Electronics", "state": 1})
        # total = 42

        # Count all active entities (not deleted)
        total = repository.count({})
        # total = 150
        ```

        Related Docs:
        - docs/shared/infrastructure/count-operations.md
        """
        # Base query excludes soft-deleted entities
        query = self.session.query(func.count(self.model_class.id)).filter(
            self.model_class.state != 2
        )

        # Apply filters (equality only)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)

        return query.scalar()
