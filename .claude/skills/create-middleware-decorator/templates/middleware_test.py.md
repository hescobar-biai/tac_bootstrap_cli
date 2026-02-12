# Middleware Test Template

**File**: `tests/unit/shared/presentation/test_{{middleware_name}}.py`

```python
"""{{middleware_class}} unit tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from starlette.testclient import TestClient
from fastapi import FastAPI


class Test{{middleware_class}}:
    @pytest.fixture
    def app(self):
        """Create test app with middleware."""
        app = FastAPI()
        {{middleware_setup}}
        return app

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    def test_middleware_processes_request(self, client):
        """Test middleware intercepts requests."""
        response = client.get("/test")
        {{request_assertions}}

    def test_middleware_handles_errors_gracefully(self, client):
        """Test middleware doesn't break on errors."""
        {{error_test}}

    def test_middleware_cleanup(self, client):
        """Test middleware cleans up context."""
        {{cleanup_test}}
```
