"""
This module wraps standard UR Script functions.
Main change is that plane infromation substitute for pose data
"""

import utils
import Rhino.Geometry as rg

# Some Constants
MAX_ACCEL = 2.5
MAX_VELOCITY = 2.5

def move_l(plane_to, accel, vel):
    """
    Function that returns UR script for linear movement in tool-space.

    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose (in UR base coordinate system)
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """

    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) >MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)

    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,plane_to)
    _axis_angle= utils.matrix_to_axis_angle(_matrix)
    # Create pose data
    _pose = [plane_to.OriginX/1000, plane_to.OriginY/1000, plane_to.OriginZ/1000,_axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f,"*6)[:-1]+"]"
    _pose_fmt = _pose_fmt%tuple(_pose)
    # Format UR script
    script = "movel(%s, a = %.2f, v = %.2f)\n"%(_pose_fmt,accel,vel)
    return script


def move_l_blend(plane_to, accel, vel, blend_radius = 0):
    """
    Function that returns UR script for linear movement in tool-space.
    
    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose (in UR base coordinate system)
        accel: tool accel in m/s^2
        vel: tool speed in m/s
        
    Returns:
        script: UR script
    """
    
    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) >MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)
    # Check blend radius is positive
    blend_radius = max(0, blend_radius)

    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,plane_to)
    _axis_angle= utils.matrix_to_axis_angle(_matrix)
    # Create pose data
    _pose = [plane_to.OriginX/1000, plane_to.OriginY/1000, plane_to.OriginZ/1000,_axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f,"*6)[:-1]+"]"
    _pose_fmt = _pose_fmt%tuple(_pose)
    # Format UR script
    script = "movel(%s, a = %.3f, v = %.3f, r = %.3f)\n"%(_pose_fmt, accel, vel, blend_radius)
    return script

def move_p_blend(plane_to, accel, vel, blend_radius = 0):
    """
    Function that returns UR script for linear movement in tool-space.
    
    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose (in UR base coordinate system)
        accel: tool accel in m/s^2
        vel: tool speed in m/s
        
    Returns:
        script: UR script
    """
    
    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) >MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)
    # Check blend radius is positive
    blend_radius = max(0, blend_radius)

    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,plane_to)
    _axis_angle= utils.matrix_to_axis_angle(_matrix)
    # Create pose data
    _pose = [plane_to.OriginX/1000, plane_to.OriginY/1000, plane_to.OriginZ/1000,_axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f,"*6)[:-1]+"]"
    _pose_fmt = _pose_fmt%tuple(_pose)
    # Format UR script
    script = "movep(%s, a = %.3f, v = %.3f, r = %.3f)\n"%(_pose_fmt, accel, vel, blend_radius)
    return script

def move_j(joints, accel, vel):
    """
    Function that returns UR script for linear movement in joint space.

    Args:
        joints: A list of 6 joint angles (double).
        accel: tool accel in m/s^2
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """
    # Check acceleration and velocity are non-negative and below a set limit

    _j_fmt = "[" + ("%.2f,"*6)[:-1]+"]"
    _j_fmt = _j_fmt%tuple(joints)
    script = "movej(%s, a = %.2f, v = %.2f)\n"%(_j_fmt,accel,vel)
    return script

def set_tcp_by_plane(x_offset, y_offset, z_offset, ref_plane=rg.Plane.WorldXY):
    """
    TODO: Need to test if this gives the correct result
    Function that returns UR script for setting tool center point

    Args:
        x_offset: float. tooltip offset in mm
        y_offset: float. tooltip offset in mm
        z_offset: float. tooltip offset in mm
        ref_plane: Plane that defines orientation of the tip. If none specified, world XY plane used as default. (in UR base coordinate system)

    Returns:
        script: UR script
    """

    if (ref_plane != rg.Plane.WorldXY):
        _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,ref_plane)
        _axis_angle= utils.matrix_to_axis_angle(_matrix)
    else:
        _axis_angle = rg.Vector3d(0,0,0)
    # Create pose data
    _pose = [x_offset/1000, y_offset/1000, z_offset/1000,_axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f,"*6)[:-1]+"]"
    _pose_fmt = _pose_fmt%tuple(_pose)

    # Format UR script
    script = "set_tcp(%s)\n"%(_pose_fmt)
    return script

