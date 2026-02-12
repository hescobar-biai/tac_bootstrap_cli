---
name: data-pipeline
description: "Designs and implements data pipelines for ETL/ELT workflows integrating BigQuery, Cloud Storage, and dbt. Use when building data ingestion, transformation, or orchestration pipelines with Airflow/Cloud Composer."
allowed-tools: Bash(python *), Bash(dbt *), Bash(bq *), Read, Write, Edit
---

# Data Pipeline Design and Implementation

Design and implement production-grade data pipelines for ETL/ELT workflows on Google Cloud Platform, integrating Cloud Storage, BigQuery, dbt, and Cloud Composer (Airflow).

## Instructions

### Prerequisites

Before starting any pipeline work, ensure the following are available:

1. **Google Cloud SDK** installed and authenticated (`gcloud auth application-default login`)
2. **BigQuery CLI** (`bq`) available in PATH
3. **dbt** installed with the `dbt-bigquery` adapter (`pip install dbt-bigquery`)
4. **Python 3.10+** with `google-cloud-bigquery` and `google-cloud-storage` libraries
5. **Cloud Composer environment** provisioned (for Airflow DAG deployment)

### Workflow

Follow this structured workflow when building a data pipeline:

#### Step 1: Understand the Data Source and Destination

1. Identify the source system (Cloud Storage bucket, API, database, streaming)
2. Determine the target schema in BigQuery (dataset, table names, partitioning)
3. Document the data format (CSV, JSON, Avro, Parquet) and expected volume
4. Define the refresh cadence (batch daily, hourly, near-real-time)

#### Step 2: Design the Pipeline Architecture

Choose the appropriate pattern based on requirements:

- **Simple Load**: Cloud Storage to BigQuery direct load (use [templates/loader.py](templates/loader.py))
- **ELT with dbt**: Load raw data first, then transform with dbt models
- **Orchestrated Pipeline**: Multi-step pipeline with Airflow DAG (use [templates/dag_template.py](templates/dag_template.py))
- **Streaming**: Pub/Sub to BigQuery via Dataflow (out of scope for this skill)

Refer to [reference.md](reference.md) for detailed patterns on each approach.

#### Step 3: Implement Data Ingestion

Use the BigQuery loader template as a starting point:

```bash
python templates/loader.py \
  --bucket my-data-bucket \
  --prefix raw/events/ \
  --dataset my_dataset \
  --table raw_events \
  --format PARQUET
```

Key considerations:
- Enable schema auto-detection for initial loads; pin schemas for production
- Use `WRITE_TRUNCATE` for full refreshes, `WRITE_APPEND` for incremental
- Configure retry logic with exponential backoff
- Partition tables by ingestion time or a date column for cost optimization

#### Step 4: Build dbt Transformations

Structure dbt models following the medallion architecture:

```
models/
  staging/          # 1:1 with source tables, light cleaning
    stg_events.sql
  intermediate/     # Business logic joins and aggregations
    int_user_sessions.sql
  marts/            # Final consumption layer
    fct_daily_active_users.sql
    dim_users.sql
```

Run and test transformations:

```bash
dbt run --select staging       # Run staging models
dbt test --select staging      # Run data tests
dbt run --select marts         # Run mart models
dbt test                       # Run all tests
```

#### Step 5: Add Data Quality Checks

Implement quality gates at each layer:

1. **Source validation**: Row counts, null checks on required fields
2. **dbt tests**: `unique`, `not_null`, `accepted_values`, `relationships`
3. **Custom dbt tests**: Business rule validations in `tests/` directory
4. **BigQuery validation queries**: Post-load checks via `BigQueryOperator`

See the "Data Quality Checks" section in [reference.md](reference.md) for detailed patterns.

#### Step 6: Create the Orchestration DAG

Use the Airflow DAG template for Cloud Composer:

1. Copy [templates/dag_template.py](templates/dag_template.py) to your DAGs folder
2. Configure `default_args` (owner, retries, retry_delay, start_date)
3. Define task dependencies: `load >> transform >> validate >> notify`
4. Set the schedule interval matching your refresh cadence
5. Add alerting on failure via Slack, PagerDuty, or email callbacks

#### Step 7: Deploy and Monitor

1. **Deploy DAG** to Cloud Composer bucket:
   ```bash
   gcloud composer environments storage dags import \
     --environment my-composer-env \
     --location us-central1 \
     --source my_pipeline_dag.py
   ```
2. **Monitor** via Airflow UI, Cloud Monitoring dashboards, and BigQuery audit logs
3. **Set alerts** for SLA breaches, task failures, and data freshness

