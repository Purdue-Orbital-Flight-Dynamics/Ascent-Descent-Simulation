#************************************************************************
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Simulation
# Script Name: descent_simulation.py
#************************************************************************

import math
import time
import sys

from modules.drag_force_descent_f import drag_force_descent
from modules.gravity_force_f import gravity_force_f
from modules.log_descent_f import log_descent_entry

def get_input(prompt, default):
    """Helper to allow quick enters for default values or custom inputs."""
    user_val = input(f"{prompt} [{default}]: ").strip()
    return float(user_val) if user_val else default

def main():
    print("--- DESCENT SIMULATION CONFIGURATION ---")
    
    # Simulation control
    DT = 0.01
    STOP_STEPS = 100000000

    # User Inputs
    try:
        burst_altitude = get_input("Enter burst altitude (m)", 6000.0)
        ground_level   = get_input("Enter ground level (m)", 0.0)
        burst_velocity = get_input("Enter initial velocity (m/s, +=up)", 5.0)
        payload_mass   = get_input("Enter payload mass (kg)", 10.0)
        
        payload_dia    = get_input("Enter payload diameter (m)", 0.75)
        payload_cd     = get_input("Enter payload Cd", 1.25)
        
        chute_dia      = get_input("Enter parachute diameter (m)", 3.6576)
        chute_cd       = get_input("Enter parachute Cd", 1.5)
        deploy_time    = get_input("Enter deployment delay (s)", 3.0)
    except ValueError:
        print("Error: Invalid numeric input. Exiting.")
        sys.exit(1)

    # Pre-calculations
    payload_area = math.pi * (payload_dia**2) / 4
    parachute_area = math.pi * (chute_dia**2) / 4

    # Track execution time
    start_calc_time = time.time()

    #=======================================================================
    # INITIAL STATE
    #=======================================================================
    current_time = 0.0
    position = burst_altitude
    velocity = burst_velocity
    acceleration = 0.0

    time_log = [current_time]
    position_log = [position]
    velocity_log = [velocity]
    acceleration_log = [acceleration]

    step_index = 0
    terminal_velocity_time = None
    terminal_velocity_value = None
    TERMINAL_ACCEL_TOLERANCE = 0.01
    simulation_error = None

    print("\nSIMULATION RUNNING...")

    #=======================================================================
    # SIMULATION LOOP
    #=======================================================================
    try:
        # Phase 1: Freefall
        while position > ground_level and current_time < deploy_time:
            if step_index >= STOP_STEPS:
                simulation_error = "Max steps reached (Phase 1)"
                break

            F_g = -gravity_force_f(position, payload_mass)
            F_d = drag_force_descent(velocity, position, payload_area, payload_cd)
            
            acceleration = (F_g + F_d) / payload_mass
            velocity += acceleration * DT
            position += velocity * DT
            current_time += DT

            time_log.append(current_time)
            position_log.append(position)
            velocity_log.append(velocity)
            acceleration_log.append(acceleration)
            step_index += 1

        # Phase 2: Parachute
        while position > ground_level and not simulation_error:
            if step_index >= STOP_STEPS:
                simulation_error = "Max steps reached (Phase 2)"
                break

            F_g = -gravity_force_f(position, payload_mass)
            F_d = drag_force_descent(velocity, position, parachute_area, chute_cd)
            
            acceleration = (F_g + F_d) / payload_mass

            if terminal_velocity_time is None and abs(acceleration) < TERMINAL_ACCEL_TOLERANCE:
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
            step_index += 1
            
    except Exception as e:
        simulation_error = str(e)

    total_calc_time = time.time() - start_calc_time

    #=======================================================================
    # LOGGING AND OUTPUT
    #=======================================================================
    summary_dict = {
        'inputs': {
            'burst_altitude': burst_altitude,
            'payload_mass': payload_mass,
            'parachute_deploy_time': deploy_time
        },
        'results': {
            'final_time': current_time,
            'final_velocity': velocity,
            'terminal_velocity_value': terminal_velocity_value,
            'calculation_time': total_calc_time
        }
    }

    log_descent_entry("SUCCESS" if not simulation_error else "ERROR", summary_dict, error=simulation_error)

    print(f"\nDONE. Final Altitude: {position:.2f}m | Time: {current_time:.2f}s")
    if terminal_velocity_value:
        print(f"Terminal Velocity: {terminal_velocity_value:.2f} m/s")

if __name__ == '__main__':
    main()