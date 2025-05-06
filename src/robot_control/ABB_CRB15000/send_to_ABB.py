import compas_rrc as rrc
from compas.geometry import Plane, Point, Vector, Frame
import json, os

def gh_to_compas_plane(gh_plane):
    origin = gh_plane.Origin
    normal = gh_plane.ZAxis
    p = Plane(Point(origin.X, origin.Y, origin.Z), Vector(normal.X, normal.Y, normal.Z))
    return p

def load_planes(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    planes = []
    for i in range(len(data)):
        plane_data = data[str(i)]
        origin = plane_data["Point"]
        normal = plane_data["Vector"]
        p = Plane(Point(origin[0], origin[1], origin[2]), Vector(normal[0], normal[1], normal[2]))
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
    robot_joints_start_position = [175.0, 0.5, 53.0, 10.0, 2.0, 10.0] # TODO!!!
    # robot_joints_end_position = [172.0, -40.0, 58.0, -5.0, 85.0, 66.0] # TODO!!!

    # Define external axis
    external_axis_dummy = []

    # Define speed 
    speed = 800
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

    for plane in planes: 
        frame = Frame.from_plane(plane)
        abb.send(rrc.MoveToFrame(frame, speed, rrc.Zone.FINE))

    # # Move robot to end position
    # done = abb.send_and_wait(rrc.MoveToJoints(robot_joints_end_position, external_axis_dummy, speed, rrc.Zone.FINE))

    # # End of Code
    # print('Finished')

    # Close client
    ros.close()
    ros.terminate()
