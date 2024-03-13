{{
  config(
    tags=['price']
  )
}}

select *
from
    {{ source('bronze', 'price_ctmarket') }}
