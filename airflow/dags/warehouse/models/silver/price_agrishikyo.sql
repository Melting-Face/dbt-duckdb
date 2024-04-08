{{
  config(
    tags=['price']
  )
}}

select
    sourceid::float source_id,
    trim(product::varchar) product_raw,
    try_cast(priceavg::varchar as float) price_avg,
    try_cast(date::varchar as date) "date",
    crawledat::bigint crawled_at,

    '1kg' unit_raw,
    'JPY' currency,
    'JP' country_id,
    'w' "type",
    'https://www.agrishikyo.jp' "page_url"
from
    {{ source('bronze', 'price_agrishikyo') }}
