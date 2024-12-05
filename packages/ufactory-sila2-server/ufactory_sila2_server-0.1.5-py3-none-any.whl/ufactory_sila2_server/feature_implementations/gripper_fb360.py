import serial
import time

# Set up the serial connection
SERIAL_PORT = 'COM5'  # Replace with your Arduino's port
BAUD_RATE = 9600

# Mapping of integer values to state names
STATE_MAP = {
    0: "CLOSED",
    1: "CLOSING",
    2: "OPENED",
    3: "OPENING",
    4: "HOLDING"
}

try:
    # Initialize the serial connection
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT} at {BAUD_RATE} baud.")
    time.sleep(2)  # Wait for Arduino to reset and be ready
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit(1)

def send_command(command):
    """
    Send a command to the Arduino and print the response.
    """
    try:
        arduino.write(command.encode())  # Send command as a single byte
        print(f"Command '{command}' sent.")
        time.sleep(0.1)  # Allow time for Arduino to process
        # Read and print the response
        response = arduino.readline().decode('utf-8').strip()
        if response:
            print(f"Arduino response: {response}")
    except Exception as e:
        print(f"Error sending command: {e}")

def get_feedback():
    """
    Request the feedback value from the Arduino and return it.
    """
    try:
        arduino.write(b'f')  # Send 'f' to request feedback
        time.sleep(0.1)  # Allow time for Arduino to process
        response = arduino.readline().decode('utf-8').strip()
        if response.isdigit():  # Ensure the response is a valid number
            feedback_value = int(response)
            print(f"Feedback value received: {feedback_value}")
            return feedback_value
        else:
            print(f"Invalid feedback received: {response}")
            return None
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return None
    
def get_state():
    """
    Request the current gripper state from the Arduino and return it as a string.
    """
    try:
        arduino.write(b's')  # Send 's' to request the current state
        time.sleep(0.1)  # Allow time for Arduino to process
        response = arduino.readline().decode('utf-8').strip()
        if response.isdigit():  # Ensure the response is a valid integer
            state_int = int(response)
            # Map the integer to a state name using the dictionary
            state_name = STATE_MAP.get(state_int, "UNKNOWN")
            print(f"Current gripper state: {state_name}")
            return state_name
        else:
            print(f"Invalid response received: {response}")
            return "UNKNOWN"
    except Exception as e:
        print(f"Error retrieving state: {e}")
        return "UNKNOWN"


def main():
    print("Commands: 'o' to open, 'c' to close, 'f' to get feedback, 's' to get state, 'q' to quit.")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == 'q':  # Quit the program
            print("Exiting program.")
            break
        elif command in ['o', 'c']:  # Valid commands
            send_command(command)
        elif command == 'f':  # Request feedback value
            feedback = get_feedback()
            # if feedback is not None:
            #     print(f"Current feedback value: {feedback}")
        elif command == 's':  # Request gripper state
            state = get_state()
            # if state:
            #     print(f"Gripper is currently in state: {state}")
        else:
            print("Invalid command. Please use 'o', 'c', 'f', 's', or 'q'.")

    # Close the serial connection
    arduino.close()
    print("Serial connection closed.")

if __name__ == "__main__":
    main()
