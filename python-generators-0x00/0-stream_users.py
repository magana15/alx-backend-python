#!/usr/bin/env python3
import mysql.connector

def stream_users():
    """
    Generator that streams rows from user_data table one by one.
    """
    # Connect to ALX_prodev database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    # Run SQL query
    cursor.execute("SELECT * FROM user_data")

    # --- Only ONE loop allowed ---
    for row in cursor:
        yield row   # give one row at a time

    cursor.close()
    conn.close()
