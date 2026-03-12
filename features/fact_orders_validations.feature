Feature: Validate fact orders data

Background: Validate distinct set
  Given a sqlite datasource "etl_test"
  And a table asset "orders data" for table "fct_orders"
  And a whole-table batch definition named "fct_orders"
  And I load a batch

Scenario: Schema should be correct
  Then the table columns should match ordered list "order_id,customer_id,amount,order_date,order_year,order_month"

Scenario: Row count should be within expected bounds
  Then the row count should be between 1 and 10000000

Scenario: order_id should be valid primary key
  Then column "order_id" should not be null
  And column "order_id" should be unique
  And column "order_id" values should be between 1 and null

Scenario: customer_id should be present
  Then column "customer_id" should not be null
  And column "customer_id" values should be between 1 and null

Scenario: amount should be present and valid
  Then column "amount" should not be null
  And column "amount" values should be between 1 and null

Scenario: order_date should be populated and well-formed
  Then column "order_date" should not be null
  And column "order_date" should match regex "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

Scenario: customer_id should reference an existing customer (FK)
  Then column "customer_id" values should exist in table "dim_customers" column "customer_id"