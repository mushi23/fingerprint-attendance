import sqlite3
import datetime
import time
from arduino.arduino_communication import ArduinoCommunication

class AttendanceSystem:
    def __init__(self, db_path='database/attendance.db'):
        """Initialize the database and Arduino connection."""
        self.db_path = db_path
        self.arduino = ArduinoCommunication()

        # Connect to Arduino
        self.arduino.connect()

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Ensure attendance table exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')
        self.conn.commit()

    def mark_attendance(self):
        """Mark attendance by scanning the fingerprint and updating the database."""
        print("Marking attendance...")

        # Wait for fingerprint scan with timeout
        start_time = time.time()
        fingerprint_id = None
        fingerprint_scanned = False  # To track if a fingerprint has been scanned successfully
        while not fingerprint_scanned:
            fingerprint_id = self.arduino.read_fingerprint_data()
            if fingerprint_id:
                print(f"Received fingerprint ID: {fingerprint_id}")
                fingerprint_scanned = True
            elif time.time() - start_time > 30:  # Timeout after 30 seconds
                print("Timeout! No fingerprint detected.")
                return
            # No need to keep printing "Waiting for valid fingerprint..."
            time.sleep(1)  # Wait a bit before trying again to reduce unnecessary load

        # Check if the fingerprint ID exists in the student database
        self.cursor.execute('SELECT * FROM students WHERE fingerprint_id = ?', (fingerprint_id,))
        student = self.cursor.fetchone()

        if student:
            # Check if attendance has already been marked today
            self.cursor.execute('''
                SELECT * FROM attendance WHERE student_id = ? AND date LIKE ?
            ''', (student[0], datetime.datetime.now().strftime('%Y-%m-%d') + '%'))

            if self.cursor.fetchone():
                print(f"Attendance for {student[1]} (Admission No: {student[2]}) has already been marked today.")
                return

            # Record the attendance with a timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
                INSERT INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
            ''', (student[0], timestamp, 'PRESENT'))
            self.conn.commit()
            print(f"Attendance marked for {student[1]} (Admission No: {student[2]}) at {timestamp}")
        else:
            print("Fingerprint not recognized. Please try again.")

    def close(self):
        """Close the database and Arduino connection."""
        self.conn.close()
        self.arduino.close_connection()
        print("Connections closed.")

