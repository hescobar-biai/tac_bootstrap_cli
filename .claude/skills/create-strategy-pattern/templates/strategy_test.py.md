# Strategy Test Template

**File**: `tests/unit/{{bounded_context}}/domain/test_{{strategy_name}}_strategies.py`

```python
"""{{strategy_class}} strategy tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.{{bounded_context}}.domain.strategies.{{strategy_name}}_factory import {{factory_class}}


class Test{{strategy_class}}Factory:
    """Test strategy factory."""

    def test_create_known_strategy(self):
        """Test creating a registered strategy."""
        strategy = {{factory_class}}.create("{{first_strategy}}")
        assert strategy is not None

    def test_create_unknown_strategy_raises(self):
        """Test unknown strategy raises ValueError."""
        with pytest.raises(ValueError):
            {{factory_class}}.create("nonexistent")

    def test_available_strategies(self):
        """Test listing available strategies."""
        available = {{factory_class}}.available()
        assert "{{first_strategy}}" in available


{{concrete_test_classes}}
```
