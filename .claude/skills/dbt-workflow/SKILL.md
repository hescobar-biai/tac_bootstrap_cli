---
name: dbt-workflow
description: "Creates and manages dbt models for BigQuery data warehouse with 6-layer architecture (ingestion, wrangling, staging, enrichment, aggregations, datawarehouse/serving). Use when building supply chain data transformations, creating multi-tenant dbt models, debugging dbt runs, or generating schema.yml files."
disable-model-invocation: true
allowed-tools: Bash(dbt *), Read, Write, Edit, Grep, Glob
---

# dbt Workflow

Scaffold, build, test, and document dbt models for BigQuery following the Celes "lake_house" architecture with 6 data layers, multi-tenant support, and supply chain domain patterns.

## Instructions

### Prerequisites

- dbt Core with `dbt-bigquery` adapter installed
- A `profiles.yml` configured for BigQuery (dev/qas/prd targets)
- A dbt project with `dbt_project.yml` (project name: `lake_house`)
- Environment variables: `client` (tenant ID), `env` (environment)

Before starting any work, read [reference.md](reference.md) for naming rules, layer patterns, and supply chain domain models.

### Workflow

#### 1. Identify the Model Layer

Celes uses **6 numbered data layers**, each with a schema naming convention `{number}_{layer}_{domain}_{env}`:

| # | Layer | Schema Example | Purpose | Materialization |
|---|-------|---------------|---------|-----------------|
| 10 | **Ingestion** | `10_ingestion_sales_dev` | External tables from GCS (parquet) | `external` |
| 15 | **Wrangling** | (ephemeral) | Light transformations, type casting | `ephemeral` |
| 20 | **Staging** | `20_staging_sales_dev` | Rename, cast, add surrogate keys | `view` |
| 30 | **Enrichment** | `30_enrichment_sales_dev` | Business logic joins, calculated fields | `view` or `table` |
| 40 | **Aggregations** | `40_dwagg_supply_chain_dev` | Data warehouse aggregations, data marts | `table` |
| 50 | **Serving** | `50_serving_supply_chain_dev` | API-ready views, dashboards | `view` |

#### 2. Scaffold the Model SQL

Use the appropriate template from [templates/](templates/):

- **Staging models**: Use [templates/stg_template.sql](templates/stg_template.sql) -- source CTE + rename/cast CTE + FARM_FINGERPRINT key
- **Aggregation models**: Use [templates/agg_template.sql](templates/agg_template.sql) -- joins staging models, computes supply chain metrics
- **Schema definitions**: Use [templates/schema_template.yml](templates/schema_template.yml) -- tests, descriptions, supply chain columns

For concrete examples, review [examples/](examples/).

#### 3. Multi-Tenant Configuration

Each model uses `env_var('client')` to select the tenant and `env_var('env')` for the environment. The `dbt_project.yml` uses conditional `enabled` flags per client and numbered schemas per layer.

#### 4. Surrogate Keys with FARM_FINGERPRINT

Use BigQuery's `FARM_FINGERPRINT` for deterministic surrogate keys (not MD5):

```sql
select
    FARM_FINGERPRINT(
        CONCAT(
            CAST(product_id AS STRING), '|',
            CAST(warehouse_id AS STRING)
        )
    ) as surrogate_key,
    product_id,
    warehouse_id
from {{ ref('stg_Products') }}
```

#### 5. External Tables from GCS

Ingestion layer uses `dbt_external_tables` package for parquet files in Cloud Storage with hive partitioning:

```yaml
# models/ingestion/schema.yml
sources:
  - name: external_source
    tables:
      - name: raw_invoices
        external:
          location: "gs://celes-data-lake/invoices/*.parquet"
          options:
            format: PARQUET
```

#### 6. Selectors for Orchestration

Use dbt selectors to run specific pipeline segments:

```yaml
# selectors.yml
selectors:
  - name: forecast
    definition:
      method: tag
      value: forecast_phase_1
  - name: daily_forecast
    definition:
      method: tag
      value: forecast_phase_2
  - name: aggregations
    definition:
      method: tag
      value: aggregations
  - name: serving
    definition:
      method: tag
      value: serving
```

Run with: `dbt run --selector forecast`

#### 7. Generate schema.yml

Every model directory must have a `schema.yml` with:

- Model-level description
- Column descriptions for all columns
- Tests: `not_null` and `unique` on primary keys
- `unique_combination_of_columns` for composite keys (from dbt_utils)
- Custom `validate_duplicated` tests for data quality
- Supply chain KPI columns (fill_rate, inventory_turnover, etc.)

#### 8. Validate with dbt Commands

```bash
dbt compile --select <model_name>              # Verify SQL compiles
dbt run --select <model_name>                  # Execute the model
dbt test --select <model_name>                 # Run associated tests
dbt run --selector forecast                     # Run selector group
dbt run --select <model_name> --full-refresh   # Rebuild incremental
dbt ls --select +<model_name>+                 # Full lineage
```

