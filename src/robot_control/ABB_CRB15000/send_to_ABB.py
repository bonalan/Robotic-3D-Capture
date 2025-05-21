import compas_rrc as rrc
from compas.geometry import Point, Vector, Frame
import json, os

def load_planes(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    planes = []
    for i in range(len(data)):
        plane_data = data[str(i)]
        origin = plane_data["Point"]
        xvec = plane_data["X"]
        yvec = plane_data["Y"]
        p = Frame(Point(origin[0], origin[1], origin[2]), Vector(xvec[0], xvec[1], xvec[2]), Vector(yvec[0], yvec[1], yvec[2]))
        planes.append(p)

    return planes


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    planes = load_planes(filename=os.path.join(current_dir, "planes.json"))
    print("Loaded planes")

    # Create Ros Client
    ros = rrc.RosClient()
    ros.run()

    # Create ABB Client
    abb = rrc.AbbClient(ros, '/rob1')
    print('Connected.')

    # Define robot joints
    robot_joints_start_position = [175.0, 0.5, 53.0, 100.0, 2.0, 10.0] 
    # robot_joints_end_position = [172.0, -40.0, 58.0, -5.0, 85.0, 66.0] # TODO!!!

    # Define external axis
    external_axis_dummy = []

    # Define speed 
    speed = 400 #800
    speed_scan = 150 

    # Set Acceleration
    acc = 100  # Unit [%]
    ramp = 100  # Unit [%]
    abb.send(rrc.SetAcceleration(acc, ramp))

    # Set Max Speed
    override = 100  # Unit [%]
    max_tcp = 2500  # Unit [mm/s]
    abb.send(rrc.SetMaxSpeed(override, max_tcp))

    # User message -> basic settings send to robot
    print('Acc and MaxSpeed sent to robot')

    # Move robot to start position
    done = abb.send_and_wait(rrc.MoveToJoints(robot_joints_start_position, external_axis_dummy, speed, rrc.Zone.FINE))

    # # # Stop task user must press play button on the FlexPendant (RobotStudio) before robot starts to move
    # # abb.send(rrc.PrintText('Press Play to move.'))
    # # abb.send(rrc.Stop())

    for frame in planes: 
        abb.send(rrc.MoveToFrame(frame, speed, rrc.Zone.Z10))

    # # Move robot to end position
    # done = abb.send_and_wait(rrc.MoveToJoints(robot_joints_end_position, external_axis_dummy, speed, rrc.Zone.FINE))

    # # End of Code
    # print('Finished')

    # Close client
    ros.close()
    ros.terminate()

    print("Process completed")
