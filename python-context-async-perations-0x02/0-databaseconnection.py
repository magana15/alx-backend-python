import sqlite3

class DatabaseConnection:
	def __init__(self, db_name):
		self.db_name = db_name
		self.conn = None

	def __enter__(self):
		print("Connecting the database")
		self.conn = sqlite3.connect(self.db_name)
		return self.conn

	def __exit__(self,exc_type, exc_value, traceback):
		if self.conn:
			print("Closing the database connection...")
			self.conn.close()
		return False


with DatabaseConnection("michezo.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("Users:")
    for row in rows:
        print(row)

