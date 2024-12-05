from xarm.wrapper import XArmAPI
import time

# Set the IP address of the xArm robot
arm_ip = '192.168.1.160'

# Create an instance of the XArmAPI
arm = XArmAPI(arm_ip)

# Connect to the arm
arm.connect()

# Enable motion on the arm
arm.motion_enable(enable=True)

# Set the mode to position control
arm.set_mode(0)

# Set the state to be ready to receive commands
arm.set_state(0)
arm.playback_trajectory
angles = arm.get_servo_angle()

print(angles)
# Move to another position

