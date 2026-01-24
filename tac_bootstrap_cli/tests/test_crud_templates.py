"""
Tests for CRUD templates.

Comprehensive unit tests for validating that the 6 templates in
`tac_bootstrap/templates/capabilities/crud_basic/` render correctly
and generate valid Python code.
"""


import pytest

from tac_bootstrap.domain.entity_config import (
    EntitySpec,
    FieldSpec,
    FieldType,
)
from tac_bootstrap.domain.models import (
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    PackageManager,
    ProjectSpec,
    TACConfig,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def tac_config() -> TACConfig:
    """Create a basic TACConfig for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="test-app",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
            framework=Framework.FASTAPI,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
    )


@pytest.fixture
def entity_spec() -> EntitySpec:
    """Create a sample EntitySpec with various field types."""
    return EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, indexed=True, max_length=50),
            FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
            FieldSpec(name="quantity", field_type=FieldType.INTEGER, required=True, default=0),
            FieldSpec(name="is_active", field_type=FieldType.BOOLEAN, required=True, default=True),
            FieldSpec(name="full_description", field_type=FieldType.TEXT, required=False),
        ],
    )


@pytest.fixture
def template_repo() -> TemplateRepository:
    """Create a TemplateRepository instance."""
    return TemplateRepository()


def make_context(entity: EntitySpec, config: TACConfig):
    """Create a template context with both entity and config."""
    return {"entity": entity, "config": config}


# ============================================================================
# TEST DOMAIN_ENTITY.PY.J2
# ============================================================================


def test_domain_entity_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that domain_entity.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/domain_entity.py.j2",
        make_context(entity_spec, tac_config),
    )

    # Verify basic structure
    assert "class Product(Entity):" in output
    assert 'type: str = Field(' in output
    assert 'default="product"' in output

    # Verify fields are present
    assert "sku: str" in output
    assert "price: Decimal" in output
    assert "quantity: int" in output
    assert "is_active: bool" in output
    assert "full_description: str | None" in output

    # Verify methods
    assert "def validate(self)" in output
    assert "def calculate_totals(self)" in output

    # Verify imports
    assert "from test_app.shared.domain.base_entity import Entity" in output
    assert "from decimal import Decimal" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_domain_entity_handles_nullable_fields(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that nullable fields are rendered correctly."""
    entity = EntitySpec(
        name="User",
        capability="auth",
        fields=[
            FieldSpec(name="username", field_type=FieldType.STRING, required=True),
            FieldSpec(name="bio", field_type=FieldType.TEXT, required=False),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/domain_entity.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Required field should not have | None
    assert "username: str" in output
    assert "username: str | None" not in output

    # Nullable field should have | None
    assert "bio: str | None" in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST SCHEMAS.PY.J2
# ============================================================================


def test_schemas_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that schemas.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/schemas.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify classes exist
    assert "class ProductCreate(BaseCreate):" in output
    assert "class ProductUpdate(BaseUpdate):" in output
    assert "class ProductResponse(BaseResponse):" in output

    # Verify imports
    assert (
        "from test_app.shared.schemas.base_schema import BaseCreate, BaseUpdate, BaseResponse"
        in output
    )
    assert "from decimal import Decimal" in output

    # Verify fields in Create schema
    assert "sku: str" in output
    assert "price: Decimal" in output

    # Verify all fields are optional in Update schema
    assert "Optional[" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_schemas_handles_optional_in_update(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that all fields in Update schema are Optional."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, required=True),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/schemas.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # In ProductUpdate, all fields should be Optional
    assert "class ProductUpdate(BaseUpdate):" in output
    assert "Optional[str]" in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST ORM_MODEL.PY.J2
# ============================================================================


def test_orm_model_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that orm_model.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/orm_model.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify class and table name
    assert "class ProductModel(Base):" in output
    assert '__tablename__ = "products"' in output

    # Verify SQLAlchemy imports
    assert "from sqlalchemy import Column" in output

    # Verify field mappings
    assert "sku = Column(String(50)" in output
    assert "price = Column(Numeric(precision=10, scale=2)" in output
    assert "quantity = Column(Integer" in output
    assert "is_active = Column(Boolean" in output
    assert "full_description = Column(Text" in output

    # Verify base entity fields
    assert "id = Column(String(36), primary_key=True" in output
    assert "created_at = Column(DateTime(timezone=True)" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_orm_model_creates_indexes(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that indexed fields generate indexes."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, indexed=True),
            FieldSpec(name="price", field_type=FieldType.DECIMAL, indexed=False),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/orm_model.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Should have __table_args__ with index
    assert "__table_args__" in output
    assert "Index('ix_products_sku', 'sku')" in output

    # Should not have index for price
    assert "ix_products_price" not in output

    compile(output, "<string>", "exec")


def test_orm_model_type_mapping(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that all FieldTypes map correctly to SQLAlchemy types."""
    entity = EntitySpec(
        name="AllTypes",
        capability="test",
        fields=[
            FieldSpec(name="str_field", field_type=FieldType.STRING),
            FieldSpec(name="int_field", field_type=FieldType.INTEGER),
            FieldSpec(name="float_field", field_type=FieldType.FLOAT),
            FieldSpec(name="bool_field", field_type=FieldType.BOOLEAN),
            FieldSpec(name="datetime_field", field_type=FieldType.DATETIME),
            FieldSpec(name="uuid_field", field_type=FieldType.UUID),
            FieldSpec(name="text_field", field_type=FieldType.TEXT),
            FieldSpec(name="decimal_field", field_type=FieldType.DECIMAL),
            FieldSpec(name="json_field", field_type=FieldType.JSON),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/orm_model.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Verify type mappings
    assert "str_field = Column(String(255)" in output
    assert "int_field = Column(Integer" in output
    assert "float_field = Column(Float" in output
    assert "bool_field = Column(Boolean" in output
    assert "datetime_field = Column(DateTime(timezone=True)" in output
    assert "uuid_field = Column(String(36)" in output
    assert "text_field = Column(Text" in output
    assert "decimal_field = Column(Numeric(precision=10, scale=2)" in output
    assert "json_field = Column(JSON" in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST REPOSITORY.PY.J2
# ============================================================================


def test_repository_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that repository.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/repository.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify class definition
    assert "class ProductRepository(BaseRepository[ProductModel]):" in output

    # Verify imports
    assert "from test_app.shared.repositories.base_repository import BaseRepository" in output
    assert "from .orm_model import ProductModel" in output

    # Verify constructor
    assert "def __init__(self, session: Session):" in output
    assert "super().__init__(session, ProductModel)" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_repository_generates_get_by_methods(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that get_by_X methods are generated for indexed fields."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, indexed=True),
            FieldSpec(name="barcode", field_type=FieldType.STRING, indexed=True),
            FieldSpec(name="price", field_type=FieldType.DECIMAL, indexed=False),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/repository.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Should have get_by methods for indexed fields
    assert "def get_by_sku(self, sku: str)" in output
    assert "def get_by_barcode(self, barcode: str)" in output

    # Should not have get_by method for non-indexed price
    assert "def get_by_price" not in output

    compile(output, "<string>", "exec")


def test_repository_generates_search_method(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that search method is generated when string fields exist."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="name", field_type=FieldType.STRING),
            FieldSpec(name="description", field_type=FieldType.TEXT),
            FieldSpec(name="price", field_type=FieldType.DECIMAL),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/repository.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Should have search method
    assert "def search(self, query: str" in output
    assert "ProductModel.name.ilike" in output
    assert "ProductModel.description.ilike" in output

    # Should not search non-string field
    assert "ProductModel.price.ilike" not in output

    compile(output, "<string>", "exec")


def test_repository_no_search_without_string_fields(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that search method is not generated without string fields."""
    entity = EntitySpec(
        name="Counter",
        capability="stats",
        fields=[
            FieldSpec(name="count", field_type=FieldType.INTEGER),
            FieldSpec(name="value", field_type=FieldType.DECIMAL),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_basic/repository.py.j2",
        {"entity": entity,
        'config': tac_config},
    )

    # Should not have search method
    assert "def search(self" not in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST SERVICE.PY.J2
# ============================================================================


def test_service_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that service.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/service.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify class definition with generics
    assert "class ProductService(BaseService[Product, ProductCreate, ProductUpdate]):" in output

    # Verify imports
    assert "from test_app.shared.services.base_service import BaseService" in output
    assert "from .domain import Product" in output
    assert "from .schemas import ProductCreate, ProductUpdate, ProductResponse" in output
    assert "from .repository import ProductRepository" in output

    # Verify constructor
    assert "def __init__(self, repository: ProductRepository):" in output

    # Verify business logic method
    assert "def apply_business_rules(self, entity: Product)" in output
    assert "entity.validate()" in output
    assert "entity.calculate_totals()" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


# ============================================================================
# TEST ROUTES.PY.J2
# ============================================================================


def test_routes_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that routes.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_basic/routes.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify router definition
    assert 'router = APIRouter(prefix="/products", tags=["products"])' in output

    # Verify imports
    assert "from fastapi import APIRouter, Depends, HTTPException, status" in output
    assert "from test_app.shared.dependencies import get_db" in output

    # Verify all 5 CRUD endpoints exist
    assert "async def create_product(" in output
    assert "async def get_product(" in output
    assert "async def list_products(" in output
    assert "async def update_product(" in output
    assert "async def delete_product(" in output

    # Verify status codes
    assert "status_code=status.HTTP_201_CREATED" in output
    assert "status_code=status.HTTP_200_OK" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_routes_has_correct_endpoints(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that routes have correct HTTP methods and paths."""
    output = template_repo.render(
        "capabilities/crud_basic/routes.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # POST /products/
    assert '@router.post(\n    "/",' in output

    # GET /products/{id}
    assert '@router.get(\n    "/{id}",' in output

    # GET /products/
    assert '@router.get(\n    "/",' in output

    # PUT /products/{id}
    assert '@router.put(\n    "/{id}",' in output

    # DELETE /products/{id}
    assert '@router.delete(\n    "/{id}",' in output

    compile(output, "<string>", "exec")


def test_routes_has_dependency_injection(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that routes use dependency injection for service."""
    output = template_repo.render(
        "capabilities/crud_basic/routes.py.j2",
        {"entity": entity_spec,
        'config': tac_config},
    )

    # Verify service factory
    assert "def get_product_service(db = Depends(get_db)) -> ProductService:" in output
    assert "repository = ProductRepository(db)" in output
    assert "return ProductService(repository)" in output

    # Verify endpoints use dependency
    assert "service: ProductService = Depends(get_product_service)" in output

    compile(output, "<string>", "exec")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


def test_all_templates_render_with_minimal_entity(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that all templates render successfully with a minimal entity."""
    minimal_entity = EntitySpec(
        name="SimpleEntity",
        capability="test",
        fields=[
            FieldSpec(name="value", field_type=FieldType.STRING),
        ],
    )

    templates = [
        "capabilities/crud_basic/domain_entity.py.j2",
        "capabilities/crud_basic/schemas.py.j2",
        "capabilities/crud_basic/orm_model.py.j2",
        "capabilities/crud_basic/repository.py.j2",
        "capabilities/crud_basic/service.py.j2",
        "capabilities/crud_basic/routes.py.j2",
    ]

    for template in templates:
        output = template_repo.render(
            template,
            {"entity": minimal_entity,
            'config': tac_config},
        )
        # Verify Python syntax is valid
        compile(output, "<string>", "exec")


def test_entity_spec_snake_name_conversion():
    """Test EntitySpec property conversions."""
    entity = EntitySpec(
        name="ProductCategory",
        capability="catalog",
        fields=[
            FieldSpec(name="title", field_type=FieldType.STRING),
        ],
    )

    assert entity.snake_name == "product_category"
    assert entity.plural_name == "product_categorys"  # Simple pluralization
    assert entity.table_name == "product_categorys"


def test_field_spec_validation():
    """Test FieldSpec validation."""
    # Valid field
    field = FieldSpec(name="valid_name", field_type=FieldType.STRING)
    assert field.name == "valid_name"

    # Test invalid format (snake_case validation)
    with pytest.raises(ValueError, match="snake_case"):
        FieldSpec(name="InvalidName", field_type=FieldType.STRING)

    # Test Python keyword rejection
    with pytest.raises(ValueError, match="reserved keyword"):
        FieldSpec(name="class", field_type=FieldType.STRING)

    # Test SQLAlchemy conflict rejection
    with pytest.raises(ValueError, match="conflicts with SQLAlchemy"):
        FieldSpec(name="metadata", field_type=FieldType.STRING)


def test_entity_spec_validation():
    """Test EntitySpec validation."""
    # Valid entity
    entity = EntitySpec(
        name="ValidName",
        capability="valid-capability",
        fields=[
            FieldSpec(name="field1", field_type=FieldType.STRING),
        ],
    )
    assert entity.name == "ValidName"

    # Test PascalCase validation
    with pytest.raises(ValueError, match="PascalCase"):
        EntitySpec(
            name="invalid_name",
            capability="test",
            fields=[FieldSpec(name="field1", field_type=FieldType.STRING)],
        )

    # Test kebab-case capability validation
    with pytest.raises(ValueError, match="kebab-case"):
        EntitySpec(
            name="ValidName",
            capability="Invalid_Capability",
            fields=[FieldSpec(name="field1", field_type=FieldType.STRING)],
        )

    # Test empty fields validation
    with pytest.raises(ValueError, match="at least one field"):
        EntitySpec(
            name="ValidName",
            capability="test",
            fields=[],
        )

    # Test reserved field names validation (happens at EntitySpec level)
    with pytest.raises(ValueError, match="reserved"):
        EntitySpec(
            name="ValidName",
            capability="test",
            fields=[FieldSpec(name="id", field_type=FieldType.STRING)],
        )

    with pytest.raises(ValueError, match="reserved"):
        EntitySpec(
            name="ValidName",
            capability="test",
            fields=[FieldSpec(name="created_at", field_type=FieldType.DATETIME)],
        )
