select *
from {{ source('bronze', 'forecast_zone_information') }}
