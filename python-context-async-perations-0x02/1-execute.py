import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        print("Opening DB connection...")
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()

        # Executing the query
        cursor.execute(self.query, self.params)

        # Storing the results
        self.results = cursor.fetchall()

        # Returning results to the with-block
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing the connection...")
        if self.conn:
            self.conn.close()

        # no suppressing errors
        return False


query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("example.db", query, params) as results:
    print("Query results:")
    for row in results:
        print(row)
