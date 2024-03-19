{{
  config(
    tags=['price', 'merge']
  )
}}

with merged_table as (
    select
        source_id,
        country_id,
        "TYPE",
        product_raw,
        variety_raw,
        grade_raw,
        origin_raw,
        seller,
        brand,
        transport_type,
        unit_raw,
        currency,
        region_raw,
        "DATE",
        hash,
        crawled_at created_at,
        image_url,
        memo,
        page_url,
        price_min,
        price_max,
        price_avg,
        volume,
        volume_unit,
        open_quantity_value,
        sold_quantity_value,
        quantity_unit_raw,
        remark,
        dense_rank() over (
            partition by
                source_id,
                country_id,
                "TYPE",
                product_raw,
                variety_raw,
                grade_raw,
                origin_raw,
                seller,
                brand,
                transport_type,
                unit_raw,
                currency,
                region_raw,
                "DATE",
                hash,
                image_url,
                memo,
                page_url,
                price_min,
                price_max,
                price_avg,
                volume,
                volume_unit,
                open_quantity_value,
                sold_quantity_value,
                quantity_unit_raw,
                remark
            order by crawled_at desc
        ) as "RANK"
    from {{ ref('union_price') }}
    where crawled_at is not null
)

select
    source_id,
    country_id,
    "TYPE",
    product_raw,
    variety_raw,
    grade_raw,
    origin_raw,
    seller,
    brand,
    transport_type,
    unit_raw,
    currency,
    region_raw,
    "DATE",
    hash,
    crawled_at created_at,
    image_url,
    memo,
    page_url,
    price_min,
    price_max,
    price_avg,
    volume,
    volume_unit,
    open_quantity_value,
    sold_quantity_value,
    quantity_unit_raw,
    remark
from merged_table
where "rank" = 1
