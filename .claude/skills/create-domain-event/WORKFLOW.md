# Domain Event Creation Workflow

## Pre-flight Checklist

```
Event Information:
- [ ] Event name (PascalCase, past tense): e.g., PromptCreated, ExecutionCompleted
- [ ] Aggregate name: e.g., Prompt, Execution
- [ ] Bounded context: e.g., prompt, execution
- [ ] Payload fields (what data the event carries)
- [ ] Handlers needed? (list subscribers)
```

## Step 1: Create Event Classes

**File**: `src/{bounded_context}/domain/events/{aggregate}_events.py`

Use template: [templates/domain_event.py.md](templates/domain_event.py.md)

## Step 2: Create Event Handlers (Optional)

**File**: `src/{bounded_context}/application/event_handlers/{aggregate}_handlers.py`

Use template: [templates/event_handler.py.md](templates/event_handler.py.md)

## Step 3: Create Unit Tests

**File**: `tests/unit/{bounded_context}/domain/test_{aggregate}_events.py`

Use template: [templates/event_test.py.md](templates/event_test.py.md)

## Step 4: Publish Events from Service/Aggregate

Add event publishing to the aggregate or service that emits these events.

## Step 5: Register Handlers

Import handler module in `src/main.py` to register decorators.

## Step 6: Validation

```bash
uv run pytest tests/unit/{bounded_context}/domain/test_{aggregate}_events.py -v
```
