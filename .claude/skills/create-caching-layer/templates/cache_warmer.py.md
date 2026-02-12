# Cache Warmer Template

**File**: `src/{{bounded_context}}/infrastructure/cache/{{cache_name}}_warmer.py`

```python
"""
IDK: cache-warmup, {{cache_name}}, startup, pre-population

Responsibility:
- Pre-populate cache on application startup
- Compile frequently used entries
"""

import structlog

logger = structlog.get_logger(__name__)


class {{cache_class}}Warmer:
    """Pre-populates {{cache_name}} cache on startup."""

    def __init__(self, cache, data_source) -> None:
        self._cache = cache
        self._data_source = data_source

    async def warmup(self, limit: int = 100) -> dict:
        """Warm cache with most frequently used entries."""
        items = await self._data_source.get_most_used(limit=limit)
        warmed = 0
        for item in items:
            try:
                {{warmup_logic}}
                warmed += 1
            except Exception as e:
                logger.warning("cache_warmup_failed", item=str(item), error=str(e))
        logger.info("cache_warmup_complete", warmed=warmed, total=len(items))
        return {"warmed": warmed, "total": len(items)}
```
