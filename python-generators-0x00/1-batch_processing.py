#!/usr/bin/env python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Yields a list (batch) of rows.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    batch = []  # container for each batch

    # ---- LOOP 1 (allowed) ----
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []  # reset for next batch

    # yield leftover batch
    if batch:
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Processes each batch and yields users over age 25.
    """
    # ---- LOOP 2 (allowed) ----
    for batch in stream_users_in_batches(batch_size):

        filtered_batch = []

        # ---- LOOP 3 (allowed) ----
        for user in batch:
            if float(user["age"]) > 25:
                filtered_batch.append(user)

        # yield only users > 25
        yield filtered_batch

	if len(batch) < batch_size:
            # last page reached → stop generator
            return
