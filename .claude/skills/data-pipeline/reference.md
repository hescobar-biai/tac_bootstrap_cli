# Data Pipeline Reference

Comprehensive reference for data pipeline patterns on Google Cloud Platform. This document covers ingestion, transformation, quality, orchestration, idempotency, backfill, and monitoring strategies.

## Table of Contents

1. [Cloud Storage to BigQuery Loading](#cloud-storage-to-bigquery-loading)
2. [dbt Transformations](#dbt-transformations)
3. [Data Quality Checks](#data-quality-checks)
4. [Cloud Composer / Airflow DAG Patterns](#cloud-composer--airflow-dag-patterns)
5. [Idempotent Pipeline Design](#idempotent-pipeline-design)
6. [Backfill Strategies](#backfill-strategies)
7. [Monitoring and Alerting](#monitoring-and-alerting)

---

## Cloud Storage to BigQuery Loading

### bq load Command

Load files directly from Cloud Storage into BigQuery using the CLI:

```bash
# CSV with auto-detected schema
bq load --autodetect \
  --source_format=CSV \
  --skip_leading_rows=1 \
  my_dataset.my_table \
  gs://my-bucket/data/*.csv

# Parquet (schema is embedded in the file)
bq load \
  --source_format=PARQUET \
  --time_partitioning_field=event_date \
  --time_partitioning_type=DAY \
  my_dataset.my_table \
  gs://my-bucket/data/*.parquet

# JSON (newline-delimited)
bq load --autodetect \
  --source_format=NEWLINE_DELIMITED_JSON \
  my_dataset.my_table \
  gs://my-bucket/data/*.json

# With explicit schema file
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  my_dataset.my_table \
  gs://my-bucket/data/*.csv \
  schema.json
```

### Write Dispositions

| Disposition | Behavior | Use Case |
|-------------|----------|----------|
| `WRITE_TRUNCATE` | Replaces entire table | Full refresh of dimension tables |
| `WRITE_APPEND` | Appends rows | Incremental fact table loads |
| `WRITE_EMPTY` | Fails if table has data | Initial loads, safety guard |

### External Tables

Create a BigQuery table that reads directly from Cloud Storage without loading data:

```sql
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.external_events`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://my-bucket/events/*.parquet'],
  hive_partition_uri_prefix = 'gs://my-bucket/events/',
  require_hive_partition_filter = true
);
```

**When to use external tables:**
- Exploratory analysis before committing to a load pattern
- Very large datasets where you only query a small subset
- Data that changes frequently and you need the latest view

**When NOT to use external tables:**
- High-frequency queries (performance is slower than native tables)
- Complex joins (native tables are significantly faster)
- When you need clustering or materialized views

### Partitioning and Clustering

Always partition and cluster production tables for cost and performance:

```sql
CREATE TABLE `project.dataset.events`
(
  event_id STRING NOT NULL,
  user_id STRING,
  event_type STRING,
  event_date DATE,
  payload JSON
)
PARTITION BY event_date
CLUSTER BY event_type, user_id
OPTIONS (
  partition_expiration_days = 365,
  require_partition_filter = true
);
```

**Partitioning guidelines:**
- Partition by date column for time-series data
- Use ingestion-time partitioning (`_PARTITIONTIME`) when no natural date column exists
- Set `require_partition_filter = true` to prevent full-table scans
- Configure partition expiration for data retention

**Clustering guidelines:**
- Cluster by columns frequently used in WHERE and JOIN clauses
- Put the most selective column first (up to 4 columns)
- Re-cluster periodically for append-heavy tables

---

## dbt Transformations

### Project Structure (Medallion Architecture)

```
dbt_project/
  dbt_project.yml
  profiles.yml
  models/
    staging/              # Bronze: 1:1 source mirrors, light cleaning
      _staging_models.yml # Source definitions and basic tests
      stg_customers.sql
      stg_orders.sql
      stg_products.sql
    intermediate/         # Silver: Business logic, joins, deduplication
      int_order_items.sql
      int_user_sessions.sql
    marts/                # Gold: Consumption-ready aggregates
      fct_daily_revenue.sql
      fct_daily_active_users.sql
      dim_customers.sql
      dim_products.sql
  tests/                  # Custom data tests
    assert_positive_revenue.sql
  macros/                 # Reusable SQL snippets
    cents_to_dollars.sql
  seeds/                  # Static reference data
    country_codes.csv
```

### Staging Model Pattern

```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_orders') }}
),

renamed AS (
    SELECT
        order_id,
        customer_id,
        CAST(order_date AS DATE) AS order_date,
        CAST(total_amount AS NUMERIC) AS total_amount_cents,
        LOWER(status) AS order_status,
        _FILE_NAME AS source_file,
        _PARTITIONTIME AS loaded_at
    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM renamed
```

### Incremental Model Pattern

```sql
-- models/marts/fct_daily_revenue.sql
{{ config(
    materialized='incremental',
    partition_by={
      'field': 'revenue_date',
      'data_type': 'date',
      'granularity': 'day'
    },
    cluster_by=['region'],
    unique_key='revenue_date || region',
    on_schema_change='append_new_columns'
) }}

SELECT
    DATE(o.order_date) AS revenue_date,
    c.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount_cents) / 100 AS total_revenue_dollars,
    AVG(o.total_amount_cents) / 100 AS avg_order_value_dollars
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('dim_customers') }} c ON o.customer_id = c.customer_id
WHERE o.order_status = 'completed'
{% if is_incremental() %}
  AND o.order_date >= (SELECT MAX(revenue_date) FROM {{ this }})
{% endif %}
GROUP BY 1, 2
```

### dbt Commands Reference

```bash
# Run all models
dbt run

# Run specific model and its upstream dependencies
dbt run --select +fct_daily_revenue

# Run only staging models
dbt run --select staging

# Run tests
dbt test

# Test a specific model
dbt test --select stg_orders

# Generate documentation
dbt docs generate && dbt docs serve

# Full refresh an incremental model
dbt run --full-refresh --select fct_daily_revenue

# Dry run (compile SQL without executing)
dbt compile --select fct_daily_revenue
```

---

## Data Quality Checks

### dbt Built-in Tests

Define in YAML schema files alongside models:

```yaml
# models/staging/_staging_models.yml
version: 2

sources:
  - name: raw
    database: my-project
    schema: raw_data
    tables:
      - name: raw_orders
        loaded_at_field: _PARTITIONTIME
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}

models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled', 'refunded']
      - name: total_amount_cents
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

### Custom dbt Tests

```sql
-- tests/assert_no_orphan_orders.sql
-- This test passes when the query returns zero rows.
SELECT
    o.order_id,
    o.customer_id
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
```

### dbt Source Freshness

Monitor that upstream data is arriving on schedule:

```bash
dbt source freshness
```

This checks the `loaded_at_field` against the `freshness` thresholds defined in the YAML schema. Failed freshness checks can trigger alerts in your orchestration layer.

### Great Expectations Integration

For pipelines requiring validation beyond dbt:

```python
import great_expectations as gx

context = gx.get_context()

# Define expectations
suite = context.add_expectation_suite("orders_suite")
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_amount", min_value=0, max_value=1_000_000
    )
)
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=1000, max_value=10_000_000
    )
)

# Run validation against BigQuery
datasource = context.sources.add_or_update_sql(
    name="bigquery",
    connection_string="bigquery://my-project/my_dataset"
)
batch = datasource.get_batch("SELECT * FROM stg_orders")
results = batch.validate(suite)

if not results.success:
    raise ValueError(f"Data quality check failed: {results}")
```

### BigQuery Validation Queries

Run post-load sanity checks directly in BigQuery:

```sql
-- Row count validation
SELECT
    CASE
        WHEN COUNT(*) BETWEEN 1000 AND 10000000 THEN 'PASS'
        ELSE 'FAIL: unexpected row count ' || CAST(COUNT(*) AS STRING)
    END AS check_result
FROM `project.dataset.stg_orders`
WHERE DATE(_PARTITIONTIME) = CURRENT_DATE();

-- Null rate check
SELECT
    COUNTIF(order_id IS NULL) AS null_order_ids,
    COUNTIF(customer_id IS NULL) AS null_customer_ids,
    COUNT(*) AS total_rows,
    SAFE_DIVIDE(COUNTIF(order_id IS NULL), COUNT(*)) AS null_rate
FROM `project.dataset.stg_orders`
WHERE DATE(_PARTITIONTIME) = CURRENT_DATE();

-- Duplicate detection
SELECT order_id, COUNT(*) AS duplicate_count
FROM `project.dataset.stg_orders`
WHERE DATE(_PARTITIONTIME) = CURRENT_DATE()
GROUP BY order_id
HAVING COUNT(*) > 1;
```

---

## Cloud Composer / Airflow DAG Patterns

### Basic DAG Structure

See [templates/dag_template.py](templates/dag_template.py) for a complete working example.

### Common Operator Patterns

**BashOperator for dbt:**

```python
dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="cd /home/airflow/gcs/dags/dbt_project && dbt run --profiles-dir .",
    env={"DBT_PROFILES_DIR": "/home/airflow/gcs/dags/dbt_project"},
)
```

**BigQueryInsertJobOperator for SQL:**

```python
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

validate_load = BigQueryInsertJobOperator(
    task_id="validate_load",
    configuration={
        "query": {
            "query": """
                SELECT COUNT(*) AS row_count
                FROM `project.dataset.table`
                WHERE DATE(_PARTITIONTIME) = '{{ ds }}'
            """,
            "useLegacySql": False,
        }
    },
)
```

**GCSToBigQueryOperator for direct loads:**

```python
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

load_task = GCSToBigQueryOperator(
    task_id="load_csv_to_bq",
    bucket="my-data-bucket",
    source_objects=["raw/events/{{ ds }}/*.csv"],
    destination_project_dataset_table="project.dataset.raw_events${{ ds_nodash }}",
    source_format="CSV",
    skip_leading_rows=1,
    write_disposition="WRITE_TRUNCATE",
    autodetect=True,
)
```

**PythonOperator for custom logic:**

```python
from airflow.operators.python import PythonOperator

def check_data_quality(**context):
    from google.cloud import bigquery
    client = bigquery.Client()
    query = f"""
        SELECT COUNT(*) AS cnt
        FROM `project.dataset.table`
        WHERE DATE(_PARTITIONTIME) = '{context["ds"]}'
    """
    result = list(client.query(query).result())
    row_count = result[0].cnt
    if row_count == 0:
        raise ValueError(f"No rows loaded for {context['ds']}")
    print(f"Loaded {row_count} rows for {context['ds']}")

quality_check = PythonOperator(
    task_id="check_data_quality",
    python_callable=check_data_quality,
    provide_context=True,
)
```

### Task Dependency Patterns

```python
# Linear pipeline
load >> transform >> validate >> notify

# Parallel loads followed by transformation
[load_a, load_b, load_c] >> transform >> validate

# Fan-out after transformation
transform >> [report_a, report_b, export]

# Diamond pattern
load >> [transform_a, transform_b] >> merge >> validate
```

### Dynamic DAG Generation

Generate DAGs programmatically for multiple tables:

```python
tables = ["customers", "orders", "products", "inventory"]

for table in tables:
    task = GCSToBigQueryOperator(
        task_id=f"load_{table}",
        bucket="my-data-bucket",
        source_objects=[f"raw/{table}/{{{{ ds }}}}/*.parquet"],
        destination_project_dataset_table=f"project.raw.{table}",
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",
    )
    start >> task >> end
```

---

## Idempotent Pipeline Design

Idempotency ensures that running a pipeline multiple times with the same input produces the same result. This is critical for reliability and backfill support.

### Principles

1. **Use partition-level operations**: Truncate and reload specific partitions rather than appending
2. **Deterministic outputs**: Same input date should always produce the same output
3. **No side effects**: Avoid auto-incrementing IDs or current-timestamp columns
4. **Atomic operations**: Use BigQuery `WRITE_TRUNCATE` on partitions or `MERGE` statements

### Partition-Level Idempotency

```sql
-- Truncate and reload a specific partition (idempotent)
-- BigQuery interprets $YYYYMMDD as a partition decorator
LOAD DATA OVERWRITE `project.dataset.events$20250115`
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://bucket/events/dt=2025-01-15/*.parquet']
);
```

In dbt, incremental models achieve idempotency by deleting and reinserting:

```sql
{{ config(
    materialized='incremental',
    unique_key='event_date || event_id',
    incremental_strategy='merge'
) }}
```

### MERGE Pattern

```sql
MERGE `project.dataset.dim_customers` AS target
USING `project.staging.stg_customers` AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
    UPDATE SET
        target.name = source.name,
        target.email = source.email,
        target.updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, created_at, updated_at)
    VALUES (source.customer_id, source.name, source.email, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
```

### Deduplication Pattern

For sources that may deliver duplicate records:

```sql
-- Deduplicate within staging
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY loaded_at DESC
        ) AS row_num
    FROM {{ source('raw', 'raw_events') }}
)
SELECT * FROM ranked WHERE row_num = 1
```

---

## Backfill Strategies

### Airflow Backfill

Use Airflow's built-in backfill to reprocess historical dates:

```bash
# Backfill a specific date range
airflow dags backfill my_pipeline_dag \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --reset-dagruns

# Backfill via Cloud Composer gcloud
gcloud composer environments run my-composer-env \
  --location us-central1 \
  dags backfill -- my_pipeline_dag \
  --start-date 2025-01-01 \
  --end-date 2025-01-31
```

### dbt Backfill

For incremental dbt models, use `--full-refresh` or date variables:

```bash
# Full refresh: drop and rebuild the entire table
dbt run --full-refresh --select fct_daily_revenue

# Targeted backfill with date variables
dbt run --select fct_daily_revenue \
  --vars '{"start_date": "2025-01-01", "end_date": "2025-01-31"}'
```

The model must support the variable:

```sql
{% if is_incremental() %}
  {% if var('start_date', none) and var('end_date', none) %}
    AND order_date BETWEEN '{{ var("start_date") }}' AND '{{ var("end_date") }}'
  {% else %}
    AND order_date >= (SELECT MAX(revenue_date) FROM {{ this }})
  {% endif %}
{% endif %}
```

### Partition-Level Backfill

For BigQuery native loads, target specific partitions:

```python
from google.cloud import bigquery
from datetime import date, timedelta

client = bigquery.Client()
start = date(2025, 1, 1)
end = date(2025, 1, 31)

current = start
while current <= end:
    partition = current.strftime("%Y%m%d")
    uri = f"gs://bucket/events/dt={current.isoformat()}/*.parquet"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    table_ref = f"project.dataset.events${partition}"
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  # Wait for completion

    print(f"Backfilled partition {partition}: {load_job.output_rows} rows")
    current += timedelta(days=1)
```

### Backfill Safety Checklist

- [ ] Verify idempotency: re-running should produce identical results
- [ ] Check downstream dependencies: notify consumers of data changes
- [ ] Monitor resource usage: backfills can spike BigQuery slot usage
- [ ] Use `WRITE_TRUNCATE` on partitions, never `WRITE_APPEND` during backfill
- [ ] Validate row counts after backfill against source of truth
- [ ] Run dbt tests after backfill completes

---

## Monitoring and Alerting

### Cloud Monitoring Metrics

Key metrics to monitor for data pipelines:

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| DAG run duration | Airflow | > 2x average duration |
| Task failure count | Airflow | > 0 per run |
| BigQuery slot usage | BigQuery | > 80% of reservation |
| Bytes scanned per query | BigQuery | > expected budget |
| Table freshness | dbt source freshness | > SLA window |
| Row count delta | Custom query | > 20% deviation from expected |
| Load job errors | BigQuery Jobs API | > 0 |

### Airflow Alerting Callbacks

```python
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook

def slack_alert_on_failure(context):
    """Send Slack alert when a task fails."""
    hook = SlackWebhookHook(slack_webhook_conn_id="slack_webhook")
    task_instance = context["task_instance"]
    message = (
        f":red_circle: *Task Failed*\n"
        f"*DAG*: {task_instance.dag_id}\n"
        f"*Task*: {task_instance.task_id}\n"
        f"*Execution Date*: {context['ds']}\n"
        f"*Log URL*: {task_instance.log_url}"
    )
    hook.send(text=message)

def slack_alert_on_success(context):
    """Send Slack alert when the entire DAG succeeds."""
    hook = SlackWebhookHook(slack_webhook_conn_id="slack_webhook")
    message = (
        f":white_check_mark: *DAG Succeeded*\n"
        f"*DAG*: {context['dag'].dag_id}\n"
        f"*Execution Date*: {context['ds']}\n"
        f"*Duration*: {context['dag_run'].end_date - context['dag_run'].start_date}"
    )
    hook.send(text=message)
```

### BigQuery Audit Logging

Query BigQuery audit logs to monitor pipeline health:

```sql
-- Recent load jobs and their status
SELECT
    protopayload_auditlog.methodName,
    protopayload_auditlog.resourceName,
    protopayload_auditlog.status.code AS status_code,
    protopayload_auditlog.status.message AS error_message,
    timestamp
FROM `project.region-us.INFORMATION_SCHEMA.JOBS`
WHERE
    job_type = 'LOAD'
    AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY creation_time DESC;
```

### Data Freshness Monitoring

Create a BigQuery scheduled query to check freshness:

```sql
-- Check that each table has been updated within its SLA
WITH table_freshness AS (
    SELECT
        'raw_orders' AS table_name,
        MAX(_PARTITIONTIME) AS last_updated,
        TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(_PARTITIONTIME), HOUR) AS hours_since_update,
        12 AS sla_hours
    FROM `project.dataset.raw_orders`

    UNION ALL

    SELECT
        'raw_events' AS table_name,
        MAX(_PARTITIONTIME) AS last_updated,
        TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(_PARTITIONTIME), HOUR) AS hours_since_update,
        6 AS sla_hours
    FROM `project.dataset.raw_events`
)
SELECT
    table_name,
    last_updated,
    hours_since_update,
    sla_hours,
    CASE
        WHEN hours_since_update > sla_hours THEN 'BREACH'
        WHEN hours_since_update > sla_hours * 0.8 THEN 'WARNING'
        ELSE 'OK'
    END AS freshness_status
FROM table_freshness;
```

### Dashboard Recommendations

Set up a monitoring dashboard with:

1. **Pipeline Health**: DAG success/failure rate over the last 7 days
2. **Data Freshness**: Time since last update for each critical table
3. **Volume Trends**: Row counts per day, with anomaly detection
4. **Cost Tracking**: BigQuery bytes scanned and slot usage per pipeline
5. **Error Log**: Recent task failures with links to Airflow logs
