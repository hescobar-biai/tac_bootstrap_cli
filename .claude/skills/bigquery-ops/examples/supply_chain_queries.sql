-- =============================================================================
-- Supply Chain Analytics - BigQuery SQL Query Examples
-- =============================================================================
-- Ready-to-use query patterns for demand forecasting, inventory management,
-- and fulfillment analytics. All queries assume tables are partitioned by date
-- and clustered by entity columns as described in reference.md.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- 1. Demand Aggregation by SKU with Date Partitioning
-- -----------------------------------------------------------------------------
-- Aggregates daily demand into weekly and monthly summaries per SKU.
-- Uses partition pruning on demand_date for cost-efficient scanning.
-- Includes rolling 4-week average for trend analysis.
-- -----------------------------------------------------------------------------

WITH daily_demand AS (
  SELECT
    demand_date,
    sku_id,
    store_id,
    category,
    units_sold,
    revenue
  FROM `project.supply_chain_demand.daily_sku_demand`
  WHERE demand_date BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
),

weekly_agg AS (
  SELECT
    DATE_TRUNC(demand_date, WEEK(MONDAY))  AS week_start,
    sku_id,
    category,
    SUM(units_sold)                        AS weekly_units,
    SUM(revenue)                           AS weekly_revenue,
    COUNT(DISTINCT store_id)               AS stores_with_sales,
    COUNT(DISTINCT demand_date)            AS selling_days
  FROM daily_demand
  GROUP BY week_start, sku_id, category
),

