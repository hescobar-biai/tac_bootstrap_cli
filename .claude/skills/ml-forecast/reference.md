# ML Forecast Reference

Multi-framework patterns, Celes forecast-api-service orchestration, and supply chain metrics for demand forecasting.

## Table of Contents

1. [SKU Classification (Syntetos-Boylan-Croston)](#1-sku-classification-syntetos-boylan-croston)
2. [Seasonal Strength Detection](#2-seasonal-strength-detection)
3. [FastAPI Orchestrator Pattern](#3-fastapi-orchestrator-pattern)
4. [AWS Step Functions Pipeline](#4-aws-step-functions-pipeline)
5. [Multi-Tenant Configuration](#5-multi-tenant-configuration)
6. [Pydantic Pipeline Models](#6-pydantic-pipeline-models)
7. [Colombia Timezone Handling](#7-colombia-timezone-handling)
8. [BigQuery Integration](#8-bigquery-integration)
9. [Prophet Patterns](#9-prophet-patterns)
10. [LightGBM and XGBoost Patterns](#10-lightgbm-and-xgboost-patterns)
11. [PyTorch Patterns](#11-pytorch-patterns)
12. [scikit-learn Patterns](#12-scikit-learn-patterns)
13. [statsmodels Patterns](#13-statsmodels-patterns)
14. [Feature Engineering Recipes](#14-feature-engineering-recipes)
15. [Supply Chain Metrics](#15-supply-chain-metrics)
16. [Ensemble Methods](#16-ensemble-methods)
17. [Hyperparameter Tuning with Optuna](#17-hyperparameter-tuning-with-optuna)

---

## 1. SKU Classification (Syntetos-Boylan-Croston)

SBC classification is the **core Celes pattern** that determines which forecast model to use for each SKU based on its demand characteristics.

### Thresholds

```python
ADI_CUTOFF = 1.32          # Average Demand Interval
CV2_CUTOFF = 0.49          # Squared Coefficient of Variation
SEASON_STRENGTH_TH = 0.64  # Seasonal strength threshold
```

### Classification Logic

```python
def classify_sku(demand_series):
    """Classify SKU using Syntetos-Boylan-Croston framework.

    Returns one of:
    - "smooth": Low ADI, Low CV2 -> Regular demand -> Use LightGBM/Prophet
    - "erratic": Low ADI, High CV2 -> Irregular magnitude -> Use XGBoost with robustness
    - "intermittent": High ADI, Low CV2 -> Sporadic but consistent -> Use Croston's method
    - "lumpy": High ADI, High CV2 -> Sporadic and irregular -> Use SBA
    """
    adi = compute_adi(demand_series)
    cv2 = compute_cv2(demand_series)

    if adi < ADI_CUTOFF:
        return "erratic" if cv2 >= CV2_CUTOFF else "smooth"
    else:
        return "lumpy" if cv2 >= CV2_CUTOFF else "intermittent"
```

### ADI (Average Demand Interval)

```python
def compute_adi(series):
    """Average number of periods between non-zero demands."""
    non_zero_idx = series[series > 0].index
    if len(non_zero_idx) < 2:
        return float('inf')  # No demand pattern
    intervals = np.diff(non_zero_idx)
    return np.mean(intervals)
```

### CV2 (Squared Coefficient of Variation)

```python
def compute_cv2(series):
    """Squared coefficient of variation of non-zero demands."""
    non_zero = series[series > 0]
    if len(non_zero) < 2:
        return 0.0
    return (non_zero.std() / non_zero.mean()) ** 2
```

### Model Selection by SBC Class

| SBC Class | ADI | CV2 | Recommended Models | Use Case |
|-----------|-----|-----|-------------------|----------|
| Smooth | < 1.32 | < 0.49 | LightGBM, Prophet, ARIMA | Regular demand (fast-movers) |
| Erratic | < 1.32 | >= 0.49 | XGBoost (robust), Quantile Regression | High variance demand |
| Intermittent | >= 1.32 | < 0.49 | Croston, SBA, TSB | Sporadic but predictable |
| Lumpy | >= 1.32 | >= 0.49 | SBA, bootstrapping, zero-inflated | Hardest to forecast |

---

## 2. Seasonal Strength Detection

```python
SEASON_STRENGTH_TH = 0.64

def detect_seasonality(series, period=7):
    """Detect if series has significant seasonality.
    Uses STL decomposition and compares seasonal vs residual variance.
    """
    from statsmodels.tsa.seasonal import STL
    stl = STL(series, period=period, robust=True)
    result = stl.fit()

    season_strength = 1 - (result.resid.var() / (result.seasonal + result.resid).var())
    return season_strength > SEASON_STRENGTH_TH, season_strength
```

A `season_strength` above 0.64 indicates significant weekly seasonality, which informs whether to enable seasonal components in Prophet or add Fourier features for LightGBM/XGBoost.

---

## 3. FastAPI Orchestrator Pattern

The real codebase uses FastAPI as an orchestrator that triggers AWS Step Functions.

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="Forecast Orchestrator")

class ForecastRequest(BaseModel):
    client_id: str
    sku_ids: list[str] | None = None  # None = all SKUs
    horizon: int = 14
    include_promotional: bool = False

@app.post("/forecast/trigger")
async def trigger_forecast(request: ForecastRequest, background_tasks: BackgroundTasks):
    """Trigger forecast pipeline via AWS Step Functions."""
    execution_arn = await start_step_function(
        state_machine_arn=get_state_machine_arn(request.client_id),
        input_payload={
            "client_id": request.client_id,
            "sku_ids": request.sku_ids,
            "horizon": request.horizon,
            "include_promotional": request.include_promotional,
        }
    )
    return {"execution_arn": execution_arn, "status": "RUNNING"}
```

---

## 4. AWS Step Functions Pipeline

```
Step 1: SKU Classification (SBC)
    |
Step 2: Feature Engineering (per SBC class)
    |
Step 3: Model Training/Selection
    |
Step 4: Forecast Generation
    |
Step 5: Post-processing (clipping, rounding)
    |
Step 6: Write to BigQuery
```

Each step receives the pipeline payload via `AwsBodyPipeline` (see section 6) and passes enriched results to the next step. SBC classification in Step 1 determines which model family Step 3 trains.

---

## 5. Multi-Tenant Configuration

```yaml
# config/{client_id}.yml
client_id: "acme_corp"
timezone: "America/Bogota"  # Colombia: UTC-5
data_source:
  type: bigquery
  project: "celes-prod"
  dataset: "50_serving_acme_corp"
  demand_table: "dm_demand_history"

forecast:
  default_horizon: 14
  min_history_days: 90
  sbc_thresholds:
    adi_cutoff: 1.32
    cv2_cutoff: 0.49
    season_strength: 0.64

  model_config:
    smooth:
      primary: lightgbm
      fallback: prophet
    erratic:
      primary: xgboost
      fallback: lightgbm
    intermittent:
      primary: croston
      fallback: sba
    lumpy:
      primary: sba
      fallback: zero_inflated
```

Each client has its own YAML config, allowing per-tenant thresholds, model selection, and data source configuration.

---

## 6. Pydantic Pipeline Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AwsBodyPipeline(BaseModel):
    """Input model for forecast pipeline."""
    client_id: str
    sku_id: str
    horizon: int = 14
    start_date: datetime
    end_date: datetime
    sbc_class: str  # "smooth", "erratic", "intermittent", "lumpy"

class AwsBodyPipelinePromotional(AwsBodyPipeline):
    """Extended model for promotional forecasts."""
    promotion_start: datetime
    promotion_end: datetime
    promotion_type: str  # "discount", "bogo", "bundle"
    expected_lift: Optional[float] = None
```

---

## 7. Colombia Timezone Handling

```python
from datetime import datetime, timezone, timedelta

COLOMBIA_TZ = timezone(timedelta(hours=-5))

def now_colombia() -> datetime:
    return datetime.now(COLOMBIA_TZ)

def to_colombia(dt: datetime) -> datetime:
    return dt.astimezone(COLOMBIA_TZ)
```

All timestamp comparisons and date boundaries in forecast pipelines must use Colombia time (UTC-5).

---

## 8. BigQuery Integration

```python
from google.cloud import bigquery

def write_forecasts_to_bq(client_id: str, forecasts_df: pd.DataFrame):
    """Write forecast results to BigQuery."""
    client = bigquery.Client()
    table_id = f"celes-prod.50_serving_{client_id}.forecast_results"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        schema=[
            bigquery.SchemaField("sku_id", "STRING"),
            bigquery.SchemaField("forecast_date", "DATE"),
            bigquery.SchemaField("forecast_value", "FLOAT64"),
            bigquery.SchemaField("lower_bound", "FLOAT64"),
            bigquery.SchemaField("upper_bound", "FLOAT64"),
            bigquery.SchemaField("model_used", "STRING"),
            bigquery.SchemaField("sbc_class", "STRING"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
        ],
    )

    job = client.load_table_from_dataframe(forecasts_df, table_id, job_config=job_config)
    job.result()
```

---

## 9. Prophet Patterns

### Basic Prophet Forecast

```python
from prophet import Prophet
import pandas as pd

df = pd.DataFrame({"ds": dates, "y": sales})

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode="multiplicative",
)
model.fit(df)

future = model.make_future_dataframe(periods=14, freq="D")
forecast = model.predict(future)
```

### Custom Seasonality and Holidays

```python
model = Prophet(
    yearly_seasonality=10,
    weekly_seasonality=3,
    seasonality_mode="multiplicative",
    changepoint_prior_scale=0.05,
    changepoint_range=0.9,
)
model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
model.add_country_holidays(country_name="CO")  # Colombia holidays

model.add_regressor("is_promotion", mode="multiplicative")
model.add_regressor("price", mode="multiplicative")
```

### Cross-Validation

```python
from prophet.diagnostics import cross_validation, performance_metrics

cv_results = cross_validation(
    model, initial="365 days", period="30 days", horizon="14 days"
)
metrics = performance_metrics(cv_results)
# Returns: mse, rmse, mae, mape, mdape, smape, coverage
```

---

## 10. LightGBM and XGBoost Patterns

### LightGBM Training

```python
import lightgbm as lgb

params = {
    "objective": "regression",
    "metric": "mae",
    "boosting_type": "gbdt",
    "n_estimators": 1000,
    "learning_rate": 0.05,
    "num_leaves": 31,
    "min_child_samples": 20,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 0.1,
    "verbose": -1,
}

model = lgb.LGBMRegressor(**params)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)],
)
```

### XGBoost Training

```python
import xgboost as xgb

params = {
    "objective": "reg:squarederror",
    "eval_metric": "mae",
    "n_estimators": 1000,
    "learning_rate": 0.05,
    "max_depth": 6,
    "min_child_weight": 5,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "tree_method": "hist",
    "verbosity": 0,
}

model = xgb.XGBRegressor(**params)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,
    verbose=100,
)
```

### Multi-Step Forecasting

```python
# Direct strategy: one model per horizon step
models = {}
for h in range(1, horizon + 1):
    df[f"target_h{h}"] = df["sales"].shift(-h)
    models[h] = lgb.LGBMRegressor(**params)
    models[h].fit(X_train, df[f"target_h{h}"].loc[train_idx])

# Recursive strategy: single model, feed predictions back
predictions = []
current_features = X_test.iloc[0].copy()
for step in range(horizon):
    pred = model.predict(current_features.values.reshape(1, -1))[0]
    predictions.append(pred)
    current_features = update_lags(current_features, pred)
```

---

## 11. PyTorch Patterns

### LSTM for Time Series

```python
import torch
import torch.nn as nn

class LSTMForecaster(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2,
                 output_size=14, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size, hidden_size=hidden_size,
            num_layers=num_layers, batch_first=True, dropout=dropout,
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, output_size),
        )

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])
```

### Temporal Fusion Transformer

```python
from pytorch_forecasting import TemporalFusionTransformer
from pytorch_forecasting.data import TimeSeriesDataSet

training = TimeSeriesDataSet(
    data=train_df,
    time_idx="time_idx",
    target="sales",
    group_ids=["sku_id"],
    max_encoder_length=60,
    max_prediction_length=14,
    static_categoricals=["category", "store"],
    time_varying_known_reals=["price", "is_promotion"],
    time_varying_unknown_reals=["sales"],
)

model = TemporalFusionTransformer.from_dataset(
    training, learning_rate=0.001, hidden_size=32,
    attention_head_size=4, dropout=0.1,
    hidden_continuous_size=16, output_size=7,
    loss=QuantileLoss(),
)
```

### Training Loop with Early Stopping

```python
def train_model(model, train_loader, val_loader, epochs=100, lr=1e-3):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
    criterion = nn.MSELoss()
    best_val_loss, patience_counter = float("inf"), 0

    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(X_batch), y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

        model.eval()
        val_loss = sum(criterion(model(X), y).item() for X, y in val_loader) / len(val_loader)
        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), "best_model.pt")
            patience_counter = 0
        elif (patience_counter := patience_counter + 1) >= 10:
            break

    model.load_state_dict(torch.load("best_model.pt"))
    return model
```

---

## 12. scikit-learn Patterns

### Pipeline with Preprocessing

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

numeric_features = ["price", "lag_1", "lag_7", "rolling_mean_7"]
categorical_features = ["day_of_week", "month", "category"]

preprocessor = ColumnTransformer(transformers=[
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_features),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", lgb.LGBMRegressor(**params)),
])
pipeline.fit(X_train, y_train)
```

### TimeSeriesSplit with GridSearchCV

```python
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

tscv = TimeSeriesSplit(n_splits=5)
param_grid = {
    "regressor__n_estimators": [500, 1000],
    "regressor__learning_rate": [0.01, 0.05, 0.1],
    "regressor__num_leaves": [15, 31, 63],
}

grid_search = GridSearchCV(
    pipeline, param_grid, cv=tscv,
    scoring="neg_mean_absolute_error", n_jobs=-1,
)
grid_search.fit(X_train, y_train)
```

### Custom Transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class LagFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lags=(1, 7, 14, 28), target_col="sales"):
        self.lags = lags
        self.target_col = target_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for lag in self.lags:
            X[f"lag_{lag}"] = X[self.target_col].shift(lag)
        return X
```

---

## 13. statsmodels Patterns

### ARIMA / SARIMAX

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(
    endog=y_train, exog=X_train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
    enforce_stationarity=False,
    enforce_invertibility=False,
)
results = model.fit(disp=False)
forecast = results.forecast(steps=14, exog=X_test)
```

### ETS (Exponential Smoothing)

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    endog=y_train, trend="add", seasonal="mul",
    seasonal_periods=7, damped_trend=True,
)
results = model.fit(optimized=True)
forecast = results.forecast(steps=14)
```

### Auto-ARIMA with pmdarima

```python
import pmdarima as pm

auto_model = pm.auto_arima(
    y_train, seasonal=True, m=7, stepwise=True,
    suppress_warnings=True, error_action="ignore",
    max_p=5, max_q=5, max_P=2, max_Q=2,
    information_criterion="aic",
)
forecast = auto_model.predict(n_periods=14)
```

---

## 14. Feature Engineering Recipes

### Lag Features

```python
def create_lag_features(df, target_col="sales", lags=(1, 2, 3, 7, 14, 21, 28)):
    for lag in lags:
        df[f"lag_{lag}"] = df.groupby("sku_id")[target_col].shift(lag)
    return df
```

### Rolling Statistics

```python
def create_rolling_features(df, target_col="sales", windows=(7, 14, 28)):
    for w in windows:
        g = df.groupby("sku_id")[target_col]
        df[f"rolling_mean_{w}"] = g.transform(lambda x: x.shift(1).rolling(w, min_periods=1).mean())
        df[f"rolling_std_{w}"] = g.transform(lambda x: x.shift(1).rolling(w, min_periods=1).std())
    return df
```

### Calendar Features

```python
def create_calendar_features(df, date_col="date"):
    dt = df[date_col]
    for name, val in [("day_of_week", dt.dt.dayofweek), ("day_of_month", dt.dt.day),
                      ("week_of_year", dt.dt.isocalendar().week.astype(int)),
                      ("month", dt.dt.month), ("quarter", dt.dt.quarter),
                      ("is_weekend", (dt.dt.dayofweek >= 5).astype(int)),
                      ("is_month_start", dt.dt.is_month_start.astype(int)),
                      ("is_month_end", dt.dt.is_month_end.astype(int))]:
        df[name] = val
    return df
```

### Holiday Features (Colombia)

```python
import holidays as holidays_lib

def create_holiday_features(df, date_col="date", country="CO"):
    """Add holiday indicator and days-to-next-holiday. Default: Colombia."""
    country_holidays = holidays_lib.country_holidays(country)
    df["is_holiday"] = df[date_col].apply(lambda d: 1 if d in country_holidays else 0)
    all_dates = pd.date_range(df[date_col].min(), df[date_col].max())
    holiday_dates = sorted(d for d in all_dates if d in country_holidays)
    df["days_to_next_holiday"] = df[date_col].apply(
        lambda d: min(((h - d).days for h in holiday_dates if h >= d), default=-1))
    return df
```

### Promotional and Price Features

```python
def create_promo_features(df, promo_col="is_promotion"):
    for w in [7, 14, 28]:
        df[f"promo_count_{w}d"] = df.groupby("sku_id")[promo_col].transform(
            lambda x: x.rolling(w, min_periods=1).sum())
    return df

def create_price_features(df, price_col="price"):
    g = df.groupby("sku_id")[price_col]
    df["price_ratio_to_avg"] = df[price_col] / g.transform("mean")
    df["price_pct_change"] = g.transform(lambda x: x.pct_change())
    df["price_discount_depth"] = 1 - (df[price_col] / g.transform("max"))
    return df
```

---

## 15. Supply Chain Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **MAPE** | `mean(abs(actual - predicted) / actual) * 100` | Avg % error. Undefined when actual = 0. |
| **WMAPE** | `sum(abs(actual - predicted)) / sum(actual) * 100` | Volume-weighted. Preferred for portfolios. |
| **Bias** | `mean((predicted - actual) / actual) * 100` | Positive = over-forecast. |
| **Fill Rate** | `sum(min(available, demand)) / sum(demand) * 100` | % demand satisfied from stock. |
| **OTIF** | `count(on_time AND in_full) / count(orders) * 100` | % orders delivered complete and on time. |
| **MAE** | `mean(abs(actual - predicted))` | Avg absolute error in units. |
| **RMSE** | `sqrt(mean((actual - predicted)^2))` | Penalizes large errors more. |

```python
import numpy as np

def mape(actual, predicted):
    mask = actual != 0
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100

def wmape(actual, predicted):
    return np.sum(np.abs(actual - predicted)) / np.sum(np.abs(actual)) * 100

def bias(actual, predicted):
    mask = actual != 0
    return np.mean((predicted[mask] - actual[mask]) / actual[mask]) * 100

def fill_rate(demand, available_stock):
    return np.sum(np.minimum(demand, available_stock)) / np.sum(demand) * 100
```

---

## 16. Ensemble Methods

### Weighted Blending

```python
from scipy.optimize import minimize
import numpy as np

def optimize_weights(predictions_list, actual, metric_fn=None):
    if metric_fn is None:
        metric_fn = lambda a, p: np.mean(np.abs(a - p))
    n_models = len(predictions_list)

    def objective(weights):
        blended = sum(w * p for w, p in zip(weights, predictions_list))
        return metric_fn(actual, blended)

    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    bounds = [(0.0, 1.0)] * n_models
    result = minimize(objective, np.ones(n_models) / n_models,
                      bounds=bounds, constraints=constraints)
    return result.x
```

### Stacking (TimeSeriesSplit + Ridge meta-learner)

```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit

def stacking_ensemble(models, X_train, y_train, X_test, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    meta_train = np.zeros((len(X_train), len(models)))
    meta_test = np.zeros((len(X_test), len(models)))
    for i, model in enumerate(models):
        test_preds = np.zeros((len(X_test), n_splits))
        for fold, (ti, vi) in enumerate(tscv.split(X_train)):
            model.fit(X_train.iloc[ti], y_train.iloc[ti])
            meta_train[vi, i] = model.predict(X_train.iloc[vi])
            test_preds[:, fold] = model.predict(X_test)
        meta_test[:, i] = test_preds.mean(axis=1)
    meta_model = Ridge(alpha=1.0)
    meta_model.fit(meta_train, y_train)
    return meta_model.predict(meta_test), meta_model
```

---

## 17. Hyperparameter Tuning with Optuna

```python
import optuna, lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit

def lgb_objective(trial):
    params = {
        "objective": "regression", "metric": "mae", "verbose": -1, "n_estimators": 1000,
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 15, 127),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
    }
    scores = []
    for ti, vi in TimeSeriesSplit(n_splits=3).split(X_train):
        m = lgb.LGBMRegressor(**params)
        m.fit(X_train.iloc[ti], y_train.iloc[ti],
              eval_set=[(X_train.iloc[vi], y_train.iloc[vi])],
              callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)])
        scores.append(wmape(y_train.iloc[vi].values, m.predict(X_train.iloc[vi])))
    return np.mean(scores)

study = optuna.create_study(direction="minimize")
study.optimize(lgb_objective, n_trials=100, show_progress_bar=True)
```
