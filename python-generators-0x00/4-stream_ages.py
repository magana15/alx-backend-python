#!/usr/bin/env python3
import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one
    from the user_data table.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT age FROM user_data")

    # ---- LOOP 1 (allowed) ----
    for (age,) in cursor:
        yield float(age)

    cursor.close()
    conn.close()


def compute_average_age():
    """
    Uses the generator to calculate average age
    WITHOUT loading all rows into memory.
    """
    total = 0
    count = 0

    # ---- LOOP 2 (allowed) ----
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total / count
        print(f"Average age of users: {average}")


# Run the calculation
compute_average_age()
