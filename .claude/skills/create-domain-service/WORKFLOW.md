# Domain Service Creation Workflow

Step-by-step process for creating a new application-layer service.

> **Documentation Standard**: All generated code must follow the IDK-first docstring format.

## Pre-flight Checklist

```
Service Information:
- [ ] Service name (PascalCase): e.g., ComparisonService, RenderingService
- [ ] Bounded context (snake_case): e.g., evaluation, execution
- [ ] Dependencies (repositories, other services, external clients)
- [ ] Methods (name, params, return type, business logic description)
- [ ] Exceptions (domain-specific errors the service can raise)
```

## Step 1: Create Service File

**File**: `src/{bounded_context}/application/services/{service_name}.py`

Use template: [templates/domain_service.py.md](templates/domain_service.py.md)

**Checklist**:
- [ ] Constructor accepts all dependencies via DI
- [ ] All methods are `async`
- [ ] Methods return VOs or DTOs, not ORM models
- [ ] Domain exceptions raised for error cases
- [ ] **Docs**: IDK includes `application-service`, domain keywords

## Step 2: Create Unit Tests

**File**: `tests/unit/{bounded_context}/application/test_{service_name}.py`

Use template: [templates/domain_service_test.py.md](templates/domain_service_test.py.md)

**Checklist**:
- [ ] Mock all dependencies with `AsyncMock` or `MagicMock`
- [ ] Test each method's happy path
- [ ] Test each method's error cases
- [ ] Verify dependency interactions (assert_called_with)

## Step 3: Register in Dependencies

Add factory function to `src/core/dependencies.py`:

```python
def get_{service_name}() -> {ServiceClass}:
    return {ServiceClass}(
        dependency_a=get_dependency_a(),
        dependency_b=get_dependency_b(),
    )
```

## Step 4: Validation

```bash
uv run pytest tests/unit/{bounded_context}/application/test_{service_name}.py -v
```
