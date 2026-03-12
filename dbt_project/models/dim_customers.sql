with base as (
  select
    id as customer_id,
    trim(name) as customer_name,
    lower(trim(email)) as email,
    date(signup_date) as signup_date
  from {{ source('raw', 'raw_customers') }}
),
enriched as (
  select
    customer_id,
    customer_name,
    email,
    signup_date,
    strftime('%Y', signup_date) as signup_year,
    strftime('%m', signup_date) as signup_month,
    -- quarter in SQLite-style (works in many engines with small edits)
    cast(((cast(strftime('%m', signup_date) as integer)-1)/3)+1 as integer) as signup_quarter,
    substr(email, instr(email, '@')+1) as email_domain
  from base
)
select * from enriched
