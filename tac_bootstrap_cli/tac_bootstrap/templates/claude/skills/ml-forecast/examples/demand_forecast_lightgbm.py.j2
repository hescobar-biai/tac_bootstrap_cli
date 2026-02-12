"""
Complete LightGBM Demand Forecasting Example
=============================================

End-to-end pipeline demonstrating:
1. Data generation (synthetic supply chain data)
2. Feature engineering (lags, rolling stats, calendar, promotions)
3. Time-based train/validation/test split
4. LightGBM model training with early stopping
5. Hyperparameter tuning with Optuna
6. Evaluation with supply chain metrics (MAPE, WMAPE, Bias)
7. Feature importance analysis
8. Actuals vs Predictions visualization

Dependencies:
    pip install pandas numpy lightgbm optuna scikit-learn matplotlib holidays
"""

from __future__ import annotations

import logging
from pathlib import Path

import holidays as holidays_lib
import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

optuna.logging.set_verbosity(optuna.logging.WARNING)

OUTPUT_DIR = Path("artifacts/lightgbm_example")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Data Generation (replace with your actual data loading)
# ---------------------------------------------------------------------------

def generate_synthetic_data(n_skus: int = 50, n_days: int = 730) -> pd.DataFrame:
    """
    Generate synthetic daily demand data for multiple SKUs.

    Includes trend, weekly seasonality, yearly seasonality,
    promotional effects, and noise.
    """
    np.random.seed(42)
    dates = pd.date_range("2022-01-01", periods=n_days, freq="D")
    us_holidays = holidays_lib.US(years=[2022, 2023, 2024])

    records = []
    for sku_idx in range(n_skus):
        base_demand = np.random.uniform(30, 300)
        trend_slope = np.random.uniform(-0.05, 0.1)
        weekly_amp = np.random.uniform(5, 30)
        yearly_amp = np.random.uniform(10, 50)
        noise_std = base_demand * 0.1

        for day_idx, date in enumerate(dates):
            # Trend
            trend = trend_slope * day_idx

            # Weekly seasonality (higher on weekends for retail)
            weekly = weekly_amp * np.sin(2 * np.pi * date.dayofweek / 7)

            # Yearly seasonality (peak in December)
            yearly = yearly_amp * np.sin(2 * np.pi * (date.dayofyear - 60) / 365)

            # Promotional effect (random promotions with uplift)
            is_promo = 1 if np.random.random() < 0.08 else 0
            promo_uplift = is_promo * base_demand * np.random.uniform(0.2, 0.5)

            # Holiday effect
            is_holiday = 1 if date in us_holidays else 0
            holiday_effect = is_holiday * base_demand * 0.15

            # Price variation
            base_price = np.random.uniform(5.0, 50.0)
            price = base_price * (0.7 if is_promo else np.random.uniform(0.95, 1.05))

            # Noise
            noise = np.random.normal(0, noise_std)

            sales = max(0, base_demand + trend + weekly + yearly + promo_uplift + holiday_effect + noise)

            records.append({
                "date": date,
                "sku_id": f"SKU_{sku_idx:03d}",
                "sales": round(sales, 2),
                "price": round(price, 2),
                "is_promotion": is_promo,
                "is_holiday": is_holiday,
                "category": f"CAT_{sku_idx % 5}",
            })

    df = pd.DataFrame(records)
    logger.info("Generated data: %d rows, %d SKUs, %d days", len(df), n_skus, n_days)
    return df


# ---------------------------------------------------------------------------
# 2. Feature Engineering
# ---------------------------------------------------------------------------

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build all features for the LightGBM model."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["sku_id", "date"]).reset_index(drop=True)

    # --- Lag features ---
    for lag in [1, 2, 3, 7, 14, 21, 28]:
        df[f"lag_{lag}"] = df.groupby("sku_id")["sales"].shift(lag)

    # --- Rolling statistics ---
    for window in [7, 14, 28]:
        grouped = df.groupby("sku_id")["sales"]
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

    # --- Calendar features ---
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_month"] = df["date"].dt.day
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["is_weekend"] = (df["date"].dt.dayofweek >= 5).astype(int)
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)

    # --- Price features ---
    grouped_price = df.groupby("sku_id")["price"]
    df["price_ratio_to_avg"] = df["price"] / grouped_price.transform("mean")
    df["price_pct_change"] = grouped_price.transform(lambda x: x.pct_change())

    # --- Promotional features ---
    for window in [7, 14, 28]:
        df[f"promo_count_{window}d"] = (
            df.groupby("sku_id")["is_promotion"]
            .transform(lambda x: x.rolling(window, min_periods=1).sum())
        )

    # --- Expanding mean (long-term average) ---
    df["expanding_mean"] = df.groupby("sku_id")["sales"].transform(
        lambda x: x.shift(1).expanding(min_periods=1).mean()
    )

    # Drop rows without enough history for lags
    df = df.dropna(subset=["lag_28"]).reset_index(drop=True)

    logger.info("Feature engineering complete: %d features", len(df.columns) - 3)
    return df


