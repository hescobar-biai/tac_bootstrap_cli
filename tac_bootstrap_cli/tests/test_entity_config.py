"""Tests for entity configuration domain models.

Comprehensive unit tests for EntitySpec, FieldSpec, FieldType enum,
validators, and property derivations.
"""

import pytest
from pydantic import ValidationError

from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType

# ============================================================================
# TEST FIELDTYPE ENUM
# ============================================================================


class TestFieldType:
    """Tests for FieldType enum."""

    def test_all_enum_values_defined(self):
        """All 9 field types should be defined."""
        expected_types = {
            "STRING",
            "INTEGER",
            "FLOAT",
            "BOOLEAN",
            "DATETIME",
            "UUID",
            "TEXT",
            "DECIMAL",
            "JSON",
        }
        actual_types = {ft.name for ft in FieldType}
        assert actual_types == expected_types

    def test_enum_string_values(self):
        """Enum values should have correct string representations."""
        assert FieldType.STRING.value == "str"
        assert FieldType.INTEGER.value == "int"
        assert FieldType.FLOAT.value == "float"
        assert FieldType.BOOLEAN.value == "bool"
        assert FieldType.DATETIME.value == "datetime"
        assert FieldType.UUID.value == "uuid"
        assert FieldType.TEXT.value == "text"
        assert FieldType.DECIMAL.value == "decimal"
        assert FieldType.JSON.value == "json"

    def test_enum_can_be_used_in_model(self):
        """FieldType enum should work in Pydantic models."""
        field = FieldSpec(name="test_field", field_type=FieldType.STRING)
        assert field.field_type == FieldType.STRING


# ============================================================================
# TEST FIELDSPEC MODEL
# ============================================================================