with_rolling_avg AS (
  SELECT
    *,
    AVG(weekly_units) OVER (
      PARTITION BY sku_id
      ORDER BY week_start
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS rolling_4wk_avg_units,
    LAG(weekly_units, 1) OVER (
      PARTITION BY sku_id
      ORDER BY week_start
    ) AS prev_week_units
  FROM weekly_agg
)

SELECT
  week_start,
  sku_id,
  category,
  weekly_units,
  weekly_revenue,
  stores_with_sales,
  selling_days,
  ROUND(rolling_4wk_avg_units, 1)                     AS rolling_4wk_avg,
  ROUND(
    SAFE_DIVIDE(
      weekly_units - prev_week_units,
      prev_week_units
    ) * 100, 1
  )                                                     AS wow_change_pct
FROM with_rolling_avg
ORDER BY sku_id, week_start;


-- -----------------------------------------------------------------------------
-- 2. Inventory Turnover Calculation
-- -----------------------------------------------------------------------------
-- Calculates inventory turnover ratio by SKU and warehouse for a given period.
-- Turnover = Cost of Goods Sold / Average Inventory Value.
-- Higher turnover indicates efficient inventory management.
-- -----------------------------------------------------------------------------

WITH cogs AS (
  -- Total cost of goods sold in the period
  SELECT
    d.sku_id,
    d.store_id,
    SUM(d.units_sold * s.unit_cost) AS total_cogs
  FROM `project.supply_chain_demand.daily_sku_demand` d
  JOIN `project.supply_chain_master.sku_master` s
    ON d.sku_id = s.sku_id
  WHERE d.demand_date BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
  GROUP BY d.sku_id, d.store_id
),

avg_inventory AS (
  -- Average inventory value over the period (beginning + ending / 2)
  SELECT
    sku_id,
    warehouse_id,
    AVG(on_hand_qty * unit_cost) AS avg_inventory_value
  FROM `project.supply_chain_inventory.weekly_store_inventory`
  WHERE snapshot_date BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
  GROUP BY sku_id, warehouse_id
)

SELECT
  c.sku_id,
  c.store_id,
  ai.warehouse_id,
  c.total_cogs,
  ROUND(ai.avg_inventory_value, 2)                        AS avg_inventory_value,
  ROUND(
    SAFE_DIVIDE(c.total_cogs, ai.avg_inventory_value), 2
  )                                                        AS inventory_turnover,
  -- Days of inventory on hand (DOH)
  ROUND(
    SAFE_DIVIDE(90.0, SAFE_DIVIDE(c.total_cogs, ai.avg_inventory_value)), 1
  )                                                        AS days_on_hand,
  CASE
    WHEN SAFE_DIVIDE(c.total_cogs, ai.avg_inventory_value) >= 12 THEN 'Fast Moving'
    WHEN SAFE_DIVIDE(c.total_cogs, ai.avg_inventory_value) >= 4  THEN 'Normal'
    WHEN SAFE_DIVIDE(c.total_cogs, ai.avg_inventory_value) >= 1  THEN 'Slow Moving'
    ELSE 'Dead Stock'
  END                                                      AS velocity_class
FROM cogs c
LEFT JOIN avg_inventory ai
  ON c.sku_id = ai.sku_id
  AND c.store_id = ai.warehouse_id
ORDER BY inventory_turnover DESC;


-- -----------------------------------------------------------------------------
-- 3. Stockout Detection Query
-- -----------------------------------------------------------------------------
-- Identifies SKU/store combinations that had zero inventory (stockout) during
-- periods when there was active demand. Flags the duration and lost revenue.
-- -----------------------------------------------------------------------------

WITH demand_signal AS (
  -- Days where there was actual demand for each SKU/store
  SELECT
    demand_date,
    sku_id,
    store_id,
    units_sold,
    revenue
  FROM `project.supply_chain_demand.daily_sku_demand`
  WHERE demand_date BETWEEN '2025-01-01' AND '2025-01-31'  -- Partition pruning
    AND units_sold > 0
),

inventory_status AS (
  -- Daily inventory position (expand weekly snapshots if needed)
  SELECT
    snapshot_date,
    sku_id,
    warehouse_id AS store_id,
    on_hand_qty
  FROM `project.supply_chain_inventory.weekly_store_inventory`
  WHERE snapshot_date BETWEEN '2025-01-01' AND '2025-01-31'  -- Partition pruning
),

stockout_events AS (
  -- Days where inventory was zero but demand existed in that store
  SELECT
    d.demand_date,
    d.sku_id,
    d.store_id,
    d.units_sold                                AS demand_units,
    d.revenue                                   AS potential_lost_revenue,
    COALESCE(i.on_hand_qty, 0)                  AS inventory_on_hand
  FROM demand_signal d
  LEFT JOIN inventory_status i
    ON d.sku_id = i.sku_id
    AND d.store_id = i.store_id
    AND d.demand_date = i.snapshot_date
  WHERE COALESCE(i.on_hand_qty, 0) = 0
)

SELECT
  sku_id,
  store_id,
  COUNT(*)                                      AS stockout_days,
  MIN(demand_date)                              AS first_stockout_date,
  MAX(demand_date)                              AS last_stockout_date,
  SUM(demand_units)                             AS total_lost_units,
  ROUND(SUM(potential_lost_revenue), 2)         AS total_lost_revenue,
  -- Consecutive stockout days (gap-and-island detection)
  DATE_DIFF(MAX(demand_date), MIN(demand_date), DAY) + 1 AS stockout_span_days
FROM stockout_events
GROUP BY sku_id, store_id
HAVING stockout_days >= 2  -- Filter out single-day anomalies
ORDER BY total_lost_revenue DESC
LIMIT 100;


-- -----------------------------------------------------------------------------
-- 4. Fill Rate Calculation
-- -----------------------------------------------------------------------------
-- Measures order fill rate: the percentage of customer demand that was
-- fulfilled from available inventory. Key supply chain service level metric.
-- Fill Rate = Units Shipped / Units Ordered.
-- -----------------------------------------------------------------------------

WITH order_lines AS (
  -- All order line items in the period
  SELECT
    order_date,
    order_id,
    sku_id,
    store_id,
    ordered_qty,
    shipped_qty,
    CASE
      WHEN shipped_qty >= ordered_qty THEN 'Fulfilled'
      WHEN shipped_qty > 0           THEN 'Partial'
      ELSE 'Unfulfilled'
    END AS fulfillment_status
  FROM `project.supply_chain_fulfillment.fact_order_lines`
  WHERE order_date BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
),

-- SKU-level fill rate
sku_fill_rate AS (
  SELECT
    sku_id,
    COUNT(*)                                            AS total_order_lines,
    SUM(ordered_qty)                                    AS total_ordered,
    SUM(shipped_qty)                                    AS total_shipped,
    COUNTIF(fulfillment_status = 'Fulfilled')           AS fully_fulfilled_lines,
    COUNTIF(fulfillment_status = 'Partial')             AS partial_lines,
    COUNTIF(fulfillment_status = 'Unfulfilled')         AS unfulfilled_lines
  FROM order_lines
  GROUP BY sku_id
),

-- Store-level fill rate
store_fill_rate AS (
  SELECT
    store_id,
    COUNT(*)                                            AS total_order_lines,
    SUM(ordered_qty)                                    AS total_ordered,
    SUM(shipped_qty)                                    AS total_shipped
  FROM order_lines
  GROUP BY store_id
)

-- SKU fill rate report
SELECT
  sku_id,
  total_order_lines,
  total_ordered,
  total_shipped,
  fully_fulfilled_lines,
  partial_lines,
  unfulfilled_lines,
  -- Unit fill rate (quantity-based)
  ROUND(SAFE_DIVIDE(total_shipped, total_ordered) * 100, 2)           AS unit_fill_rate_pct,
  -- Line fill rate (order-line-based)
  ROUND(SAFE_DIVIDE(fully_fulfilled_lines, total_order_lines) * 100, 2) AS line_fill_rate_pct,
  -- Service level classification
  CASE
    WHEN SAFE_DIVIDE(total_shipped, total_ordered) >= 0.98 THEN 'Excellent (98%+)'
    WHEN SAFE_DIVIDE(total_shipped, total_ordered) >= 0.95 THEN 'Good (95-98%)'
    WHEN SAFE_DIVIDE(total_shipped, total_ordered) >= 0.90 THEN 'Fair (90-95%)'
    ELSE 'Poor (<90%)'
  END AS service_level
FROM sku_fill_rate
ORDER BY unit_fill_rate_pct ASC;  -- Worst performers first

-- Store fill rate report (uncomment to use instead)
-- SELECT
--   store_id,
--   total_order_lines,
--   total_ordered,
--   total_shipped,
--   ROUND(SAFE_DIVIDE(total_shipped, total_ordered) * 100, 2) AS unit_fill_rate_pct
-- FROM store_fill_rate
-- ORDER BY unit_fill_rate_pct ASC;


-- -----------------------------------------------------------------------------
-- 5. Weekly Demand Forecast Comparison
-- -----------------------------------------------------------------------------
-- Compares actual demand against forecasted demand at the weekly SKU level.
-- Calculates forecast accuracy metrics: MAPE, bias, and weighted MAPE.
-- Essential for evaluating and tuning forecasting models.
-- -----------------------------------------------------------------------------

WITH actuals AS (
  -- Aggregate daily actuals to weekly level
  SELECT
    DATE_TRUNC(demand_date, WEEK(MONDAY)) AS week_start,
    sku_id,
    store_id,
    SUM(units_sold)                       AS actual_units,
    SUM(revenue)                          AS actual_revenue
  FROM `project.supply_chain_demand.daily_sku_demand`
  WHERE demand_date BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
  GROUP BY week_start, sku_id, store_id
),

forecasts AS (
  -- Weekly forecast values (already at weekly grain)
  SELECT
    forecast_week    AS week_start,
    sku_id,
    store_id,
    forecast_units,
    forecast_model,
    forecast_generated_at
  FROM `project.supply_chain_analytics.weekly_sku_forecast`
  WHERE forecast_week BETWEEN '2025-01-01' AND '2025-03-31'  -- Partition pruning
),

comparison AS (
  SELECT
    COALESCE(a.week_start, f.week_start)  AS week_start,
    COALESCE(a.sku_id, f.sku_id)          AS sku_id,
    COALESCE(a.store_id, f.store_id)      AS store_id,
    f.forecast_model,
    a.actual_units,
    f.forecast_units,
    -- Error metrics
    (f.forecast_units - a.actual_units)   AS error,
    ABS(f.forecast_units - a.actual_units) AS abs_error,
    -- Percentage error (avoid division by zero)
    SAFE_DIVIDE(
      ABS(f.forecast_units - a.actual_units),
      a.actual_units
    )                                      AS abs_pct_error,
    -- Bias direction
    SIGN(f.forecast_units - a.actual_units) AS bias_direction
  FROM actuals a
  FULL OUTER JOIN forecasts f
    ON a.week_start = f.week_start
    AND a.sku_id = f.sku_id
    AND a.store_id = f.store_id
)

SELECT
  sku_id,
  forecast_model,
  COUNT(*)                                          AS weeks_compared,
  -- Accuracy metrics
  ROUND(AVG(abs_pct_error) * 100, 2)               AS mape_pct,
  ROUND(
    SAFE_DIVIDE(
      SUM(abs_error),
      SUM(actual_units)
    ) * 100, 2
  )                                                 AS weighted_mape_pct,
  -- Bias metrics
  ROUND(AVG(error), 1)                              AS avg_bias_units,
  ROUND(
    SAFE_DIVIDE(SUM(error), SUM(actual_units)) * 100, 2
  )                                                 AS bias_pct,
  CASE
    WHEN SAFE_DIVIDE(SUM(error), SUM(actual_units)) > 0.05  THEN 'Over-forecasting'
    WHEN SAFE_DIVIDE(SUM(error), SUM(actual_units)) < -0.05 THEN 'Under-forecasting'
    ELSE 'Balanced'
  END                                               AS bias_classification,
  -- Volume context
  SUM(actual_units)                                 AS total_actual_units,
  SUM(forecast_units)                               AS total_forecast_units,
  -- Accuracy classification
  CASE
    WHEN AVG(abs_pct_error) <= 0.10 THEN 'Excellent (<=10% MAPE)'
    WHEN AVG(abs_pct_error) <= 0.20 THEN 'Good (10-20% MAPE)'
    WHEN AVG(abs_pct_error) <= 0.30 THEN 'Fair (20-30% MAPE)'
    ELSE 'Poor (>30% MAPE)'
  END                                               AS accuracy_class
FROM comparison
WHERE actual_units IS NOT NULL
  AND forecast_units IS NOT NULL
GROUP BY sku_id, forecast_model
ORDER BY mape_pct ASC;
