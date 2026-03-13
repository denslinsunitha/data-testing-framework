# Data Testing Framework

A comprehensive data testing framework that combines DBT (Data Build Tool) for data transformations with Behave for behavior-driven testing and Allure for test reporting.

## Project Overview

This project provides a complete data testing pipeline that:
- Loads sample data into a SQLite database
- Transforms data using DBT models
- Validates data quality using behavior-driven tests
- Generates comprehensive test reports with Allure

## Project Structure

```
data-testing-framework/
├── dbt_project/              # DBT project configuration and models
│   ├── dbt_project.yml       # DBT project configuration
│   ├── models/               # DBT transformation models
│   │   ├── dim_customers.sql
│   │   ├── fct_orders.sql
│   │   └── source.yml
│   └── tests/                # DBT schema tests
│       └── schema.yml
├── features/                 # Behave feature files and step definitions
│   ├── customer_data_validations.feature
│   ├── fact_orders_validations.feature
│   ├── environment.py
│   └── steps/
│       └── validations_steps.py
├── scripts/                  # Utility scripts
│   └── load_sample_data.py   # Script to load test data
├── test_data/               # Sample CSV data files
│   ├── raw_customers.csv
│   └── raw_orders.csv
├── utils/                   # Utility modules
│   ├── data_loader.py
│   └── db_connection.py
├── reports/                 # Generated test reports
│   └── ge/                  # Great Expectations reports
├── requirements.txt         # Python dependencies
├── behave.ini              # Behave configuration
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Allure CLI (for report generation)

### Installing Allure

**macOS (using Homebrew):**
```bash
brew install allure
```

**Linux/Windows:**
Download from [Allure releases](https://github.com/allure-framework/allure2/releases) and add to PATH.

## Setup Instructions

### 1. Install Packages

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv-dbt
source venv-dbt/bin/activate
pip install -r requirements.txt
```

### 2. Load Test Data

Load the sample data into the SQLite database:

```bash
python scripts/load_sample_data.py
```

This script will:
- Read CSV files from `test_data/` directory
- Create SQLite tables (`raw_customers` and `raw_orders`)
- Load the data into the database

### 3. Run DBT

Execute DBT transformations to create dimension and fact tables:

Update the schema_directory and main path in the `project.yml`

```bash
main=/absolute/path/to/etl_test.sqlite3
schema_directory=/absolute/path/to/your/project
```

And then run the following command:

```bash
dbt run --profile my_project_profile --target dev
```

This will:
- Transform raw data into analytical models
- Create `dim_customers` and `fct_orders` tables
- Apply any configured tests

### 4. Run Behave Tests

Execute the behavior-driven tests:

```bash
behave
```

This runs all feature files in the `features/` directory and validates:
- Data quality checks
- Business rule validations
- Schema validations

### 5. Generate Test Reports

Generate and view Allure reports:

```bash
# Generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Open report in browser
allure open reports/allure-report
```
<img width="1728" height="805" alt="Screenshot 2026-03-12 at 19 13 25" src="https://github.com/user-attachments/assets/579abc22-4592-4747-99c8-73d672933a93" />

<img width="1728" height="896" alt="Screenshot 2026-03-12 at 19 14 17" src="https://github.com/user-attachments/assets/e76a8dbe-467a-429b-848b-29cf0baf8cc7" />


## Key Components

### DBT Models
- **dim_customers.sql**: Customer dimension table
- **fct_orders.sql**: Orders fact table
- **source.yml**: Source table definitions

### Test Features
- **customer_data_validations.feature**: Customer data quality tests
- **fact_orders_validations.feature**: Orders data validation tests

### Dependencies
- **behave**: BDD testing framework
- **dbt-core**: Data transformation tool
- **dbt-sqlite**: SQLite adapter for DBT
- **great-expectations**: Data validation library
- **allure-behave**: Allure reporting for Behave
- **pandas**: Data manipulation library
- **sqlalchemy**: Database toolkit

## Configuration

### DBT Profile
The project uses the profile name `my_project_profile` with target `dev`. Ensure your DBT profiles are configured accordingly.

### Behave Configuration
Behave settings are defined in `behave.ini` with output capture disabled for better debugging.

## Troubleshooting

### Common Issues

1. **Virtual environment not activated**
   ```bash
   source venv-dbt/bin/activate
   ```

2. **DBT profile not found**
   - Ensure DBT profiles are properly configured
   - Check `~/.dbt/profiles.yml`

3. **Allure command not found**
   - Install Allure CLI as described in prerequisites
   - Ensure Allure is in your system PATH

4. **Database connection issues**
   - Verify SQLite database is created after running step 2
   - Check database connection settings in `utils/db_connection.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the full test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
