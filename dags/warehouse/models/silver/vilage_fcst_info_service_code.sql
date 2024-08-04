select *
from {{ source('bronze', 'vilage_fcst_info_service_code') }}
