"""
Complete Prophet Demand Forecasting Example
============================================

End-to-end pipeline demonstrating:
1. Data preparation in Prophet format (ds, y)
2. Seasonal decomposition (weekly, yearly, custom)
3. Holiday effects with country-specific calendars
4. Trend changepoint detection
5. External regressors (promotions, price)
6. Cross-validation with Prophet diagnostics
7. Multi-SKU forecasting loop
8. Visualization of components and forecast

Dependencies:
    pip install pandas numpy prophet matplotlib holidays
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import holidays as holidays_lib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

warnings.filterwarnings("ignore", category=FutureWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Suppress Prophet's verbose logging
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

OUTPUT_DIR = Path("artifacts/prophet_example")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Data Generation
# ---------------------------------------------------------------------------

def generate_synthetic_data(n_skus: int = 10, n_days: int = 730) -> pd.DataFrame:
    """
    Generate synthetic daily demand data suitable for Prophet.

    Includes strong seasonality, promotions, holidays, and trend shifts.
    """
    np.random.seed(42)
    dates = pd.date_range("2022-01-01", periods=n_days, freq="D")
    us_holidays = holidays_lib.US(years=[2022, 2023, 2024])

    records = []
    for sku_idx in range(n_skus):
        base_demand = np.random.uniform(50, 250)
        trend_slope = np.random.uniform(-0.03, 0.08)
        weekly_amp = np.random.uniform(10, 40)
        yearly_amp = np.random.uniform(15, 60)
        noise_std = base_demand * 0.08

        # Simulate a trend changepoint (e.g., product relaunch)
        changepoint_day = np.random.randint(200, 500)

        for day_idx, date in enumerate(dates):
            # Piecewise trend
            if day_idx < changepoint_day:
                trend = trend_slope * day_idx
            else:
                new_slope = trend_slope * np.random.uniform(0.5, 2.0)
                trend = trend_slope * changepoint_day + new_slope * (day_idx - changepoint_day)

            # Weekly seasonality
            weekly = weekly_amp * np.sin(2 * np.pi * date.dayofweek / 7)

            # Yearly seasonality
            yearly = yearly_amp * np.sin(2 * np.pi * (date.dayofyear - 60) / 365)

            # Promotions
            is_promo = 1 if np.random.random() < 0.07 else 0
            promo_uplift = is_promo * base_demand * np.random.uniform(0.15, 0.4)

            # Holiday effect
            is_holiday = 1 if date in us_holidays else 0
            holiday_effect = is_holiday * base_demand * 0.2

            # Price
            base_price = np.random.uniform(8.0, 45.0)
            price = base_price * (0.75 if is_promo else np.random.uniform(0.95, 1.05))

            noise = np.random.normal(0, noise_std)
            sales = max(0, base_demand + trend + weekly + yearly + promo_uplift + holiday_effect + noise)

            records.append({
                "date": date,
                "sku_id": f"SKU_{sku_idx:03d}",
                "sales": round(sales, 2),
                "price": round(price, 2),
                "is_promotion": is_promo,
            })

    df = pd.DataFrame(records)
    logger.info("Generated data: %d rows, %d SKUs, %d days", len(df), n_skus, n_days)
    return df


# ---------------------------------------------------------------------------
# 2. Prophet Data Preparation
# ---------------------------------------------------------------------------

def prepare_prophet_data(
    df: pd.DataFrame,
    sku_id: str,
) -> pd.DataFrame:
    """
    Filter data for a single SKU and convert to Prophet format.

    Prophet requires:
    - ds: datetime column
    - y: target column
    - Additional columns for regressors
    """
    sku_df = df[df["sku_id"] == sku_id].copy()
    sku_df = sku_df.sort_values("date").reset_index(drop=True)

    prophet_df = pd.DataFrame({
        "ds": sku_df["date"],
        "y": sku_df["sales"],
        "is_promotion": sku_df["is_promotion"].astype(float),
        "price": sku_df["price"].astype(float),
    })
    return prophet_df


# ---------------------------------------------------------------------------
# 3. Build and Fit Prophet Model
# ---------------------------------------------------------------------------

def build_prophet_model(
    train_df: pd.DataFrame,
    country: str = "US",
    yearly_seasonality: int = 10,
    weekly_seasonality: int = 3,
    changepoint_prior_scale: float = 0.05,
    seasonality_mode: str = "multiplicative",
) -> Prophet:
    """
    Configure and fit a Prophet model.

    Args:
        train_df: Training data in Prophet format (ds, y, regressors).
        country: Country code for holiday effects.
        yearly_seasonality: Fourier order for yearly seasonality.
        weekly_seasonality: Fourier order for weekly seasonality.
        changepoint_prior_scale: Flexibility of trend changepoints.
        seasonality_mode: "multiplicative" or "additive".

    Returns:
        Fitted Prophet model.
    """
    model = Prophet(
        yearly_seasonality=yearly_seasonality,
        weekly_seasonality=weekly_seasonality,
        daily_seasonality=False,
        seasonality_mode=seasonality_mode,
        changepoint_prior_scale=changepoint_prior_scale,
        changepoint_range=0.9,
        n_changepoints=25,
    )

    # Add country-specific holidays
    model.add_country_holidays(country_name=country)

    # Add custom monthly seasonality
    model.add_seasonality(
        name="monthly",
        period=30.5,
        fourier_order=5,
    )

    # Add external regressors
    if "is_promotion" in train_df.columns:
        model.add_regressor("is_promotion", mode="multiplicative")
    if "price" in train_df.columns:
        model.add_regressor("price", mode="multiplicative")

    model.fit(train_df)
    return model


# ---------------------------------------------------------------------------
# 4. Forecast and Evaluate
# ---------------------------------------------------------------------------

def forecast_and_evaluate(
    model: Prophet,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    horizon_days: int = 28,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Generate forecast and evaluate against test data.

    Returns:
        Tuple of (forecast DataFrame, metrics dictionary).
    """
    # Create future dataframe
    future = model.make_future_dataframe(periods=horizon_days, freq="D")

    # Merge regressor values from train + test
    full_data = pd.concat([train_df, test_df], ignore_index=True)
    future = future.merge(
        full_data[["ds", "is_promotion", "price"]],
        on="ds",
        how="left",
    )

    # Fill missing regressor values with defaults
    future["is_promotion"] = future["is_promotion"].fillna(0)
    future["price"] = future["price"].fillna(full_data["price"].median())

    # Predict
    forecast = model.predict(future)

    # Evaluate on test period only
    test_dates = set(test_df["ds"].dt.date)
    forecast_test = forecast[forecast["ds"].dt.date.isin(test_dates)].copy()
    actuals_test = test_df[test_df["ds"].dt.date.isin(forecast_test["ds"].dt.date)]

    if len(actuals_test) == 0:
        return forecast, {"MAPE (%)": float("inf"), "WMAPE (%)": float("inf"), "Bias (%)": 0.0}

    actual = actuals_test["y"].values
    predicted = forecast_test["yhat"].values
    predicted = np.maximum(0, predicted)  # Non-negative

    nonzero = actual != 0
    mape_val = float(np.mean(np.abs((actual[nonzero] - predicted[nonzero]) / actual[nonzero])) * 100) if nonzero.any() else float("inf")

    total = np.sum(np.abs(actual))
    wmape_val = float(np.sum(np.abs(actual - predicted)) / total * 100) if total > 0 else float("inf")

    bias_val = float(np.mean((predicted[nonzero] - actual[nonzero]) / actual[nonzero]) * 100) if nonzero.any() else 0.0

    mae_val = float(np.mean(np.abs(actual - predicted)))

    metrics = {
        "MAE": round(mae_val, 2),
        "MAPE (%)": round(mape_val, 2),
        "WMAPE (%)": round(wmape_val, 2),
        "Bias (%)": round(bias_val, 2),
    }

    return forecast, metrics


