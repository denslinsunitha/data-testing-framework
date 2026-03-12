import sqlite3
import os

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'etl_test.sqlite3')
    return sqlite3.connect(db_path)