# Domain Event Template

**File**: `src/{{bounded_context}}/domain/events/{{aggregate_name_snake}}_events.py`

```python
"""
IDK: domain-event, {{aggregate_name_snake}}, event-driven, {{bounded_context}}

Responsibility:
- Define domain events for {{aggregate_name}} aggregate
- Carry event payload for subscribers
- Support event correlation and tracing

Invariants:
- All events are frozen (immutable)
- Named in past tense
- event_id and occurred_at auto-generated
"""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class {{aggregate_name}}Created(BaseModel):
    """Event: {{aggregate_name}} was created."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None

    {{aggregate_id_field}}: str
    {{payload_fields}}

    @property
    def event_type(self) -> str:
        return "{{aggregate_name_snake}}.created"


class {{aggregate_name}}Updated(BaseModel):
    """Event: {{aggregate_name}} was updated."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None

    {{aggregate_id_field}}: str
    changed_fields: tuple[str, ...] = Field(default_factory=tuple)
    updated_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{aggregate_name_snake}}.updated"


class {{aggregate_name}}Deleted(BaseModel):
    """Event: {{aggregate_name}} was deleted."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None

    {{aggregate_id_field}}: str
    deleted_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{aggregate_name_snake}}.deleted"
```
