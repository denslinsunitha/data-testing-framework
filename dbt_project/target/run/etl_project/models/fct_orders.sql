
  
    
    
    create  table main."fct_orders"
    as
        select
  cast(order_id as integer) as order_id,
  cast(customer_id as integer) as customer_id,
  cast(amount as numeric) as amount,
  date(order_date) as order_date,
  strftime('%Y', date(order_date)) as order_year,
  strftime('%m', date(order_date)) as order_month
from main."raw_orders"
where amount is not null

  