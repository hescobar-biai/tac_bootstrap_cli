---
name: create-middleware-decorator
description: Generate FastAPI middleware or provider decorator wrappers for cross-cutting concerns. Use when adding request/response interceptors, provider wrappers, or aspect-oriented behaviors. Triggers on requests like "create middleware", "add decorator", "new request interceptor".
---

# Create Middleware / Decorator

Generate FastAPI middleware or provider decorator wrappers for cross-cutting concerns like logging, metrics, tracing, rate limiting, and PII filtering.

## Quick Start

1. **Gather info**: Name, concern type (middleware vs decorator), hooks
2. **Generate middleware or decorator**: Based on concern type
3. **Generate config**: Configuration value object
4. **Generate tests**: Unit tests for the interceptor

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).

## Architecture Overview

```
src/
└── shared/
    ├── presentation/
    │   └── middleware/
    │       └── {middleware_name}.py            # FastAPI middleware
    └── infrastructure/
        └── decorators/
            └── {decorator_name}.py            # Provider decorator
tests/
└── unit/
    └── shared/
        ├── presentation/
        │   └── test_{middleware_name}.py
        └── infrastructure/
            └── test_{decorator_name}.py
```

## Variants

| Variant | Use Case | Location |
|---------|----------|----------|
| **FastAPI Middleware** | HTTP request/response interception | `shared/presentation/middleware/` |
| **Provider Decorator** | LLM provider call wrapping | `shared/infrastructure/decorators/` |

## Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{middleware_name}}` | snake_case name | `metrics_middleware` |
| `{{concern_type}}` | Cross-cutting concern | `logging`, `metrics`, `tracing` |
| `{{pre_hook}}` | Logic before the main call | `start timer, bind context` |
| `{{post_hook}}` | Logic after the main call | `record metrics, clean context` |

## Templates Reference

- [fastapi_middleware.py.md](templates/fastapi_middleware.py.md) - FastAPI middleware
- [provider_decorator.py.md](templates/provider_decorator.py.md) - Provider decorator
- [middleware_config.py.md](templates/middleware_config.py.md) - Configuration VO
- [middleware_test.py.md](templates/middleware_test.py.md) - Unit tests

## Best Practices

1. **Non-blocking**: Middleware must not block request processing
2. **Fail-safe**: Cross-cutting concerns must not break main logic
3. **Configurable**: Enable/disable via configuration
4. **Ordered**: Middleware order matters — document expected order
5. **Clean up**: Always clean up context in `finally` blocks