# ---------------------------------------------------------------------------
# 3. Time-Based Split
# ---------------------------------------------------------------------------

def split_data(
    df: pd.DataFrame,
    val_days: int = 28,
    test_days: int = 28,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split data into train/validation/test by date."""
    max_date = df["date"].max()
    test_cutoff = max_date - pd.Timedelta(days=test_days)
    val_cutoff = test_cutoff - pd.Timedelta(days=val_days)

    train = df[df["date"] <= val_cutoff].copy()
    val = df[(df["date"] > val_cutoff) & (df["date"] <= test_cutoff)].copy()
    test = df[df["date"] > test_cutoff].copy()

    logger.info("Train: %d rows (up to %s)", len(train), val_cutoff.date())
    logger.info("Val:   %d rows (%s to %s)", len(val), (val_cutoff + pd.Timedelta(days=1)).date(), test_cutoff.date())
    logger.info("Test:  %d rows (%s to %s)", len(test), (test_cutoff + pd.Timedelta(days=1)).date(), max_date.date())

    return train, val, test


# ---------------------------------------------------------------------------
# 4. Metrics
# ---------------------------------------------------------------------------

def compute_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    """Compute supply chain forecasting metrics."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    mae_val = float(np.mean(np.abs(actual - predicted)))
    rmse_val = float(np.sqrt(np.mean((actual - predicted) ** 2)))

    nonzero = actual != 0
    mape_val = float(np.mean(np.abs((actual[nonzero] - predicted[nonzero]) / actual[nonzero])) * 100) if nonzero.any() else float("inf")

    total = np.sum(np.abs(actual))
    wmape_val = float(np.sum(np.abs(actual - predicted)) / total * 100) if total > 0 else float("inf")

    bias_val = float(np.mean((predicted[nonzero] - actual[nonzero]) / actual[nonzero]) * 100) if nonzero.any() else 0.0

    return {
        "MAE": round(mae_val, 2),
        "RMSE": round(rmse_val, 2),
        "MAPE (%)": round(mape_val, 2),
        "WMAPE (%)": round(wmape_val, 2),
        "Bias (%)": round(bias_val, 2),
    }


# ---------------------------------------------------------------------------
# 5. LightGBM Training
# ---------------------------------------------------------------------------

def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """Get feature columns excluding non-feature columns."""
    exclude = {"date", "sales", "sku_id"}
    return [c for c in df.columns if c not in exclude]


def train_lightgbm(
    train: pd.DataFrame,
    val: pd.DataFrame,
    params: dict | None = None,
) -> lgb.LGBMRegressor:
    """Train a LightGBM model with early stopping."""
    feature_cols = get_feature_columns(train)

    if params is None:
        params = {
            "objective": "regression",
            "metric": "mae",
            "boosting_type": "gbdt",
            "n_estimators": 2000,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "max_depth": -1,
            "min_child_samples": 20,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,
            "reg_lambda": 0.1,
            "verbose": -1,
        }

    model = lgb.LGBMRegressor(**params)
    model.fit(
        train[feature_cols], train["sales"],
        eval_set=[(val[feature_cols], val["sales"])],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=200),
        ],
    )

    logger.info("Best iteration: %d", model.best_iteration_)
    return model


# ---------------------------------------------------------------------------
# 6. Hyperparameter Tuning with Optuna
# ---------------------------------------------------------------------------

def tune_hyperparameters(
    train: pd.DataFrame,
    n_trials: int = 50,
    n_splits: int = 3,
) -> dict:
    """Use Optuna to find optimal LightGBM hyperparameters."""
    feature_cols = get_feature_columns(train)
    X = train[feature_cols]
    y = train["sales"]

    def objective(trial: optuna.Trial) -> float:
        params = {
            "objective": "regression",
            "metric": "mae",
            "boosting_type": "gbdt",
            "n_estimators": 1000,
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 127),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
            "verbose": -1,
        }

        tscv = TimeSeriesSplit(n_splits=n_splits)
        scores = []

        for train_idx, val_idx in tscv.split(X):
            model = lgb.LGBMRegressor(**params)
            model.fit(
                X.iloc[train_idx], y.iloc[train_idx],
                eval_set=[(X.iloc[val_idx], y.iloc[val_idx])],
                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)],
            )
            preds = model.predict(X.iloc[val_idx])
            actual = y.iloc[val_idx].values

            total = np.sum(np.abs(actual))
            score = np.sum(np.abs(actual - preds)) / total * 100 if total > 0 else float("inf")
            scores.append(score)

        return np.mean(scores)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    logger.info("Best trial WMAPE: %.2f%%", study.best_value)
    logger.info("Best params: %s", study.best_params)

    return study.best_params


# ---------------------------------------------------------------------------
# 7. Visualization
# ---------------------------------------------------------------------------

