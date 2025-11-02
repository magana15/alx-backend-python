#!/usr/bin/env python3
import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a single page of users starting at 'offset'
    and limited to 'page_size'.
    Returns a list of rows.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def lazy_paginate(page_size):
    """
    Lazily fetches pages one by one.
    Loads the next page ONLY when needed.
    Uses ONLY ONE loop.
    """
    offset = 0  # start at the beginning (page 0)

    # ---- ONLY ONE LOOP (REQUIRED) ----
    while True:
        page = paginate_users(page_size, offset)

        if not page:   # no more data
            break

        yield page     # give one page to the caller

        offset += page_size  # move to the next page
