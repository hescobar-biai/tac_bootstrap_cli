-- Staging model: stg_Products
-- Source: external GCS parquet via dbt_external_tables
-- Grain: one row per product
-- Schema: 20_staging_products_{env}
-- Materialization: view

{{
    config(
        materialized='view'
    )
}}

with source as (

    select * from {{ source('external_source', 'raw_products') }}

),

renamed as (

    select
        -- Surrogate key (FARM_FINGERPRINT for BigQuery)
        FARM_FINGERPRINT(CAST(product_id AS STRING)) as sk_product,

        -- Natural key
        product_id,

        -- Dimensions
        product_name,
        category,
        subcategory,
        brand,
        uom as unit_of_measure,

        -- Metrics
        CAST(unit_cost AS FLOAT64) as unit_cost,
        CAST(unit_price AS FLOAT64) as unit_price,
        CAST(lead_time_days AS INT64) as lead_time_days,
        CAST(minimum_order_qty AS INT64) as minimum_order_qty,

        -- Classification
        abc_class,
        xyz_class,

        -- Status
        CAST(is_active AS BOOL) as is_active

    from source

)

select * from renamed
