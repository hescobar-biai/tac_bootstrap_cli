---
name: bigquery-ops
description: "Manages BigQuery datasets, tables, and queries for supply chain analytics. Use when working with BigQuery schemas, optimizing queries, creating data pipelines, or generating Python clients with google-cloud-bigquery."
allowed-tools: Bash(bq *), Bash(gcloud *), Read, Write, Grep
---

# BigQuery Operations for Supply Chain Analytics

Skill for managing BigQuery resources -- DDL generation, query optimization, Python client scaffolding, schema validation, and cost estimation -- tailored to supply chain analytics workloads (demand forecasting, inventory management, fulfillment tracking).

## Instructions

### Prerequisites

- Google Cloud SDK installed and authenticated (`gcloud auth login`)
- `bq` CLI available (bundled with Google Cloud SDK)
- Python 3.10+ with `google-cloud-bigquery` package for client generation
- A GCP project with BigQuery API enabled

### Workflow

Follow these steps depending on the task at hand. Each task type has its own sub-workflow.

#### 1. DDL Generation

When the user needs to create or modify BigQuery tables, datasets, or views:

1. **Gather requirements**: Identify the dataset name, table name, column definitions, and data types.
2. **Apply naming conventions**: Use `snake_case` for all identifiers. Prefix datasets with the domain (e.g., `supply_chain_demand`, `supply_chain_inventory`). See [reference.md](reference.md) for full naming conventions.
3. **Choose partitioning strategy**:
   - Time-series data (demand, sales, shipments): Partition by date column (e.g., `demand_date`, `order_date`).
   - Log/event data (ETL logs, audit trails): Partition by `_PARTITIONTIME` (ingestion time).
   - See [reference.md](reference.md) for detailed partitioning strategies.
4. **Choose clustering columns**: Select up to 4 columns that are frequently used in `WHERE` and `GROUP BY` clauses (e.g., `sku_id`, `store_id`, `category`).
5. **Generate the DDL statement**: Produce a `CREATE TABLE` or `CREATE OR REPLACE TABLE` statement with partitioning, clustering, labels, and description.
6. **Validate**: Dry-run the DDL with `bq query --dry_run` to check syntax without executing.

#### 2. Query Optimization

When the user wants to improve query performance or reduce costs:

1. **Analyze the existing query**: Read the SQL and identify anti-patterns (SELECT *, full table scans, cross joins, lack of partition pruning).
2. **Check partitioning usage**: Ensure WHERE clauses include the partition column to enable partition pruning.
3. **Check clustering alignment**: Verify that filter and group-by columns match the table's clustering columns in order.
4. **Estimate cost before and after**: Use `bq query --dry_run` to compare bytes processed.
5. **Apply optimizations**:
   - Replace `SELECT *` with explicit column lists.
   - Add partition filters to prune scanned data.
   - Use approximate aggregation functions (`APPROX_COUNT_DISTINCT`) where exact counts are not required.
   - Consider materialized views for repeated aggregation patterns.
   - Denormalize judiciously to avoid expensive JOINs on large tables.
6. **Validate**: Dry-run the optimized query and compare bytes processed to the original.

See [reference.md](reference.md) for cost optimization patterns and slot estimation formulas.

#### 3. Python Client Scaffolding

When the user needs a Python module to interact with BigQuery:

1. **Identify the operations needed**: Read, write, query, or stream data.
2. **Generate a client module** with:
   - `google-cloud-bigquery` client initialization with project ID.
   - Typed dataclass or Pydantic model for the table schema.
   - Functions for common operations: `run_query()`, `insert_rows()`, `export_to_gcs()`, `load_from_gcs()`.
   - Proper error handling with `google.api_core.exceptions`.
   - Retry configuration for transient errors.
3. **Include docstrings and type hints** following the project's conventions.
4. **Add a usage example** as a `if __name__ == "__main__"` block.

#### 4. Schema Validation

When the user wants to verify or compare schemas:

1. **Fetch current schema**: Use `bq show --schema --format=prettyjson <dataset>.<table>`.
2. **Compare with expected schema**: Diff column names, types, modes (NULLABLE, REQUIRED, REPEATED).
3. **Report mismatches**: List added, removed, or changed columns.
4. **Generate migration DDL** if schema changes are needed (ALTER TABLE ADD COLUMN, etc.).

#### 5. Cost Estimation

When the user wants to estimate query or storage costs:

1. **Dry-run the query**: `bq query --dry_run --use_legacy_sql=false '<SQL>'` to get bytes processed.
2. **Calculate on-demand cost**: `(bytes_processed / 1 TB) * $6.25` (current on-demand pricing).
3. **Estimate slot usage**: See [reference.md](reference.md) for slot estimation formulas.
4. **Report storage costs**: `$0.02/GB/month` for active storage, `$0.01/GB/month` for long-term (90+ days).

### Reference Materials

- For BigQuery best practices, naming conventions, partitioning strategies, and cost formulas, see [reference.md](reference.md).
- For ready-to-use supply chain SQL query patterns, see [examples/supply_chain_queries.sql](examples/supply_chain_queries.sql).

## Examples

### Example 1: Create a Partitioned Demand Table

