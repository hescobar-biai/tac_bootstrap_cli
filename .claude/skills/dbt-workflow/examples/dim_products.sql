-- Dimension model: dim_products
-- Grain: one row per product (latest version)
-- Purpose: Provides a clean, deduplicated product dimension with enriched
--          attributes for joining into fact tables and powering analytics.
-- Materialization: table

{{
    config(
        materialized='table'
    )
}}

with products as (

    select * from {{ ref('stg_shopify__products') }}

),

product_categories as (

    select * from {{ ref('stg_internal__product_categories') }}

),

-- Deduplicate: keep the latest version of each product
latest_products as (

    select
        *,
        row_number() over (
            partition by product_id
            order by updated_at desc
        ) as row_num

    from products

),

-- Enrich with category hierarchy and computed attributes
enriched as (

    select
        -- Primary key
        lp.product_id,

        -- Descriptive attributes
        lp.product_name,
        lp.sku,
        lp.brand,
        lp.vendor,

        -- Category hierarchy (from internal mapping)
        coalesce(pc.department, 'Uncategorized') as department,
        coalesce(pc.category, 'Uncategorized') as category,
        coalesce(pc.subcategory, 'Uncategorized') as subcategory,

        -- Product characteristics
        lp.product_type,
        lp.weight_kg,
        lp.weight_unit,

        -- Pricing
        lp.price as current_price,
        lp.compare_at_price,
        case
            when lp.compare_at_price is not null and lp.compare_at_price > 0
            then round((1 - (lp.price / lp.compare_at_price)) * 100, 1)
            else 0
        end as discount_pct,

        -- Inventory flags
        lp.is_active,
        lp.requires_shipping,
        lp.is_taxable,
        lp.inventory_quantity as current_inventory_qty,

        -- Classification
        case
            when lp.price >= 100 then 'premium'
            when lp.price >= 30 then 'mid-range'
            else 'budget'
        end as price_tier,

        case
            when lp.inventory_quantity <= 0 then 'out_of_stock'
            when lp.inventory_quantity <= 10 then 'low_stock'
            when lp.inventory_quantity <= 50 then 'normal_stock'
            else 'high_stock'
        end as stock_status,

        -- Variant count
        lp.variant_count,

        -- Lifecycle timestamps
        lp.created_at as product_created_at,
        lp.updated_at as product_updated_at,
        lp.published_at as product_published_at,

        -- Computed: days since product was created (cross-database)
        {% if target.type == 'bigquery' %}
            date_diff(current_date(), date(lp.created_at), day) as days_since_creation
        {% elif target.type == 'postgres' %}
            (current_date - lp.created_at::date) as days_since_creation
        {% endif %}

    from latest_products as lp

    left join product_categories as pc
        on lp.product_id = pc.product_id

    where lp.row_num = 1

)

select * from enriched
