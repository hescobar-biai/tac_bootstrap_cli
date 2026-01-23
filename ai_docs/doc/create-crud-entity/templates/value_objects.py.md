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
- Validation in __post_init__
- Equality based on all attributes
- No identity field

Related Docs:
- docs/{{capability}}/domain/value-objects.md
- docs/architecture/ddd-patterns.md
"""

from dataclasses import dataclass
from typing import Self
import re
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Email:
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
        email = Email("user@example.com")
        print(email.address)  # user@example.com
        print(email.domain)   # example.com
    """

    address: str

    def __post_init__(self) -> None:
        """Validate email format."""
        if not self.address:
            raise ValueError("Email address cannot be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.address):
            raise ValueError(f"Invalid email format: {self.address}")

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


@dataclass(frozen=True, slots=True)
class Money:
    """
    Money value object with currency.

    Usage:
        price = Money(Decimal("99.99"), "USD")
        total = price + Money(Decimal("10.00"), "USD")
    """

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        """Validate money values."""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter ISO code")

        object.__setattr__(self, "currency", self.currency.upper())

    def __add__(self, other: "Money") -> "Money":
        """Add two money values."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        """Subtract money values."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} and {other.currency}")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: int | float | Decimal) -> "Money":
        """Multiply by a factor."""
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    @classmethod
    def zero(cls, currency: str = "USD") -> "Money":
        """Create zero money."""
        return cls(Decimal("0"), currency)


@dataclass(frozen=True, slots=True)
class PhoneNumber:
    """
    Phone number value object with validation.

    Usage:
        phone = PhoneNumber("+1", "5551234567")
        print(phone.formatted)  # +1 555-123-4567
    """

    country_code: str
    number: str

    def __post_init__(self) -> None:
        """Validate phone number."""
        # Remove any non-digit characters for validation
        digits_only = re.sub(r"\D", "", self.number)

        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError(f"Invalid phone number length: {self.number}")

        if not self.country_code.startswith("+"):
            object.__setattr__(self, "country_code", f"+{self.country_code}")

        object.__setattr__(self, "number", digits_only)

    @property
    def formatted(self) -> str:
        """Format phone number."""
        if len(self.number) == 10:
            return f"{self.country_code} {self.number[:3]}-{self.number[3:6]}-{self.number[6:]}"
        return f"{self.country_code} {self.number}"

    def __str__(self) -> str:
        return self.formatted


@dataclass(frozen=True, slots=True)
class Address:
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

    street: str
    city: str
    state: str
    postal_code: str
    country: str = "US"

    def __post_init__(self) -> None:
        """Validate address."""
        if not self.street:
            raise ValueError("Street is required")
        if not self.city:
            raise ValueError("City is required")
        if not self.postal_code:
            raise ValueError("Postal code is required")

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


@dataclass(frozen=True, slots=True)
class DateRange:
    """
    Date range value object.

    Usage:
        range = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))
        print(range.days)  # 365
    """

    from datetime import date

    start: date
    end: date

    def __post_init__(self) -> None:
        """Validate date range."""
        if self.start > self.end:
            raise ValueError("Start date must be before end date")

    @property
    def days(self) -> int:
        """Get number of days in range."""
        return (self.end - self.start).days

    def contains(self, date: "DateRange.date") -> bool:
        """Check if date is within range."""
        return self.start <= date <= self.end

    def overlaps(self, other: "DateRange") -> bool:
        """Check if ranges overlap."""
        return self.start <= other.end and other.start <= self.end

    def __str__(self) -> str:
        return f"{self.start} to {self.end}"


@dataclass(frozen=True, slots=True)
class Percentage:
    """
    Percentage value object (0-100).

    Usage:
        discount = Percentage(15)
        price = Decimal("100")
        discounted = price * discount.as_decimal  # 85
    """

    value: float

    def __post_init__(self) -> None:
        """Validate percentage."""
        if self.value < 0 or self.value > 100:
            raise ValueError(f"Percentage must be 0-100, got {self.value}")

    @property
    def as_decimal(self) -> Decimal:
        """Get as decimal (0.0 - 1.0)."""
        return Decimal(str(self.value)) / Decimal("100")

    @property
    def complement(self) -> "Percentage":
        """Get complement (100 - value)."""
        return Percentage(100 - self.value)

    def __str__(self) -> str:
        return f"{self.value}%"


@dataclass(frozen=True, slots=True)
class SKU:
    """
    Stock Keeping Unit value object.

    Usage:
        sku = SKU("PROD-CAT-001")
        print(sku.category)  # CAT
    """

    value: str

    def __post_init__(self) -> None:
        """Validate SKU format."""
        if not self.value:
            raise ValueError("SKU cannot be empty")

        # Example format: PREFIX-CATEGORY-NUMBER
        pattern = r"^[A-Z]{2,10}-[A-Z]{2,10}-\d{3,10}$"
        normalized = self.value.upper().strip()

        if not re.match(pattern, normalized):
            raise ValueError(
                f"Invalid SKU format: {self.value}. "
                "Expected: PREFIX-CATEGORY-NUMBER (e.g., PROD-ELEC-001)"
            )

        object.__setattr__(self, "value", normalized)

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


@dataclass(frozen=True, slots=True)
class Quantity:
    """
    Non-negative quantity value object.

    Usage:
        qty = Quantity(10)
        remaining = qty - Quantity(3)
    """

    value: int

    def __post_init__(self) -> None:
        """Validate quantity."""
        if self.value < 0:
            raise ValueError(f"Quantity cannot be negative: {self.value}")

    def __add__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.value + other.value)

    def __sub__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.value - other.value)

    def __mul__(self, factor: int) -> "Quantity":
        return Quantity(self.value * factor)

    def __bool__(self) -> bool:
        return self.value > 0

    @classmethod
    def zero(cls) -> "Quantity":
        return cls(0)
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

For using value objects with Pydantic schemas:

```python
# src/shared/application/value_object_types.py
"""Pydantic type adapters for value objects."""

from typing import Annotated, Any
from pydantic import BeforeValidator, PlainSerializer
from decimal import Decimal

from shared.domain.value_objects import Money, Email, SKU


# Email type for Pydantic
def validate_email(v: Any) -> Email:
    if isinstance(v, Email):
        return v
    return Email(str(v))


EmailType = Annotated[
    Email,
    BeforeValidator(validate_email),
    PlainSerializer(lambda x: x.address, return_type=str),
]


# Money type for Pydantic
def validate_money(v: Any) -> Money:
    if isinstance(v, Money):
        return v
    if isinstance(v, dict):
        return Money(Decimal(str(v["amount"])), v.get("currency", "USD"))
    return Money(Decimal(str(v)))


MoneyType = Annotated[
    Money,
    BeforeValidator(validate_money),
    PlainSerializer(lambda x: {"amount": str(x.amount), "currency": x.currency}),
]


# SKU type for Pydantic
def validate_sku(v: Any) -> SKU:
    if isinstance(v, SKU):
        return v
    return SKU(str(v))


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