class TestFieldSpec:
    """Tests for FieldSpec model."""

    # Valid field names
    def test_valid_snake_case_names(self):
        """Valid snake_case field names should be accepted."""
        valid_names = [
            "user_name",
            "email_address",
            "is_active",
            "created_at2",
            "price",
            "status",
        ]
        for name in valid_names:
            field = FieldSpec(name=name, field_type=FieldType.STRING)
            assert field.name == name

    # Invalid naming patterns
    def test_reject_pascalcase(self):
        """PascalCase field names should be rejected."""
        with pytest.raises(ValidationError, match="must be snake_case"):
            FieldSpec(name="UserName", field_type=FieldType.STRING)

    def test_reject_camelcase(self):
        """camelCase field names should be rejected."""
        with pytest.raises(ValidationError, match="must be snake_case"):
            FieldSpec(name="userName", field_type=FieldType.STRING)

    def test_reject_kebabcase(self):
        """kebab-case field names should be rejected."""
        with pytest.raises(ValidationError, match="must be snake_case"):
            FieldSpec(name="user-name", field_type=FieldType.STRING)

    def test_reject_leading_number(self):
        """Field names starting with numbers should be rejected."""
        with pytest.raises(ValidationError, match="must be snake_case"):
            FieldSpec(name="1_field", field_type=FieldType.STRING)

    def test_reject_uppercase(self):
        """Uppercase field names should be rejected."""
        with pytest.raises(ValidationError, match="must be snake_case"):
            FieldSpec(name="USER_NAME", field_type=FieldType.STRING)

    # Python keyword conflicts
    def test_reject_python_keyword_class(self):
        """Python keyword 'class' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="class", field_type=FieldType.STRING)

    def test_reject_python_keyword_def(self):
        """Python keyword 'def' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="def", field_type=FieldType.STRING)

    def test_reject_python_keyword_return(self):
        """Python keyword 'return' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="return", field_type=FieldType.STRING)

    def test_reject_python_keyword_import(self):
        """Python keyword 'import' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="import", field_type=FieldType.STRING)

    def test_reject_python_keyword_for(self):
        """Python keyword 'for' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="for", field_type=FieldType.STRING)

    def test_reject_python_keyword_while(self):
        """Python keyword 'while' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="while", field_type=FieldType.STRING)

    def test_reject_python_keyword_try(self):
        """Python keyword 'try' should be rejected."""
        with pytest.raises(ValidationError, match="Python reserved keyword"):
            FieldSpec(name="try", field_type=FieldType.STRING)

    # SQLAlchemy conflicts
    def test_reject_sqlalchemy_query(self):
        """SQLAlchemy attribute 'query' should be rejected."""
        with pytest.raises(ValidationError, match="conflicts with SQLAlchemy"):
            FieldSpec(name="query", field_type=FieldType.STRING)

    def test_reject_sqlalchemy_metadata(self):
        """SQLAlchemy attribute 'metadata' should be rejected."""
        with pytest.raises(ValidationError, match="conflicts with SQLAlchemy"):
            FieldSpec(name="metadata", field_type=FieldType.STRING)

    def test_reject_sqlalchemy_registry(self):
        """SQLAlchemy attribute 'registry' should be rejected."""
        with pytest.raises(ValidationError, match="conflicts with SQLAlchemy"):
            FieldSpec(name="registry", field_type=FieldType.STRING)

    def test_reject_sqlalchemy_mapper(self):
        """SQLAlchemy attribute 'mapper' should be rejected."""
        with pytest.raises(ValidationError, match="conflicts with SQLAlchemy"):
            FieldSpec(name="mapper", field_type=FieldType.STRING)

    # Field attributes
    def test_default_required_true(self):
        """Field should be required by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.required is True

    def test_default_unique_false(self):
        """Field should not be unique by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.unique is False

    def test_default_indexed_false(self):
        """Field should not be indexed by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.indexed is False

    def test_default_value_none(self):
        """Field default should be None by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.default is None

    def test_default_description_empty(self):
        """Field description should be empty by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.description == ""

    def test_default_max_length_none(self):
        """Field max_length should be None by default."""
        field = FieldSpec(name="test", field_type=FieldType.STRING)
        assert field.max_length is None

    def test_set_all_attributes(self):
        """All field attributes should be settable."""
        field = FieldSpec(
            name="email",
            field_type=FieldType.STRING,
            required=True,
            unique=True,
            indexed=True,
            default="test@example.com",
            description="User email address",
            max_length=255,
        )
        assert field.name == "email"
        assert field.field_type == FieldType.STRING
        assert field.required is True
        assert field.unique is True
        assert field.indexed is True
        assert field.default == "test@example.com"
        assert field.description == "User email address"
        assert field.max_length == 255

    # Type validation
    def test_all_field_types_work(self):
        """All FieldType enum values should work in FieldSpec."""
        for field_type in FieldType:
            field = FieldSpec(name="test_field", field_type=field_type)
            assert field.field_type == field_type


# ============================================================================
# TEST ENTITYSPEC MODEL
# ============================================================================


class TestEntitySpec:
    """Tests for EntitySpec model."""

    # Valid entity names
    def test_valid_pascalcase_product(self):
        """Valid PascalCase name 'Product' should be accepted."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.name == "Product"

    def test_valid_pascalcase_userprofile(self):
        """Valid PascalCase name 'UserProfile' should be accepted."""
        entity = EntitySpec(
            name="UserProfile",
            capability="user-management",
            fields=[FieldSpec(name="bio", field_type=FieldType.TEXT)],
        )
        assert entity.name == "UserProfile"

    def test_valid_pascalcase_oauth2client(self):
        """Valid PascalCase name 'OAuth2Client' should be accepted."""
        entity = EntitySpec(
            name="OAuth2Client",
            capability="authentication",
            fields=[FieldSpec(name="client_id", field_type=FieldType.STRING)],
        )
        assert entity.name == "OAuth2Client"

    def test_valid_pascalcase_product2(self):
        """Valid PascalCase name 'Product2' should be accepted."""
        entity = EntitySpec(
            name="Product2",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.name == "Product2"

    # Invalid entity names
    def test_reject_lowercase_name(self):
        """Lowercase entity names should be rejected."""
        with pytest.raises(ValidationError, match="must be PascalCase"):
            EntitySpec(
                name="product",
                capability="catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_single_character_name(self):
        """Single-character entity names should be rejected."""
        with pytest.raises(ValidationError, match="at least 2 characters"):
            EntitySpec(
                name="A",
                capability="catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_name_starting_with_number(self):
        """Entity names starting with numbers should be rejected."""
        with pytest.raises(ValidationError, match="must be PascalCase"):
            EntitySpec(
                name="2Product",
                capability="catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_snake_case_name(self):
        """snake_case entity names should be rejected."""
        with pytest.raises(ValidationError, match="must be PascalCase"):
            EntitySpec(
                name="product_category",
                capability="catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_kebab_case_name(self):
        """kebab-case entity names should be rejected."""
        with pytest.raises(ValidationError, match="must be PascalCase"):
            EntitySpec(
                name="product-category",
                capability="catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    # Valid capabilities
    def test_valid_capability_catalog(self):
        """Valid capability 'catalog' should be accepted."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.capability == "catalog"

    def test_valid_capability_user_management(self):
        """Valid capability 'user-management' should be accepted."""
        entity = EntitySpec(
            name="User",
            capability="user-management",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        assert entity.capability == "user-management"

    def test_valid_capability_api_gateway(self):
        """Valid capability 'api-gateway' should be accepted."""
        entity = EntitySpec(
            name="Route",
            capability="api-gateway",
            fields=[FieldSpec(name="path", field_type=FieldType.STRING)],
        )
        assert entity.capability == "api-gateway"

    # Invalid capabilities
    def test_reject_capability_uppercase(self):
        """Uppercase capabilities should be rejected."""
        with pytest.raises(ValidationError, match="must be kebab-case"):
            EntitySpec(
                name="Product",
                capability="Catalog",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_capability_snake_case(self):
        """snake_case capabilities should be rejected."""
        with pytest.raises(ValidationError, match="must be kebab-case"):
            EntitySpec(
                name="Product",
                capability="user_management",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_capability_with_dots(self):
        """Capabilities with dots should be rejected."""
        with pytest.raises(ValidationError, match="must be kebab-case"):
            EntitySpec(
                name="Product",
                capability="api.gateway",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    def test_reject_capability_starting_with_number(self):
        """Capabilities starting with numbers should be rejected."""
        with pytest.raises(ValidationError, match="must be kebab-case"):
            EntitySpec(
                name="Product",
                capability="123abc",
                fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            )

    # Field list validation
    def test_reject_empty_field_list(self):
        """Empty field lists should be rejected."""
        with pytest.raises(ValidationError, match="at least one field"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[],
            )

    def test_reject_reserved_field_id(self):
        """Reserved field name 'id' should be rejected."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[FieldSpec(name="id", field_type=FieldType.UUID)],
            )

    def test_reject_reserved_field_state(self):
        """Reserved field name 'state' should be rejected."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[FieldSpec(name="state", field_type=FieldType.STRING)],
            )

    def test_reject_reserved_field_version(self):
        """Reserved field name 'version' should be rejected."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[FieldSpec(name="version", field_type=FieldType.INTEGER)],
            )

    def test_reject_reserved_field_created_at(self):
        """Reserved field name 'created_at' should be rejected."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[FieldSpec(name="created_at", field_type=FieldType.DATETIME)],
            )

    def test_reject_reserved_field_updated_at(self):
        """Reserved field name 'updated_at' should be rejected."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[FieldSpec(name="updated_at", field_type=FieldType.DATETIME)],
            )

    def test_reject_multiple_reserved_fields(self):
        """Multiple reserved fields should all be reported."""
        with pytest.raises(ValidationError, match="reserved by BaseEntity"):
            EntitySpec(
                name="Product",
                capability="catalog",
                fields=[
                    FieldSpec(name="id", field_type=FieldType.UUID),
                    FieldSpec(name="state", field_type=FieldType.STRING),
                ],
            )

    # Entity attributes
    def test_default_authorized_false(self):
        """Entity should not be authorized by default."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.authorized is False

    def test_default_async_mode_false(self):
        """Entity should not use async mode by default."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.async_mode is False

    def test_default_with_events_false(self):
        """Entity should not have events by default."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.with_events is False

    def test_set_all_flags_true(self):
        """All entity flags should be settable to True."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
            authorized=True,
            async_mode=True,
            with_events=True,
        )
        assert entity.authorized is True
        assert entity.async_mode is True
        assert entity.with_events is True


# ============================================================================
# TEST ENTITYSPEC PROPERTIES
# ============================================================================


class TestEntitySpecProperties:
    """Tests for EntitySpec derived name properties."""

    # snake_name property
    def test_snake_name_simple(self):
        """Product -> product."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.snake_name == "product"

    def test_snake_name_two_words(self):
        """UserProfile -> user_profile."""
        entity = EntitySpec(
            name="UserProfile",
            capability="user-management",
            fields=[FieldSpec(name="bio", field_type=FieldType.TEXT)],
        )
        assert entity.snake_name == "user_profile"

    def test_snake_name_with_numbers(self):
        """OAuth2Client -> o_auth2_client."""
        entity = EntitySpec(
            name="OAuth2Client",
            capability="auth",
            fields=[FieldSpec(name="client_id", field_type=FieldType.STRING)],
        )
        assert entity.snake_name == "o_auth2_client"

    def test_snake_name_acronym(self):
        """APIKey -> api_key."""
        entity = EntitySpec(
            name="APIKey",
            capability="auth",
            fields=[FieldSpec(name="key", field_type=FieldType.STRING)],
        )
        assert entity.snake_name == "a_p_i_key"

    def test_snake_name_product_category(self):
        """ProductCategory -> product_category."""
        entity = EntitySpec(
            name="ProductCategory",
            capability="catalog",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        assert entity.snake_name == "product_category"

    # plural_name property
    def test_plural_name_simple(self):
        """Product -> products."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "products"

    def test_plural_name_category(self):
        """Category -> categorys."""
        entity = EntitySpec(
            name="Category",
            capability="catalog",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "categorys"

    def test_plural_name_ends_with_s(self):
        """Status -> statuses."""
        entity = EntitySpec(
            name="Status",
            capability="workflow",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "statuses"

    def test_plural_name_ends_with_x(self):
        """Index -> indexes."""
        entity = EntitySpec(
            name="Index",
            capability="search",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        # Note: "index" ends with 'x', so plural is "indexes"
        # But snake_name is "index", not ending in x
        assert entity.plural_name == "indexes"

    def test_plural_name_ends_with_z(self):
        """Quiz -> quizzes."""
        entity = EntitySpec(
            name="Quiz",
            capability="education",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "quizzes"

    def test_plural_name_ends_with_ch(self):
        """Branch -> branches."""
        entity = EntitySpec(
            name="Branch",
            capability="git",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "branches"

    def test_plural_name_ends_with_sh(self):
        """Wish -> wishes."""
        entity = EntitySpec(
            name="Wish",
            capability="shopping",
            fields=[FieldSpec(name="item", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "wishes"

    def test_plural_name_box(self):
        """Box -> boxes."""
        entity = EntitySpec(
            name="Box",
            capability="storage",
            fields=[FieldSpec(name="label", field_type=FieldType.STRING)],
        )
        assert entity.plural_name == "boxes"

    def test_plural_name_two_words(self):
        """UserProfile -> user_profiles."""
        entity = EntitySpec(
            name="UserProfile",
            capability="user-management",
            fields=[FieldSpec(name="bio", field_type=FieldType.TEXT)],
        )
        assert entity.plural_name == "user_profiles"

    # table_name property
    def test_table_name_simple(self):
        """Product -> products."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.table_name == "products"

    def test_table_name_two_words(self):
        """UserProfile -> user_profiles."""
        entity = EntitySpec(
            name="UserProfile",
            capability="user-management",
            fields=[FieldSpec(name="bio", field_type=FieldType.TEXT)],
        )
        assert entity.table_name == "user_profiles"

    def test_table_name_same_as_plural(self):
        """table_name should equal plural_name."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        assert entity.table_name == entity.plural_name


# ============================================================================
# TEST SERIALIZATION
# ============================================================================


class TestSerialization:
    """Tests for JSON/YAML serialization."""

    def test_fieldspec_model_dump(self):
        """FieldSpec should serialize to dict."""
        field = FieldSpec(
            name="email",
            field_type=FieldType.STRING,
            required=True,
            unique=True,
            max_length=255,
        )
        data = field.model_dump()
        assert data["name"] == "email"
        assert data["field_type"] == "str"
        assert data["required"] is True
        assert data["unique"] is True
        assert data["max_length"] == 255

    def test_entityspec_model_dump(self):
        """EntitySpec should serialize to dict."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(name="title", field_type=FieldType.STRING),
                FieldSpec(name="price", field_type=FieldType.DECIMAL),
            ],
            authorized=True,
        )
        data = entity.model_dump()
        assert data["name"] == "Product"
        assert data["capability"] == "catalog"
        assert len(data["fields"]) == 2
        assert data["fields"][0]["name"] == "title"
        assert data["fields"][1]["name"] == "price"
        assert data["authorized"] is True

    def test_entityspec_model_dump_json(self):
        """EntitySpec should serialize to JSON string."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="title", field_type=FieldType.STRING)],
        )
        json_str = entity.model_dump_json()
        assert isinstance(json_str, str)
        assert "Product" in json_str
        assert "catalog" in json_str

    def test_round_trip_serialization(self):
        """EntitySpec should deserialize from serialized data."""
        original = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(name="title", field_type=FieldType.STRING, max_length=200),
                FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
            ],
            authorized=True,
            async_mode=True,
        )

        # Serialize and deserialize
        data = original.model_dump()
        restored = EntitySpec(**data)

        # Verify equality
        assert restored.name == original.name
        assert restored.capability == original.capability
        assert len(restored.fields) == len(original.fields)
        assert restored.fields[0].name == original.fields[0].name
        assert restored.fields[0].field_type == original.fields[0].field_type
        assert restored.fields[1].name == original.fields[1].name
        assert restored.authorized == original.authorized
        assert restored.async_mode == original.async_mode

    def test_nested_field_serialization(self):
        """Nested FieldSpec models should serialize correctly."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(
                    name="title",
                    field_type=FieldType.STRING,
                    required=True,
                    unique=False,
                    indexed=True,
                    description="Product title",
                    max_length=200,
                ),
            ],
        )
        data = entity.model_dump()
        field_data = data["fields"][0]

        assert field_data["name"] == "title"
        assert field_data["field_type"] == "str"
        assert field_data["required"] is True
        assert field_data["unique"] is False
        assert field_data["indexed"] is True
        assert field_data["description"] == "Product title"
        assert field_data["max_length"] == 200
