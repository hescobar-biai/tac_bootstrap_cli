"""
Tests for authorized CRUD templates.

Comprehensive unit tests for validating that the 3 templates in
`tac_bootstrap/templates/capabilities/crud_authorized/` render correctly,
generate valid Python code, and include proper multi-tenant authorization logic.
"""

from types import SimpleNamespace

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
    """Create a sample EntitySpec with authorized=True."""
    return EntitySpec(
        name="Product",
        capability="catalog",
        authorized=True,
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, indexed=True, max_length=50),
            FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
            FieldSpec(name="quantity", field_type=FieldType.INTEGER, required=True, default=0),
            FieldSpec(name="description", field_type=FieldType.TEXT, required=False),
        ],
    )


@pytest.fixture
def template_repo() -> TemplateRepository:
    """Create a TemplateRepository instance."""
    return TemplateRepository()


def make_context(entity: EntitySpec, config: TACConfig):
    """Create a template context with both entity and config."""
    return SimpleNamespace(entity=entity, config=config)


# ============================================================================
# TEST REPOSITORY_AUTHORIZED.PY.J2
# ============================================================================


def test_repository_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that repository_authorized.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
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


def test_repository_authorized_has_org_filter_in_get_by_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that get_by_id filters by organization_id."""
    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify method signature includes organization_id
    assert "def get_by_id(self, id: str, organization_id: str)" in output

    # Verify organization filter is applied
    assert "ProductModel.organization_id == organization_id" in output

    # Verify TODO comment for audit logging
    assert "TODO: Add audit logging for authorization failures" in output

    compile(output, "<string>", "exec")


def test_repository_authorized_has_org_filter_in_get_all(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that get_all filters by organization_id."""
    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify method signature includes organization_id
    assert "def get_all(self, skip: int, limit: int, organization_id: str)" in output

    # Verify organization filter is applied
    assert "ProductModel.organization_id == organization_id" in output

    compile(output, "<string>", "exec")


