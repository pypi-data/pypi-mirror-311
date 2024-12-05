from asyncio import sleep
from ufactory_sila2_server import Client
from ufactory_sila2_server.generated.ufcontroller import MoveJoints_Responses

# Discover and connect to the uFactory SiLA2 Server
client = Client.discover()
print("Connected to uFactory SiLA2 server")

# Define the target location for the arm (joint angles)
pos1 = [5.700013, 62.800013, 129.999998, 0.0, 67.199985, 7.599999]
pos2 = [3.900009, 102.900011, 204.60002, 0.0, 101.700009, 3.000007]
pos3 = [-50.900024, 102.900011, 204.60002, 0.0, 101.700009, 35.400025]
pos4 = [-55.099976, 75.999987, 152.199993, 0.0, 76.200006, 33.700002]
pos5 = [-55.399977, 76.700027, 149.700006, 0.0, 72.99998, 33.799984]
pos5_5 =[-54.814185, 90.196563, 173.861808, -2.153347, 83.477774, 34.24437,]

pos6 = [-55.399977, 87.199994, 173.900025, -0.0, 86.699974, 32.899981, 0.0]
pos7 =[-51.600006, 108.199986, 220.5, 0.0, 112.300014, 37.099991, 0.0]
pos8 =[20.499972, 102.999993, 199.800009, 0.0, 96.800016, 22.700015, 0.0]
pos9 =[19.799989, 125.599969, 216.80001, 0.0, 91.199984, 22.899977, 0.0]   
pos10 = [19.42579, 128.028966, 214.598134, -0.351567, 87.670908, 19.742407, 0.0]
pos10_5 =[20.439639, 131.129069, 219.176353, -2.416965, 87.2452, 20.126976]

# Move the arm to the specified location
# response: MoveJoints_Responses = client.UFController.MoveJoints(JointAngles=location1)
# print(f"Arm moved to angles: {response.JointAngles}")
# client.UFController.MoveJoints(pos9)

def go_into_opentron():
    client.UFController.MoveJoints(JointAngles=pos1)
    client.UFController.MoveJoints(JointAngles=pos2)
    client.UFController.MoveJoints(JointAngles=pos3)
    client.UFController.MoveJoints(JointAngles=pos4)
    client.UFController.MoveJoints(JointAngles=pos5)

def go_out_to_plate():
    client.UFController.MoveJoints(JointAngles=pos6)
    client.UFController.MoveJoints(JointAngles=pos7)
    client.UFController.MoveJoints(JointAngles=pos8)
    client.UFController.MoveJoints(JointAngles=pos9)
    client.UFController.MoveJoints(JointAngles=pos10_5)

def reverse_gotoplate():
    client.UFController.MoveJoints(JointAngles=pos10_5)
    client.UFController.MoveJoints(JointAngles=pos9)
    client.UFController.MoveJoints(JointAngles=pos8)
    client.UFController.MoveJoints(JointAngles=pos7)
    client.UFController.MoveJoints(JointAngles=pos6)
    client.UFController.MoveJoints(JointAngles=pos5_5)
    

go_into_opentron()
client.UFController.CloseGripper()

for x in range(0,9):
    go_out_to_plate()

    client.UFController.OpenGripper()

    client.UFController.MoveJoints(JointAngles=pos9)
    client.UFController.MoveJoints(JointAngles=pos10_5)

    client.UFController.CloseGripper()

    client.UFController.MoveJoints(JointAngles=pos9)

    reverse_gotoplate()
    
    client.UFController.OpenGripper()

    client.UFController.MoveJoints(JointAngles=pos4)
    client.UFController.MoveJoints(JointAngles=pos5)

    client.UFController.CloseGripper()





