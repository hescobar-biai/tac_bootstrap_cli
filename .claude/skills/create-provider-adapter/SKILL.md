---
name: create-provider-adapter
description: Generate LLM provider implementations with adapter, config, error mapping, and tests. Use when adding a new LLM provider (Vertex AI, OpenRouter, Bedrock, etc.). Triggers on requests like "add provider", "new LLM adapter", "implement provider".
---

# Create Provider Adapter

Generate complete LLM provider implementations following the hexagonal architecture adapter pattern.

## Quick Start

1. **Gather provider info**: Name, SDK package, auth type, model list
2. **Generate adapter**: Implements `LLMProvider` interface
3. **Generate config**: Provider-specific configuration VO
4. **Generate error mapping**: Maps SDK errors to domain exceptions
5. **Generate tests**: Unit tests with mocked SDK

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).

## Architecture Overview

Provider adapters live in the infrastructure layer:

```
src/
└── provider/
    ├── domain/
    │   └── interfaces/
    │       └── llm_provider.py              # LLMProvider ABC (shared)
    ├── infrastructure/
    │   ├── adapters/
    │   │   └── {provider_name}.py           # Provider adapter
    │   └── config/
    │       └── {provider_name}_config.py    # Provider config VO
    └── application/
        └── services/
            └── provider_registry.py         # Registry (shared)
tests/
└── unit/
    └── provider/
        └── infrastructure/
            └── test_{provider_name}.py
```

## Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{provider_name}}` | snake_case provider | `vertex_ai` |
| `{{provider_class}}` | PascalCase adapter | `VertexAIProvider` |
| `{{sdk_package}}` | Python SDK package | `google-cloud-aiplatform` |
| `{{auth_type}}` | Authentication method | `service_account`, `api_key`, `iam_role` |
| `{{model_list}}` | Supported models | `["gemini-1.5-pro", "gemini-1.5-flash"]` |

## Templates Reference

- [provider_adapter.py.md](templates/provider_adapter.py.md) - Provider adapter
- [provider_config.py.md](templates/provider_config.py.md) - Config value object
- [provider_error_mapping.py.md](templates/provider_error_mapping.py.md) - Error mapping
- [provider_test.py.md](templates/provider_test.py.md) - Unit tests

## Invariants

- Provider MUST implement `LLMProvider` abstract interface
- All API calls MUST be async
- Token counts MUST be extracted from response metadata
- Latency MUST be measured for every request
- Raw SDK errors MUST be mapped to domain exceptions
- Credentials MUST NOT be hardcoded
