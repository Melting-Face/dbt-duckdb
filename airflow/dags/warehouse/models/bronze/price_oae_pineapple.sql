select *
from
    {{ source('external_source', 'price_oae_pineapple') }}
