# Caching Layer Creation Workflow

## Pre-flight Checklist

```
Cache Information:
- [ ] Cache name: e.g., schema, token_count, provider_response
- [ ] Cached type: what is stored in cache
- [ ] Max size: maximum entries (default: 1000)
- [ ] TTL: time-to-live in seconds (None for no expiry)
- [ ] Hash function: how to compute cache key from input
- [ ] Need Redis? (for multi-instance deployments)
- [ ] Need warmup? (for pre-populating on startup)
```

## Step 1: Create LRU Cache

**File**: `src/{bounded_context}/infrastructure/cache/{cache_name}_cache.py`

Use template: [templates/lru_cache.py.md](templates/lru_cache.py.md)

## Step 2: Create Async Wrapper

**File**: `src/{bounded_context}/infrastructure/cache/async_{cache_name}_cache.py`

Use template: [templates/async_cache_wrapper.py.md](templates/async_cache_wrapper.py.md)

## Step 3: Create Redis Cache (Optional)

**File**: `src/{bounded_context}/infrastructure/cache/redis_{cache_name}_cache.py`

Use template: [templates/redis_cache.py.md](templates/redis_cache.py.md)

## Step 4: Create Cache Warmer (Optional)

**File**: `src/{bounded_context}/infrastructure/cache/{cache_name}_warmer.py`

Use template: [templates/cache_warmer.py.md](templates/cache_warmer.py.md)

## Step 5: Create Unit Tests

**File**: `tests/unit/{bounded_context}/infrastructure/test_{cache_name}_cache.py`

Use template: [templates/cache_test.py.md](templates/cache_test.py.md)

## Step 6: Validation

```bash
uv run pytest tests/unit/{bounded_context}/infrastructure/test_{cache_name}_cache.py -v
```
