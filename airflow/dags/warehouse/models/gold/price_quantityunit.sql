{{
  config(
    tags=['price'],
  )
}}

select
    source_id,
    quantity_unit_raw
from {{ ref('merged_price') }}
