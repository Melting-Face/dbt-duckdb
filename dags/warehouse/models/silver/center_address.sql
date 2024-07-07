select
    center_id,
    center_name,
    concat_ws(' ', state, city, line_1) as address,
    '' as zip_code
from
    {{ source('bronze', '166386_2024_06_10') }}
where concat_ws(' ', state, city, line_1) != ''
