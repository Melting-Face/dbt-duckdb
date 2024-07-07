select *
from
    {{ source('bronze', 'dipopen1405') }}
