"""
Base Training Pipeline for Demand Forecasting
==============================================

A scikit-learn-compatible training pipeline with:
- Time-based train/validation/test split
- Feature engineering functions (lags, rolling stats, calendar)
- Configurable model framework (LightGBM, XGBoost, Ridge)
- Metrics computation and reporting

Usage:
    Adapt this template to your specific dataset and requirements.
    Replace placeholder column names with your actual schema.

Dependencies:
    pip install pandas numpy scikit-learn lightgbm xgboost joblib
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class PipelineConfig:
    """Configuration for the forecasting pipeline."""

    # Data columns
    date_col: str = "date"
    target_col: str = "sales"
    group_col: str = "sku_id"

    # Split parameters
    val_days: int = 14
    test_days: int = 14

    # Feature engineering
    lag_days: tuple[int, ...] = (1, 2, 3, 7, 14, 21, 28)
    rolling_windows: tuple[int, ...] = (7, 14, 28)

    # Model framework: "lightgbm", "xgboost", or "ridge"
    framework: str = "lightgbm"

    # Model hyperparameters (framework-specific)
    model_params: dict[str, Any] = field(default_factory=lambda: {
        "n_estimators": 1000,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "max_depth": -1,
        "min_child_samples": 20,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0.1,
        "reg_lambda": 0.1,
        "verbose": -1,
    })

    # Output
    output_dir: str = "artifacts"


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def create_lag_features(
    df: pd.DataFrame,
    target_col: str = "sales",
    group_col: str = "sku_id",
    lags: tuple[int, ...] = (1, 2, 3, 7, 14, 21, 28),
) -> pd.DataFrame:
    """Create lagged values of the target variable."""
    df = df.copy()
    for lag in lags:
        df[f"lag_{lag}"] = df.groupby(group_col)[target_col].shift(lag)
    return df


def create_rolling_features(
    df: pd.DataFrame,
    target_col: str = "sales",
    group_col: str = "sku_id",
    windows: tuple[int, ...] = (7, 14, 28),
) -> pd.DataFrame:
    """Compute rolling mean, std, min, max over specified windows."""
    df = df.copy()
    for window in windows:
        grouped = df.groupby(group_col)[target_col]
        df[f"rolling_mean_{window}"] = grouped.transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).mean()
        )
        df[f"rolling_std_{window}"] = grouped.transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).std()
        )
        df[f"rolling_min_{window}"] = grouped.transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).min()
        )
        df[f"rolling_max_{window}"] = grouped.transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).max()
        )
    return df


def create_calendar_features(
    df: pd.DataFrame,
    date_col: str = "date",
) -> pd.DataFrame:
    """Extract calendar-based features from the date column."""
    df = df.copy()
    dt = pd.to_datetime(df[date_col])
    df["day_of_week"] = dt.dt.dayofweek
    df["day_of_month"] = dt.dt.day
    df["week_of_year"] = dt.dt.isocalendar().week.astype(int)
    df["month"] = dt.dt.month
    df["quarter"] = dt.dt.quarter
    df["is_weekend"] = (dt.dt.dayofweek >= 5).astype(int)
    df["is_month_start"] = dt.dt.is_month_start.astype(int)
    df["is_month_end"] = dt.dt.is_month_end.astype(int)
    return df


def engineer_features(df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Apply all feature engineering steps in sequence."""
    logger.info("Engineering features...")
    df = create_lag_features(
        df,
        target_col=config.target_col,
        group_col=config.group_col,
        lags=config.lag_days,
    )
    df = create_rolling_features(
        df,
        target_col=config.target_col,
        group_col=config.group_col,
        windows=config.rolling_windows,
    )
    df = create_calendar_features(df, date_col=config.date_col)

    # Drop rows with NaN from lag/rolling features
    initial_len = len(df)
    df = df.dropna(subset=[f"lag_{max(config.lag_days)}"])
    logger.info(
        "Dropped %d rows with insufficient history (%.1f%%)",
        initial_len - len(df),
        (initial_len - len(df)) / initial_len * 100,
    )
    return df


