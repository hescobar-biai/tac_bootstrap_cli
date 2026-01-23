# Schemas Template (DTOs)

Template for creating request/response schemas (Data Transfer Objects).

## Usage

Replace placeholders:
- `{{EntityName}}` - PascalCase entity name (e.g., `Product`)
- `{{capability}}` - snake_case capability name (e.g., `product_catalog`)
- `{{create_fields}}` - Entity-specific fields for creation
- `{{update_fields}}` - Entity-specific fields (all optional) for updates
- `{{response_fields}}` - Entity-specific fields for response

## Template

```python
"""
IDK: dto, schema, {{entity_name}}-dto

Module: schemas

Responsibility:
- Define request/response DTOs for {{EntityName}}
- Validate input data for create/update operations
- Structure response data for API endpoints
- Enforce field-level validation rules

Invariants:
- Create schema requires code and name
- Update schema has all fields optional
- Response schema includes all entity fields
- Validation errors raise Pydantic ValidationError

Related Docs:
- docs/{{capability}}/application/schemas.md
- docs/shared/application/base-schema.md
"""

from pydantic import Field
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse


class {{EntityName}}Create(BaseCreate):
    """
    IDK: dto, create-schema, input-validation

    Responsibility:
    - Validate {{EntityName}} creation input
    - Define required fields for new entities
    - Enforce field constraints and business rules

    Invariants:
    - code and name are required (inherited from BaseCreate)
    - Entity-specific required fields must be provided
    - All validation rules must pass

    Inherited Fields:
    - code (str): required, business identifier
    - name (str): required, display name
    - description (str | None): optional description

    Fields:
    - {{create_fields}}

    Related Docs:
    - docs/{{capability}}/application/schemas.md
    """

    # Entity-specific required fields
    {{create_fields}}


class {{EntityName}}Update(BaseUpdate):
    """
    IDK: dto, update-schema, partial-update

    Responsibility:
    - Validate {{EntityName}} update input
    - Allow partial updates (all fields optional)
    - Enforce field constraints

    Invariants:
    - All fields are optional
    - Only provided fields will be updated
    - Validation applies to provided fields only

    Inherited Fields:
    - name (str | None): optional name update
    - description (str | None): optional description update

    Fields:
    - {{update_fields}}

    Related Docs:
    - docs/{{capability}}/application/schemas.md
    """

    # Entity-specific fields (all optional)
    {{update_fields}}


class {{EntityName}}Response(BaseResponse):
    """
    IDK: dto, response-schema, api-response

    Responsibility:
    - Structure {{EntityName}} data for API responses
    - Include all entity fields in response
    - Support serialization from ORM models

    Invariants:
    - Contains all base entity fields
    - Contains all entity-specific fields
    - Can be constructed from ORM models

    Inherited Fields:
    - id, code, name, description, type
    - created_at, created_by, updated_at, updated_by
    - state, status, version
    - organization_id, project_id, owner

    Fields:
    - {{response_fields}}

    Related Docs:
    - docs/{{capability}}/application/schemas.md
    """

    # Entity-specific fields
    {{response_fields}}
```

## Example: Product Schemas

