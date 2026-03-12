Feature: Validate dim customer data

 
Background: Validate distinct set
  Given a sqlite datasource "etl_test"
  And a table asset "customer data" for table "dim_customers"
  And a whole-table batch definition named "dim_customers"
  And I load a batch

  Scenario: Schema should be correct
    Then the table columns should match ordered list "customer_id,customer_name,email,signup_date,signup_year,signup_month,signup_quarter,email_domain"

  Scenario: Row count should be within expected bounds
    Then the row count should be between 1 and 10000000

  Scenario: customer_id should be valid primary key
    Then column "customer_id" should not be null
    And column "customer_id" should be unique
    And column "customer_id" values should be between 1 and null

  Scenario: customer_name should be populated and well-formed
    Then column "customer_name" should not be null
    And column "customer_name" should not match regex "^\s*$"
    And column "customer_name" length should be between 3 and 100

  Scenario: email should be valid and clean
    Then column "email" should not be null
    And column "email" should not match regex "\s"
    And column "email" should match regex "^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"

  Scenario: signup_year should be present and within range
    Then column "signup_year" should not be null
    And column "signup_year" values should be between 1990 and 2027

















