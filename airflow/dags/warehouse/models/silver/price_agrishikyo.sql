{{
  config(
    tags=['price']
  )
}}

select
    SOURCEID::float "SOURCE_ID",
    trim(PRODUCT::varchar) "PRODUCT_RAW",
    try_cast(PRICEAVG::varchar as float) "PRICE_AVG",
    try_cast(DATE::varchar as date) "DATE",
    try_cast(CRAWLEDAT::integer as timestamptz) "CRAWLED_AT",

    '1kg' "UNIT_RAW",
    'JPY' "CURRENCY",
    'JP' "COUNTRY_ID",
    'w' "TYPE",
    'https://www.agrishikyo.jp' "PAGE_URL"
from
    {{ source('bronze', 'price_agrishikyo') }}
