#************************************************************************
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Simulation
#
# Script Name: descent_simulation.py
#
# Contributors: Cayden Varno
# Date Created: 4/6/26
# Last Updated: 4/6/26
#
# Script Description:
#   Simulates the vertical descent of a cylindrical payload with a
#   deployable parachute. Uses forward Euler integration to propagate
#   position and velocity from burst altitude to ground level.
#
#   Drag is computed in two phases:
#     1. Pre-deployment: cylinder (flat face into airflow) drag only
#     2. Post-deployment: parachute drag dominates
#
#   Gravity and atmospheric density vary with altitude via external
#   function modules.
#
# References:
#
# Input variables (user-editable parameters):
#   - DT: simulation timestep, s, positive
#   - STOP_STEPS: maximum iteration count before forced exit, -, positive
#   - burst_altitude: initial altitude at balloon burst, m, positive
#   - ground_level: target termination altitude, m, positive or zero
#   - burst_velocity: initial vertical velocity at burst, m/s, varies
#                     (positive = upward)
#   - payload_mass: total descending payload mass, kg, positive
#   - payload_diameter: diameter of cylindrical payload body, m, positive
#   - payload_cd: drag coefficient of cylinder (flat face), -, positive
#   - parachute_diameter: nominal parachute canopy diameter, m, positive
#   - parachute_cd: parachute drag coefficient, -, positive
#   - parachute_deploy_time: elapsed time before chute deploys, s, positive
#
# Output variables:
#   - time_log: time history of simulation, s, positive
#   - position_log: altitude history, m, positive
#   - velocity_log: vertical velocity history, m/s, varies
#   - acceleration_log: vertical acceleration history, m/s^2, varies
#
#************************************************************************

import math

from modules.drag_force_descent_f import drag_force_descent
from modules.gravity_force_f import gravity_force_f

#=======================================================================
# USER-EDITABLE PARAMETERS
#=======================================================================

# Simulation control
DT = 0.01                       # timestep, s
STOP_STEPS = 100000000          # max iterations before forced stop, -

# Initial conditions
burst_altitude = 6000.0      # altitude at balloon burst, m
ground_level = 0.0           # termination altitude (ground), m
burst_velocity = 5.0         # initial vertical velocity (up = +), m/s

payload_mass = 10.0          # total payload mass, kg

# Payload geometry (cylinder, flat face into airflow)
payload_diameter = 0.75      # cylinder diameter, m
payload_cd = 1.25            # cylinder drag coefficient, -

# Reference area computed from diameter (do not edit unless overriding geometry)
payload_area = math.pi * (payload_diameter**2) / 4  # projected frontal area, m^2

# Parachute
parachute_diameter = 3.6576  # nominal canopy diameter, m
parachute_cd = 1.5           # parachute drag coefficient, -
parachute_deploy_time = 3.0  # time after burst before chute deploys, s

# Parachute reference area computed from diameter
parachute_area = math.pi * (parachute_diameter**2) / 4  # canopy projected area, m^2


def main():

    #=======================================================================
    # INITIAL STATE
    #=======================================================================

    current_time = 0.0           # elapsed simulation time, s
    position = burst_altitude    # current altitude, m
    velocity = burst_velocity    # current vertical velocity (up = +), m/s
    acceleration = 0.0           # current vertical acceleration, m/s^2

    # State history logs
    time_log = [current_time]
    position_log = [position]
    velocity_log = [velocity]
    acceleration_log = [acceleration]

    step_index = 0               # current iteration count, -

    # Terminal velocity tracking
    terminal_velocity_time = None
    terminal_velocity_value = None

    print("\nDESCENT SIMULATION STARTED")
    print("==========================\n")

    #=======================================================================
    # SIMULATION LOOP
    #=======================================================================

    while position > ground_level:

        if step_index >= STOP_STEPS:
            print("Simulation stopped: maximum step count reached.")
            break

        if current_time < parachute_deploy_time:
            area = payload_area
            cd = payload_cd
            phase = "PAYLOAD"
        else:
            area = parachute_area
            cd = parachute_cd
            phase = "CHUTE"

        F_gravity = -gravity_force_f(position, payload_mass)
        F_drag = drag_force_descent(velocity, position, area, cd)

        F_net = F_gravity + F_drag
        acceleration = F_net / payload_mass

        TERMINAL_ACCEL_TOLERANCE = 0.01
        if phase == "CHUTE" and terminal_velocity_time is None:
            if abs(acceleration) < TERMINAL_ACCEL_TOLERANCE:
                terminal_velocity_time = current_time
                terminal_velocity_value = velocity

        velocity += acceleration * DT
        position += velocity * DT
        current_time += DT

        if position <= ground_level:
            position = ground_level
            velocity = 0.0

        time_log.append(current_time)
        position_log.append(position)
        velocity_log.append(velocity)
        acceleration_log.append(acceleration)

        if step_index % (2 / DT) == 0:
            print(f"[{phase}] t={current_time:.1f}s | h={position:.2f}m | v={velocity:.2f}m/s | a={acceleration:.2f}m/s²")

        step_index += 1

    #=======================================================================
    # FINAL OUTPUT
    #=======================================================================

    print("\nSIMULATION COMPLETE")
    print("===================")
    print(f"Final time:     {current_time:.2f} s")
    print(f"Final position: {position:.2f} m")
    print(f"Final velocity: {velocity:.2f} m/s")

    if terminal_velocity_time is not None:
        print(f"Terminal velocity reached at: {terminal_velocity_time:.2f} s ({terminal_velocity_value:.2f} m/s)")
    else:
        print("Terminal velocity: not reached during simulation")
        
if __name__ == '__main__':
    main()