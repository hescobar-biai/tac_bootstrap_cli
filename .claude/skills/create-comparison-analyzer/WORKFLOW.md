# Comparison Analyzer Creation Workflow

## Pre-flight Checklist

```
Analyzer Information:
- [ ] Analyzer name: e.g., TokenUsage, Latency, Cost, SchemaValidity
- [ ] Metric type: what is being measured
- [ ] Metric fields: specific measurements captured
- [ ] Ranking criteria: how models are ranked
- [ ] Input: what data the analyzer receives (execution results)
```

## Step 1: Create Metric Value Objects

**File**: `<source-dir>/<capability>/domain/value_objects/{metric_type}_metrics.py`

Use template: [templates/analysis_metrics_vo.py.md](templates/analysis_metrics_vo.py.md)

## Step 2: Create Analyzer Service

**File**: `<source-dir>/<capability>/application/services/{analyzer_name}_analyzer.py`

Use template: [templates/analyzer_service.py.md](templates/analyzer_service.py.md)

## Step 3: Create API Endpoint

**File**: `<source-dir>/<capability>/api/routes/{analyzer_name}_routes.py`

Use template: [templates/analysis_endpoint.py.md](templates/analysis_endpoint.py.md)

## Step 4: Create Unit Tests

**File**: `<test-dir>/<capability>/application/test_{analyzer_name}_analyzer.py`

Use template: [templates/analyzer_test.py.md](templates/analyzer_test.py.md)

## Step 5: Validation

```bash
uv run pytest <test-dir>/<capability>/application/test_{analyzer_name}_analyzer.py -v
```
