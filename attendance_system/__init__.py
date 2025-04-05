# Initialize the attendance system package

# Import the main components for easy access
from .enrollment import EnrollmentSystem
from .attendance import AttendanceSystem
from .view import ViewAttendance
from .delete import DeleteRecords
from arduino.arduino_communication import ArduinoCommunication

# Initialize the package with some useful attributes
__version__ = "1.0"
__author__ = "Mushi.RR"

