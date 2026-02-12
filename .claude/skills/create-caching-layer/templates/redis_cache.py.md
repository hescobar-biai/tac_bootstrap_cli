# Redis Cache Template

**File**: `src/{{bounded_context}}/infrastructure/cache/redis_{{cache_name}}_cache.py`

```python
"""
IDK: redis-cache, distributed, {{cache_name}}, fallback

Responsibility:
- Distributed cache with Redis backend
- Local cache as L1, Redis as L2
- Graceful fallback on Redis failure
"""

import structlog
from .{{cache_name}}_cache import {{cache_class}}Cache

logger = structlog.get_logger(__name__)


class Redis{{cache_class}}Cache:
    """Distributed cache with Redis backend and local fallback."""

    def __init__(self, redis_client, local_cache: {{cache_class}}Cache, prefix: str = "{{cache_name}}:") -> None:
        self._redis = redis_client
        self._local = local_cache
        self._prefix = prefix

    async def get(self, key_data) -> any:
        cached = self._local.get(key_data)
        if cached is not None:
            return cached
        try:
            key = f"{self._prefix}{self._local._hash_key(key_data)}"
            serialized = await self._redis.get(key)
            if serialized:
                value = self._deserialize(serialized)
                self._local.put(key_data, value)
                return value
        except Exception as e:
            logger.warning("redis_cache_error", error=str(e))
        return None

    async def put(self, key_data, value, ttl: int = 3600) -> None:
        self._local.put(key_data, value)
        try:
            key = f"{self._prefix}{self._local._hash_key(key_data)}"
            serialized = self._serialize(value)
            await self._redis.setex(key, ttl, serialized)
        except Exception as e:
            logger.warning("redis_cache_write_error", error=str(e))

    def _serialize(self, value) -> bytes:
        """Serialize value for Redis storage."""
        import pickle
        return pickle.dumps(value)

    def _deserialize(self, data: bytes):
        """Deserialize value from Redis storage."""
        import pickle
        return pickle.loads(data)
```
