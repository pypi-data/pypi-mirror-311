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
    client.UFController.MoveJoints(JointAngles=pos10)

def reverse_gotoplate():
    client.UFController.MoveJoints(JointAngles=pos10)
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
    client.UFController.MoveJoints(JointAngles=pos10)

    client.UFController.CloseGripper()

    client.UFController.MoveJoints(JointAngles=pos9)

    reverse_gotoplate()
    
    client.UFController.OpenGripper()

    client.UFController.MoveJoints(JointAngles=pos4)
    client.UFController.MoveJoints(JointAngles=pos5)

    client.UFController.CloseGripper()