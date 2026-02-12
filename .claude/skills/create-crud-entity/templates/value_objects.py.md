# Value Objects Template

Template for creating immutable value objects that encapsulate domain concepts.

## Overview

Value objects:
- Are **immutable** - once created, they cannot be changed
- Have **no identity** - equality is based on all attributes, not an ID
- Encapsulate **domain concepts** with validation
- Are **self-validating** - invalid states cannot be created

## Directory Structure

```
src/
└── {capability}/
    └── domain/
        ├── {entity}.py
        └── value_objects.py    # Value objects for this capability
```

---

## Value Object Template

**File**: `src/{capability}/domain/value_objects.py`

```python
"""
IDK: value-object, immutable, self-validating, domain-concept

Module: value_objects

Responsibility:
- Define immutable value objects for domain
- Encapsulate validation logic
- Provide type-safe domain concepts
- Prevent invalid states

Invariants:
- All value objects are frozen (immutable)
- Validation via model_validator
- Equality based on all attributes
- No identity field

Related Docs:
- docs/{{capability}}/domain/value-objects.md
- docs/architecture/ddd-patterns.md
"""

from typing import Self
import re
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Email(BaseModel):
    """
    IDK: value-object, email-validation, immutable

    Responsibility:
    - Represent valid email address
    - Validate email format
    - Provide domain/local part access

    Invariants:
    - address matches email regex pattern
    - Immutable after creation
    - Cannot be empty

    Failure Modes:
    - ValueError: invalid email format

    Usage:
        email = Email(address="user@example.com")
        print(email.address)  # user@example.com
        print(email.domain)   # example.com
    """

    model_config = ConfigDict(frozen=True)

    address: str

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate email format."""
        if not self.address:
            raise ValueError("Email address cannot be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.address):
            raise ValueError(f"Invalid email format: {self.address}")

        return self

    @property
    def domain(self) -> str:
        """Get email domain."""
        return self.address.split("@")[1]

    @property
    def local_part(self) -> str:
        """Get local part (before @)."""
        return self.address.split("@")[0]

    def __str__(self) -> str:
        return self.address


class Money(BaseModel):
    """
    Money value object with currency.

    Usage:
        price = Money(amount=Decimal("99.99"), currency="USD")
        total = price + Money(amount=Decimal("10.00"), currency="USD")
    """

    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: str = "USD"

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: dict) -> dict:
        """Normalize money values before validation."""
        if isinstance(data, dict):
            if "amount" in data and not isinstance(data["amount"], Decimal):
                data["amount"] = Decimal(str(data["amount"]))
            if "currency" in data:
                data["currency"] = str(data["currency"]).upper()
        return data

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate money values."""
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter ISO code")

        return self

    def __add__(self, other: "Money") -> "Money":
        """Add two money values."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        """Subtract money values."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} and {other.currency}")
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __mul__(self, factor: int | float | Decimal) -> "Money":
        """Multiply by a factor."""
        return Money(amount=self.amount * Decimal(str(factor)), currency=self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    @classmethod
    def zero(cls, currency: str = "USD") -> "Money":
        """Create zero money."""
        return cls(amount=Decimal("0"), currency=currency)


class PhoneNumber(BaseModel):
    """
    Phone number value object with validation.

    Usage:
        phone = PhoneNumber(country_code="+1", number="5551234567")
        print(phone.formatted)  # +1 555-123-4567
    """

    model_config = ConfigDict(frozen=True)

    country_code: str
    number: str

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: dict) -> dict:
        """Normalize phone number before validation."""
        if isinstance(data, dict):
            if "number" in data:
                data["number"] = re.sub(r"\D", "", str(data["number"]))
            if "country_code" in data and not str(data["country_code"]).startswith("+"):
                data["country_code"] = f"+{data['country_code']}"
        return data

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate phone number."""
        if len(self.number) < 7 or len(self.number) > 15:
            raise ValueError(f"Invalid phone number length: {self.number}")

        return self

    @property
    def formatted(self) -> str:
        """Format phone number."""
        if len(self.number) == 10:
            return f"{self.country_code} {self.number[:3]}-{self.number[3:6]}-{self.number[6:]}"
        return f"{self.country_code} {self.number}"

    def __str__(self) -> str:
        return self.formatted


class Address(BaseModel):
    """
    Address value object.

    Usage:
        address = Address(
            street="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US"
        )
    """

    model_config = ConfigDict(frozen=True)

    street: str
    city: str
    state: str
    postal_code: str
    country: str = "US"

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate address."""
        if not self.street:
            raise ValueError("Street is required")
        if not self.city:
            raise ValueError("City is required")
        if not self.postal_code:
            raise ValueError("Postal code is required")

        return self

    @property
    def formatted(self) -> str:
        """Format address as single line."""
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    @property
    def multiline(self) -> str:
        """Format address as multiple lines."""
        return f"{self.street}\n{self.city}, {self.state} {self.postal_code}\n{self.country}"

    def __str__(self) -> str:
        return self.formatted


class DateRange(BaseModel):
    """
    Date range value object.

    Usage:
        range = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))
        print(range.days)  # 365
    """

    model_config = ConfigDict(frozen=True)

    start: date
    end: date

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate date range."""
        if self.start > self.end:
            raise ValueError("Start date must be before end date")

        return self

    @property
    def days(self) -> int:
        """Get number of days in range."""
        return (self.end - self.start).days

    def contains(self, check_date: date) -> bool:
        """Check if date is within range."""
        return self.start <= check_date <= self.end

    def overlaps(self, other: "DateRange") -> bool:
        """Check if ranges overlap."""
        return self.start <= other.end and other.start <= self.end

    def __str__(self) -> str:
        return f"{self.start} to {self.end}"


class Percentage(BaseModel):
    """
    Percentage value object (0-100).

    Usage:
        discount = Percentage(value=15)
        price = Decimal("100")
        discounted = price * discount.as_decimal  # 85
    """

    model_config = ConfigDict(frozen=True)

    value: float

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate percentage."""
        if self.value < 0 or self.value > 100:
            raise ValueError(f"Percentage must be 0-100, got {self.value}")

        return self

    @property
    def as_decimal(self) -> Decimal:
        """Get as decimal (0.0 - 1.0)."""
        return Decimal(str(self.value)) / Decimal("100")

    @property
    def complement(self) -> "Percentage":
        """Get complement (100 - value)."""
        return Percentage(value=100 - self.value)

    def __str__(self) -> str:
        return f"{self.value}%"


class SKU(BaseModel):
    """
    Stock Keeping Unit value object.

    Usage:
        sku = SKU(value="PROD-CAT-001")
        print(sku.category)  # CAT
    """

    model_config = ConfigDict(frozen=True)

    value: str

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: dict) -> dict:
        """Normalize SKU value before validation."""
        if isinstance(data, dict) and "value" in data:
            data["value"] = str(data["value"]).upper().strip()
        return data

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate SKU format."""
        if not self.value:
            raise ValueError("SKU cannot be empty")

        # Example format: PREFIX-CATEGORY-NUMBER
        pattern = r"^[A-Z]{2,10}-[A-Z]{2,10}-\d{3,10}$"
        if not re.match(pattern, self.value):
            raise ValueError(
                f"Invalid SKU format: {self.value}. "
                "Expected: PREFIX-CATEGORY-NUMBER (e.g., PROD-ELEC-001)"
            )

        return self

    @property
    def prefix(self) -> str:
        """Get SKU prefix."""
        return self.value.split("-")[0]

    @property
    def category(self) -> str:
        """Get SKU category."""
        return self.value.split("-")[1]

    @property
    def number(self) -> str:
        """Get SKU number."""
        return self.value.split("-")[2]

    def __str__(self) -> str:
        return self.value


class Quantity(BaseModel):
    """
    Non-negative quantity value object.

    Usage:
        qty = Quantity(value=10)
        remaining = qty - Quantity(value=3)
    """

    model_config = ConfigDict(frozen=True)

    value: int

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate quantity."""
        if self.value < 0:
            raise ValueError(f"Quantity cannot be negative: {self.value}")

        return self

    def __add__(self, other: "Quantity") -> "Quantity":
        return Quantity(value=self.value + other.value)

    def __sub__(self, other: "Quantity") -> "Quantity":
        return Quantity(value=self.value - other.value)

    def __mul__(self, factor: int) -> "Quantity":
        return Quantity(value=self.value * factor)

    def __bool__(self) -> bool:
        return self.value > 0

    @classmethod
    def zero(cls) -> "Quantity":
        return cls(value=0)
```

