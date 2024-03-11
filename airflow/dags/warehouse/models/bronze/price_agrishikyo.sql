select *
from
    {{ source('external_source', 'price_agrishikyo') }}
