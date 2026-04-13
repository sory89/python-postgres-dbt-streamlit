select
    cast(id as integer)                    as promotion_id,
    cast(product_id as integer)            as product_id,
    trim(name)                             as promotion_name,
    trim(description)                      as description,
    cast(start_date as date)               as promotion_start_date,
    cast(end_date as date)                 as promotion_end_date,
    cast(discount_rate as numeric(10, 4))  as discount_rate,
    is_holiday::boolean                    as is_holiday
from {{ source('raw', 'promotions') }}