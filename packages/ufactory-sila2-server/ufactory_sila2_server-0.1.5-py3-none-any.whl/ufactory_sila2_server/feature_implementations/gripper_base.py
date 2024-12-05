import serial
import time

class ArduinoGripper:
    STATE_MAP = {
        0: "CLOSED",
        1: "CLOSING",
        2: "OPENED",
        3: "OPENING",
        4: "HOLDING"
    }

    def __init__(self, port='COM5', baud_rate=9600, timeout=1):
        """
        Initialize the ArduinoGripper class by setting up the serial connection.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.arduino = None

        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=timeout)
            print(f"Connected to Arduino on {port} at {baud_rate} baud.")
            time.sleep(2)  # Wait for Arduino to reset
        except Exception as e:
            print(f"Error connecting to Arduino: {e}")
            exit(1)

    def send_command(self, command):
        """
        Send a command to the Arduino and print the response.
        """
        try:
            self.arduino.write(command.encode())
            print(f"Command '{command}' sent.")
            time.sleep(0.1)  # Allow time for Arduino to process
            response = self.arduino.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino response: {response}")
        except Exception as e:
            print(f"Error sending command: {e}")

    def get_feedback(self):
        """
        Request the feedback value from the Arduino and return it.
        """
        try:
            self.arduino.write(b'f')  # Send 'f' to request feedback
            time.sleep(0.1)
            response = self.arduino.readline().decode('utf-8').strip()
            if response.isdigit():
                feedback_value = int(response)
                print(f"Feedback value received: {feedback_value}")
                return feedback_value
            else:
                print(f"Invalid feedback received: {response}")
                return None
        except Exception as e:
            print(f"Error retrieving feedback: {e}")
            return None

    def get_state(self):
        """
        Request the current gripper state from the Arduino and return it as a string.
        """
        try:
            self.arduino.write(b's')  # Send 's' to request the current state
            time.sleep(0.1)
            response = self.arduino.readline().decode('utf-8').strip()
            if response.isdigit():
                state_int = int(response)
                state_name = self.STATE_MAP.get(state_int, "UNKNOWN")
                print(f"Current gripper state: {state_name}")
                return state_name
            else:
                print(f"Invalid response received: {response}")
                return "UNKNOWN"
        except Exception as e:
            print(f"Error retrieving state: {e}")
            return "UNKNOWN"

    def close(self):
        """
        Close the serial connection.
        """
        if self.arduino:
            self.arduino.close()
            print("Serial connection closed.")


def main():
    gripper = ArduinoGripper()

    print("Commands: 'o' to open, 'c' to close, 'f' to get feedback, 's' to get state, 'q' to quit.")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == 'q':
            print("Exiting program.")
            break
        elif command in ['o', 'c']:
            gripper.send_command(command)
        elif command == 'f':
            gripper.get_feedback()
        elif command == 's':
            gripper.get_state()
        else:
            print("Invalid command. Please use 'o', 'c', 'f', 's', or 'q'.")

    gripper.close()


if __name__ == "__main__":
    main()