```python
"""
IDK: dto, schema, product-dto

Module: schemas

Responsibility:
- Define Product request/response DTOs
- Validate product creation and update data
- Structure product API responses
- Enforce product field validation

Invariants:
- SKU and unit_price required for creation
- Update allows partial field updates
- Response includes all product fields
- Validation enforces business constraints

Related Docs:
- docs/product_catalog/application/schemas.md
"""

from pydantic import Field
from shared.application.base_schema import BaseCreate, BaseUpdate, BaseResponse


class ProductCreate(BaseCreate):
    """
    IDK: dto, create-schema, input-validation, product-creation

    Responsibility:
    - Validate product creation input
    - Require SKU and unit_price
    - Enforce field constraints (price >= 0, etc.)
    - Support optional fields with defaults

    Invariants:
    - code and name required (from BaseCreate)
    - sku required and 1-50 characters
    - unit_price required and >= 0
    - stock_quantity defaults to 0 and >= 0
    - is_available defaults to True

    Inherited Fields:
    - code (str): required business code
    - name (str): required product name
    - description (str | None): optional description

    Fields:
    - sku (str): stock keeping unit, required, 1-50 chars
    - unit_price (float): price per unit, required, >= 0
    - category (str | None): product category, optional
    - brand (str | None): product brand, optional
    - is_available (bool): availability flag, default True
    - stock_quantity (int): inventory count, default 0, >= 0
    - tags (list[str]): product tags, default empty list

    Related Docs:
    - docs/product_catalog/application/schemas.md
    - docs/product_catalog/domain/product.md
    """

    # Product-specific required fields
    sku: str = Field(..., min_length=1, max_length=50, description="Stock Keeping Unit")
    unit_price: float = Field(..., ge=0, description="Price per unit")

    # Product-specific optional fields
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool = Field(default=True)
    stock_quantity: int = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list)


class ProductUpdate(BaseUpdate):
    """
    IDK: dto, update-schema, partial-update, product-update

    Responsibility:
    - Validate product update input
    - Allow partial field updates
    - Enforce field constraints on provided values

    Invariants:
    - All fields optional (partial update)
    - Validation applies to non-None fields
    - sku if provided: 1-50 characters
    - unit_price if provided: >= 0
    - stock_quantity if provided: >= 0

    Inherited Fields:
    - name (str | None): optional name update
    - description (str | None): optional description update

    Fields:
    - sku (str | None): optional SKU update
    - unit_price (float | None): optional price update
    - category (str | None): optional category update
    - brand (str | None): optional brand update
    - is_available (bool | None): optional availability update
    - stock_quantity (int | None): optional stock update
    - tags (list[str] | None): optional tags update

    Related Docs:
    - docs/product_catalog/application/schemas.md
    """

    sku: str | None = Field(default=None, min_length=1, max_length=50)
    unit_price: float | None = Field(default=None, ge=0)
    category: str | None = None
    brand: str | None = None
    is_available: bool | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    tags: list[str] | None = None


class ProductResponse(BaseResponse):
    """
    IDK: dto, response-schema, api-response, product-response

    Responsibility:
    - Structure product data for API responses
    - Include all product fields
    - Support ORM model serialization
    - Provide complete product representation

    Invariants:
    - Contains all base entity fields
    - Contains all product-specific fields
    - Can serialize from ProductModel ORM
    - All fields properly typed

    Inherited Fields:
    - id, code, name, description, type
    - created_at, created_by, updated_at, updated_by
    - state, status, version
    - organization_id, project_id, owner

    Fields:
    - sku (str): stock keeping unit
    - unit_price (float): price per unit
    - category (str | None): product category
    - brand (str | None): product brand
    - is_available (bool): availability status
    - stock_quantity (int): current inventory
    - tags (list[str]): product tags

    Related Docs:
    - docs/product_catalog/application/schemas.md
    - docs/product_catalog/domain/product.md
    """

    # Product-specific fields
    sku: str
    unit_price: float
    category: str | None
    brand: str | None
    is_available: bool
    stock_quantity: int
    tags: list[str]
```

## Validation Patterns

### Field Constraints

```python
from pydantic import Field, field_validator, EmailStr
from shared.application.base_schema import BaseCreate

class ExampleCreate(BaseCreate):
    """
    IDK: dto, validation, field-constraints

    Responsibility:
    - Demonstrate validation patterns
    - Enforce field-level constraints
    - Provide validation examples
    """

    # String constraints
    reference: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Z0-9-]+$",
        description="Uppercase alphanumeric reference"
    )

    # Numeric constraints
    price: float = Field(..., ge=0, le=1000000, description="Price between 0 and 1M")
    quantity: int = Field(default=0, ge=0, le=999999, description="Quantity 0-999999")

    # Email validation
    email: EmailStr | None = Field(default=None, description="Valid email address")

    # Custom validator
    @field_validator('reference')
    @classmethod
    def validate_reference(cls, v: str) -> str:
        """
        IDK: custom-validation, business-rule

        Responsibility:
        - Validate reference format
        - Enforce uppercase requirement

        Invariants:
        - Reference must be uppercase
        - Raises ValueError if not uppercase
        """
        if not v.isupper():
            raise ValueError('Reference must be uppercase')
        return v
```

### Cross-Field Validation

```python
from pydantic import model_validator

class DateRangeCreate(BaseCreate):
    """
    IDK: dto, cross-field-validation, date-range

    Responsibility:
    - Validate date range
    - Ensure start before end
    """

    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def validate_date_range(self) -> 'DateRangeCreate':
        """
        IDK: validation, date-range, business-rule

        Responsibility:
        - Ensure start_date before end_date
        - Validate logical date ordering

        Failure Modes:
        - ValueError: start_date >= end_date
        """
        if self.start_date >= self.end_date:
            raise ValueError('start_date must be before end_date')
        return self
```

## Using Paginated Response

```python
from fastapi import APIRouter, Query, Depends
from shared.application.base_schema import PaginatedResponse
from .schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    """
    IDK: http-endpoint, pagination, product-list

    Responsibility:
    - List products with pagination
    - Return structured paginated response

    Outputs:
    - PaginatedResponse[ProductResponse]: paginated products
    """
    result = service.get_all(page=page, page_size=page_size)
    return result
```