# ---------------------------------------------------------------------------
# 5. Cross-Validation
# ---------------------------------------------------------------------------

def run_cross_validation(
    model: Prophet,
    initial_days: int = 365,
    period_days: int = 30,
    horizon_days: int = 28,
) -> pd.DataFrame:
    """
    Run Prophet's built-in cross-validation.

    Args:
        model: Fitted Prophet model.
        initial_days: Initial training period.
        period_days: Spacing between cutoff dates.
        horizon_days: Forecast horizon per fold.

    Returns:
        DataFrame with cross-validation performance metrics.
    """
    logger.info(
        "Running cross-validation (initial=%dd, period=%dd, horizon=%dd)...",
        initial_days, period_days, horizon_days,
    )

    cv_results = cross_validation(
        model,
        initial=f"{initial_days} days",
        period=f"{period_days} days",
        horizon=f"{horizon_days} days",
    )

    metrics_df = performance_metrics(cv_results)
    logger.info("Cross-validation metrics:\n%s", metrics_df[["horizon", "mape", "mae", "rmse"]].to_string())

    return metrics_df


# ---------------------------------------------------------------------------
# 6. Visualization
# ---------------------------------------------------------------------------

def plot_prophet_forecast(
    model: Prophet,
    forecast: pd.DataFrame,
    test_df: pd.DataFrame,
    sku_id: str,
) -> None:
    """Plot Prophet forecast with components."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 16))

    # Plot 1: Forecast with actuals overlay
    ax1 = axes[0]
    ax1.plot(forecast["ds"], forecast["yhat"], label="Forecast", color="#FF5722", linewidth=1.5)
    ax1.fill_between(
        forecast["ds"],
        forecast["yhat_lower"],
        forecast["yhat_upper"],
        alpha=0.15,
        color="#FF5722",
        label="95% CI",
    )
    ax1.scatter(test_df["ds"], test_df["y"], label="Actual (Test)", color="#2196F3", s=15, zorder=5)
    ax1.set_title(f"{sku_id} - Prophet Forecast vs Actuals", fontsize=12, fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Trend component
    ax2 = axes[1]
    ax2.plot(forecast["ds"], forecast["trend"], color="#4CAF50", linewidth=2)
    if "trend_lower" in forecast.columns:
        ax2.fill_between(
            forecast["ds"],
            forecast["trend_lower"],
            forecast["trend_upper"],
            alpha=0.15,
            color="#4CAF50",
        )
    # Mark changepoints
    if hasattr(model, "changepoints") and model.changepoints is not None:
        for cp in model.changepoints:
            ax2.axvline(x=cp, color="gray", linestyle="--", alpha=0.5, linewidth=0.5)
    ax2.set_title("Trend Component (with changepoints)", fontsize=12)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Weekly seasonality
    ax3 = axes[2]
    if "weekly" in forecast.columns:
        # Show one week of weekly seasonality
        weekly_data = forecast[["ds", "weekly"]].copy()
        weekly_data["day_of_week"] = weekly_data["ds"].dt.dayofweek
        weekly_avg = weekly_data.groupby("day_of_week")["weekly"].mean()
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ax3.bar(days, weekly_avg.values, color="#9C27B0", alpha=0.7)
        ax3.set_title("Weekly Seasonality (average effect)", fontsize=12)
        ax3.set_ylabel("Seasonal Effect")
        ax3.grid(True, alpha=0.3, axis="y")
    else:
        ax3.text(0.5, 0.5, "No weekly seasonality component", ha="center", va="center")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"prophet_forecast_{sku_id}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Forecast plot saved for %s", sku_id)


def plot_multi_sku_comparison(all_results: list[dict]) -> None:
    """Plot WMAPE comparison across all SKUs."""
    sku_ids = [r["sku_id"] for r in all_results]
    wmapes = [r["metrics"]["WMAPE (%)"] for r in all_results]
    biases = [r["metrics"]["Bias (%)"] for r in all_results]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # WMAPE bar chart
    colors = ["#4CAF50" if w < 15 else "#FF9800" if w < 25 else "#F44336" for w in wmapes]
    axes[0].barh(sku_ids, wmapes, color=colors, edgecolor="white")
    axes[0].set_xlabel("WMAPE (%)")
    axes[0].set_title("Forecast Accuracy by SKU (WMAPE)", fontsize=12, fontweight="bold")
    axes[0].axvline(x=15, color="gray", linestyle="--", alpha=0.5, label="15% threshold")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis="x")

    # Bias bar chart
    bias_colors = ["#F44336" if abs(b) > 10 else "#FF9800" if abs(b) > 5 else "#4CAF50" for b in biases]
    axes[1].barh(sku_ids, biases, color=bias_colors, edgecolor="white")
    axes[1].set_xlabel("Bias (%)")
    axes[1].set_title("Forecast Bias by SKU", fontsize=12, fontweight="bold")
    axes[1].axvline(x=0, color="black", linewidth=1)
    axes[1].axvline(x=5, color="gray", linestyle="--", alpha=0.5)
    axes[1].axvline(x=-5, color="gray", linestyle="--", alpha=0.5)
    axes[1].grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "multi_sku_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Multi-SKU comparison saved.")


# ---------------------------------------------------------------------------
# 7. Main Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full Prophet forecasting pipeline for multiple SKUs."""
    logger.info("=" * 60)
    logger.info("Prophet Demand Forecasting Pipeline")
    logger.info("=" * 60)

    # Step 1: Load data
    logger.info("\n--- Step 1: Generating synthetic data ---")
    df = generate_synthetic_data(n_skus=10, n_days=730)
    sku_ids = df["sku_id"].unique().tolist()

    # Step 2: Configure split
    horizon_days = 28
    max_date = df["date"].max()
    test_cutoff = max_date - pd.Timedelta(days=horizon_days)

    all_results = []

    for sku_id in sku_ids:
        logger.info("\n--- Processing %s ---", sku_id)

        # Prepare data
        prophet_df = prepare_prophet_data(df, sku_id)

        # Split
        train_df = prophet_df[prophet_df["ds"] <= test_cutoff].copy()
        test_df = prophet_df[prophet_df["ds"] > test_cutoff].copy()

        if len(train_df) < 60 or len(test_df) == 0:
            logger.warning("Skipping %s: insufficient data", sku_id)
            continue

        # Build and fit model
        model = build_prophet_model(
            train_df,
            country="US",
            yearly_seasonality=10,
            weekly_seasonality=3,
            changepoint_prior_scale=0.05,
            seasonality_mode="multiplicative",
        )

        # Forecast and evaluate
        forecast, metrics = forecast_and_evaluate(model, train_df, test_df, horizon_days)
        logger.info("%s metrics: %s", sku_id, metrics)

        all_results.append({
            "sku_id": sku_id,
            "metrics": metrics,
            "model": model,
            "forecast": forecast,
        })

        # Plot first 3 SKUs in detail
        if len(all_results) <= 3:
            plot_prophet_forecast(model, forecast, test_df, sku_id)

    # Step 3: Cross-validation on best SKU
    if all_results:
        best_sku = min(all_results, key=lambda r: r["metrics"]["WMAPE (%)"])
        logger.info("\n--- Cross-Validation on best SKU: %s ---", best_sku["sku_id"])
        cv_metrics = run_cross_validation(
            best_sku["model"],
            initial_days=365,
            period_days=30,
            horizon_days=28,
        )
        cv_metrics.to_csv(OUTPUT_DIR / "cross_validation_metrics.csv", index=False)

    # Step 4: Multi-SKU comparison
    logger.info("\n--- Multi-SKU Comparison ---")
    plot_multi_sku_comparison(all_results)

    # Step 5: Summary table
    summary_records = []
    for r in all_results:
        row = {"sku_id": r["sku_id"], **r["metrics"]}
        summary_records.append(row)

    summary_df = pd.DataFrame(summary_records).sort_values("WMAPE (%)")
    summary_df.to_csv(OUTPUT_DIR / "prophet_summary.csv", index=False)

    logger.info("\nSummary:")
    logger.info("\n%s", summary_df.to_string())
    logger.info("\nAggregate WMAPE: %.2f%%", summary_df["WMAPE (%)"].mean())
    logger.info("Aggregate Bias: %+.2f%%", summary_df["Bias (%)"].mean())

    logger.info("\n" + "=" * 60)
    logger.info("Pipeline complete. Artifacts saved to %s/", OUTPUT_DIR)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
