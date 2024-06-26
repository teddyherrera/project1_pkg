import numpy as np


def wrap_to_180(angle):
    """Wrap an angle in degrees to [-180, 180]."""
    return (angle + 180) % 360 - 180


def rad_to_deg(angle):
    """Convert radians to degrees."""
    return angle * (180.0 / np.pi)


def deg_to_rad(angle):
    """Convert degrees to radians."""
    return angle * (np.pi / 180.0)


def cte(bx, by, fx, fy, tx, ty, rho):
    """
    Calculate the ordered heading based on current and target positions.

    Parameters:
        bx, by: current x/y position
        fx, fy: "from" point x/y position
        tx, ty: "to" point x/y position
        rho: desired approach point (distance in front of vehicle)
    Output:
        ordered_heading: desired heading in degrees
    """
    # Normal to the path vector
    normal = np.array([ty - fy, -(tx - fx)])
    # Position vector from from-point to current position
    position = np.array([bx - fx, by - fy])
    # Error projection on the normal
    e = np.dot(normal, position) / np.linalg.norm(normal)
    # Direction to the target point
    psitrack = np.degrees(np.arctan2(ty - fy, tx - fx))
    # Compensated heading
    psicom = psitrack + np.degrees(np.arctan2(e, rho))
    # Convert to degrees and wrap
    ordered_heading = wrap_to_180(psicom)

    return ordered_heading
