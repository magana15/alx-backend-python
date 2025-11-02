#!/usr/bin/env python3

import os
import csv
import uuid
from decimal import Decimal, InvalidOperation
import mysql.connector
from mysql.connector import errorcode

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MY if it does not exist.
    """
    create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET 'utf8mb4'"
    cursor = connection.cursor()
    try:
        cursor.execute(create_db_sql)
        connection.commit()
        print(f"Database `{DB_NAME}` ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database {DB_NAME}: {err}")
        raise
    finally:
        cursor.close()

def connect_to_prodev():
    """
    Connects to the database and returns the connection.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DB_NAME,
            autocommit=False
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to database", DB_NAME, ":", err)
        raise

def create_table(connection):
    """
    Creates table user_data with fields:
      - user_id (CHAR(36), PRIMARY KEY)
      - name (VARCHAR(255), NOT NULL)
      - email (VARCHAR(255), NOT NULL)
      - age (DECIMAL(5,2), NOT NULL)
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
        user_id CHAR(36) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        PRIMARY KEY (user_id),
        INDEX idx_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print(f"Table `{TABLE_NAME}` ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating table {TABLE_NAME}: {err}")
        raise
    finally:
        cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        
        user_id = data.get("user_id") or str(uuid.uuid4())
        user_id = user_id.strip()
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        age_val = data.get("age")

        if not name or not email:
            raise ValueError("name and email are required fields")

        try:
            # Accept numeric strings or numbers
            age = Decimal(str(age_val)).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError):
            raise ValueError(f"Invalid age value: {age_val}")

        # Check existence by user_id first
        cursor.execute(f"SELECT 1 FROM `{TABLE_NAME}` WHERE user_id = %s LIMIT 1", (user_id,))
        if cursor.fetchone():
            # Already exists by user_id
            return False

        # Check existence by email (avoid duplicate records)
        cursor.execute(f"SELECT 1 FROM `{TABLE_NAME}` WHERE email = %s LIMIT 1", (email,))
        if cursor.fetchone():
            # Already exists by email
            return False

        insert_sql = f"""
        INSERT INTO `{TABLE_NAME}` (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (user_id, name, email, str(age)))
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

# ----------generator ----------
def stream_user_rows(connection, batch_size=1000):
    
    cursor = connection.cursor(dictionary=True)  
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM `{TABLE_NAME}`")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            
            yield row
    finally:
        cursor.close()

# ---------- Utility to load CSV and insert ----------
def load_csv_and_insert(connection, csv_path=CSV_FILE):
    inserted = 0
    skipped = 0

    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        # normalize headers to lower-case keys
        for raw_row in reader:
            row = {k.strip(): v.strip() for k, v in raw_row.items() if k is not None}
            # Accept both lower and upper keys
            mapped = {
                "user_id": row.get("user_id") or row.get("id") or None,
                "name": row.get("name") or row.get("full_name") or None,
                "email": row.get("email") or row.get("e-mail") or None,
                "age": row.get("age") or row.get("Age") or None
            }
            try:
                ok = insert_data(connection, mapped)
                if ok:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"Error inserting row {mapped}: {e}")
                skipped += 1

    return inserted, skipped

# ---------- Main script ----------
def main():
    print("Connecting to MySQL server...")
    server_conn = connect_db()
    try:
        create_database(server_conn)
    finally:
        server_conn.close()

    print(f"Connecting to database `{DB_NAME}`...")
    db_conn = connect_to_prodev()
    try:
        create_table(db_conn)

        # Load CSV and insert data
        if os.path.exists(CSV_FILE):
            print(f"Loading CSV data from {CSV_FILE} ...")
            inserted, skipped = load_csv_and_insert(db_conn, CSV_FILE)
            print(f"Insert complete. Inserted: {inserted}. Skipped: {skipped}.")
        else:
            print(f"CSV file {CSV_FILE} not found. Skipping data load.")

        # Demonstrate streaming generator (prints first 5 rows)
        print("\nDemonstrating streaming generator (first 5 rows):")
        cnt = 0
        for row in stream_user_rows(db_conn):
            print(row)
            cnt += 1
            if cnt >= 5:
                break

    finally:
        db_conn.close()
        print("Done.")

if __name__ == "__main__":
    main()

