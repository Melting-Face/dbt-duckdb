select *
from
    {{ source('bronze', 'dipopen1622') }}
