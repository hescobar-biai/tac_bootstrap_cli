---
name: ml-forecast
description: "Builds and optimizes demand forecasting systems using FastAPI orchestration, AWS Step Functions pipelines, BigQuery data sources, and Syntetos-Boylan-Croston classification. Use when creating forecast pipelines, configuring multi-tenant forecast execution, implementing SKU classification, or building ML models with LightGBM, Prophet, XGBoost, PyTorch, scikit-learn, and statsmodels."
context: fork
agent: ml-engineer
---

# ML Demand Forecasting

Build production-quality demand forecasting systems for supply chain prediction. This skill covers the full stack: FastAPI orchestration services, AWS Step Functions pipeline execution, BigQuery data integration, SKU classification, and multi-framework ML modeling.

## Instructions

### 1. Understand the Forecasting Architecture

Celes uses a **three-tier forecasting architecture**:

```
FastAPI Orchestrator (forecast-api-service)
    |
    +-- BigQuery: Read historical data (stg_agg_Invoices)
    +-- AWS Step Functions: Execute ML pipeline (wk-forecast-gcp-aws)
    +-- AWS Lambda: Execute promotional forecast
```

- **FastAPI Service**: Orchestrates pipeline execution, handles multi-tenant config
- **AWS Step Functions**: Runs the actual ML training/prediction workflow
- **BigQuery**: Source of truth for historical sales data
- **Multi-tenant**: Each client has its own configuration (YAML per environment)

### 2. SKU Classification: Syntetos-Boylan-Croston

Before selecting a forecasting model, classify SKUs using the **SBC framework**:

| Parameter | Threshold | Purpose |
|-----------|-----------|---------|
| **ADI_CUTOFF** | 1.32 | Average Demand Interval -- separates intermittent from regular demand |
| **CV2_CUTOFF** | 0.49 | Coefficient of Variation squared -- separates erratic from smooth demand |
| **SEASON_STRENGTH_TH** | 0.64 | Season strength threshold -- identifies seasonal patterns |

**Classification Matrix**:

| ADI < 1.32 | CV2 < 0.49 | Classification | Recommended Model |
|------------|-----------|----------------|-------------------|
| Yes | Yes | Smooth | LightGBM/XGBoost, ETS |
| Yes | No | Erratic | Ensemble (LightGBM + Prophet) |
| No | Yes | Intermittent | Croston's method, SBA |
| No | No | Lumpy | Croston's method, simple average |

### 3. Multi-Tenant Configuration

Each tenant is configured via YAML files per environment (`dev`, `qas`, `prd`):

```yaml
# config/dev.yml
bigquery:
  project_id: "celes-platform-dev"
  dataset: "analytics"
aws:
  region: "us-east-1"
  step_function_arn: "arn:aws:states:us-east-1:ACCOUNT:stateMachine:wk-forecast-gcp-aws"
thresholds:
  ADI_CUTOFF: 1.32
  CV2_CUTOFF: 0.49
  SEASON_STRENGTH_TH: 0.64
```

### 4. Pipeline Execution Patterns

#### Standard Forecast Pipeline (AWS Step Functions)

```python
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

def get_current_date_colombia():
    """Returns current date in Colombia timezone (UTC-5)."""
    fecha_colombia = datetime.utcnow() - timedelta(hours=5)
    return fecha_colombia.strftime("%Y-%m-%d")

class AwsBodyPipeline(BaseModel):
    tenant_id: str
    execution_type: str = Field(default='TEST', description="LIVE or TEST")
    env: str = Field(default='dev', description="dev, qas, or prd")
    date_read_export: str = Field(default_factory=get_current_date_colombia)
    backtest_interval: str = Field(default='28')
    stage: str = Field(default="aws_pipeline_execute")
    backtest_start_date: str | None = None
    forecast_start_date: str | None = None
```

#### Promotional Forecast Pipeline (AWS Lambda)

```python
class AwsBodyPipelinePromotional(BaseModel):
    client: str
    tenant: str
    environment: str = Field(default='dev')
    distributed: str = Field(default='True')
    mode: str = Field(default='run_all')
```

### 5. BigQuery Data Integration

The forecast pipeline reads from BigQuery to determine start dates:

```python
from google.cloud import bigquery

def get_default_start_date_from_bq(tenant_id: str, env: str) -> str:
    """Query BigQuery for the last invoice date to set forecast start."""
    client = bigquery.Client()
    query = f"""
        SELECT MAX(date) as last_date
        FROM `celes-platform-{env}.{tenant_id}.stg_agg_Invoices`
    """
    result = client.query(query).result()
    for row in result:
        return row.last_date.strftime("%Y-%m-%d")
```