def plot_results(
    test: pd.DataFrame,
    predictions: np.ndarray,
    n_skus: int = 4,
) -> None:
    """Plot actuals vs predictions for top SKUs by volume."""
    test = test.copy()
    test["predicted"] = predictions

    top_skus = (
        test.groupby("sku_id")["sales"]
        .sum()
        .nlargest(n_skus)
        .index.tolist()
    )

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, sku_id in enumerate(top_skus):
        ax = axes[idx]
        sku_data = test[test["sku_id"] == sku_id].sort_values("date")

        ax.plot(sku_data["date"], sku_data["sales"], label="Actual", color="#2196F3", linewidth=1.5)
        ax.plot(sku_data["date"], sku_data["predicted"], label="Predicted", color="#FF5722", linewidth=1.5, linestyle="--")
        ax.fill_between(sku_data["date"], sku_data["sales"], sku_data["predicted"], alpha=0.15, color="#FF5722")

        metrics = compute_metrics(sku_data["sales"].values, sku_data["predicted"].values)
        ax.set_title(f"{sku_id}  |  WMAPE: {metrics['WMAPE (%)']:.1f}%  |  Bias: {metrics['Bias (%)']:+.1f}%", fontsize=10)
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)

    fig.suptitle("LightGBM Demand Forecast - Actuals vs Predictions", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "actuals_vs_predictions.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Plot saved to %s", OUTPUT_DIR / "actuals_vs_predictions.png")


def plot_feature_importance(model: lgb.LGBMRegressor, feature_cols: list[str], top_n: int = 20) -> None:
    """Plot top feature importances."""
    importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=True).tail(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(importance["feature"], importance["importance"], color="#2196F3", edgecolor="white")
    ax.set_title(f"Top {top_n} Feature Importances (LightGBM)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Importance")
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Feature importance plot saved to %s", OUTPUT_DIR / "feature_importance.png")


# ---------------------------------------------------------------------------
# 8. Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full LightGBM forecasting pipeline."""
    logger.info("=" * 60)
    logger.info("LightGBM Demand Forecasting Pipeline")
    logger.info("=" * 60)

    # Step 1: Load data
    logger.info("\n--- Step 1: Generating synthetic data ---")
    df = generate_synthetic_data(n_skus=50, n_days=730)

    # Step 2: Feature engineering
    logger.info("\n--- Step 2: Feature engineering ---")
    df = create_features(df)

    # Step 3: Split data
    logger.info("\n--- Step 3: Time-based split ---")
    train, val, test = split_data(df, val_days=28, test_days=28)

    # Step 4: Hyperparameter tuning (optional -- comment out for faster runs)
    logger.info("\n--- Step 4: Hyperparameter tuning ---")
    best_params = tune_hyperparameters(train, n_trials=30, n_splits=3)
    tuned_params = {
        "objective": "regression",
        "metric": "mae",
        "boosting_type": "gbdt",
        "n_estimators": 2000,
        "verbose": -1,
        **best_params,
    }

    # Step 5: Train final model
    logger.info("\n--- Step 5: Training final model ---")
    model = train_lightgbm(train, val, params=tuned_params)

    # Step 6: Evaluate on test set
    logger.info("\n--- Step 6: Evaluation ---")
    feature_cols = get_feature_columns(test)
    test_preds = model.predict(test[feature_cols])
    test_preds = np.maximum(0, test_preds)  # Ensure non-negative

    metrics = compute_metrics(test["sales"].values, test_preds)
    logger.info("Test Set Metrics:")
    for metric, value in metrics.items():
        logger.info("  %s: %s", metric, value)

    # Per-SKU breakdown
    test_copy = test.copy()
    test_copy["predicted"] = test_preds
    sku_metrics = []
    for sku_id, group in test_copy.groupby("sku_id"):
        m = compute_metrics(group["sales"].values, group["predicted"].values)
        m["sku_id"] = sku_id
        sku_metrics.append(m)

    sku_df = pd.DataFrame(sku_metrics).sort_values("WMAPE (%)")
    sku_df.to_csv(OUTPUT_DIR / "per_sku_metrics.csv", index=False)
    logger.info("\nPer-SKU metrics saved. Top 5 most accurate:")
    logger.info("\n%s", sku_df.head(5).to_string())
    logger.info("\nBottom 5 (worst accuracy):")
    logger.info("\n%s", sku_df.tail(5).to_string())

    # Step 7: Visualization
    logger.info("\n--- Step 7: Visualization ---")
    plot_results(test, test_preds, n_skus=4)
    plot_feature_importance(model, feature_cols, top_n=20)

    # Step 8: Save model
    import joblib
    model_path = OUTPUT_DIR / "lightgbm_model.joblib"
    joblib.dump(model, model_path)
    logger.info("Model saved to %s", model_path)

    logger.info("\n" + "=" * 60)
    logger.info("Pipeline complete. Artifacts saved to %s/", OUTPUT_DIR)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