User request:
```
Create a BigQuery table for daily SKU demand data with partitioning and clustering.
```

You would:
1. Define the schema based on supply chain demand requirements:
   - `demand_date DATE` (partition column)
   - `sku_id STRING`, `store_id STRING`, `category STRING` (clustering columns)
   - `units_sold INT64`, `revenue NUMERIC`, `units_forecast INT64`
2. Generate the DDL:
   ```sql
   CREATE TABLE IF NOT EXISTS `project.supply_chain_demand.daily_sku_demand`
   (
     demand_date       DATE NOT NULL,
     sku_id            STRING NOT NULL,
     store_id          STRING NOT NULL,
     category          STRING,
     units_sold        INT64,
     revenue           NUMERIC,
     units_forecast    INT64,
     created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
     updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
   )
   PARTITION BY demand_date
   CLUSTER BY sku_id, store_id, category
   OPTIONS (
     description = 'Daily demand by SKU and store for supply chain analytics',
     labels = [('domain', 'supply_chain'), ('data_tier', 'gold')],
     partition_expiration_days = 730,
     require_partition_filter = true
   );
   ```
3. Validate with dry-run:
   ```bash
   bq query --dry_run --use_legacy_sql=false < ddl_daily_sku_demand.sql
   ```
4. Confirm no errors and report the table definition to the user.

### Example 2: Optimize an Existing Query

User request:
```
This query is scanning too much data. Optimize it:
SELECT * FROM `project.supply_chain_demand.daily_sku_demand`
WHERE category = 'Electronics'
ORDER BY demand_date DESC
```

You would:
1. Identify anti-patterns:
   - `SELECT *` fetches all columns including unused ones.
   - No partition filter on `demand_date` -- full table scan.
   - `ORDER BY` on a large result set without `LIMIT`.
2. Apply optimizations:
   ```sql
   SELECT
     demand_date,
     sku_id,
     store_id,
     units_sold,
     revenue
   FROM `project.supply_chain_demand.daily_sku_demand`
   WHERE demand_date BETWEEN '2025-01-01' AND '2025-12-31'
     AND category = 'Electronics'
   ORDER BY demand_date DESC
   LIMIT 1000;
   ```
3. Dry-run both queries to compare:
   ```bash
   bq query --dry_run --use_legacy_sql=false 'SELECT * FROM ...'
   bq query --dry_run --use_legacy_sql=false 'SELECT demand_date, sku_id, ...'
   ```
4. Report the reduction in bytes processed and estimated cost savings.

### Example 3: Generate a Python Client

User request:
```
Generate a Python client for querying our daily demand table.
```

You would:
1. Scaffold a Python module with the `google-cloud-bigquery` client:
   ```python
   """BigQuery client for daily SKU demand data."""

   from dataclasses import dataclass
   from datetime import date
   from typing import Optional

   from google.cloud import bigquery
   from google.api_core import exceptions as gcp_exceptions

   PROJECT_ID = "your-gcp-project"
   DATASET_ID = "supply_chain_demand"
   TABLE_ID = "daily_sku_demand"
   FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


   @dataclass
   class DemandRecord:
       """Represents a single daily demand record."""
       demand_date: date
       sku_id: str
       store_id: str
       category: Optional[str]
       units_sold: Optional[int]
       revenue: Optional[float]
       units_forecast: Optional[int]


   def get_client() -> bigquery.Client:
       """Initialize and return a BigQuery client."""
       return bigquery.Client(project=PROJECT_ID)


   def query_demand_by_sku(
       client: bigquery.Client,
       sku_id: str,
       start_date: date,
       end_date: date,
   ) -> list[DemandRecord]:
       """Query demand records for a specific SKU within a date range."""
       sql = f"""
           SELECT demand_date, sku_id, store_id, category,
                  units_sold, revenue, units_forecast
           FROM `{FULL_TABLE_ID}`
           WHERE demand_date BETWEEN @start_date AND @end_date
             AND sku_id = @sku_id
           ORDER BY demand_date
       """
       job_config = bigquery.QueryJobConfig(
           query_parameters=[
               bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
               bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
               bigquery.ScalarQueryParameter("sku_id", "STRING", sku_id),
           ]
       )
       try:
           results = client.query(sql, job_config=job_config).result()
           return [
               DemandRecord(
                   demand_date=row.demand_date,
                   sku_id=row.sku_id,
                   store_id=row.store_id,
                   category=row.category,
                   units_sold=row.units_sold,
                   revenue=float(row.revenue) if row.revenue else None,
                   units_forecast=row.units_forecast,
               )
               for row in results
           ]
       except gcp_exceptions.NotFound:
           raise ValueError(f"Table {FULL_TABLE_ID} not found")


   if __name__ == "__main__":
       bq_client = get_client()
       records = query_demand_by_sku(
           bq_client,
           sku_id="SKU-12345",
           start_date=date(2025, 1, 1),
           end_date=date(2025, 1, 31),
       )
       for r in records:
           print(f"{r.demand_date} | {r.sku_id} | {r.units_sold} units")
   ```
2. Explain each function, its parameters, and error handling.
3. Suggest adding retry logic and connection pooling for production use.
