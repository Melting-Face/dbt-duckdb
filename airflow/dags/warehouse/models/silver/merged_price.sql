{{
  config(
    materialized='incremental',
    tags=['price', 'merge']
  )
}}

with union_table as (
  select *
  from {{
    dbt_utils.union_relations(
      relations = dbt_utils.get_relations_by_prefix(
        'main_silver',
        'price_%',
      )
    )
  }}
),

merged_table as (
    select
        source_id,
        country_id,
        "type",
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
        "date",
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
        row_number() over (
            partition by
                source_id,
                country_id,
                "type",
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
                "date",
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
        ) as "row_number"
    from union_table
)

select
    source_id,
    country_id,
    "type",
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
    "date",
    hash,
    created_at,
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
where "row_number" = 1
{% if is_incremental() %}
  and created_at > (select coalesce(max(created_at), (TIMESTAMP '2000-01-01')::bigint) from {{ this }})
{% endif %}
