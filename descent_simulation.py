#************************************************************************
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: descent_simulation_driver
# File Name: descent_simulation_driver.py
#
# Contributors: Samuel Landers, Aanand Shah, Garion Cheng
# Date Created: 02/04/2026
# Last Updated: 02/16/2026
#
# Function Description:
#   Simulates vertical descent of the high-altitude balloon (HAB)
#   after burst using forward time integration.
#
#   Sign Convention:
#       Upward direction is positive.
#       During descent, velocity is negative.
#
#   Inputs (user prompt):
#   - burst_altitude: initial altitude, meters, positive
#   - ground_level: ground altitude, meters, positive
#   - burst_velocity: velocity at burst, m/s, varies (negative for descent)
#
#   Outputs:
#   - Prints average descent rate, m/s, positive magnitude
#
# References:
#   N/A
#
#************************************************************************

import numpy as np

from modules.drag_force_descent_f import drag_force_descent_f
from modules.gravity_force_f import gravity_force_f
from modules.system_m_f import system_mass_f


# --- Simulation constants
DT = 1.0            # time step, seconds
STOP_STEPS = 1000   # maximum iteration steps, dimensionless


# --- User inputs (SI units)
burst_altitude = float(input("Enter balloon burst altitude (m): "))  # m, positive
ground_level = float(input("Enter ground level (m): "))              # m, positive
burst_velocity = float(input("Enter velocity at burst (m/s): "))     # m/s, varies


# --- Initial state
current_time = 0.0            # seconds
position = burst_altitude     # meters
velocity = burst_velocity     # m/s
acceleration = 0.0            # m/s^2

# System mass (kg)
total_mass, helium_mass = system_mass_f(position, 0)


# --- Data logging vectors
time_log = [current_time]     # seconds
position_log = [position]     # meters
velocity_log = [velocity]     # m/s
acceleration_log = [acceleration]  # m/s^2


step_index = 0


#************************************************************************
# Simulation Loop
#************************************************************************
while position > ground_level:

    if step_index >= STOP_STEPS:
        break

    # --- Gravity force (must be downward = negative if upward is positive)
    gravity_force = gravity_force_f(position, total_mass)  # N
    if gravity_force > 0:
        gravity_force = -gravity_force

    # --- Drag force (must oppose velocity direction)
    try:
        drag_force = drag_force_descent_f(velocity, position, helium_mass)  # N
    except TypeError:
        drag_force = drag_force_descent_f(velocity, position)  # N

    # If drag function returns magnitude only, enforce correct sign
    if velocity > 0:
        drag_force = -abs(drag_force)
    elif velocity < 0:
        drag_force = abs(drag_force)
    else:
        drag_force = 0.0

    # --- Net force
    net_force = gravity_force + drag_force  # N

    # --- State update (Forward Euler)
    acceleration = net_force / total_mass         # m/s^2
    velocity = velocity + acceleration * DT      # m/s
    position = position + velocity * DT          # m
    current_time = current_time + DT             # s

    # --- Log state
    time_log.append(current_time)
    position_log.append(position)
    velocity_log.append(velocity)
    acceleration_log.append(acceleration)

    step_index += 1


#************************************************************************
# Statistics
#************************************************************************

# Average descent rate (positive magnitude)
descent_speeds = [-v for v in velocity_log if v < 0]  # m/s
if len(descent_speeds) > 0:
    average_descent_rate = float(np.mean(descent_speeds))  # m/s
else:
    average_descent_rate = 0.0

print(f"Average descent rate: {average_descent_rate:.2f} m/s")
