#************************************************************************
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Simulation
#
# Function Name: drag_force_descent
# File Name: drag_force_descent_f.py
#
# Contributors:
# Date Created:
# Last Updated:
#
# Function Description:
#   Computes the aerodynamic drag force acting on the payload or parachute
#   during descent. Drag opposes the direction of motion — upward when
#   descending (negative velocity), downward when ascending (positive
#   velocity).
#
# References:
#
# Input variables:
#   - velocity: vertical velocity of payload, m/s, varies (up = positive)
#   - altitude: current altitude above sea level, m, positive
#   - area: aerodynamic reference area (frontal), m^2, positive
#   - cd: drag coefficient of the body, -, positive
#
# Output variables:
#   - drag_force: aerodynamic drag force, N, varies
#                 (positive = upward, opposes direction of motion)
#
#************************************************************************

from modules.atmosphere_f import atmosphere_m


def drag_force_descent(velocity: float, altitude: float, area: float, cd: float) -> float:

    # Retrieve atmospheric properties at current altitude
    atmosphere = atmosphere_m(altitude, output="dict")  # atmospheric state dictionary
    rho = atmosphere.get("rho", 1.225)  # air density, kg/m^3 (fallback: sea-level standard)

    # Drag magnitude: Fd = 0.5 * rho * Cd * A * v^2
    drag_magnitude = 0.5 * rho * cd * area * velocity**2  # N, always positive

    # Apply sign: drag opposes motion, so sign is opposite to velocity
    if velocity > 0:
        drag_force = -drag_magnitude  # payload moving up, drag acts downward, N
    else:
        drag_force = drag_magnitude   # payload moving down, drag acts upward, N

    return drag_force  # net drag force, N, varies