#### 9. Incremental Models

Use incremental materialization for large fact tables (e.g., current_stock):

```sql
{{
    config(
        materialized='incremental',
        unique_key='surrogate_key',
        incremental_strategy='merge',
        on_schema_change='append_new_columns',
        tags=['current_stock', 'real_time']
    )
}}

select * from {{ ref('stg_Stocks') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Supply Chain Domain Models

| Domain | Key Models | Description |
|--------|-----------|-------------|
| **Products** | stg_Products, stg_ABC | Product catalog with ABC classification |
| **Warehouses** | stg_Warehouses, stg_DistributionWarehouses | Storage locations |
| **Sales** | stg_Invoices, stg_agg_Invoices | Transaction history |
| **Purchasing** | stg_Purchases, stg_Suppliers | Procurement data |
| **Inventory** | stg_Stocks, stg_Warehouse_Transactions | Current and historical stock |
| **Forecast** | stg_Adjusted_Forecast | Demand predictions |
| **Supply Chain** | stg_rel_PS_WDW, stg_rel_PS_WDW_Params | Product-Supplier-Warehouse relationships |
| **Promotions** | stg_Promotions | Promotional calendar |

### Data Marts

| Mart | Schema | KPIs |
|------|--------|------|
| **DM_Sales** | `40_dwagg_sales_{env}` | Revenue, units, growth |
| **DM_Purchase** | `40_dwagg_purchase_{env}` | Cost, lead time, fill rate |
| **DM_Supply_Chain** | `40_dwagg_supply_chain_{env}` | OTIF, stockout frequency, inventory turnover |
| **DM_Forecast** | `40_dwagg_forecast_{env}` | MAPE, bias, forecast accuracy |
| **DM_Indicators** | `40_dwagg_indicators_{env}` | Gross margin, on_time_delivery_rate |

### Supporting Files Reference

| File | Purpose |
|------|---------|
| [reference.md](reference.md) | Layer patterns, multi-tenant config, BigQuery patterns, testing |
| [templates/stg_template.sql](templates/stg_template.sql) | Staging model with FARM_FINGERPRINT |
| [templates/agg_template.sql](templates/agg_template.sql) | Aggregation/data mart template |
| [templates/schema_template.yml](templates/schema_template.yml) | Schema with supply chain tests |
| [examples/stg_products.sql](examples/stg_products.sql) | Staging model for Products |
| [examples/dm_supply_chain.sql](examples/dm_supply_chain.sql) | Data mart for supply chain KPIs |
| [examples/dim_products.sql](examples/dim_products.sql) | Dimension model with ABC classification |

## Examples

### Example 1: Create a Staging Model for Products

User request:
```
Create a staging model for the Products external table from GCS
```

You would:
1. Read [templates/stg_template.sql](templates/stg_template.sql)
2. Create `models/staging/stg_Products.sql`:
   ```sql
   with source as (
       select * from {{ source('external_source', 'raw_products') }}
   ),
   renamed as (
       select
           FARM_FINGERPRINT(CAST(product_id AS STRING)) as sk_product,
           product_id,
           product_name,
           category,
           subcategory,
           CAST(unit_cost AS FLOAT64) as unit_cost,
           CAST(unit_price AS FLOAT64) as unit_price,
           CAST(is_active AS BOOL) as is_active
       from source
   )
   select * from renamed
   ```
3. Add to `models/staging/schema.yml` with tests
4. Run: `dbt run --select stg_Products`

### Example 2: Build a Supply Chain Data Mart

User request:
```
Create the DM_Supply_Chain aggregation with fill rate and stockout frequency
```

You would:
1. Read [templates/agg_template.sql](templates/agg_template.sql)
2. Create `models/datawarehouse/DM_Supply_Chain.sql` joining stg_Invoices, stg_Stocks, stg_Products
3. Compute KPIs: fill_rate, stockout_frequency, inventory_turnover, gross_margin
4. Tag with `aggregations` for selector-based orchestration
5. Run: `dbt run --selector aggregations`

### Example 3: Debug a Failing dbt Test

User request:
```
My unique_combination_of_columns test on stg_rel_PS_WDW is failing
```

You would:
1. Check compiled test: `dbt compile --select test_name`
2. Read the model SQL and identify the composite key columns
3. Query BigQuery for duplicates:
   ```sql
   SELECT product_id, supplier_id, warehouse_id, COUNT(*)
   FROM stg_rel_PS_WDW
   GROUP BY 1, 2, 3
   HAVING COUNT(*) > 1
   ```
4. Fix: add deduplication in the staging model or update the source query
5. Re-run: `dbt run --select stg_rel_PS_WDW && dbt test --select stg_rel_PS_WDW`
