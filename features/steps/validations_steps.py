# features/steps/ge_steps.py
from behave import given, when, then
import great_expectations.expectations as gex
import great_expectations as gx
import json
import os
from pathlib import Path

@given('a sqlite datasource "{datasource_name}"')
def step_add_sqlite_datasource(context, datasource_name):
    connection_string = "sqlite:////Users/denrobin0/Documents/data_learning/interview_work/data-testing-framework/etl_test.sqlite3"
     # Create GE context once if not present (in case you didn't use environment.py)
    if not hasattr(context, "ge_context"):
        context.ge_context = gx.get_context()

    ge_context = context.ge_context

    # Reuse datasource if it already exists
    try:
        context.data_source = ge_context.data_sources.get(datasource_name)
    except Exception:
        context.data_source = ge_context.data_sources.add_sqlite(
            name=datasource_name,
            connection_string=connection_string
        )


@given('a table asset "{asset_name}" for table "{table_name}"')
def step_add_table_asset(context, asset_name, table_name):
    # Reuse existing asset if it already exists
    try:
        # GE Fluent datasources usually expose .get_asset(name=...)
        context.data_asset = context.data_source.get_asset(asset_name)
    except Exception:
        # Create only if missing
        context.data_asset = context.data_source.add_table_asset(
            name=asset_name,
            table_name=table_name
        )



@given('a whole-table batch definition named "{batch_def_name}"')
def step_add_whole_table_batch_def(context, batch_def_name):
    try:
        context.batch_definition = context.data_asset.get_batch_definition(batch_def_name)
    except Exception:
        context.batch_definition = context.data_asset.add_batch_definition_whole_table(
            name=batch_def_name
        )




@given("I load a batch")
def step_load_batch(context):
    context.batch = context.batch_definition.get_batch()


# -----------------------------
# Helper: validate expectation and store results
# -----------------------------

def _validate(context, expectation):
    result = context.batch.validate(expectation)

    if not hasattr(context, "validation_results"):
        context.validation_results = []

    context.validation_results.append(result)

    if not result["success"]:
        # Pretty-print GE failure info
        ge_details = json.dumps(result["result"], indent=2, default=str)
        raise AssertionError(
            f"Great Expectations validation failed:\n{ge_details}"
        )
    
    # Store the validation result in a JSON file for later inspection (optional)

    Path("reports/ge").mkdir(parents=True, exist_ok=True)

    with open(f"reports/ge/{expectation.__class__.__name__}.json", "w") as f:
        json.dump(result, f, indent=2, default=str)




# -----------------------------
# Then steps: schema + volume
# -----------------------------
@then('the table columns should match ordered list "{columns_csv}"')
def step_columns_match_order(context, columns_csv):
    columns = [c.strip() for c in columns_csv.split(",") if c.strip()]
    exp = gex.ExpectTableColumnsToMatchOrderedList(column_list=columns)
    _validate(context, exp)


@then("the row count should be between {min_rows:d} and {max_rows:d}")
def step_row_count_between(context, min_rows, max_rows):
    exp = gex.ExpectTableRowCountToBeBetween(min_value=min_rows, max_value=max_rows)
    _validate(context, exp)


# -----------------------------
# Then steps: column null / unique / range / length / regex
# -----------------------------
@then('column "{column_name}" should not be null')
def step_column_not_null(context, column_name):
    exp = gex.ExpectColumnValuesToNotBeNull(column=column_name)
    _validate(context, exp)


@then('column "{column_name}" should be unique')
def step_column_unique(context, column_name):
    exp = gex.ExpectColumnValuesToBeUnique(column=column_name)
    _validate(context, exp)


@then('column "{column_name}" values should be between {min_value} and {max_value}')
def step_column_between(context, column_name, min_value, max_value):
    # Allow "null" to represent no bound
    min_v = None if str(min_value).lower() == "null" else int(min_value)
    max_v = None if str(max_value).lower() == "null" else int(max_value)

    exp = gex.ExpectColumnValuesToBeBetween(
        column=column_name,
        min_value=min_v,
        max_value=max_v
    )
    _validate(context, exp)


@then('column "{column_name}" length should be between {min_len:d} and {max_len:d}')
def step_column_length_between(context, column_name, min_len, max_len):
    exp = gex.ExpectColumnValueLengthsToBeBetween(
        column=column_name,
        min_value=min_len,
        max_value=max_len
    )
    _validate(context, exp)


@then('column "{column_name}" should match regex "{regex}"')
def step_column_matches_regex(context, column_name, regex):
    exp = gex.ExpectColumnValuesToMatchRegex(column=column_name, regex=regex)
    _validate(context, exp)


@then('column "{column_name}" should not match regex "{regex}"')
def step_column_not_match_regex(context, column_name, regex):
    exp = gex.ExpectColumnValuesToNotMatchRegex(column=column_name, regex=regex)
    _validate(context, exp)

@then('column "{fk_column}" values should exist in table "{dim_table}" column "{dim_column}"')
def step_fk_exists(context, fk_column, dim_table, dim_column):
    
    conn = context.data_source.execution_engine.engine.raw_connection()
    cur = conn.cursor()
    cur.execute(f"select distinct {dim_column} from {dim_table}")
    allowed = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    exp = gex.ExpectColumnValuesToBeInSet(
        column=fk_column,
        value_set=allowed
    )
    _validate(context, exp)

