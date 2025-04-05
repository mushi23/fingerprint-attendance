import sqlite3

class ViewAttendance:
    def __init__(self, db_path='database/attendance.db'):
        """Initialize the SQLite database connection."""
        self.db_path = db_path

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def view_attendance(self):
        """Fetch and display all attendance records."""
        print("Viewing attendance records...")

        # Retrieve attendance records along with student details
        self.cursor.execute('''
            SELECT students.name, students.admission_number, attendance.date, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
        ''')
        rows = self.cursor.fetchall()

        # Display the attendance records
        print("Name | Admission No | Date | Status")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    def close(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")

