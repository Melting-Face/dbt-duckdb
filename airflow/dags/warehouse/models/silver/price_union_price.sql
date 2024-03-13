{{
  config(
    tags=['price', 'union']
  )
}}

select *
from {{
  dbt_utils.union_relations(
    relations = dbt_utils.get_relations_by_prefix(
      'main_silver',
      'price_%',
      exclude='price_union_price%'
    )
  )
}}
