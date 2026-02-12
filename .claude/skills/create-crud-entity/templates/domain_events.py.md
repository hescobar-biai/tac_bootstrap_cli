# Domain Events Template

Template for implementing domain events for loose coupling between capabilities.

## Overview

Domain events enable:
- **Loose coupling**: Capabilities communicate without direct dependencies
- **Eventual consistency**: Async processing of side effects
- **Audit trail**: Record of business-significant occurrences
- **Extensibility**: Add handlers without modifying emitter

## Directory Structure

```
src/
├── shared/
│   └── domain/
│       ├── base_entity.py
│       └── events.py           # Event infrastructure
└── {capability}/
    └── domain/
        ├── {entity}.py
        └── events.py           # Capability-specific events
```

---

## Event Infrastructure

**File**: `src/shared/domain/events.py`

```python
"""
IDK: domain-event, event-bus, pub-sub, loose-coupling

Module: events

Responsibility:
- Provide domain event infrastructure
- Implement event bus for pub/sub pattern
- Support sync and async event handlers
- Enable loose coupling between capabilities

Invariants:
- Events are immutable (frozen Pydantic models)
- Events named in past tense
- Event bus is singleton
- Handlers executed in registration order

Related Docs:
- docs/shared/domain/events.md
- docs/architecture/event-driven.md
"""

from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Callable, Type, TypeVar
from uuid import uuid4
import asyncio
from collections import defaultdict

from pydantic import BaseModel, ConfigDict, Field


class DomainEvent(BaseModel, ABC):
    """
    IDK: domain-event, immutable-record, past-tense

    Responsibility:
    - Base class for all domain events
    - Provide event metadata (id, timestamp, correlation)
    - Enforce immutability

    Invariants:
    - Events are frozen (immutable)
    - Named in past tense (e.g., ProductCreated)
    - event_id auto-generated
    - occurred_at auto-set to UTC now

    Related Docs:
    - docs/shared/domain/events.md
    """

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Return the event type identifier."""
        pass


T = TypeVar("T", bound=DomainEvent)
EventHandler = Callable[[DomainEvent], None]
AsyncEventHandler = Callable[[DomainEvent], asyncio.coroutine]


class EventBus:
    """
    Simple in-memory event bus for domain events.

    For production, consider using:
    - Redis Pub/Sub
    - RabbitMQ
    - Apache Kafka
    - AWS EventBridge
    """

    _instance: "EventBus | None" = None
    _handlers: dict[Type[DomainEvent], list[EventHandler]]
    _async_handlers: dict[Type[DomainEvent], list[AsyncEventHandler]]

    def __new__(cls) -> "EventBus":
        """Singleton pattern for event bus."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = defaultdict(list)
            cls._instance._async_handlers = defaultdict(list)
        return cls._instance

    def subscribe(
        self,
        event_type: Type[T],
        handler: EventHandler,
    ) -> None:
        """Subscribe a sync handler to an event type."""
        self._handlers[event_type].append(handler)

    def subscribe_async(
        self,
        event_type: Type[T],
        handler: AsyncEventHandler,
    ) -> None:
        """Subscribe an async handler to an event type."""
        self._async_handlers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: Type[T],
        handler: EventHandler,
    ) -> None:
        """Unsubscribe a handler from an event type."""
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    def publish(self, event: DomainEvent) -> None:
        """
        Publish an event to all subscribed sync handlers.

        Args:
            event: The domain event to publish
        """
        event_type = type(event)
        for handler in self._handlers[event_type]:
            try:
                handler(event)
            except Exception as e:
                # Log error but don't stop other handlers
                print(f"Error in event handler: {e}")

    async def publish_async(self, event: DomainEvent) -> None:
        """
        Publish an event to all subscribed async handlers.

        Args:
            event: The domain event to publish
        """
        event_type = type(event)

        # Run sync handlers
        for handler in self._handlers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in sync event handler: {e}")

        # Run async handlers
        tasks = []
        for handler in self._async_handlers[event_type]:
            tasks.append(asyncio.create_task(handler(event)))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"Error in async event handler: {result}")

    def clear(self) -> None:
        """Clear all handlers (useful for testing)."""
        self._handlers.clear()
        self._async_handlers.clear()


# Global event bus instance
event_bus = EventBus()


def on_event(event_type: Type[T]):
    """
    Decorator for registering event handlers.

    Usage:
        @on_event(OrderCreated)
        def handle_order_created(event: OrderCreated):
            # Handle event
            pass
    """
    def decorator(handler: EventHandler) -> EventHandler:
        event_bus.subscribe(event_type, handler)
        return handler
    return decorator


def on_event_async(event_type: Type[T]):
    """
    Decorator for registering async event handlers.

    Usage:
        @on_event_async(OrderCreated)
        async def handle_order_created(event: OrderCreated):
            # Handle event
            pass
    """
    def decorator(handler: AsyncEventHandler) -> AsyncEventHandler:
        event_bus.subscribe_async(event_type, handler)
        return handler
    return decorator
```

---

## Capability-Specific Events

**File**: `src/{capability}/domain/events.py`

```python
"""{{EntityName}} domain events."""

from pydantic import Field

from shared.domain.events import DomainEvent


class {{EntityName}}Created(DomainEvent):
    """Event raised when a {{EntityName}} is created."""

    entity_id: str
    code: str
    name: str
    created_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{entity_name}}.created"


class {{EntityName}}Updated(DomainEvent):
    """Event raised when a {{EntityName}} is updated."""

    entity_id: str
    code: str
    changed_fields: tuple[str, ...] = Field(default_factory=tuple)
    updated_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{entity_name}}.updated"


class {{EntityName}}Deleted(DomainEvent):
    """Event raised when a {{EntityName}} is deleted (soft delete)."""

    entity_id: str
    code: str
    deleted_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{entity_name}}.deleted"


class {{EntityName}}Activated(DomainEvent):
    """Event raised when a {{EntityName}} is activated."""

    entity_id: str
    code: str
    activated_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{entity_name}}.activated"


class {{EntityName}}Deactivated(DomainEvent):
    """Event raised when a {{EntityName}} is deactivated."""

    entity_id: str
    code: str
    deactivated_by: str | None = None

    @property
    def event_type(self) -> str:
        return "{{entity_name}}.deactivated"
```

