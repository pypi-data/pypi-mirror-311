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

pos1 = [5.700013, 62.800013, 129.999998, 0.0, 67.199985, 7.599999]
pos2 = [3.900009, 102.900011, 204.60002, 0.0, 101.700009, 3.000007]
pos3 = [-50.900024, 102.900011, 204.60002, 0.0, 101.700009, 35.400025]
pos4 = [-55.099976, 75.999987, 152.199993, 0.0, 76.200006, 33.700002]
pos5 = [-55.399977, 76.700027, 149.700006, 0.0, 72.99998, 33.799984]

pos6 = [-55.399977, 87.199994, 173.900025, -0.0, 86.699974, 32.899981, 0.0]
pos7 =[-51.600006, 108.199986, 220.5, 0.0, 112.300014, 37.099991, 0.0]
pos8 =[20.499972, 102.999993, 199.800009, 0.0, 96.800016, 22.700015, 0.0]
pos9 =[19.799989, 125.599969, 216.80001, 0.0, 91.199984, 22.899977, 0.0]   
pos10 = [19.42579, 128.028966, 214.598134, -0.351567, 87.670908, 19.742407, 0.0]


arm.set_servo_angle(angle=pos1,wait=True)
arm.set_servo_angle(angle=pos2,wait=True)
arm.set_servo_angle(angle=pos3,wait=True)
arm.set_servo_angle(angle=pos4,wait=True)
arm.set_servo_angle(angle=pos5,wait=True)

# grip

arm.set_servo_angle(angle=pos6,wait=True)
arm.set_servo_angle(angle=pos7,wait=True)
arm.set_servo_angle(angle=pos8,wait=True)
arm.set_servo_angle(angle=pos9,wait=True)
arm.set_servo_angle(angle=pos10,wait=True)

# release

arm.set_servo_angle(angle=pos9,wait=True)
arm.move_gohome()


