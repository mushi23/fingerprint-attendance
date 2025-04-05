import serial
import time
from serial.tools import list_ports

class ArduinoCommunication:
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self.port = None
        self.arduino = None

    def find_arduino_port(self):
        """Automatically detect the Arduino's serial port."""
        ports = list_ports.comports()
        for port in ports:
            if 'Arduino' in port.description or 'usbmodem' in port.device or 'usbserial' in port.device:
                print(f"Detected Arduino on {port.device}")
                self.port = port.device
                return self.port
        print("No Arduino detected. Please check your connection.")
        return None

    def connect(self):
        """Connect to the Arduino at the detected port."""
        if not self.find_arduino_port():
            raise ConnectionError("No Arduino detected. Please check your connection.")

        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print("Arduino connected successfully.")
        except serial.SerialException as e:
            raise ConnectionError(f"Error connecting to Arduino: {e}")
        return self.arduino

    def read_fingerprint_data(self):
        """Read fingerprint data from the Arduino."""
        if self.arduino and self.arduino.in_waiting > 0:
            data = self.arduino.readline().decode('utf-8').strip()
            if data.startswith("Fingerprint ID:"):
                return int(data.split(":")[1].strip())
        return None

    def close_connection(self):
        """Close the Arduino connection."""
        if self.arduino:
            self.arduino.close()
            print("Arduino connection closed.")