### Supporting Files

| File | Description |
|------|-------------|
| [reference.md](reference.md) | Comprehensive pipeline patterns, idempotency strategies, backfill procedures, and monitoring |
| [templates/dag_template.py](templates/dag_template.py) | Airflow DAG skeleton for Cloud Composer with dbt and BigQuery tasks |
| [templates/loader.py](templates/loader.py) | BigQuery data loader with Cloud Storage discovery, schema detection, and retry logic |

## Examples

### Example 1: Daily CSV Ingestion from Cloud Storage to BigQuery

User request:
```
Load daily CSV files from gs://my-bucket/sales/ into BigQuery dataset analytics.raw_sales
```

You would:
1. Review the CSV structure by examining a sample file in the bucket:
   ```bash
   bq load --autodetect --dry_run \
     analytics.raw_sales \
     gs://my-bucket/sales/2025-01-01/*.csv
   ```
2. Adapt `templates/loader.py` with the specific bucket, prefix, dataset, and table
3. Configure the load job for CSV format with header row skipping and `WRITE_TRUNCATE` disposition
4. Add date-based partitioning on the ingestion date column
5. Create a simple Airflow DAG with a single `PythonOperator` calling the loader
6. Add a downstream `BigQueryCheckOperator` to verify row counts post-load
7. Deploy the DAG to Cloud Composer and verify the first run succeeds

### Example 2: ELT Pipeline with dbt Transformations

User request:
```
Build an ELT pipeline that loads raw event data into BigQuery, then transforms it with dbt to produce a daily active users mart
```

You would:
1. Set up the ingestion layer using `templates/loader.py` to load raw events from Cloud Storage into `analytics.raw_events`
2. Initialize dbt project structure if not present:
   ```bash
   dbt init my_analytics
   ```
3. Create staging model `stg_events.sql`:
   ```sql
   SELECT
     event_id,
     user_id,
     event_type,
     TIMESTAMP(event_timestamp) AS event_at,
     _FILE_NAME AS source_file
   FROM {{ source('raw', 'raw_events') }}
   WHERE event_id IS NOT NULL
   ```
4. Create mart model `fct_daily_active_users.sql`:
   ```sql
   SELECT
     DATE(event_at) AS activity_date,
     COUNT(DISTINCT user_id) AS active_users
   FROM {{ ref('stg_events') }}
   GROUP BY 1
   ```
5. Add dbt tests for uniqueness on `event_id` and not-null on `user_id`
6. Build the Airflow DAG from `templates/dag_template.py` with tasks: `load_raw >> dbt_run_staging >> dbt_test_staging >> dbt_run_marts >> dbt_test_all`
7. Configure the DAG schedule for daily at 06:00 UTC
8. Deploy and run a backfill for the past 7 days:
   ```bash
   dbt run --select fct_daily_active_users --vars '{"start_date": "2025-01-01", "end_date": "2025-01-07"}'
   ```

### Example 3: Orchestrated Multi-Source Pipeline with Quality Gates

User request:
```
Create a pipeline that ingests data from 3 Cloud Storage sources, runs dbt transformations, validates quality, and sends a Slack notification on completion or failure
```

You would:
1. Create three loader tasks using `templates/loader.py`, one per source (customers, orders, products)
2. Build a comprehensive Airflow DAG based on `templates/dag_template.py`:
   ```python
   # Parallel ingestion
   [load_customers, load_orders, load_products] >> dbt_run_staging

   # Sequential transformation and validation
   dbt_run_staging >> dbt_test_staging >> dbt_run_marts >> dbt_test_all

   # Quality gate
   dbt_test_all >> bq_validation_query >> slack_notify_success

   # Failure callback on any task
   default_args = {'on_failure_callback': slack_alert_failure}
   ```
3. Configure each loader with appropriate write dispositions:
   - Customers: `WRITE_TRUNCATE` (full refresh, small dimension)
   - Orders: `WRITE_APPEND` with deduplication in dbt (incremental)
   - Products: `WRITE_TRUNCATE` (full refresh, small dimension)
4. Add BigQuery validation query to check cross-source referential integrity:
   ```sql
   SELECT COUNT(*) AS orphan_orders
   FROM `analytics.stg_orders` o
   LEFT JOIN `analytics.stg_customers` c ON o.customer_id = c.customer_id
   WHERE c.customer_id IS NULL
   ```
5. Configure Slack webhook for success and failure notifications
6. Set up Cloud Monitoring alert for DAG SLA breach (pipeline not complete by 08:00 UTC)
7. Deploy, trigger a manual run, and verify end-to-end execution in the Airflow UI
