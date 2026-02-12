"""
Forecast Evaluation Script
==========================

Compute supply chain metrics and generate visualizations for demand forecasts.

Metrics computed:
- MAPE (Mean Absolute Percentage Error)
- WMAPE (Weighted Mean Absolute Percentage Error)
- Bias (systematic over/under forecasting)
- Fill Rate (demand fulfillment from stock)
- OTIF (On-Time In-Full delivery)

Outputs:
- Aggregate metrics summary
- Per-SKU breakdown table
- Actuals vs Predictions plot
- Residual distribution plot

Dependencies:
    pip install pandas numpy matplotlib seaborn
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class EvalConfig:
    """Configuration for evaluation."""

    date_col: str = "date"
    actual_col: str = "actual"
    predicted_col: str = "predicted"
    sku_col: str = "sku_id"

    # Optional columns for fill rate / OTIF
    available_stock_col: str | None = None
    on_time_col: str | None = None
    in_full_col: str | None = None

    # Output
    output_dir: str = "evaluation_output"
    fig_width: int = 14
    fig_height: int = 6


# ---------------------------------------------------------------------------
# Supply Chain Metrics
# ---------------------------------------------------------------------------

def mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Mean Absolute Percentage Error.

    Excludes zero actuals to avoid division by zero.
    Returns percentage value (e.g., 12.5 means 12.5%).
    """
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    mask = actual != 0
    if not mask.any():
        return float("inf")
    return float(np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100)


def wmape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Weighted Mean Absolute Percentage Error.

    Volume-weighted: total absolute error / total actual volume.
    Preferred for SKU portfolio evaluation.
    """
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    total = np.sum(np.abs(actual))
    if total == 0:
        return float("inf")
    return float(np.sum(np.abs(actual - predicted)) / total * 100)


def forecast_bias(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Forecast Bias.

    Positive value means over-forecasting (predicting too high).
    Negative value means under-forecasting (predicting too low).
    """
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    mask = actual != 0
    if not mask.any():
        return 0.0
    return float(np.mean((predicted[mask] - actual[mask]) / actual[mask]) * 100)


def mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Mean Absolute Error in original units."""
    return float(np.mean(np.abs(np.asarray(actual) - np.asarray(predicted))))


def rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(np.mean((np.asarray(actual) - np.asarray(predicted)) ** 2)))


def fill_rate(demand: np.ndarray, available_stock: np.ndarray) -> float:
    """
    Fill Rate: percentage of demand met from available inventory.

    fill_rate = sum(min(demand, stock)) / sum(demand) * 100
    """
    demand = np.asarray(demand, dtype=float)
    stock = np.asarray(available_stock, dtype=float)
    total_demand = np.sum(demand)
    if total_demand == 0:
        return 100.0
    fulfilled = np.sum(np.minimum(demand, stock))
    return float(fulfilled / total_demand * 100)


def otif(on_time: np.ndarray, in_full: np.ndarray) -> float:
    """
    On-Time In-Full: percentage of orders that are both on time and complete.

    otif = count(on_time AND in_full) / total_orders * 100
    """
    on_time = np.asarray(on_time, dtype=bool)
    in_full = np.asarray(in_full, dtype=bool)
    if len(on_time) == 0:
        return 0.0
    return float(np.mean(on_time & in_full) * 100)


# ---------------------------------------------------------------------------
# Aggregate Metrics
# ---------------------------------------------------------------------------

def compute_aggregate_metrics(
    df: pd.DataFrame,
    config: EvalConfig,
) -> dict[str, float]:
    """Compute all supply chain metrics at the aggregate level."""
    actual = df[config.actual_col].values
    predicted = df[config.predicted_col].values

    metrics = {
        "MAPE (%)": round(mape(actual, predicted), 2),
        "WMAPE (%)": round(wmape(actual, predicted), 2),
        "Bias (%)": round(forecast_bias(actual, predicted), 2),
        "MAE": round(mae(actual, predicted), 4),
        "RMSE": round(rmse(actual, predicted), 4),
    }

    # Optional: Fill Rate
    if config.available_stock_col and config.available_stock_col in df.columns:
        stock = df[config.available_stock_col].values
        metrics["Fill Rate (%)"] = round(fill_rate(actual, stock), 2)

    # Optional: OTIF
    if (
        config.on_time_col
        and config.in_full_col
        and config.on_time_col in df.columns
        and config.in_full_col in df.columns
    ):
        ot = df[config.on_time_col].values
        inf = df[config.in_full_col].values
        metrics["OTIF (%)"] = round(otif(ot, inf), 2)

    return metrics


# ---------------------------------------------------------------------------
# Per-SKU Breakdown
# ---------------------------------------------------------------------------

def compute_per_sku_metrics(
    df: pd.DataFrame,
    config: EvalConfig,
) -> pd.DataFrame:
    """Compute metrics for each SKU individually."""
    results = []

    for sku_id, group in df.groupby(config.sku_col):
        actual = group[config.actual_col].values
        predicted = group[config.predicted_col].values

        row = {
            "sku_id": sku_id,
            "n_records": len(group),
            "total_actual": round(float(np.sum(actual)), 2),
            "total_predicted": round(float(np.sum(predicted)), 2),
            "MAPE (%)": round(mape(actual, predicted), 2),
            "WMAPE (%)": round(wmape(actual, predicted), 2),
            "Bias (%)": round(forecast_bias(actual, predicted), 2),
            "MAE": round(mae(actual, predicted), 4),
        }
        results.append(row)

    breakdown = pd.DataFrame(results)
    breakdown = breakdown.sort_values("WMAPE (%)", ascending=True).reset_index(drop=True)
    return breakdown


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_actuals_vs_predictions(
    df: pd.DataFrame,
    config: EvalConfig,
    sku_ids: list[str] | None = None,
    max_skus: int = 6,
) -> plt.Figure:
    """
    Plot actuals vs predictions over time.

    If sku_ids is None, selects up to max_skus SKUs with highest volume.
    """
    if sku_ids is None:
        top_skus = (
            df.groupby(config.sku_col)[config.actual_col]
            .sum()
            .nlargest(max_skus)
            .index.tolist()
        )
        sku_ids = top_skus

    n_skus = len(sku_ids)
    n_cols = min(2, n_skus)
    n_rows = (n_skus + n_cols - 1) // n_cols

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(config.fig_width, config.fig_height * n_rows),
        squeeze=False,
    )

    for idx, sku_id in enumerate(sku_ids):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]

        sku_data = df[df[config.sku_col] == sku_id].sort_values(config.date_col)
        dates = pd.to_datetime(sku_data[config.date_col])
        actual_vals = sku_data[config.actual_col].values
        predicted_vals = sku_data[config.predicted_col].values

        ax.plot(dates, actual_vals, label="Actual", color="#2196F3", linewidth=1.5)
        ax.plot(dates, predicted_vals, label="Predicted", color="#FF5722", linewidth=1.5, linestyle="--")
        ax.fill_between(dates, actual_vals, predicted_vals, alpha=0.15, color="#FF5722")

        sku_wmape = wmape(actual_vals, predicted_vals)
        sku_bias = forecast_bias(actual_vals, predicted_vals)
        ax.set_title(f"{sku_id}  |  WMAPE: {sku_wmape:.1f}%  |  Bias: {sku_bias:+.1f}%", fontsize=10)
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)

    # Hide unused subplots
    for idx in range(n_skus, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    fig.suptitle("Actuals vs Predictions", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def plot_residual_distribution(
    df: pd.DataFrame,
    config: EvalConfig,
) -> plt.Figure:
    """Plot the distribution of residuals (predicted - actual)."""
    residuals = df[config.predicted_col].values - df[config.actual_col].values

    fig, axes = plt.subplots(1, 2, figsize=(config.fig_width, config.fig_height))

    # Histogram
    axes[0].hist(residuals, bins=50, color="#2196F3", alpha=0.7, edgecolor="white")
    axes[0].axvline(x=0, color="#FF5722", linestyle="--", linewidth=1.5)
    axes[0].axvline(x=np.mean(residuals), color="#4CAF50", linestyle="-", linewidth=1.5, label=f"Mean: {np.mean(residuals):.2f}")
    axes[0].set_title("Residual Distribution (Predicted - Actual)")
    axes[0].set_xlabel("Residual")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Residuals over time
    dates = pd.to_datetime(df[config.date_col])
    axes[1].scatter(dates, residuals, alpha=0.3, s=5, color="#2196F3")
    axes[1].axhline(y=0, color="#FF5722", linestyle="--", linewidth=1.5)
    axes[1].set_title("Residuals Over Time")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Residual")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def plot_sku_accuracy_heatmap(
    sku_metrics: pd.DataFrame,
    max_skus: int = 30,
) -> plt.Figure:
    """Plot a heatmap of per-SKU metrics."""
    display_df = sku_metrics.head(max_skus).set_index("sku_id")
    metric_cols = [c for c in display_df.columns if c not in ("n_records", "total_actual", "total_predicted")]
    plot_data = display_df[metric_cols]

    fig, ax = plt.subplots(figsize=(10, max(4, len(plot_data) * 0.4)))
    sns.heatmap(
        plot_data,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn_r",
        ax=ax,
        linewidths=0.5,
        cbar_kws={"label": "Metric Value"},
    )
    ax.set_title("Per-SKU Forecast Accuracy", fontsize=12, fontweight="bold")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Full Evaluation Report
# ---------------------------------------------------------------------------

def run_evaluation(
    df: pd.DataFrame,
    config: EvalConfig | None = None,
    save_plots: bool = True,
) -> dict:
    """
    Run the full evaluation pipeline.

    Args:
        df: DataFrame with columns for date, actual, predicted, and sku_id.
        config: Evaluation configuration. Uses defaults if None.
        save_plots: Whether to save plots to disk.

    Returns:
        Dictionary with aggregate metrics, per-SKU breakdown, and figures.
    """
    if config is None:
        config = EvalConfig()

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Aggregate metrics
    logger.info("Computing aggregate metrics...")
    agg_metrics = compute_aggregate_metrics(df, config)
    logger.info("Aggregate Metrics:")
    for metric, value in agg_metrics.items():
        logger.info("  %s: %s", metric, value)

    # 2. Per-SKU breakdown
    logger.info("Computing per-SKU breakdown...")
    sku_breakdown = compute_per_sku_metrics(df, config)
    logger.info("Per-SKU breakdown (top 5 most accurate):")
    logger.info("\n%s", sku_breakdown.head(5).to_string())

    # Save breakdown to CSV
    breakdown_path = output_dir / "sku_breakdown.csv"
    sku_breakdown.to_csv(breakdown_path, index=False)
    logger.info("SKU breakdown saved to %s", breakdown_path)

    # 3. Visualizations
    figures = {}

    logger.info("Generating actuals vs predictions plot...")
    fig_avp = plot_actuals_vs_predictions(df, config)
    figures["actuals_vs_predictions"] = fig_avp
    if save_plots:
        fig_avp.savefig(output_dir / "actuals_vs_predictions.png", dpi=150, bbox_inches="tight")

    logger.info("Generating residual distribution plot...")
    fig_res = plot_residual_distribution(df, config)
    figures["residual_distribution"] = fig_res
    if save_plots:
        fig_res.savefig(output_dir / "residual_distribution.png", dpi=150, bbox_inches="tight")

    logger.info("Generating SKU accuracy heatmap...")
    fig_heat = plot_sku_accuracy_heatmap(sku_breakdown)
    figures["sku_heatmap"] = fig_heat
    if save_plots:
        fig_heat.savefig(output_dir / "sku_accuracy_heatmap.png", dpi=150, bbox_inches="tight")

    if save_plots:
        logger.info("All plots saved to %s/", output_dir)

    plt.close("all")

    return {
        "aggregate_metrics": agg_metrics,
        "sku_breakdown": sku_breakdown,
        "figures": figures,
    }


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage with synthetic evaluation data
    np.random.seed(42)
    n_skus = 15
    n_days = 28
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")

    records = []
    for sku in range(n_skus):
        base = np.random.uniform(50, 200)
        for date in dates:
            actual = max(0, base + np.random.normal(0, 15))
            # Simulate predictions with some error
            error_pct = np.random.uniform(-0.15, 0.20)
            predicted = actual * (1 + error_pct)
            records.append({
                "date": date,
                "sku_id": f"SKU_{sku:03d}",
                "actual": round(actual, 2),
                "predicted": round(predicted, 2),
            })

    eval_df = pd.DataFrame(records)

    results = run_evaluation(eval_df)
    print("\nAggregate Metrics:")
    for metric, value in results["aggregate_metrics"].items():
        print(f"  {metric}: {value}")
