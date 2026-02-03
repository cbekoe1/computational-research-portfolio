import math

def wake_radius(x, r0, k):
    """
    Jensen wake radius: r(x) = r0 + kx
    x: downstream distance [m]
    r0: rotor radius [m]
    k: wake expansion coefficient [-]
    """
    return r0 + k * x

def velocity_deficit(x, U_inf, C_T, r0, k):
    """
    Jensen velocity deficit:
    ΔU / U_inf = (1 - sqrt(1 - C_T)) / (1 + kx/r0)^2
    """
    if x <= 0:
        return 0.0
    denom = (1 + (k * x / r0)) ** 2
    return (1 - math.sqrt(1 - C_T)) / denom

def is_in_wake(x_turb, y_turb, x_up, y_up, r0, k):
    """
    Check if a downstream turbine (x_turb, y_turb) is inside
    the wake of an upstream turbine at (x_up, y_up).
    Wind is from left to right (increasing x).
    """
    dx = x_turb - x_up
    if dx <= 0:
        return False

    dy = y_turb - y_up
    r = wake_radius(dx, r0, k)
    return abs(dy) <= r

def turbulence_intensity_increment(x, D, a, TI0):
    """
    Simple turbulence intensity model.
    TI = TI0 + 0.73 a / (1 + 0.83 x / D)^2
    """
    if x <= 0:
        return 0.0
    return 0.73 * a / (1 + 0.83 * x / D) ** 2
