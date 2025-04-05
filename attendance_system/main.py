from attendance_system.enrollment import EnrollmentSystem
from attendance_system.attendance import AttendanceSystem
from attendance_system.view import ViewAttendance
from attendance_system.delete import DeleteRecords
from attendance_system.view_students import ViewStudents
from arduino.arduino_communication import ArduinoCommunication


def main():
    # Set up Arduino communication
    arduino_communicator = ArduinoCommunication()

    # Connect to the Arduino (auto detects the port)
    arduino = arduino_communicator.connect()
    if arduino is None:
        print("Error: Could not connect to Arduino. Exiting.")
        return

    # Set up the database
    db_path = 'database/attendance.db'
    delete_records = DeleteRecords(db_path)
    enroll_student = EnrollmentSystem(db_path)
    mark_attendance = AttendanceSystem(db_path)
    view_students = ViewStudents(db_path)
    view_records = ViewAttendance(db_path)

    while True:
        print("\nOptions:")
        print("1 - Enroll New Student")
        print("2 - Mark Attendance")
        print("3 - View Attendance Records")
        print("4 - View Student Records")
        print("5 - Delete All Records")
        print("6 - Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            enroll_student.enroll_student()
        elif choice == '2':
            mark_attendance.mark_attendance()  # Adjust method call
        elif choice == '3':
            view_records.view_attendance()
        elif choice == '4':
            view_students.view_students()
        elif choice == '5':
            delete_records.delete_all_records()
        elif choice == '6':
            print("Exiting system.")
            break
        else:
            print("Invalid option! Please try again.")

    # Close the Arduino connection before exiting
    arduino_communicator.close_connection()
    delete_records.close()

if __name__ == "__main__":
    main()
