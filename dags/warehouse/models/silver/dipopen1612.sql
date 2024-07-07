select *
from
    {{ source('bronze', 'dipopen1612') }}
