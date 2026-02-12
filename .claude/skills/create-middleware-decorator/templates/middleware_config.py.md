# Middleware Config Template

**File**: `src/shared/infrastructure/config/{{middleware_name}}_config.py`

```python
"""
IDK: config, {{middleware_name}}, value-object

Responsibility:
- Configuration for {{middleware_name}}
"""

from pydantic import BaseModel, ConfigDict, Field


class {{config_class}}(BaseModel):
    """Configuration for {{middleware_class}}."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    {{config_fields}}
```
