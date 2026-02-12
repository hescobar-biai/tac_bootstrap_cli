# Value Object Test Template

Template for unit tests of a frozen Pydantic value object.

## Placeholders

- `{{vo_class}}` - PascalCase class name
- `{{vo_name}}` - snake_case module name
- `{{bounded_context}}` - Bounded context name

---

## Template

**File**: `tests/unit/{{bounded_context}}/domain/test_{{vo_name}}.py`

```python
"""{{vo_class}} value object unit tests."""

import pytest
from pydantic import ValidationError

from src.{{bounded_context}}.domain.value_objects.{{vo_name}} import {{vo_class}}


class Test{{vo_class}}:
    """Test suite for {{vo_class}} value object."""

    def test_create_with_valid_values(self):
        """Test creation with valid field values."""
        obj = {{vo_class}}({{valid_params}})
        {{valid_assertions}}

    def test_create_with_defaults(self):
        """Test creation using default values."""
        obj = {{vo_class}}({{minimal_params}})
        {{default_assertions}}

    def test_invalid_{{field}}_raises_error(self):
        """Test that invalid {{field}} raises ValueError."""
        with pytest.raises((ValueError, ValidationError)):
            {{vo_class}}({{invalid_params}})

    def test_immutability(self):
        """Test that value object cannot be mutated."""
        obj = {{vo_class}}({{valid_params}})
        with pytest.raises(ValidationError):
            obj.{{field}} = {{new_value}}

    def test_equality(self):
        """Test that equal values produce equal objects."""
        obj1 = {{vo_class}}({{valid_params}})
        obj2 = {{vo_class}}({{valid_params}})
        assert obj1 == obj2

    def test_inequality(self):
        """Test that different values produce unequal objects."""
        obj1 = {{vo_class}}({{params_1}})
        obj2 = {{vo_class}}({{params_2}})
        assert obj1 != obj2

    def test_str_representation(self):
        """Test string representation."""
        obj = {{vo_class}}({{valid_params}})
        result = str(obj)
        assert isinstance(result, str)
        assert len(result) > 0
```

---

## Example: TestRetryConfig

```python
import pytest
from pydantic import ValidationError

from src.provider.domain.value_objects.retry_config import RetryConfig


class TestRetryConfig:
    def test_create_with_defaults(self):
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.initial_delay_ms == 1000
        assert config.jitter is True

    def test_create_with_custom_values(self):
        config = RetryConfig(max_retries=5, initial_delay_ms=500)
        assert config.max_retries == 5
        assert config.initial_delay_ms == 500

    def test_initial_delay_exceeds_max_raises_error(self):
        with pytest.raises((ValueError, ValidationError)):
            RetryConfig(initial_delay_ms=50000, max_delay_ms=1000)

    def test_immutability(self):
        config = RetryConfig()
        with pytest.raises(ValidationError):
            config.max_retries = 10

    def test_equality(self):
        c1 = RetryConfig(max_retries=3)
        c2 = RetryConfig(max_retries=3)
        assert c1 == c2
```
