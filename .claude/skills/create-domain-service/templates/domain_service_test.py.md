# Domain Service Test Template

## Template

**File**: `tests/unit/{{bounded_context}}/application/test_{{service_name}}.py`

```python
"""{{service_class}} unit tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.{{bounded_context}}.application.services.{{service_name}} import {{service_class}}


class Test{{service_class}}:
    """Test suite for {{service_class}}."""

    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies."""
        return {
            {{mock_dependencies}}
        }

    @pytest.fixture
    def service(self, mock_dependencies):
        """Create service with mocked dependencies."""
        return {{service_class}}(**mock_dependencies)

    @pytest.mark.asyncio
    async def test_{{method_name}}_success(self, service, mock_dependencies):
        """Test successful {{method_name}} execution."""
        # Arrange
        {{arrange}}

        # Act
        result = await service.{{method_name}}({{call_params}})

        # Assert
        {{assertions}}

    @pytest.mark.asyncio
    async def test_{{method_name}}_error_case(self, service, mock_dependencies):
        """Test {{method_name}} error handling."""
        # Arrange
        {{error_arrange}}

        # Act & Assert
        with pytest.raises({{expected_exception}}):
            await service.{{method_name}}({{error_params}})
```
