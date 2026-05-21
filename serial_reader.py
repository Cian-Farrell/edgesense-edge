import serial
import time

# Configure serial connection to Arduino
SERIAL_PORT = 'COM3'  # This may need to change depending on your Arduino port
BAUD_RATE = 9600

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Arduino on {SERIAL_PORT}")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Received: {line}")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")

if __name__ == "__main__":
    read_serial()