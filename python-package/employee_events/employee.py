# Import the QueryBase class
from employee_events.query_base import QueryBase

# Import dependencies needed for sql execution
from .sql_execution import execute_sql, execute_sql_df


# Define a subclass of QueryBase called Employee
class Employee(QueryBase):

    # Set the class attribute `name`
    name = "employee"

    # Define a method called `names`
    # that receives no arguments
    def names(self):
        # Query 3
        # Select employee's full name and id
        query = """
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee;
        """
        return execute_sql(query)

    # Define a method called `username`
    # that receives an `id` argument
    def username(self, id):
        # Query 4
        # Select the full name of the employee with given id
        query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id};
        """
        return execute_sql(query)

    # Method with an SQL query for ML model
    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id};
        """
        # return as pandas dataframe
        return execute_sql_df(query)
