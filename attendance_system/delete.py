import sqlite3

class DeleteRecords:
    def __init__(self, db_path='database/attendance.db'):
        """Initialize the SQLite database connection."""
        self.db_path = db_path

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def delete_all_records(self):
        """Delete all records from students and attendance tables."""
        print("Deleting all records...")

        # Delete all attendance records first to maintain referential integrity
        self.cursor.execute('DELETE FROM attendance')
        print("All attendance records deleted.")

        # Then delete all student records
        self.cursor.execute('DELETE FROM students')
        print("All student records deleted.")

        self.conn.commit()
        print("All records deleted successfully!")

    def close(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")

