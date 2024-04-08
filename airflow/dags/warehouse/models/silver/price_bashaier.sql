{{
  config(
    tags=['price']
  )
}}

select
    sourceid::float "source_id",
    try_cast(date::varchar as date) "date",
    "المحصول"::varchar product_raw,
    crawledat::bigint "crawled_at",
    case
        when try_cast("الحد الأدني" as double) <= 0 then null
        else try_cast("الحد الأدني" as double)
    end as "price_min",
    case
        when try_cast("الحد الأقصي" as double) <= 0 then null
        else try_cast("الحد الأقصي" as double)
    end as "price_max",
    case
        when try_cast("المتوسط" as double) <= 0 then null
        else try_cast("المتوسط" as double)
    end as "price_avg",
    -- -- GUIDE CONSTANT
    'EG' "country_id",
    'EGP' "currency",
    '1 kg'::varchar "unit_raw",
    'Cairo'::varchar "region_raw",
    'w' "type",
    'https://bashaier.net/pricing/market' page_url
from
    {{ source('bronze', 'price_bashaier') }}
where
    price_min is not null
    or price_max is not null
    or price_avg is not null
