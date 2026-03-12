import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_connection import get_connection

conn = get_connection()

customers = pd.read_csv("test_data/raw_customers.csv")
orders = pd.read_csv("test_data/raw_orders.csv")

customers.to_sql("raw_customers", conn, if_exists="replace", index=False)
orders.to_sql("raw_orders", conn, if_exists="replace", index=False)

print("Data loaded successfully")