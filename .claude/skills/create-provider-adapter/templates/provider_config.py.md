# Provider Config Template

**File**: `src/provider/infrastructure/config/{{provider_name}}_config.py`

```python
"""
IDK: provider-config, {{provider_name}}, value-object, infrastructure

Responsibility:
- Define configuration for {{provider_class}}
- Validate provider-specific settings
"""

from pydantic import BaseModel, ConfigDict, Field


class {{config_class}}(BaseModel):
    """Configuration for {{provider_class}}."""

    model_config = ConfigDict(frozen=True)

    {{config_fields}}
```
