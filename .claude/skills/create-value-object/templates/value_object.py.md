# Value Object Template

Template for creating a frozen Pydantic value object.

## Placeholders

- `{{vo_class}}` - PascalCase class name (e.g., `RetryConfig`)
- `{{vo_name}}` - snake_case module name (e.g., `retry_config`)
- `{{bounded_context}}` - Bounded context name (e.g., `provider`)
- `{{fields}}` - Field definitions
- `{{validators}}` - Validation logic

---

## Template

**File**: `src/{{bounded_context}}/domain/value_objects/{{vo_name}}.py`

```python
"""
IDK: value-object, immutable, self-validating, {{vo_name}}

Module: {{vo_name}}

Responsibility:
- Define immutable {{vo_class}} value object
- Encapsulate validation logic for {{vo_name}}
- Provide type-safe domain concept
- Prevent invalid states

Invariants:
- Frozen (immutable) after creation
- All fields validated via model_validator
- Equality based on all attributes
- No identity field

Related Docs:
- docs/{{bounded_context}}/domain/value-objects.md
"""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class {{vo_class}}(BaseModel):
    """
    IDK: value-object, immutable, {{vo_name}}

    Responsibility:
    - Represent a valid {{vo_class}}
    - Validate all fields on creation
    - Provide computed properties

    Invariants:
    - {{validators}}
    - Immutable after creation

    Failure Modes:
    - ValueError: invalid field values

    Usage:
        obj = {{vo_class}}({{fields_example}})
    """

    model_config = ConfigDict(frozen=True)

    {{fields}}

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Validate {{vo_class}} invariants."""
        {{validation_logic}}
        return self

    def __str__(self) -> str:
        return "{{str_representation}}"
```

---

## Example: RetryConfig

```python
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator


class RetryConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    max_retries: int = Field(default=3, ge=0)
    initial_delay_ms: int = Field(default=1000, gt=0)
    max_delay_ms: int = Field(default=30000, gt=0)
    exponential_base: float = Field(default=2.0, gt=1.0)
    jitter: bool = True

    @model_validator(mode="after")
    def _validate(self) -> Self:
        if self.initial_delay_ms > self.max_delay_ms:
            raise ValueError("initial_delay_ms cannot exceed max_delay_ms")
        return self

    def __str__(self) -> str:
        return f"RetryConfig(retries={self.max_retries}, delay={self.initial_delay_ms}ms)"
```
