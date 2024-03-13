{{
  config(
    tags=['price']
  )
}}

select
    SOURCEID::float "SOURCE_ID",
    try_cast(DATE::varchar as date) "DATE",
    try_cast(CRAWLEDAT::integer as timestamptz) "CRAWLED_AT",
    case
        when try_to_number("الحد الأدني"::varchar, 20, 10) <= 0 then null
        else try_to_number("الحد الأدني"::varchar, 20, 10)
    end as "PRICE_MIN",
    case
        when try_to_number("الحد الأقصي"::varchar, 20, 10) <= 0 then null
        else try_to_number("الحد الأقصي"::varchar, 20, 10)
    end as "PRICE_MAX",
    case
        when try_to_number("المتوسط"::varchar, 20, 10) <= 0 then null
        else try_to_number("المتوسط"::varchar, 20, 10)
    end as "PRICE_AVG",
    -- -- GUIDE CONSTANT
    'EG' "COUNTRY_ID",
    'EGP' "CURRENCY",
    '1 kg'::varchar "UNIT_RAW",
    'Cairo'::varchar "REGION_RAW",
    'w' TYPE,
    'https://bashaier.net/pricing/market' PAGE_URL

from
    {{ source('bronze', 'price_bashaier') }}
where
    PRICE_MIN is not null
    or PRICE_MAX is not null
    or PRICE_AVG is not null;
