from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd
import os

# Path to database
db_path = Path(__file__).parent / "employee_events.db"

# OPTION 1: MIXIN
class QueryMixin:
    
    def pandas_query(self, sql_query: str):
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=columns)
    
    def query(self, sql_query: str):
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            return cursor.fetchall()

 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query

def execute_sql(query: str):
    """Execute a SQL query and return a list of tuples"""
    connection = connect(db_path)
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result


def execute_sql_df(query: str):
    """Execute a SQL query and return a pandas DataFrame"""
    connection = connect(db_path)
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df
