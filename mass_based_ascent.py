import numpy as np
import random

#######################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Script Name: mass_based_ascent
# File Name: mass_based_ascent.m
#
# Contributors: Cayden Varno
# Date Created: 11/20/2025
# Last Updated: 11/20/2025
#
# Script Description:
#   Iteratively determines the helium mass required to achieve a target
#   mean ascent rate between a starting altitude and a specified burst
#   altitude. For each helium mass, this script integrates the vertical
#   motion using buoyant, drag, and gravity forces, and records the first
#   net force for the final (target) case.
#
# References:
#######################################################################

from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f

# Instructions
print('\n***********************************************************\n\n' \
'INSTRUCTIONS\n\nStarting altitude must be greater than or equal to zero.\n' \
'Burst altitude must be less than or equal to 100 km.\n' \
'Burst altitude must be larger than starting altitude.\n' \
'Desired ascent rate must be greater than 0.\n')
    
if random.random() < 0.04:
    print('\nI will tickle your tonsils if you break this code.\n\n')

print('***********************************************************\n')

time_step_s = 0.1   # [s] integration time step

burst_altitude_m = float(input("Burst Altitude [m]: "))           # [m]
start_altitude_m = float(input("Starting Altitude [m]: "))        # [m]
target_ascent_rate_mps = float(input("Desired Ascent Rate [m/s]: "))  # [m/s]

if start_altitude_m < 0 or burst_altitude_m <= start_altitude_m or target_ascent_rate_mps <= 0:
    print('\n\nYour dumbass can\'t read instructions.\n\nTry again.')
else:
            
    
    MASS_STEP_KG       = 0.01   # [kg] helium mass increment per iteration
    helium_mass_kg     = -MASS_STEP_KG  # [kg] so first loop adds to 0
    CONSTANT_MASS_KG   = 8.8     # [kg] payload + structure, assumed constant
    ascent_rate_mps    = 0       # [m/s] current mean ascent rate estimate
    
    MAX_HELIUM_MASS_KG = 50      # [kg] safety limit on helium mass
    gage_force  = np.nan         # [N] first net force at start altitude
    
    while ascent_rate_mps < target_ascent_rate_mps and helium_mass_kg < MAX_HELIUM_MASS_KG:
    
        # Reset state for this helium mass
        position_m  = start_altitude_m   # [m]
        velocity_mps = 0                 # [m/s]
    
        position_history_m       = []    # [m]
        velocity_history_mps     = []    # [m/s]
        acceleration_history_mps2 = []   # [m/s^2]
    
        had_error   = False
        step_index  = 1
    
        helium_mass_kg = helium_mass_kg + MASS_STEP_KG   # [kg]
    
        total_mass_kg = CONSTANT_MASS_KG + helium_mass_kg   # [kg]
        
        # Print statement for user to see that program is running
        print(f"Mass increased to [kg]: {helium_mass_kg:.4f}")
        
        while position_m < burst_altitude_m:
    
            # Compute buoyant force safely
            try:
                buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg) # [N]
            except Exception:
                had_error = True
                break
    
            drag_force_N    = drag_force_f(velocity_mps, helium_mass_kg, position_m) # [N]
            gravity_force_N = gravity_force_f(position_m, total_mass_kg)             # [N]
            correction_force_N = force_correction_f(helium_mass_kg, position_m)      # [N]
    
            net_force_N = buoyant_force_N - drag_force_N - gravity_force_N           # [N]
    
            # Save FIRST net force only (for this helium mass)
            if step_index == 1:
                gage_force = buoyant_force_N - correction_force_N   # overwrite every run
    
            # Update state
            net_accel_mps2     = net_force_N / total_mass_kg       # [m/s^2]
            acceleration_mps2  = net_accel_mps2                    # [m/s^2]
            velocity_mps       = velocity_mps + acceleration_mps2 * time_step_s # [m/s]
            position_m         = position_m + velocity_mps * time_step_s        # [m]
    
            # Log histories
            position_history_m.append(position_m)
            velocity_history_mps.append(velocity_mps)
            acceleration_history_mps2.append(acceleration_mps2)
    
            if net_force_N <= 0:
                had_error = True
                break
    
            step_index = step_index + 1
    
        if not had_error and len(velocity_history_mps) > 0:
            ascent_rate_mps = np.mean(velocity_history_mps)    # [m/s]
    
    # FINAL OUTPUT ONLY
    print("Mass for target rate [kg]:")
    print(f"{helium_mass_kg:.4f}")
    
    print("Initial net force for target rate [N]:")
    print(f"{gage_force:.4f}")
    
    print("Final achieved ascent rate [m/s]:")
    print(f"{ascent_rate_mps:.4f}")
