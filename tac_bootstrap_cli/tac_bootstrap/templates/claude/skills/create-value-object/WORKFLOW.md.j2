# Value Object Creation Workflow

Step-by-step process for creating a new frozen Pydantic value object.

> **Documentation Standard**: All generated code must follow the IDK-first docstring format. Every class and function requires IDK keywords, Responsibility, and Invariants sections.

## Pre-flight Checklist

```
Value Object Information:
- [ ] VO name (PascalCase): e.g., RetryConfig, PromptTemplate, LatencyMetrics
- [ ] Bounded context (snake_case): e.g., provider, prompt, evaluation
- [ ] Fields (name, type, default, constraints)
- [ ] Validation rules (ranges, formats, relationships between fields)
- [ ] Normalization rules (case conversion, trimming, etc.)
```

## Step 1: Create Value Object File

**File**: `src/{bounded_context}/domain/value_objects/{vo_name}.py`

Use template: [templates/value_object.py.md](templates/value_object.py.md)

**Checklist**:
- [ ] Uses `ConfigDict(frozen=True)` for immutability
- [ ] Fields have type hints and optional defaults
- [ ] `model_validator(mode="after")` validates invariants
- [ ] Optional `model_validator(mode="before")` for normalization
- [ ] Properties for computed/derived values
- [ ] `__str__` override for human-readable output
- [ ] **Docs**: IDK includes `value-object`, `immutable`, domain-specific keywords
- [ ] **Docs**: Invariants document validation rules

## Step 2: Create Unit Tests

**File**: `tests/unit/{bounded_context}/domain/test_{vo_name}.py`

Use template: [templates/value_object_test.py.md](templates/value_object_test.py.md)

**Checklist**:
- [ ] Test valid creation with all fields
- [ ] Test valid creation with defaults
- [ ] Test each validation rule (negative cases raise ValueError)
- [ ] Test immutability (setting attributes raises ValidationError)
- [ ] Test equality (same values are equal)
- [ ] Test `__str__` output
- [ ] Test normalization if applicable
- [ ] Test properties and computed values

## Step 3: Register in Package

Add import to `src/{bounded_context}/domain/value_objects/__init__.py`:

```python
from .{vo_name} import {VoClass}

__all__ = ["{VoClass}"]
```

## Step 4: Validation

```bash
# Run type checker
pyright src/{bounded_context}/domain/value_objects/{vo_name}.py

# Run tests
uv run pytest tests/unit/{bounded_context}/domain/test_{vo_name}.py -v
```
