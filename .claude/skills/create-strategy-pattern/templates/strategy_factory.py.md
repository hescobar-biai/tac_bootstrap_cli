# Strategy Factory Template

**File**: `src/{{bounded_context}}/domain/strategies/{{strategy_name}}_factory.py`

```python
"""
IDK: factory-pattern, {{strategy_name}}, strategy-selection

Responsibility:
- Create appropriate strategy instance based on selection criteria
- Register available strategies
"""

from src.{{bounded_context}}.domain.strategies.{{strategy_name}}_strategy import {{strategy_class}}


class {{strategy_name_pascal}}Factory:
    """Factory for creating {{strategy_class}} instances."""

    _strategies: dict[str, type[{{strategy_class}}]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: type[{{strategy_class}}]) -> None:
        """Register a strategy implementation."""
        cls._strategies[name] = strategy_class

    @classmethod
    def create(cls, name: str, **kwargs) -> {{strategy_class}}:
        """Create a strategy instance by name."""
        if name not in cls._strategies:
            available = ", ".join(cls._strategies.keys())
            raise ValueError(f"Unknown strategy '{name}'. Available: {available}")
        return cls._strategies[name](**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        """List available strategy names."""
        return list(cls._strategies.keys())
```
