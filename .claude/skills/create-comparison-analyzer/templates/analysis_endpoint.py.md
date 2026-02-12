# Analysis Endpoint Template

**File**: `src/evaluation/api/routes/{{analyzer_name}}_routes.py`

```python
"""
IDK: api-endpoint, {{analyzer_name}}, evaluation

Responsibility:
- Expose {{analyzer_name}} analysis via REST API
"""

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/evaluation/{{analyzer_name_kebab}}", tags=["evaluation"])


@router.post("/analyze")
async def analyze_{{analyzer_name}}(
    request: dict,
) -> dict:
    """Analyze {{metric_type}} across execution results."""
    analyzer = {{analyzer_class}}()
    return analyzer.analyze(request.get("results", []))
```
