import sqlite3
import functools
from datetime import datetime
#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG] Executing SQL Query: {query} At {timestamp}")
        return func(query, *args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
