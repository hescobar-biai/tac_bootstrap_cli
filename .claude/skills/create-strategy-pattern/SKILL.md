---
name: create-strategy-pattern
description: Generate Strategy ABC, concrete implementations, factory, and tests. Use when implementing interchangeable algorithms, execution modes, or pluggable behaviors. Triggers on requests like "create strategy", "add strategy pattern", "implement pluggable algorithm".
---

# Create Strategy Pattern

Generate Strategy ABC + concrete implementations + factory + tests following DDD patterns.

## Quick Start

1. **Gather strategy info**: Name, method signature, concrete strategies
2. **Generate interface**: ABC defining strategy contract
3. **Generate implementations**: Concrete strategy classes
4. **Generate factory**: Strategy selection/creation
5. **Generate tests**: Tests for each implementation

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).

## Architecture Overview

```
src/
└── {bounded_context}/
    ├── domain/
    │   └── strategies/
    │       ├── __init__.py
    │       ├── {strategy_name}_strategy.py       # ABC interface
    │       └── {strategy_name}_factory.py        # Factory
    └── infrastructure/
        └── strategies/
            ├── {concrete_a}.py                    # Concrete impl A
            └── {concrete_b}.py                    # Concrete impl B
tests/
└── unit/
    └── {bounded_context}/
        └── domain/
            └── test_{strategy_name}_strategies.py
```

## Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{strategy_name}}` | snake_case strategy name | `execution_mode` |
| `{{strategy_class}}` | PascalCase ABC name | `ExecutionModeStrategy` |
| `{{strategies_list}}` | Concrete implementations | `["parallel", "sequential", "fallback"]` |
| `{{method_signature}}` | Strategy method signature | `async def execute(self, requests: list) -> list` |
| `{{bounded_context}}` | Bounded context name | `execution` |

## Templates Reference

- [strategy_interface.py.md](templates/strategy_interface.py.md) - Strategy ABC
- [strategy_concrete.py.md](templates/strategy_concrete.py.md) - Concrete implementation
- [strategy_factory.py.md](templates/strategy_factory.py.md) - Strategy factory
- [strategy_test.py.md](templates/strategy_test.py.md) - Unit tests

## Best Practices

1. **Interface first**: Define the ABC before implementations
2. **Single method**: Keep the strategy interface focused on one method
3. **Factory**: Use factory for strategy selection, not direct instantiation
4. **Immutable config**: Strategy config should be a frozen value object
5. **Testing**: Test each concrete strategy independently