---

## Using Value Objects in Entities

```python
# src/product_catalog/domain/product.py
"""Product domain model with value objects."""

from shared.domain.base_entity import Entity
from .value_objects import SKU, Money, Quantity


class Product(Entity):
    """Product domain entity."""

    type: str = "product"

    # Using value objects
    sku: SKU
    unit_price: Money
    stock_quantity: Quantity

    # Simple fields
    category: str
    brand: str | None = None
    is_available: bool = True
```

---

## Pydantic Integration

Since value objects are already Pydantic models, they can be used directly in schemas.
For cases where you need custom serialization (e.g., accepting a plain string for an Email),
use `Annotated` types with `BeforeValidator`:

```python
# src/shared/application/value_object_types.py
"""Pydantic type adapters for value objects."""

from typing import Annotated, Any
from pydantic import BeforeValidator, PlainSerializer
from decimal import Decimal

from shared.domain.value_objects import Money, Email, SKU


# Email type — accept plain string input, serialize as string
def validate_email(v: Any) -> Email:
    if isinstance(v, Email):
        return v
    return Email(address=str(v))


EmailType = Annotated[
    Email,
    BeforeValidator(validate_email),
    PlainSerializer(lambda x: x.address, return_type=str),
]


# Money type — accept dict input, serialize as dict
def validate_money(v: Any) -> Money:
    if isinstance(v, Money):
        return v
    if isinstance(v, dict):
        return Money(amount=Decimal(str(v["amount"])), currency=v.get("currency", "USD"))
    return Money(amount=Decimal(str(v)))


MoneyType = Annotated[
    Money,
    BeforeValidator(validate_money),
    PlainSerializer(lambda x: {"amount": str(x.amount), "currency": x.currency}),
]


# SKU type — accept plain string input, serialize as string
def validate_sku(v: Any) -> SKU:
    if isinstance(v, SKU):
        return v
    return SKU(value=str(v))


SKUType = Annotated[
    SKU,
    BeforeValidator(validate_sku),
    PlainSerializer(lambda x: x.value, return_type=str),
]
```