### 6. Select the Right ML Framework

Choose based on SKU classification and data characteristics:

| Framework | Best For | When to Use |
|-----------|----------|-------------|
| **LightGBM/XGBoost** | Smooth & erratic demand | Large datasets, many features, promotional effects |
| **Prophet** | Seasonal patterns | Strong seasonality, holiday effects, quick prototyping |
| **Croston/SBA** | Intermittent & lumpy demand | Spare parts, low-volume SKUs |
| **PyTorch (LSTM/TFT)** | Complex temporal patterns | Multi-horizon, multivariate |
| **statsmodels (ARIMA/ETS)** | Statistical baselines | Baseline comparison, interpretability |

For detailed framework patterns and code templates, see [reference.md](reference.md).

### 7. Feature Engineering for Supply Chain

Build features in this order:

1. **Lag features**: 1, 2, 3, 7, 14, 21, 28-day lags
2. **Rolling statistics**: Mean, std, min, max over 7, 14, 28-day windows
3. **Calendar features**: day_of_week, month, is_weekend, is_holiday (Colombia holidays)
4. **Promotional features**: is_promotion, discount_depth, days_since_last_promo
5. **Price features**: Price ratio to average, price changes

### 8. Evaluation with Supply Chain Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| **WMAPE** | `sum(abs(A-F)) / sum(A) * 100` | Primary metric for portfolios |
| **MAPE** | `mean(abs(A-F)/A) * 100` | Per-SKU accuracy (exclude zero demand) |
| **Bias** | `mean((F-A)/A) * 100` | Detect systematic over/under-forecasting |
| **Fill Rate** | `sum(min(stock, demand)) / sum(demand)` | Inventory service level |
| **OTIF** | `count(on_time AND in_full) / count(orders)` | Delivery performance |

Use the evaluation script at [templates/evaluate.py](templates/evaluate.py) for standardized computation.

### 9. Output Artifacts

Every pipeline execution should produce:
- Forecast predictions (uploaded to BigQuery)
- Backtest metrics report (WMAPE, bias per SKU family)
- SKU classification results (SBC matrix)
- Feature importance rankings
- Step Functions execution ARN for tracking

## Examples

### Example 1: Configure a New Tenant Forecast Pipeline

User request:
```
Set up forecast pipeline for a new client "acme" in dev environment
```

You would:
1. Create tenant config YAML at `config/dev.yml` with BigQuery and AWS settings
2. Configure the AwsBodyPipeline with tenant_id="acme", env="dev"
3. Query BigQuery for historical data availability: `stg_agg_Invoices`
4. Set backtest_interval based on data history (default 28 days)
5. Execute pipeline via the `/execute_forecast_aws` endpoint
6. Monitor via AWS Step Functions console using the returned ARN

### Example 2: Implement SKU Classification

User request:
```
Classify our SKU portfolio using Syntetos-Boylan-Croston before running forecasts
```

You would:
1. Query historical demand data from BigQuery
2. Calculate ADI (Average Demand Interval) per SKU
3. Calculate CV2 (Coefficient of Variation squared) per SKU
4. Apply thresholds: ADI_CUTOFF=1.32, CV2_CUTOFF=0.49
5. Assign each SKU to: Smooth, Erratic, Intermittent, or Lumpy
6. Route each group to the appropriate forecasting method
7. Generate classification report with distribution summary

### Example 3: Build a LightGBM Forecast with Backtesting

User request:
```
Build a LightGBM model for smooth-demand SKUs with 28-day backtest
```

You would:
1. Filter SKUs classified as "Smooth" (ADI < 1.32, CV2 < 0.49)
2. Use [templates/train_pipeline.py](templates/train_pipeline.py) as base
3. Engineer features: lags, rolling stats, calendar, promotions
4. Time-based split with 28-day backtest window
5. Train LightGBM with early stopping, tune with Optuna
6. Evaluate using WMAPE and bias from [templates/evaluate.py](templates/evaluate.py)
7. Compare against naive baseline (seasonal naive)
8. Upload forecasts to BigQuery forecast table

## Supporting Files

| File | Purpose |
|------|---------|
| [reference.md](reference.md) | Multi-framework API patterns, SBC classification, feature engineering, metrics |
| [templates/train_pipeline.py](templates/train_pipeline.py) | Base training pipeline with time-based splits |
| [templates/evaluate.py](templates/evaluate.py) | Supply chain metrics computation |
| [examples/demand_forecast_lightgbm.py](examples/demand_forecast_lightgbm.py) | Complete LightGBM example |
| [examples/demand_forecast_prophet.py](examples/demand_forecast_prophet.py) | Complete Prophet example |
