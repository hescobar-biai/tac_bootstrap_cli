# FastAPI Middleware Template

**File**: `src/shared/presentation/middleware/{{middleware_name}}.py`

```python
"""
IDK: middleware, {{concern_type}}, cross-cutting, fastapi

Responsibility:
- Intercept HTTP requests/responses for {{concern_type}}
- Execute pre-hook before request processing
- Execute post-hook after response generation
- Clean up context in finally block

Invariants:
- Must not block request processing
- Must not break main logic on failure
- Context cleaned up in finally block
"""

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class {{middleware_class}}(BaseHTTPMiddleware):
    """
    {{concern_type}} middleware for cross-cutting {{concern_type}} concerns.
    """

    def __init__(self, app, {{config_params}}) -> None:
        super().__init__(app)
        {{config_assignments}}

    async def dispatch(self, request: Request, call_next) -> Response:
        """Intercept request for {{concern_type}}."""
        try:
            # Pre-hook
            {{pre_hook}}

            response = await call_next(request)

            # Post-hook
            {{post_hook}}

            return response
        except Exception as e:
            logger.error("middleware_error", middleware="{{middleware_name}}", error=str(e))
            raise
        finally:
            # Clean up
            {{cleanup}}
```
