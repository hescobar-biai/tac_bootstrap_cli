# Provider Decorator Template

**File**: `src/shared/infrastructure/decorators/{{decorator_name}}.py`

```python
"""
IDK: decorator, {{concern_type}}, provider-wrapper, cross-cutting

Responsibility:
- Wrap LLM provider calls with {{concern_type}} behavior
- Execute pre-hook before provider execution
- Execute post-hook after provider execution
"""

import structlog

from src.provider.domain.interfaces.llm_provider import LLMProvider, LLMRequest, LLMResponse

logger = structlog.get_logger(__name__)


class {{decorator_class}}(LLMProvider):
    """
    Decorator that adds {{concern_type}} to any LLM provider.
    """

    def __init__(self, wrapped: LLMProvider, {{config_params}}) -> None:
        self._wrapped = wrapped
        {{config_assignments}}

    @property
    def name(self) -> str:
        return self._wrapped.name

    async def execute(self, request: LLMRequest) -> LLMResponse:
        """Execute with {{concern_type}} wrapper."""
        # Pre-hook
        {{pre_hook}}

        try:
            response = await self._wrapped.execute(request)
            # Post-hook (success)
            {{post_hook_success}}
            return response
        except Exception as e:
            # Post-hook (failure)
            {{post_hook_failure}}
            raise

    async def health_check(self) -> bool:
        return await self._wrapped.health_check()

    def get_available_models(self) -> list[str]:
        return self._wrapped.get_available_models()
```
