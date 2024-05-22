select *
from
    {{ source('bronze', 'child_age') }}