Usage in schemas:

```python
# src/product_catalog/application/schemas.py
from shared.application.value_object_types import MoneyType, SKUType


class ProductCreate(BaseCreate):
    sku: SKUType
    unit_price: MoneyType


class ProductResponse(BaseResponse):
    sku: str  # Serialized as string
    unit_price: dict  # Serialized as {"amount": "99.99", "currency": "USD"}
```

---

## Testing Value Objects

```python
"""Test value objects."""

import pytest
from decimal import Decimal

from product_catalog.domain.value_objects import Money, Email, SKU, Quantity


class TestMoney:
    """Test Money value object."""

    def test_create_valid_money(self):
        money = Money(Decimal("99.99"), "USD")
        assert money.amount == Decimal("99.99")
        assert money.currency == "USD"

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError):
            Money(Decimal("-10"), "USD")

    def test_add_same_currency(self):
        m1 = Money(Decimal("10"), "USD")
        m2 = Money(Decimal("20"), "USD")
        result = m1 + m2
        assert result.amount == Decimal("30")

    def test_add_different_currency_raises_error(self):
        m1 = Money(Decimal("10"), "USD")
        m2 = Money(Decimal("10"), "EUR")
        with pytest.raises(ValueError):
            m1 + m2

    def test_immutability(self):
        money = Money(Decimal("100"), "USD")
        with pytest.raises(AttributeError):
            money.amount = Decimal("200")


class TestEmail:
    """Test Email value object."""

    def test_valid_email(self):
        email = Email("user@example.com")
        assert email.address == "user@example.com"
        assert email.domain == "example.com"

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValueError):
            Email("invalid-email")

    def test_empty_email_raises_error(self):
        with pytest.raises(ValueError):
            Email("")
```
