-- Staging model: stg_shopify__orders
-- Source: shopify.orders
-- Grain: one row per order
-- Materialization: view

{{
    config(
        materialized='view'
    )
}}

with source as (

    select * from {{ source('shopify', 'orders') }}

),

renamed as (

    select
        -- ids
        id as order_id,
        customer_id,
        store_id,

        -- dimensions
        status as order_status,
        lower(channel) as order_channel,
        shipping_country as ship_to_country,
        currency_code,

        -- metrics
        total_price / 100.0 as total_amount,
        subtotal_price / 100.0 as subtotal_amount,
        total_tax / 100.0 as tax_amount,
        total_discounts / 100.0 as discount_amount,
        total_line_items as item_count,
        total_weight_grams / 1000.0 as total_weight_kg,

        -- booleans
        case
            when financial_status = 'paid' then true
            else false
        end as is_paid,
        case
            when cancelled_at is not null then true
            else false
        end as is_cancelled,

        -- timestamps
        cast(created_at as timestamp) as created_at,
        cast(updated_at as timestamp) as updated_at,
        cast(processed_at as timestamp) as processed_at,
        cast(cancelled_at as timestamp) as cancelled_at,
        cast(closed_at as timestamp) as closed_at

    from source

)

select * from renamed
