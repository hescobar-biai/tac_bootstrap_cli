"""
TAC Bootstrap Entity Configuration Models

Pydantic models for defining entity specifications used in code generation.
These models provide type safety, validation, and naming conventions for
generating complete CRUD entities following vertical slice architecture.

Example usage:
    from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType

    entity = EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(
                name="title",
                field_type=FieldType.STRING,
                required=True,
                max_length=200
            ),
            FieldSpec(
                name="price",
                field_type=FieldType.DECIMAL,
                required=True
            ),
            FieldSpec(
                name="description",
                field_type=FieldType.TEXT,
                required=False
            )
        ],
        authorized=True,
        async_mode=True
    )

    # Access derived names
    print(entity.snake_name)    # "product"
    print(entity.plural_name)   # "products"
    print(entity.table_name)    # "products"
"""

import keyword
import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator

# ============================================================================
# CONSTANTS - Reserved Names and Validation Patterns
# ============================================================================

# Field names reserved by BaseEntity and framework
RESERVED_FIELD_NAMES = (
    "id",
    "state",
    "version",
    "created_at",
    "updated_at",
)

# Field names that conflict with SQLAlchemy attributes
SQLALCHEMY_CONFLICTS = (
    "query",
    "metadata",
    "registry",
    "mapper",
)

# Naming convention patterns
PASCALCASE_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
KEBABCASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
SNAKECASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


# ============================================================================
# ENUMS - Field Type Definitions
# ============================================================================


class FieldType(str, Enum):
    """
    Supported database field types for entity generation.

    Types:
        STRING: Variable-length string (VARCHAR), use max_length to specify size
        INTEGER: Standard integer (INT)
        FLOAT: Floating-point number (FLOAT/DOUBLE)
        BOOLEAN: Boolean flag (BOOLEAN/BIT)
        DATETIME: Timestamp with timezone (TIMESTAMP)
        UUID: Universally unique identifier (UUID)
        TEXT: Large text field (TEXT/CLOB)
        DECIMAL: Fixed-precision decimal (DECIMAL/NUMERIC)
        JSON: JSON data structure (JSON/JSONB)
    """

    STRING = "str"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "bool"
    DATETIME = "datetime"
    UUID = "uuid"
    TEXT = "text"
    DECIMAL = "decimal"
    JSON = "json"


# ============================================================================
# FIELD SPECIFICATION MODEL
# ============================================================================


class FieldSpec(BaseModel):
    """
    Specification for a single entity field.

    Defines the name, type, constraints, and metadata for a field
    in the generated entity. Field names must be snake_case and
    cannot conflict with Python keywords or SQLAlchemy attributes.

    Attributes:
        name: Field name in snake_case (e.g., "user_name", "email_address")
        field_type: Database/Python type from FieldType enum
        required: Whether field is required (non-nullable)
        unique: Whether field must be unique across records
        indexed: Whether to create database index on this field
        default: Default value (not type-validated at this level)
        description: Human-readable field documentation
        max_length: Maximum string length (for STRING/TEXT types)

    Example:
        field = FieldSpec(
            name="email_address",
            field_type=FieldType.STRING,
            required=True,
            unique=True,
            indexed=True,
            max_length=255,
            description="User's primary email address"
        )
    """

    name: str
    field_type: FieldType
    required: bool = True
    unique: bool = False
    indexed: bool = False
    default: Any = None
    description: str = ""
    max_length: int | None = None

    @field_validator("name")
    @classmethod
    def validate_field_name(cls, v: str) -> str:
        """
        Validate field name follows conventions and doesn't conflict.

        Rules:
        - Must be snake_case (lowercase with underscores)
        - Cannot be a Python reserved keyword
        - Cannot conflict with SQLAlchemy attribute names

        Args:
            v: Field name to validate

        Returns:
            Validated field name

        Raises:
            ValueError: If validation fails
        """
        # Check snake_case pattern
        if not SNAKECASE_PATTERN.match(v):
            raise ValueError(
                f"Field name '{v}' must be snake_case (lowercase with underscores). "
                "Examples: user_name, email_address, is_active"
            )

        # Check Python keywords
        if keyword.iskeyword(v):
            raise ValueError(
                f"Field name '{v}' is a Python reserved keyword and cannot be used. "
                "Choose a different name."
            )

        # Check SQLAlchemy conflicts
        if v in SQLALCHEMY_CONFLICTS:
            raise ValueError(
                f"Field name '{v}' conflicts with SQLAlchemy attributes. "
                f"Reserved names: {', '.join(SQLALCHEMY_CONFLICTS)}"
            )

        return v


# ============================================================================
# ENTITY SPECIFICATION MODEL
# ============================================================================


