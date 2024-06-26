from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped


def depth_heading_updater(depth_control_signal, heading_control_signal, stability_thrust, rpm_adjustment):
    """
    Update heading based on depth control signal and heading control signal.
    Parameters:
        depth_control_signal: Depth control signal. Used for controlling vehicle's depth.
        heading_control_signal: Heading control signal. Used for controlling vehicle's heading.
        stability_thrust: Stability thrust value. Used so RPMs are in a range to affect vehicle dynamics
        rpm_adjustment: RPM adjustment value. Used for prioritizing vehicles surge movement.
    Output:
        :return: Dictionary containing updated thruster commands.
    """

    # Define maximum RPM limits
    max_rpm_depth = 1200.0
    heading_control_signal = max(min(heading_control_signal, 25.0), -25.0)

    # Apply constraints to thruster commands to be within +/- 1200 RPM
    vert_port_command = max(min(-depth_control_signal, max_rpm_depth), -max_rpm_depth)  # Positive RPMs send down
    vert_stbd_command = max(min(depth_control_signal, max_rpm_depth), -max_rpm_depth)  # Positive RPMs send up

    bow_port_command = -stability_thrust + heading_control_signal  # Negative for clockwise due to positive RPMs send CCW
    bow_stbd_command = stability_thrust + heading_control_signal   # Positive sends CCW, need negative for CW
    aft_port_command = -stability_thrust + rpm_adjustment
    aft_stbd_command = stability_thrust - rpm_adjustment

    return {
        'vert_port': FloatStamped(data=vert_port_command),
        'vert_stbd': FloatStamped(data=vert_stbd_command),
        'bow_port': FloatStamped(data=bow_port_command),
        'bow_stbd': FloatStamped(data=bow_stbd_command),
        'aft_port': FloatStamped(data=aft_port_command),
        'aft_stbd': FloatStamped(data=aft_stbd_command)
    }
