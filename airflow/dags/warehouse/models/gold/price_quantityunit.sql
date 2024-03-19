{{
  config(
    tags=['price'],
    unique_key=[
      "SOURCE_ID",
      "QUANTITY_UNIT_RAW"
    ]
  )
}}

select
    source_id,
    current_timestamp created_at,
    current_timestamp updated_at,
    'p' status,
    '' submission_memo,
    '' escalation_reason,
    '' evaluation_memo,
    quantity_unit_raw,
    null quantity_unit
from {{ ref('merged_price') }}
