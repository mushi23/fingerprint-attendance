import sqlite3

class ViewStudents:
    def __init__(self, db_path='database/attendance.db'):
        """Initialize the SQLite database connection."""
        self.db_path = db_path

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def view_students(self):
        """Fetch and display all students."""
        print("Viewing student records...")

        # Retrieve student records
        self.cursor.execute('SELECT * FROM students')
        rows = self.cursor.fetchall()

        # Display the student records
        print("ID | Name | Admission No | Fingerprint ID")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    def close(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")