# ---------------------------------------------------------------------------
# Time-Based Splitting
# ---------------------------------------------------------------------------

def time_based_split(
    df: pd.DataFrame,
    config: PipelineConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split data into train/validation/test using time-based cutoffs.

    Layout:
        |--- Training ---|--- Validation ---|--- Test ---|
           oldest data      recent data       newest data
    """
    df = df.sort_values(config.date_col).reset_index(drop=True)
    max_date = pd.to_datetime(df[config.date_col]).max()

    test_cutoff = max_date - pd.Timedelta(days=config.test_days)
    val_cutoff = test_cutoff - pd.Timedelta(days=config.val_days)

    dates = pd.to_datetime(df[config.date_col])
    train = df[dates <= val_cutoff].copy()
    val = df[(dates > val_cutoff) & (dates <= test_cutoff)].copy()
    test = df[dates > test_cutoff].copy()

    logger.info(
        "Split sizes -- Train: %d, Validation: %d, Test: %d",
        len(train), len(val), len(test),
    )
    return train, val, test


# ---------------------------------------------------------------------------
# Model Factory
# ---------------------------------------------------------------------------

def create_model(config: PipelineConfig) -> BaseEstimator:
    """Create a model instance based on the configured framework."""
    framework = config.framework.lower()

    if framework == "lightgbm":
        import lightgbm as lgb
        return lgb.LGBMRegressor(**config.model_params)

    elif framework == "xgboost":
        import xgboost as xgb
        params = config.model_params.copy()
        # Translate LightGBM-specific params to XGBoost equivalents
        params.pop("num_leaves", None)
        params.pop("min_child_samples", None)
        params.setdefault("max_depth", 6)
        params.setdefault("tree_method", "hist")
        params["verbosity"] = params.pop("verbose", 0)
        return xgb.XGBRegressor(**params)

    elif framework == "ridge":
        from sklearn.linear_model import Ridge
        alpha = config.model_params.get("alpha", 1.0)
        return Ridge(alpha=alpha)

    else:
        raise ValueError(
            f"Unsupported framework: {framework}. "
            "Choose from: lightgbm, xgboost, ridge"
        )


# ---------------------------------------------------------------------------
# Pipeline Construction
# ---------------------------------------------------------------------------

def build_sklearn_pipeline(
    config: PipelineConfig,
    numeric_features: list[str],
    categorical_features: list[str],
) -> Pipeline:
    """Build a scikit-learn Pipeline with preprocessing and model."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]), numeric_features),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]), categorical_features),
        ],
        remainder="drop",
    )

    model = create_model(config)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", model),
    ])
    return pipeline


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_metrics(
    actual: np.ndarray,
    predicted: np.ndarray,
) -> dict[str, float]:
    """Compute forecasting metrics."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    mae = float(np.mean(np.abs(actual - predicted)))
    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))

    # MAPE and WMAPE: handle zero actuals
    nonzero_mask = actual != 0
    if nonzero_mask.any():
        mape = float(
            np.mean(np.abs((actual[nonzero_mask] - predicted[nonzero_mask]) / actual[nonzero_mask])) * 100
        )
        bias = float(
            np.mean((predicted[nonzero_mask] - actual[nonzero_mask]) / actual[nonzero_mask]) * 100
        )
    else:
        mape = float("inf")
        bias = 0.0

    total_actual = np.sum(np.abs(actual))
    wmape = float(np.sum(np.abs(actual - predicted)) / total_actual * 100) if total_actual > 0 else float("inf")

    return {
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "MAPE": round(mape, 2),
        "WMAPE": round(wmape, 2),
        "Bias": round(bias, 2),
    }


# ---------------------------------------------------------------------------
# Main Pipeline Execution
# ---------------------------------------------------------------------------

def run_pipeline(
    df: pd.DataFrame,
    config: PipelineConfig | None = None,
) -> dict[str, Any]:
    """
    Execute the full training pipeline.

    Args:
        df: Raw input DataFrame with at minimum date_col, target_col, group_col.
        config: Pipeline configuration. Uses defaults if None.

    Returns:
        Dictionary with trained pipeline, metrics, and feature importance.
    """
    if config is None:
        config = PipelineConfig()

    # Step 1: Feature engineering
    df = engineer_features(df, config)

    # Step 2: Time-based split
    train, val, test = time_based_split(df, config)

    # Step 3: Define feature columns
    exclude_cols = {config.date_col, config.target_col, config.group_col}
    feature_cols = [c for c in train.columns if c not in exclude_cols]

    numeric_features = [
        c for c in feature_cols
        if train[c].dtype in ("float64", "float32", "int64", "int32")
    ]
    categorical_features = [
        c for c in feature_cols
        if train[c].dtype == "object" or train[c].dtype.name == "category"
    ]

    logger.info(
        "Features -- Numeric: %d, Categorical: %d",
        len(numeric_features), len(categorical_features),
    )

    # Step 4: Build and train pipeline
    X_train, y_train = train[feature_cols], train[config.target_col]
    X_val, y_val = val[feature_cols], val[config.target_col]
    X_test, y_test = test[feature_cols], test[config.target_col]

    pipeline = build_sklearn_pipeline(config, numeric_features, categorical_features)

    logger.info("Training %s model...", config.framework)

    if config.framework.lower() in ("lightgbm", "xgboost"):
        # Use early stopping for tree-based models
        pipeline.fit(X_train, y_train)
    else:
        pipeline.fit(X_train, y_train)

    # Step 5: Evaluate
    val_preds = pipeline.predict(X_val)
    test_preds = pipeline.predict(X_test)

    val_metrics = compute_metrics(y_val.values, val_preds)
    test_metrics = compute_metrics(y_test.values, test_preds)

    logger.info("Validation metrics: %s", val_metrics)
    logger.info("Test metrics: %s", test_metrics)

    # Step 6: Feature importance (for tree-based models)
    feature_importance = None
    regressor = pipeline.named_steps["regressor"]
    if hasattr(regressor, "feature_importances_"):
        # Get feature names after preprocessing
        preprocessor = pipeline.named_steps["preprocessor"]
        try:
            feature_names = preprocessor.get_feature_names_out()
        except Exception:
            feature_names = [f"feature_{i}" for i in range(len(regressor.feature_importances_))]

        feature_importance = pd.DataFrame({
            "feature": feature_names,
            "importance": regressor.feature_importances_,
        }).sort_values("importance", ascending=False).reset_index(drop=True)

        logger.info("Top 10 features:\n%s", feature_importance.head(10).to_string())

    # Step 7: Save artifacts
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / f"model_{config.framework}.joblib"
    joblib.dump(pipeline, model_path)
    logger.info("Model saved to %s", model_path)

    return {
        "pipeline": pipeline,
        "val_metrics": val_metrics,
        "test_metrics": test_metrics,
        "feature_importance": feature_importance,
        "val_predictions": val_preds,
        "test_predictions": test_preds,
        "val_actuals": y_val.values,
        "test_actuals": y_test.values,
    }


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage with synthetic data
    np.random.seed(42)
    n_skus = 10
    n_days = 365
    dates = pd.date_range("2023-01-01", periods=n_days, freq="D")

    records = []
    for sku in range(n_skus):
        base_demand = np.random.uniform(50, 200)
        trend = np.linspace(0, np.random.uniform(-10, 10), n_days)
        seasonality = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)
        noise = np.random.normal(0, 10, n_days)
        sales = np.maximum(0, base_demand + trend + seasonality + noise)

        for i, date in enumerate(dates):
            records.append({
                "date": date,
                "sku_id": f"SKU_{sku:03d}",
                "sales": round(sales[i], 2),
            })

    df = pd.DataFrame(records)

    config = PipelineConfig(
        framework="lightgbm",
        val_days=14,
        test_days=14,
    )

    results = run_pipeline(df, config)
    print("\nFinal Test Metrics:")
    for metric, value in results["test_metrics"].items():
        print(f"  {metric}: {value}")
