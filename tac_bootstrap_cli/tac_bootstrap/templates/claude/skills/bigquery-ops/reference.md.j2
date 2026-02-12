# BigQuery Best Practices for Supply Chain Analytics

Reference guide for partitioning, clustering, materialized views, cost optimization, and naming conventions in supply chain BigQuery workloads.

## Table of Contents

- [Partitioning Strategies](#partitioning-strategies)
- [Clustering Strategies](#clustering-strategies)
- [Materialized Views](#materialized-views)
- [Slot Estimation Formulas](#slot-estimation-formulas)
- [Cost Optimization Patterns](#cost-optimization-patterns)
- [Naming Conventions](#naming-conventions)

---

## Partitioning Strategies

Partitioning divides a table into segments based on a column value, allowing BigQuery to scan only the relevant partitions. This is the single most impactful optimization for large supply chain tables.

### By Date Column (Time-Series Demand Data)

Use explicit date or timestamp partitioning for tables where queries almost always filter by a date range. This is the default choice for demand, sales, and shipment data.

```sql
-- Daily demand table partitioned by demand_date
CREATE TABLE `project.supply_chain_demand.daily_sku_demand`
(
  demand_date   DATE NOT NULL,
  sku_id        STRING NOT NULL,
  store_id      STRING NOT NULL,
  units_sold    INT64,
  revenue       NUMERIC
)
PARTITION BY demand_date
OPTIONS (
  require_partition_filter = true,
  partition_expiration_days = 730
);
```

**When to use**:
- Demand forecasting tables (`demand_date`)
- Sales transaction tables (`order_date`, `sale_date`)
- Shipment tracking tables (`ship_date`, `delivery_date`)
- Purchase order tables (`po_date`)

**Guidelines**:
- Always set `require_partition_filter = true` for large tables to prevent accidental full scans.
- Set `partition_expiration_days` to auto-delete old partitions (e.g., 730 days = 2 years for demand history).
- Use `DATE` type partitioning for daily granularity, `TIMESTAMP` for finer granularity.
- For tables with fewer than 10 GB, partitioning overhead may not be worth it.

### By Ingestion Time (Logs and ETL Events)

Use ingestion-time partitioning for append-only log tables where the data does not have a reliable business date column.

```sql
-- ETL pipeline log table partitioned by ingestion time
CREATE TABLE `project.supply_chain_ops.etl_pipeline_logs`
(
  pipeline_name   STRING NOT NULL,
  status          STRING,
  records_loaded  INT64,
  error_message   STRING,
  metadata        JSON
)
PARTITION BY _PARTITIONDATE
OPTIONS (
  require_partition_filter = true,
  partition_expiration_days = 90
);
```

**When to use**:
- ETL job logs and audit trails
- Data quality check results
- System event logs
- Streaming insert buffers before transformation

### By Integer Range

Use integer-range partitioning when queries filter on a numeric identifier with predictable ranges.

```sql
-- Store performance table partitioned by store region code
CREATE TABLE `project.supply_chain_inventory.store_performance`
(
  region_code   INT64 NOT NULL,
  store_id      STRING NOT NULL,
  period_date   DATE,
  total_revenue NUMERIC
)
PARTITION BY RANGE_BUCKET(region_code, GENERATE_ARRAY(1, 100, 1));
```

**When to use**: Rare in supply chain -- prefer date partitioning in most cases.

---

## Clustering Strategies

Clustering sorts data within each partition by up to 4 columns. BigQuery uses clustering metadata to skip blocks of data that do not match the filter, reducing bytes scanned.

### Recommended Clustering Columns by Table Type

| Table Type | Cluster Column 1 | Cluster Column 2 | Cluster Column 3 | Cluster Column 4 |
|---|---|---|---|---|
| Daily Demand | `sku_id` | `store_id` | `category` | -- |
| Inventory Snapshot | `warehouse_id` | `sku_id` | `status` | -- |
| Sales Transactions | `sku_id` | `store_id` | `payment_method` | -- |
| Shipments | `carrier_id` | `origin_warehouse` | `destination_store` | -- |
| Purchase Orders | `supplier_id` | `sku_id` | `status` | -- |
| Forecasts | `sku_id` | `store_id` | `forecast_model` | -- |

### Clustering Guidelines

1. **Order matters**: Place the most frequently filtered column first. BigQuery uses the clustering order for block pruning.
2. **Match query patterns**: Clustering is effective only when queries filter or group by the clustering columns.
3. **High cardinality columns benefit most**: `sku_id` (thousands of values) clusters better than `status` (3-5 values).
4. **Combine with partitioning**: Partition by date, then cluster by entity columns for maximum pruning.
5. **Reclustering is automatic**: BigQuery periodically re-clusters data in the background at no cost.

```sql
-- Optimal: partition by date, cluster by high-cardinality entity columns
CREATE TABLE `project.supply_chain_demand.daily_sku_demand`
(
  demand_date DATE NOT NULL,
  sku_id      STRING NOT NULL,
  store_id    STRING NOT NULL,
  category    STRING
)
PARTITION BY demand_date
CLUSTER BY sku_id, store_id, category;
```

---

## Materialized Views

Materialized views pre-compute and cache aggregation results. BigQuery automatically maintains them as the base table changes, and the query optimizer transparently rewrites queries to use them when possible.

### Demand Aggregation Views

```sql
-- Weekly demand aggregation materialized view
CREATE MATERIALIZED VIEW `project.supply_chain_demand.mv_weekly_demand`
OPTIONS (
  enable_refresh = true,
  refresh_interval_minutes = 60
)
AS
SELECT
  DATE_TRUNC(demand_date, WEEK(MONDAY)) AS week_start,
  sku_id,
  store_id,
  category,
  SUM(units_sold)                       AS total_units,
  SUM(revenue)                          AS total_revenue,
  AVG(units_sold)                       AS avg_daily_units,
  COUNT(*)                              AS days_with_sales
FROM `project.supply_chain_demand.daily_sku_demand`
GROUP BY week_start, sku_id, store_id, category;
```

```sql
-- Monthly category-level demand summary
CREATE MATERIALIZED VIEW `project.supply_chain_demand.mv_monthly_category_demand`
OPTIONS (
  enable_refresh = true,
  refresh_interval_minutes = 120
)
AS
SELECT
  DATE_TRUNC(demand_date, MONTH)  AS month_start,
  category,
  SUM(units_sold)                 AS total_units,
  SUM(revenue)                    AS total_revenue,
  COUNT(DISTINCT sku_id)          AS active_skus,
  COUNT(DISTINCT store_id)        AS active_stores
FROM `project.supply_chain_demand.daily_sku_demand`
GROUP BY month_start, category;
```

### When to Use Materialized Views

- Dashboard queries that aggregate daily data into weekly/monthly summaries.
- Reports that are run repeatedly with the same aggregation pattern.
- Cross-table aggregations that are expensive to compute on the fly.

### Limitations

- Only support `SELECT`, `FROM`, `WHERE`, `GROUP BY` with aggregate functions.
- No `JOIN`, `UNION`, subqueries, or window functions.
- Base table must be partitioned or clustered.
- Maximum 20 materialized views per base table.

---

## Slot Estimation Formulas

BigQuery slots are units of computational capacity. Understanding slot consumption helps with capacity planning for flat-rate or edition pricing.

### Estimating Slot-Seconds

```
slot_seconds = (bytes_shuffled / bytes_per_slot_second) * complexity_factor
```

**Rules of thumb**:

| Query Type | Estimated Slots per TB Scanned | Typical Duration |
|---|---|---|
| Simple scan + filter | 100-500 slots | 2-10 seconds |
| Aggregation (GROUP BY) | 500-2,000 slots | 5-30 seconds |
| JOIN (two large tables) | 2,000-5,000 slots | 10-60 seconds |
| Complex multi-stage | 5,000-10,000+ slots | 30-300 seconds |

### Slot Hour Calculation

```
slot_hours = total_slot_seconds / 3600
```

For capacity planning:
```
required_slots = peak_concurrent_queries * avg_slots_per_query
```

### Supply Chain Specific Estimates

| Workload | Queries/Day | Avg TB Scanned | Avg Slots | Est. Slot Hours/Day |
|---|---|---|---|---|
| Demand dashboards | 200 | 0.5 | 500 | 14 |
| Inventory reports | 50 | 1.0 | 1,000 | 14 |
| Forecast model training | 10 | 5.0 | 3,000 | 42 |
| Ad-hoc analytics | 100 | 0.2 | 300 | 2 |
| **Total** | **360** | -- | -- | **~72** |

At 72 slot-hours/day, a 100-slot reservation covers peak demand with headroom.

---

## Cost Optimization Patterns

### Pattern 1: Avoid SELECT *

**Bad** -- scans all columns:
```sql
SELECT * FROM `project.dataset.large_table` WHERE demand_date = '2025-01-15';
```

**Good** -- scans only needed columns:
```sql
SELECT sku_id, store_id, units_sold
FROM `project.dataset.large_table`
WHERE demand_date = '2025-01-15';
```

BigQuery is columnar storage. Each column not selected is a column not scanned. On a 50-column table, selecting 3 columns reduces cost by ~94%.

### Pattern 2: Use Partition Pruning

**Bad** -- scans entire table:
```sql
SELECT sku_id, SUM(units_sold)
FROM `project.supply_chain_demand.daily_sku_demand`
GROUP BY sku_id;
```

**Good** -- scans only the needed partitions:
```sql
SELECT sku_id, SUM(units_sold)
FROM `project.supply_chain_demand.daily_sku_demand`
WHERE demand_date BETWEEN '2025-01-01' AND '2025-03-31'
GROUP BY sku_id;
```

Set `require_partition_filter = true` on large tables to enforce this at the schema level.

### Pattern 3: Denormalize Carefully

In BigQuery, JOINs between large tables are expensive because they require shuffling data across slots. For frequently joined dimension tables:

**Consider denormalizing**:
```sql
-- Instead of joining daily_demand with sku_master every query,
-- create a denormalized table
CREATE TABLE `project.supply_chain_demand.daily_demand_enriched`
AS
SELECT
  d.*,
  s.product_name,
  s.brand,
  s.weight_kg,
  s.supplier_id
FROM `project.supply_chain_demand.daily_sku_demand` d
JOIN `project.supply_chain_master.sku_master` s
  ON d.sku_id = s.sku_id;
```

**When to denormalize**:
- Dimension table is small (< 10 GB) and rarely changes.
- The join is used in > 50% of queries against the fact table.
- Query latency requirements are strict (dashboards, APIs).

**When NOT to denormalize**:
- Dimension data changes frequently (prices, inventory levels).
- Storage cost is a concern (denormalization duplicates data).
- Multiple dimension tables would need to be joined (creates wide, sparse rows).

### Pattern 4: Use Approximate Functions

```sql
-- Exact (expensive for high-cardinality columns)
SELECT COUNT(DISTINCT sku_id) FROM large_table;

-- Approximate (much faster, ~1% error margin)
SELECT APPROX_COUNT_DISTINCT(sku_id) FROM large_table;
```

### Pattern 5: Limit Query Results

```sql
-- For exploratory queries, always add LIMIT
SELECT sku_id, demand_date, units_sold
FROM `project.supply_chain_demand.daily_sku_demand`
WHERE demand_date = '2025-01-15'
ORDER BY units_sold DESC
LIMIT 100;
```

Note: `LIMIT` does not reduce bytes scanned, but it does reduce bytes returned and processing time for `ORDER BY`.

### Pattern 6: Use BI Engine for Dashboards

For repeated dashboard queries under 10 GB, enable BI Engine to cache results in memory:

```sql
-- BI Engine automatically accelerates queries on reserved memory
-- Configure via Console: BigQuery > BI Engine > Create Reservation
-- Typical supply chain reservation: 2-10 GB
```

### On-Demand Pricing Quick Reference

| Resource | Cost |
|---|---|
| Queries (on-demand) | $6.25 per TB scanned |
| Active storage | $0.02 per GB/month |
| Long-term storage (90+ days) | $0.01 per GB/month |
| Streaming inserts | $0.01 per 200 MB |
| Flat-rate slots (Enterprise) | ~$0.04 per slot-hour |

---

## Naming Conventions

### Datasets

Use the pattern: `{domain}_{subdomain}`

| Dataset Name | Purpose |
|---|---|
| `supply_chain_demand` | Demand forecasting and actuals |
| `supply_chain_inventory` | Inventory levels, movements, snapshots |
| `supply_chain_fulfillment` | Orders, shipments, delivery tracking |
| `supply_chain_master` | Master data (SKU, store, supplier, warehouse) |
| `supply_chain_ops` | Operational logs, ETL metadata, auditing |
| `supply_chain_analytics` | Derived/aggregated tables for analytics |
| `supply_chain_staging` | Staging tables for raw data loading |

### Tables

Use the pattern: `{granularity}_{entity}_{qualifier}`

| Table Name | Description |
|---|---|
| `daily_sku_demand` | Daily grain, by SKU |
| `weekly_store_inventory` | Weekly grain, by store |
| `monthly_category_revenue` | Monthly grain, by category |
| `raw_po_lines` | Raw purchase order line items |
| `dim_sku_master` | Dimension table for SKU attributes |
| `dim_store_master` | Dimension table for store attributes |
| `fact_shipments` | Fact table for shipment events |
| `stg_erp_sales_extract` | Staging table from ERP source |

### Columns

- Use `snake_case` for all column names.
- Suffix date columns with `_date` (e.g., `demand_date`, `ship_date`).
- Suffix timestamp columns with `_at` (e.g., `created_at`, `updated_at`).
- Suffix boolean columns with `is_` or `has_` prefix (e.g., `is_active`, `has_promotion`).
- Suffix ID columns with `_id` (e.g., `sku_id`, `store_id`).
- Suffix count columns with `_count` or `_qty` (e.g., `line_count`, `order_qty`).
- Suffix monetary columns with `_amount` or use descriptive names like `revenue`, `cost`.

### Materialized Views

Prefix with `mv_`: `mv_weekly_demand`, `mv_monthly_category_demand`.

### Labels

Apply labels to all tables and datasets for cost attribution and governance:

```sql
OPTIONS (
  labels = [
    ('domain', 'supply_chain'),
    ('data_tier', 'gold'),       -- raw | staging | silver | gold
    ('team', 'demand_planning'),
    ('cost_center', 'sc-001')
  ]
)
```