---

## Publishing Events from Service

**File**: `src/{capability}/application/service.py` (updated)

```python
"""{{EntityName}} service with domain events."""

from shared.domain.events import event_bus
from ..domain.events import (
    {{EntityName}}Created,
    {{EntityName}}Updated,
    {{EntityName}}Deleted,
)


class {{EntityName}}Service(BaseService[...]):
    """Service for {{EntityName}} with event publishing."""

    def create(
        self,
        data: {{EntityName}}Create,
        user_id: str | None = None,
    ) -> {{EntityName}}Response:
        """Create entity and publish event."""
        result = super().create(data, user_id)

        # Publish domain event
        event_bus.publish(
            {{EntityName}}Created(
                entity_id=result.id,
                code=result.code,
                name=result.name,
                created_by=user_id,
            )
        )

        return result

    def update(
        self,
        entity_id: str,
        data: {{EntityName}}Update,
        user_id: str | None = None,
    ) -> {{EntityName}}Response:
        """Update entity and publish event."""
        # Track changed fields
        changed_fields = tuple(data.model_dump(exclude_unset=True).keys())

        result = super().update(entity_id, data, user_id)

        # Publish domain event
        event_bus.publish(
            {{EntityName}}Updated(
                entity_id=result.id,
                code=result.code,
                changed_fields=changed_fields,
                updated_by=user_id,
            )
        )

        return result

    def delete(
        self,
        entity_id: str,
        user_id: str | None = None,
    ) -> bool:
        """Delete entity and publish event."""
        entity = self.get_by_id(entity_id)

        result = super().delete(entity_id, user_id)

        # Publish domain event
        event_bus.publish(
            {{EntityName}}Deleted(
                entity_id=entity_id,
                code=entity.code,
                deleted_by=user_id,
            )
        )

        return result
```

---

## Event Handlers

**File**: `src/{capability}/application/event_handlers.py`

```python
"""{{EntityName}} event handlers."""

from shared.domain.events import on_event, on_event_async

from ..domain.events import {{EntityName}}Created, {{EntityName}}Updated


@on_event({{EntityName}}Created)
def log_{{entity_name}}_created(event: {{EntityName}}Created) -> None:
    """Log when {{EntityName}} is created."""
    print(f"{{EntityName}} created: {event.code} by {event.created_by}")


@on_event_async({{EntityName}}Created)
async def send_{{entity_name}}_notification(event: {{EntityName}}Created) -> None:
    """Send notification when {{EntityName}} is created."""
    # Example: Send email, push notification, etc.
    # await notification_service.send(...)
    pass


@on_event({{EntityName}}Updated)
def audit_{{entity_name}}_update(event: {{EntityName}}Updated) -> None:
    """Audit {{EntityName}} updates."""
    # Example: Write to audit log
    print(f"{{EntityName}} {event.code} updated: {event.changed_fields}")
```

---

## Cross-Capability Event Handling

**File**: `src/order_fulfillment/application/event_handlers.py`

```python
"""Order event handlers that react to other capabilities."""

from shared.domain.events import on_event
from product_catalog.domain.events import ProductUpdated
from inventory.domain.events import StockDepleted


@on_event(ProductUpdated)
def handle_product_update_in_orders(event: ProductUpdated) -> None:
    """React to product updates in order context."""
    if "unit_price" in event.changed_fields:
        # Update pending orders with new price
        pass


@on_event(StockDepleted)
def handle_stock_depleted(event: StockDepleted) -> None:
    """React to stock depletion."""
    # Notify pending orders, send alerts, etc.
    pass
```

---

## Registering Handlers on Startup

**File**: `src/main.py` (updated)

```python
"""Application entry point with event handler registration."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import event handlers to register them
from product_catalog.application import event_handlers as product_handlers
from order_fulfillment.application import event_handlers as order_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle."""
    # Event handlers are auto-registered via decorators
    yield


app = FastAPI(lifespan=lifespan)
```

---

## Testing Events

```python
"""Test domain events."""

import pytest
from unittest.mock import MagicMock

from shared.domain.events import EventBus
from product_catalog.domain.events import ProductCreated


class TestEventBus:
    """Test event bus functionality."""

    @pytest.fixture
    def event_bus(self):
        """Create fresh event bus for each test."""
        bus = EventBus()
        bus.clear()
        return bus

    def test_publish_calls_handler(self, event_bus):
        """Test that publishing calls subscribed handler."""
        handler = MagicMock()
        event_bus.subscribe(ProductCreated, handler)

        event = ProductCreated(
            entity_id="123",
            code="PROD-001",
            name="Test Product",
        )
        event_bus.publish(event)

        handler.assert_called_once_with(event)

    def test_multiple_handlers(self, event_bus):
        """Test multiple handlers for same event."""
        handler1 = MagicMock()
        handler2 = MagicMock()

        event_bus.subscribe(ProductCreated, handler1)
        event_bus.subscribe(ProductCreated, handler2)

        event = ProductCreated(
            entity_id="123",
            code="PROD-001",
            name="Test",
        )
        event_bus.publish(event)

        handler1.assert_called_once()
        handler2.assert_called_once()
```
