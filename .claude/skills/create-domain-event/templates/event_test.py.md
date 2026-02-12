# Event Test Template

**File**: `tests/unit/{{bounded_context}}/domain/test_{{aggregate_name_snake}}_events.py`

```python
"""{{aggregate_name}} domain event tests."""

import pytest
from datetime import datetime

from src.{{bounded_context}}.domain.events.{{aggregate_name_snake}}_events import (
    {{aggregate_name}}Created,
    {{aggregate_name}}Updated,
    {{aggregate_name}}Deleted,
)


class Test{{aggregate_name}}Created:
    def test_create_event(self):
        event = {{aggregate_name}}Created(
            {{aggregate_id_field}}="test-id",
            {{test_payload_fields}}
        )
        assert event.{{aggregate_id_field}} == "test-id"
        assert event.event_id is not None
        assert event.occurred_at is not None

    def test_event_type(self):
        event = {{aggregate_name}}Created(
            {{aggregate_id_field}}="test-id",
            {{test_payload_fields}}
        )
        assert event.event_type == "{{aggregate_name_snake}}.created"

    def test_immutability(self):
        event = {{aggregate_name}}Created(
            {{aggregate_id_field}}="test-id",
            {{test_payload_fields}}
        )
        with pytest.raises(Exception):
            event.{{aggregate_id_field}} = "new-id"


class Test{{aggregate_name}}Updated:
    def test_create_event(self):
        event = {{aggregate_name}}Updated(
            {{aggregate_id_field}}="test-id",
            changed_fields=("name", "description"),
        )
        assert event.changed_fields == ("name", "description")

    def test_event_type(self):
        event = {{aggregate_name}}Updated({{aggregate_id_field}}="test-id")
        assert event.event_type == "{{aggregate_name_snake}}.updated"


class Test{{aggregate_name}}Deleted:
    def test_create_event(self):
        event = {{aggregate_name}}Deleted(
            {{aggregate_id_field}}="test-id",
            deleted_by="user-1",
        )
        assert event.deleted_by == "user-1"
```