class EntitySpec(BaseModel):
    """
    Complete specification for a generated entity.

    Defines the entity name, capability grouping, fields, and generation
    options for creating a complete CRUD layer following vertical slice
    architecture. Provides derived names for consistent code generation.

    Attributes:
        name: Entity name in PascalCase (e.g., "Product", "UserProfile")
        capability: Capability grouping in kebab-case (e.g., "catalog", "user-management")
        fields: List[Any] of field specifications (must not be empty)
        authorized: Generate with authentication templates
        async_mode: Use async repository pattern
        with_events: Generate domain event support

    Properties:
        snake_name: Entity name in snake_case (e.g., "product", "user_profile")
        plural_name: Pluralized snake_case name (e.g., "products", "user_profiles")
        table_name: Database table name (same as plural_name)

    Example:
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(name="title", field_type=FieldType.STRING),
                FieldSpec(name="price", field_type=FieldType.DECIMAL)
            ],
            authorized=True,
            async_mode=True,
            with_events=True
        )

        # Access derived names
        entity.snake_name    # "product"
        entity.plural_name   # "products"
        entity.table_name    # "products"
    """

    name: str
    capability: str
    fields: list[FieldSpec]
    authorized: bool = False
    async_mode: bool = False
    with_events: bool = False

    @field_validator("name")
    @classmethod
    def validate_entity_name(cls, v: str) -> str:
        """
        Validate entity name is PascalCase with minimum 2 characters.

        Rules:
        - Must be PascalCase (starts with uppercase, alphanumeric)
        - Minimum 2 characters
        - Cannot start with a number

        Args:
            v: Entity name to validate

        Returns:
            Validated entity name

        Raises:
            ValueError: If validation fails
        """
        if len(v) < 2:
            raise ValueError(
                "Entity name must be at least 2 characters long"
            )

        if not PASCALCASE_PATTERN.match(v):
            raise ValueError(
                f"Entity name '{v}' must be PascalCase (start with uppercase letter, "
                "followed by letters and numbers). Examples: Product, UserProfile, OAuth2Client"
            )

        return v

    @field_validator("capability")
    @classmethod
    def validate_capability(cls, v: str) -> str:
        """
        Validate capability is kebab-case.

        Rules:
        - Must be kebab-case (lowercase with hyphens)
        - Cannot start with number or hyphen

        Args:
            v: Capability name to validate

        Returns:
            Validated capability name

        Raises:
            ValueError: If validation fails
        """
        if not KEBABCASE_PATTERN.match(v):
            raise ValueError(
                f"Capability '{v}' must be kebab-case (lowercase with hyphens). "
                "Examples: catalog, user-management, api-gateway"
            )

        return v

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, v: list[FieldSpec]) -> list[FieldSpec]:
        """
        Validate field list is not empty and has no reserved names.

        Rules:
        - Must have at least one field
        - No field names can match RESERVED_FIELD_NAMES

        Args:
            v: List[Any] of field specifications

        Returns:
            Validated field list

        Raises:
            ValueError: If validation fails
        """
        if not v:
            raise ValueError(
                "Entity must have at least one field"
            )

        # Check for reserved field names
        reserved_found = [
            field.name for field in v
            if field.name in RESERVED_FIELD_NAMES
        ]

        if reserved_found:
            raise ValueError(
                f"Field names {reserved_found} are reserved by BaseEntity. "
                f"Reserved names: {', '.join(RESERVED_FIELD_NAMES)}"
            )

        return v

    @property
    def snake_name(self) -> str:
        """
        Convert entity name from PascalCase to snake_case.

        Returns:
            Entity name in snake_case

        Example:
            Product -> product
            UserProfile -> user_profile
            OAuth2Client -> o_auth2_client
        """
        # Insert underscore before uppercase letters (except first)
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", self.name)
        return name.lower()

    @property
    def plural_name(self) -> str:
        """
        Generate plural form of entity name in snake_case.

        Pluralization rules:
        - Ends in z: double z and append 'es' (quiz -> quizzes)
        - Ends in s, x, ch, sh: append 'es'
        - Otherwise: append 's'

        Returns:
            Pluralized entity name in snake_case

        Example:
            Product -> products
            Category -> categorys
            Box -> boxes
            Quiz -> quizzes
            Branch -> branches
            Wish -> wishes
        """
        snake = self.snake_name

        # Words ending in 'z' need to double the z before adding 'es'
        if snake.endswith('z'):
            return snake + "zes"

        # Check for other special endings that need 'es'
        if snake.endswith(('s', 'x')) or snake.endswith(('ch', 'sh')):
            return snake + "es"

        return snake + "s"

    @property
    def table_name(self) -> str:
        """
        Generate database table name (lowercase plural).

        Returns:
            Database table name

        Example:
            Product -> products
            UserProfile -> user_profiles
        """
        return self.plural_name
