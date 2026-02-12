-- Staging model template
-- File: models/staging/stg_<EntityName>.sql
--
-- Staging models are 1:1 with source/external tables.
-- Only rename columns, cast types, add FARM_FINGERPRINT surrogate key.
-- No joins. No aggregations. No business logic.
-- Schema: 20_staging_<domain>_{env}
--
-- Materialization: view (always)

{{
    config(
        materialized='view'
    )
}}

with source as (

    select * from {{ source('external_source', 'raw_table_name') }}

),

renamed as (

    select
        -- Surrogate key (FARM_FINGERPRINT for BigQuery)
        FARM_FINGERPRINT(CAST(natural_key AS STRING)) as sk_entity,

        -- Natural key
        natural_key as entity_id,

        -- Dimensions
        -- Example: product_name,
        -- Example: category,
        -- Example: LOWER(status) as status,

        -- Metrics (explicit casts)
        -- Example: CAST(unit_cost AS FLOAT64) as unit_cost,
        -- Example: CAST(quantity AS INT64) as quantity,

        -- Booleans
        -- Example: CAST(is_active AS BOOL) as is_active,

        -- Timestamps
        -- Example: CAST(created_at AS TIMESTAMP) as created_at,
        -- Example: CAST(updated_at AS TIMESTAMP) as updated_at

    from source

)

select * from renamed
