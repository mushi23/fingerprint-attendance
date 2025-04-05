import sqlite3
import time
from arduino.arduino_communication import ArduinoCommunication

class EnrollmentSystem:
    def __init__(self, db_path='database/attendance.db'):
        """Initialize the database and Arduino connection."""
        self.db_path = db_path
        self.arduino = ArduinoCommunication()

        # Connect to Arduino
        self.arduino.connect()

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create the students table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                admission_number TEXT NOT NULL UNIQUE,
                fingerprint_id INTEGER NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    def enroll_student(self):
        """Enroll a new student by adding their details and fingerprint ID to the database."""
        print("Enrolling new student...")

        # Collect student details
        name = input("Enter student's name: ")
        admission_number = input("Enter student's admission number: ")

        # Check if admission number already exists
        self.cursor.execute('SELECT * FROM students WHERE admission_number = ?', (admission_number,))
        existing_student = self.cursor.fetchone()
        if existing_student:
            print(f"Student with admission number {admission_number} already exists!")
            return

        # Wait for fingerprint data from Arduino
        print("Place your finger on the sensor...")
        fingerprint_id = None
        start_time = time.time()

        while fingerprint_id is None:
            data = self.arduino.read_fingerprint_data()
            if data:
                fingerprint_id = data
                print(f"Fingerprint enrolled with ID: {fingerprint_id}")
            elif time.time() - start_time > 30:  # Timeout after 30 seconds
                print("Timeout! No fingerprint data received.")
                return

        # Check if fingerprint ID already exists in database
        self.cursor.execute('SELECT * FROM students WHERE fingerprint_id = ?', (fingerprint_id,))
        if self.cursor.fetchone():
            print(f"Fingerprint ID {fingerprint_id} already exists in the database!")
            return  # Don't overwrite, ask to enroll again

        # Store the fingerprint ID and student info in the database
        try:
            self.cursor.execute('''
                INSERT INTO students (name, admission_number, fingerprint_id)
                VALUES (?, ?, ?)
            ''', (name, admission_number, fingerprint_id))
            self.conn.commit()
            print(f"Student {name} enrolled successfully with Fingerprint ID {fingerprint_id}!")
        except sqlite3.DatabaseError as e:
            print(f"Error storing student data in the database: {e}")
            self.conn.rollback()

    def close(self):
        """Close the database and Arduino connection."""
        try:
            self.conn.close()
            self.arduino.close_connection()
            print("Connections closed successfully.")
        except Exception as e:
            print(f"Error closing connections: {e}")

if __name__ == "__main__":
    enrollment_system = EnrollmentSystem()

    try:
        # Call the enroll student method to start enrollment
        enrollment_system.enroll_student()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed after the enrollment process
        enrollment_system.close()

