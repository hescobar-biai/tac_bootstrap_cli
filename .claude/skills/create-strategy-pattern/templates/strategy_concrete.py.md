# Strategy Concrete Implementation Template

**File**: `src/{{bounded_context}}/infrastructure/strategies/{{concrete_name}}.py`

```python
"""
IDK: strategy-pattern, {{concrete_name}}, implementation

Responsibility:
- Implement {{strategy_class}} with {{concrete_name}} algorithm

Invariants:
- Honors {{strategy_class}} interface contract
"""

from src.{{bounded_context}}.domain.strategies.{{strategy_name}}_strategy import {{strategy_class}}


class {{concrete_class}}({{strategy_class}}):
    """{{concrete_name}} implementation of {{strategy_class}}."""

    {{method_implementation}}
```