def test_repository_authorized_update_validates_ownership(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that update method validates organization ownership."""
    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify update signature includes organization_id
    assert "def update(self, id: str, data: dict, organization_id: str)" in output

    # Verify ownership validation via organization filter
    assert "ProductModel.organization_id == organization_id" in output

    # Verify returns None if not found
    assert "if not entity:" in output
    assert "return None" in output

    compile(output, "<string>", "exec")


def test_repository_authorized_delete_validates_ownership(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that delete method validates organization ownership."""
    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify delete signature includes organization_id
    assert "def delete(self, id: str, organization_id: str)" in output

    # Verify ownership validation
    assert "ProductModel.organization_id == organization_id" in output

    # Verify soft delete
    assert "entity.state = 2" in output

    compile(output, "<string>", "exec")


def test_repository_authorized_indexed_fields_have_org_filter(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that get_by_X methods for indexed fields filter by organization."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        authorized=True,
        fields=[
            FieldSpec(name="sku", field_type=FieldType.STRING, indexed=True),
            FieldSpec(name="barcode", field_type=FieldType.STRING, indexed=True),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity, "config": tac_config},
    )

    # Should have get_by methods with organization_id parameter
    assert "def get_by_sku(self, sku: str, organization_id: str)" in output
    assert "def get_by_barcode(self, barcode: str, organization_id: str)" in output

    # Should filter by organization_id
    assert "ProductModel.organization_id == organization_id" in output

    compile(output, "<string>", "exec")


def test_repository_authorized_search_has_org_filter(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that search method filters by organization_id."""
    entity = EntitySpec(
        name="Product",
        capability="catalog",
        authorized=True,
        fields=[
            FieldSpec(name="name", field_type=FieldType.STRING),
            FieldSpec(name="description", field_type=FieldType.TEXT),
        ],
    )

    output = template_repo.render(
        "capabilities/crud_authorized/repository_authorized.py.j2",
        {"entity": entity, "config": tac_config},
    )

    # Should have search method with organization_id
    assert "def search(self, query: str, skip: int, limit: int, organization_id: str)" in output

    # Should filter by organization_id
    assert "ProductModel.organization_id == organization_id" in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST SERVICE_AUTHORIZED.PY.J2
# ============================================================================


def test_service_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that service_authorized.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify class definition with generics
    assert "class ProductService(BaseService[Product, ProductCreate, ProductUpdate]):" in output

    # Verify imports
    assert "from test_app.shared.services.base_service import BaseService" in output
    assert "from .domain import Product" in output
    assert "from .schemas import ProductCreate, ProductUpdate, ProductResponse" in output
    assert "from .repository import ProductRepository" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_service_authorized_create_sets_organization_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that create method sets organization_id and created_by."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify create signature includes user_id and organization_id
    assert "def create(self, data: ProductCreate, user_id: str, organization_id: str)" in output

    # Verify organization_id and created_by are set
    assert "data_dict['organization_id'] = organization_id" in output
    assert "data_dict['created_by'] = user_id" in output

    # Verify comment about security
    assert "critical for security" in output or "never trust client" in output

    compile(output, "<string>", "exec")


def test_service_authorized_get_by_id_passes_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that get_by_id passes organization_id to repository."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify signature includes organization_id
    assert "def get_by_id(self, id: str, organization_id: str)" in output

    # Verify it's passed to repository
    assert "self.repository.get_by_id(id, organization_id)" in output

    compile(output, "<string>", "exec")


def test_service_authorized_get_all_passes_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that get_all passes organization_id to repository."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify signature includes organization_id
    assert "def get_all(self, skip: int, limit: int, organization_id: str)" in output

    # Verify it's passed to repository
    assert "self.repository.get_all(skip, limit, organization_id)" in output

    compile(output, "<string>", "exec")


def test_service_authorized_update_passes_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that update passes organization_id to repository."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify signature includes organization_id
    assert "def update(self, id: str, data: ProductUpdate, organization_id: str)" in output

    # Verify it's passed to repository
    assert "self.repository.update(id, update_dict, organization_id)" in output

    compile(output, "<string>", "exec")


def test_service_authorized_soft_delete_passes_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that soft_delete passes organization_id to repository."""
    output = template_repo.render(
        "capabilities/crud_authorized/service_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify signature includes organization_id
    assert "def soft_delete(self, id: str, organization_id: str)" in output

    # Verify it's passed to repository
    assert "self.repository.delete(id, organization_id)" in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST ROUTES_AUTHORIZED.PY.J2
# ============================================================================


def test_routes_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that routes_authorized.py.j2 renders valid Python."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify router definition
    assert 'router = APIRouter(prefix="/products", tags=["products"])' in output

    # Verify imports
    assert "from fastapi import APIRouter, Depends, HTTPException, status, Header" in output
    assert "from test_app.shared.dependencies import get_db" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_routes_authorized_has_current_user_model(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that CurrentUser model is defined."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify CurrentUser model
    assert "class CurrentUser(BaseModel):" in output
    assert "user_id: str" in output
    assert "organization_id: str" in output

    compile(output, "<string>", "exec")


def test_routes_authorized_has_get_current_user_dependency(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that get_current_user dependency is defined."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify dependency function
    assert "def get_current_user(authorization: str = Header(...))" in output

    # Verify it extracts Bearer token
    assert 'authorization.startswith("Bearer ")' in output

    # Verify JWT decoding
    assert "jwt.decode" in output

    # Verify TODO comments for production implementation
    assert "TODO: Replace mock JWT validation" in output or "TODO: Use proper JWT secret" in output

    # Verify 401 error handling
    assert "HTTPException" in output
    assert "status.HTTP_401_UNAUTHORIZED" in output

    compile(output, "<string>", "exec")


def test_routes_authorized_all_endpoints_have_current_user(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that all endpoints inject current_user dependency."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # All CRUD endpoints should exist
    assert "async def create_product(" in output
    assert "async def get_product(" in output
    assert "async def list_products(" in output
    assert "async def update_product(" in output
    assert "async def delete_product(" in output

    # Count current_user dependency injections (should be 5 endpoints)
    current_user_count = output.count("current_user: CurrentUser = Depends(get_current_user)")
    assert current_user_count == 5, (
        f"Expected 5 endpoints with current_user, found {current_user_count}"
    )

    compile(output, "<string>", "exec")


def test_routes_authorized_create_passes_user_context(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that create endpoint passes user_id and organization_id to service."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify create passes user context
    assert "service.create(data, current_user.user_id, current_user.organization_id)" in output

    compile(output, "<string>", "exec")


def test_routes_authorized_endpoints_pass_organization_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that read/update/delete endpoints pass organization_id to service."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify get_by_id passes organization_id
    assert "service.get_by_id(id, current_user.organization_id)" in output

    # Verify get_all passes organization_id
    assert "organization_id=current_user.organization_id" in output

    # Verify update passes organization_id
    assert "service.update(id, data, current_user.organization_id)" in output

    # Verify delete passes organization_id
    assert "service.soft_delete(id, current_user.organization_id)" in output

    compile(output, "<string>", "exec")


def test_routes_authorized_returns_404_not_403(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that routes return 404 instead of 403 to prevent information leakage."""
    output = template_repo.render(
        "capabilities/crud_authorized/routes_authorized.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Should raise 404 when entity not found
    assert 'raise HTTPException(status_code=404, detail="Product not found")' in output

    # Should NOT have 403 status code
    assert "status_code=403" not in output
    assert "status.HTTP_403_FORBIDDEN" not in output

    # Should have comment about preventing information leakage
    assert "prevent information leakage" in output or "prevents information leakage" in output

    compile(output, "<string>", "exec")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


def test_all_authorized_templates_render_with_minimal_entity(
    template_repo: TemplateRepository, tac_config: TACConfig
):
    """Test that all authorized templates render successfully with a minimal entity."""
    minimal_entity = EntitySpec(
        name="SimpleEntity",
        capability="test",
        authorized=True,
        fields=[
            FieldSpec(name="value", field_type=FieldType.STRING),
        ],
    )

    templates = [
        "capabilities/crud_authorized/repository_authorized.py.j2",
        "capabilities/crud_authorized/service_authorized.py.j2",
        "capabilities/crud_authorized/routes_authorized.py.j2",
    ]

    for template in templates:
        output = template_repo.render(
            template,
            {"entity": minimal_entity, "config": tac_config},
        )
        # Verify Python syntax is valid
        compile(output, "<string>", "exec")


def test_authorized_templates_render_valid_python(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that all authorized templates compile to valid Python."""
    templates = [
        "capabilities/crud_authorized/repository_authorized.py.j2",
        "capabilities/crud_authorized/service_authorized.py.j2",
        "capabilities/crud_authorized/routes_authorized.py.j2",
        "capabilities/crud_authorized/domain_entity.py.j2",
        "capabilities/crud_authorized/schemas.py.j2",
        "capabilities/crud_authorized/orm_model.py.j2",
    ]

    for template in templates:
        output = template_repo.render(
            template,
            {"entity": entity_spec, "config": tac_config},
        )
        # This will raise SyntaxError if Python is invalid
        compile(output, f"<{template}>", "exec")


# ============================================================================
# TEST DOMAIN_ENTITY.PY.J2 (AUTHORIZED)
# ============================================================================


def test_domain_entity_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that domain_entity.py.j2 renders valid Python for authorized mode."""
    output = template_repo.render(
        "capabilities/crud_authorized/domain_entity.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify class definition
    assert "class Product(Entity):" in output

    # Verify imports
    assert "from test_app.shared.domain.base_entity import Entity" in output

    # Verify fields are present
    assert "sku:" in output
    assert "price:" in output

    # Verify validation method validates organization_id
    assert "def validate(self)" in output
    assert "organization_id" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_domain_entity_authorized_validates_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that domain entity validate method checks organization_id."""
    output = template_repo.render(
        "capabilities/crud_authorized/domain_entity.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Should validate organization_id is set
    assert "if not self.organization_id:" in output
    assert 'raise ValueError("organization_id is required' in output

    compile(output, "<string>", "exec")


# ============================================================================
# TEST SCHEMAS.PY.J2 (AUTHORIZED)
# ============================================================================


def test_schemas_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that schemas.py.j2 renders valid Python for authorized mode."""
    output = template_repo.render(
        "capabilities/crud_authorized/schemas.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify schema class definitions
    assert "class ProductCreate(BaseCreate):" in output
    assert "class ProductUpdate(BaseUpdate):" in output
    assert "class ProductResponse(BaseResponse):" in output
    # Verify imports
    assert (
        "from test_app.shared.schemas.base_schema import BaseCreate, BaseUpdate, BaseResponse"
        in output
    )
    # Verify imports
    assert (
        "from test_app.shared.schemas.base_schema import "
        "BaseCreate, BaseUpdate, BaseResponse"
    ) in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_schemas_authorized_create_excludes_org_fields(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that Create schema doesn't include organization_id or created_by."""
    output = template_repo.render(
        "capabilities/crud_authorized/schemas.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Find the ProductCreate class
    create_class_start = output.find("class ProductCreate(BaseCreate):")
    update_class_start = output.find("class ProductUpdate(BaseUpdate):")
    create_section = output[create_class_start:update_class_start]

    # Create schema should NOT have organization_id or created_by fields
    # (these are in the docstring but not as field definitions)
    assert "organization_id:" not in create_section or "NOT in this schema" in create_section
    assert "created_by:" not in create_section

    # Should have comment about server-side injection
    assert "injected server-side" in output or "set server-side" in output

    compile(output, "<string>", "exec")


def test_schemas_authorized_update_excludes_org_fields(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that Update schema doesn't include organization_id or created_by."""
    output = template_repo.render(
        "capabilities/crud_authorized/schemas.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Find the ProductUpdate class
    update_class_start = output.find("class ProductUpdate(BaseUpdate):")
    response_class_start = output.find("class ProductResponse(BaseResponse):")
    update_section = output[update_class_start:response_class_start]

    # Update schema should NOT have organization_id or created_by fields
    assert "organization_id:" not in update_section
    assert "created_by:" not in update_section

    compile(output, "<string>", "exec")


# ============================================================================
# TEST ORM_MODEL.PY.J2 (AUTHORIZED)
# ============================================================================


def test_orm_model_authorized_renders(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that orm_model.py.j2 renders valid Python for authorized mode."""
    output = template_repo.render(
        "capabilities/crud_authorized/orm_model.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Verify model class definition
    assert "class ProductModel(Base):" in output

    # Verify table name
    assert '__tablename__ = "products"' in output

    # Verify imports
    assert "from sqlalchemy import Column" in output

    # Verify Python syntax is valid
    compile(output, "<string>", "exec")


def test_orm_model_authorized_has_required_org_id(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that organization_id is required (required=True) in authorized mode."""
    output = template_repo.render(
        "capabilities/crud_authorized/orm_model.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # organization_id should be nullable=False (required) and indexed
    assert "organization_id = Column(String(100), nullable=False, index=True)" in output

    # Should have comment about multi-tenancy
    assert "REQUIRED for authorized entities" in output or "Required and indexed" in output

    compile(output, "<string>", "exec")


def test_orm_model_authorized_has_required_created_by(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that created_by is required (required=True) in authorized mode."""
    output = template_repo.render(
        "capabilities/crud_authorized/orm_model.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # created_by should be nullable=False (required)
    assert "created_by = Column(String(255), nullable=False)" in output

    # Should have comment about multi-tenancy
    assert "Required for multi-tenant" in output

    compile(output, "<string>", "exec")


def test_orm_model_authorized_has_org_indexes(
    template_repo: TemplateRepository, entity_spec: EntitySpec, tac_config: TACConfig
):
    """Test that ORM model has proper indexes for organization queries."""
    output = template_repo.render(
        "capabilities/crud_authorized/orm_model.py.j2",
        {"entity": entity_spec, "config": tac_config},
    )

    # Should have organization_id index
    assert "ix_products_organization_id" in output

    # Should have composite index for org + state
    assert "ix_products_org_state" in output

    # Should have composite indexes for org + indexed fields
    assert "ix_products_org_sku" in output  # sku is indexed in entity_spec

    compile(output, "<string>", "exec")
