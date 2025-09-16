# Import any dependencies needed to execute sql queries
import pandas as pd
from sqlite3 import connect
from pathlib import Path
from .sql_execution import QueryMixin




# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase:
    
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""
    
    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # This will be overridden in subclasses
        return []
    

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        
        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set id column dynamically
        # order by the event_date column
        query = f"""
            SELECT event_date,
                   SUM(positive_events) AS total_positive,
                   SUM(negative_events) AS total_negative
            FROM {self.name}
            JOIN employee_events
                ON {self.name}.{self.name}_id = employee_events.{self.name}_id
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date;
            """
        return super().pandas_query(sql)
        

    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        
        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table for the correct entity type
        sql = f"""
        SELECT note_date, note
        FROM notes 
        JOIN {self.name}
            ON {self.name}.{self.name}_id = notes.{self.name}_id
        WHERE {self.name}.{self.name}_id = {id}
        ORDER BY note_date;
        """
        return super().pandas_query(sql)
        