def set_tcp_by_angles(x_offset, y_offset, z_offset, x_rotate, y_rotate, z_rotate):
    """
    TODO(Jason): Need to test this
    Function that returns UR script for setting tool center point

    Args:
        x_offset: float. tooltip offset in mm
        y_offset: float. tooltip offset in mm
        z_offset: float. tooltip offset in mm
        x_rotation: float. rotation around world x axis in radians
        y_rotation: float. rotation around world y axis in radians
        z_rotation: float. rotation around world z axis in radians

    Returns:
        script: UR script
    """

    #Create rotation matrix
    _rX = rg.Transform.Rotation(x_rotate, rg.Vector3d(1,0,0), rg.Point3d(0,0,0))
    _rY = rg.Transform.Rotation(y_rotate, rg.Vector3d(0,1,0), rg.Point3d(0,0,0))
    _rZ = rg.Transform.Rotation(z_rotate, rg.Vector3d(0,0,1), rg.Point3d(0,0,0))
    _r = _rX * _rY * _rZ
    _axis_angle= utils.matrix_to_axis_angle(_r)

    # Create pose data
    _pose = [x_offset/1000, y_offset/1000, z_offset/1000,_axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f,"*6)[:-1]+"]"
    _pose_fmt = _pose_fmt%tuple(_pose)

    # Format UR script
    script = "set_tcp(%s)\n"%(_pose_fmt)
    return script

def popup(message, title):
    """
    Function that returns UR script for popup

    Args:
        message: float. tooltip offset in mm
        title: float. tooltip offset in mm

    Returns:
        script: UR script
    """
    script = 'popup("%s","%s") \n' %(message,title)
    return script

def sleep(time):
    """
    Function that returns UR script for sleep()

    Args:
        time: float.in s

    Returns:
        script: UR script
    """
    script = "sleep(%s) \n" %(time)
    return script

def set_digital_out(id, signal):
    """
    Function that returns UR script for setting digital out
    
    Args:
        id: int. Input id number
        signal: boolean. signal level - on or off
    
    Returns:
        script: UR script
    """
    
    # Format UR script
    script = "set_digital_out(%s,%s)\n"%(id,signal)
    return script

def get_digital_in(id):
    """
    Function that returns UR script for getting digital in
    
    Args:
        id: int. Input id number
    
    Returns:
        script: UR script
    """
    
    # Format UR script
    script = "get_standard_digital_in(%s) \n" %(id)
    return script

def set_standard_analog_out(n, f):
    """
    Parameters
    n: The number (id) of the output, integer: [0:1]
    f: The relative signal level [0;1] (float)

    Example command: set_standard_analog_out(1,1.0)
    n is standard analog output port 1
    f = 1.0, that corresponds to 10V (or 20mA depending on
    domain setting) on the output port
    """
    script = "set_standard_analog_out(%s,%s)\n"%(n,f)
    return script

def textmsg(s1,s2):
    """
    Send text message to log
    """
    # Format UR script
    script = 'textmsg("%s","%s") \n' %(s1,s2)
    return script

def multi_conditions(c1, c2):
    """
    Combine 2 digital inputs as one condition
    """
    script = c1.replace("\n", "")
    script += "and "
    script += c2.replace("\n", "")
    return script

def add_condition(type, con, bool):
    """
    Add condition to UR script.
    type : 0 is for loop, 1 is while loop
           2 is for elif
    con : string text, can be an UR script
    bool : True or False
    eg : if get_standard_digital_in(0) == True:
    """
    
    if type == 0:
        script = "if \t"
    elif type == 1:
        script = "while \t"
    elif type == 2:
        script = "elif \t"  
    script += con.replace("\n", "")
    script += "\t==\t"
    if bool == True:
        script += " True: \n"
    elif bool == False:
        script += " False: \n"
    return script

def end_condition():
    """
    End condition 
    """
    script = "end\n"
    return script