## Common Field Types

| Type | Pydantic Field | Example | Validation |
|------|---------------|---------|------------|
| Required string | `str` | `name: str` | Non-empty by default |
| Optional string | `str \| None` | `category: str \| None = None` | Can be None |
| Constrained string | `str = Field(...)` | `code: str = Field(min_length=1, max_length=50)` | Length limits |
| Pattern string | `str = Field(pattern=...)` | `ref: str = Field(pattern=r'^[A-Z]+$')` | Regex match |
| Email | `EmailStr` | `email: EmailStr` | Valid email format |
| Integer | `int` | `quantity: int` | Whole number |
| Constrained int | `int = Field(...)` | `age: int = Field(ge=0, le=120)` | Range limits |
| Float | `float` | `price: float` | Decimal number |
| Constrained float | `float = Field(...)` | `price: float = Field(ge=0)` | >= 0 |
| Boolean | `bool` | `is_active: bool = True` | True/False |
| List | `list[str]` | `tags: list[str] = []` | Array of strings |
| Dict | `dict` | `metadata: dict = {}` | Key-value pairs |
| DateTime | `datetime` | `scheduled_at: datetime` | ISO 8601 datetime |

## Best Practices

1. **Use BaseCreate/BaseUpdate/BaseResponse** - Don't redefine common fields
2. **Add Field descriptions** - Help API documentation and users
3. **Validate at schema level** - Catch issues before business logic
4. **Use type hints** - Enable IDE autocomplete and type checking
5. **Default values** - Provide sensible defaults for optional fields
6. **Constraints** - Use Field() for min/max, patterns, ranges
7. **Custom validators** - Implement complex business rule validation

## Anti-Patterns to Avoid

**Don't redefine base fields:**
```python
# BAD: Redefining inherited fields
class ProductCreate(BaseCreate):
    code: str  # Already in BaseCreate
    name: str  # Already in BaseCreate
    sku: str

# GOOD: Only add new fields
class ProductCreate(BaseCreate):
    sku: str  # Only product-specific fields
```

**Don't skip validation:**
```python
# BAD: No constraints
class ProductCreate(BaseCreate):
    unit_price: float  # Could be negative!

# GOOD: Add appropriate constraints
class ProductCreate(BaseCreate):
    unit_price: float = Field(..., ge=0, description="Must be non-negative")
```

**Don't make update fields required:**
```python
# BAD: Required fields in update schema
class ProductUpdate(BaseUpdate):
    sku: str  # Forces client to send all fields

# GOOD: All fields optional for partial update
class ProductUpdate(BaseUpdate):
    sku: str | None = None  # Optional for partial update
```

## Testing Schemas

```python
# tests/unit/{{capability}}/application/test_schemas.py
import pytest
from pydantic import ValidationError
from {{capability}}.application.schemas import (
    {{EntityName}}Create,
    {{EntityName}}Update,
    {{EntityName}}Response,
)


def test_create_schema_valid():
    """Test valid create schema."""
    data = {
        "code": "PROD-001",
        "name": "Test Product",
        "sku": "SKU-001",
        "unit_price": 99.99,
    }
    schema = ProductCreate(**data)
    assert schema.code == "PROD-001"
    assert schema.unit_price == 99.99


def test_create_schema_missing_required():
    """Test create schema rejects missing required fields."""
    data = {
        "code": "PROD-001",
        # Missing name (required from BaseCreate)
        # Missing sku (required)
    }
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(**data)

    errors = exc_info.value.errors()
    field_names = {error['loc'][0] for error in errors}
    assert 'name' in field_names
    assert 'sku' in field_names


def test_create_schema_invalid_constraint():
    """Test create schema validates field constraints."""
    data = {
        "code": "PROD-001",
        "name": "Test Product",
        "sku": "SKU-001",
        "unit_price": -10.0,  # Invalid: negative price
    }
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(**data)

    errors = exc_info.value.errors()
    assert any(error['loc'][0] == 'unit_price' for error in errors)


def test_update_schema_partial():
    """Test update schema allows partial updates."""
    data = {"unit_price": 89.99}  # Only updating price
    schema = ProductUpdate(**data)
    assert schema.unit_price == 89.99
    assert schema.name is None  # Not provided


def test_response_schema_from_orm():
    """Test response schema from ORM model."""
    from {{capability}}.infrastructure.models import ProductModel

    model = ProductModel(
        id="test-id",
        code="PROD-001",
        name="Test Product",
        sku="SKU-001",
        unit_price=99.99,
        state=1,
    )

    response = ProductResponse.model_validate(model)
    assert response.code == "PROD-001"
    assert response.sku == "SKU-001"
```
