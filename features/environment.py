# features/environment.py
import great_expectations as gx

def before_all(context):
    # Behave runtime context != Great Expectations context
    context.ge_context = gx.get_context()

def after_scenario(context, scenario):
    # Optional: if you want to clean scenario variables
    for attr in ["data_source", "data_asset", "batch_definition", "batch", "validation_result"]:
        if hasattr(context, attr):
            delattr(context, attr)