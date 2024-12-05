import serial
import time

# Replace 'COM7' with the actual port where your Arduino is connected
arduino_port = 'COM8'
baud_rate = 9600

try:
    # Initialize the serial connection
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the Arduino to initialize
    print("Connected to Arduino on port", arduino_port)

    # Function to send a command to Arduino
    def control_gripper(command):
        if command.upper() in ["OPEN", "CLOSE"]:
            ser.write(f"{command.upper()}\n".encode())
            print(f"Command sent: {command}")
        else:
            print("Invalid command. Use 'OPEN' or 'CLOSE'.")

    # Interactive command loop
    while True:
        command = input("Enter command ('OPEN', 'CLOSE', or 'EXIT' to quit): ")
        if command.upper() == "EXIT":
            print("Exiting...")
            break
        control_gripper(command)
        time.sleep(1)  # Short delay to allow the command to process

    # Close the serial connection
    ser.close()
    print("Serial connection closed.")

except serial.SerialException as e:
    print(f"Error: Could not open port {arduino_port}. {e}")
