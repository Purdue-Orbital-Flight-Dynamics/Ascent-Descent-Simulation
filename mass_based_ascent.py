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
# Last Updated: 01/28/2026
#
# Script Description:
#   Determines the helium mass required to achieve a target mean ascent
#   rate between a starting altitude and a specified burst altitude.
#
#   First checks whether a defined maximum helium mass is sufficient.
#   If not sufficient, evaluates and reports the maximum ascent rate
#   possible under the imposed helium mass limit.
#
#   If sufficient, performs a binary search on helium mass to converge
#   on the required ascent rate within a specified tolerance.
#
# References:
#######################################################################

from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f
from modules.simulate_ascent_motion_f import simulate_ascent_motion_f

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

if start_altitude_m < 0 or burst_altitude_m <= start_altitude_m or \
   target_ascent_rate_mps <= 0 or burst_altitude_m > 100000:

    print('\n\nYour dumbass can\'t read instructions.\n\nTry again.')
    if random.random() < 0.04:
        print('\n\n\nRetard.\n')
    raise SystemExit

#######################################################################
# Constants
#######################################################################

CONSTANT_MASS_KG    = 8.8     # [kg] payload + structure
MAX_HELIUM_MASS_KG = 50.0    # [kg] maximum allowable helium mass

RATE_DECIMALS = 5            # [-] ascent rate matching precision
MAX_BINARY_ITERS = 80        # [-] safety limit on binary search iterations

#######################################################################
# Ascent Simulation Function
#######################################################################

def simulate_ascent_rate(helium_mass_kg):
    """
    Simulates vertical ascent for a given helium mass.

    Outputs:
        mean_ascent_rate_mps : float
        gage_force           : float
        had_error            : bool
    """

    total_mass_kg = CONSTANT_MASS_KG + helium_mass_kg   # [kg]

    position_m    = start_altitude_m    # [m]
    velocity_mps  = 0.0                 # [m/s]

    velocity_history_mps = []           # [m/s]
    gage_force = np.nan                 # [N]

    step_index = 1
    had_error  = False

    while position_m < burst_altitude_m:

        # Compute buoyant force safely
        try:
            buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg)
        except Exception:
            had_error = True
            break

        drag_force_N       = drag_force_f(velocity_mps, helium_mass_kg, position_m)
        gravity_force_N    = gravity_force_f(position_m, total_mass_kg)
        correction_force_N = force_correction_f(helium_mass_kg, position_m)

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N

        # Save FIRST net force only
        if step_index == 1:
            gage_force = buoyant_force_N - correction_force_N

        # Abort if net force cannot sustain ascent
        if net_force_N <= 0:
            had_error = True
            break

        # Update state (explicit Euler)
        acceleration_mps2 = net_force_N / total_mass_kg
        velocity_mps     = velocity_mps + acceleration_mps2 * time_step_s
        position_m       = position_m + velocity_mps * time_step_s

        velocity_history_mps.append(velocity_mps)
        step_index += 1

    if had_error or len(velocity_history_mps) == 0 or position_m < burst_altitude_m:
        return 0.0, gage_force, True

    mean_ascent_rate_mps = np.mean(velocity_history_mps)

    return mean_ascent_rate_mps, gage_force, False

#######################################################################
# Maximum Helium Mass Check
#######################################################################

max_rate_mps, max_gage_force, max_failed = simulate_ascent_rate(MAX_HELIUM_MASS_KG)

# If maximum helium mass cannot meet the target ascent rate,
# print the maximum ascent rate possible (under the limit) and exit.
if max_failed or max_rate_mps < target_ascent_rate_mps:

    print("\nMaximum helium mass is insufficient for these conditions.\n")
    print("Maximum helium mass [kg]:")
    print(f"{MAX_HELIUM_MASS_KG:.4f}")

    print("Maximum achieved ascent rate [m/s] under limit:")
    print(f"{max_rate_mps:.4f}")

    print("Initial net force at maximum mass [N]:")
    print(f"{max_gage_force:.4f}")

    raise SystemExit

#######################################################################
# Binary Search on Helium Mass
#######################################################################

low_mass_kg  = 0.0
high_mass_kg = MAX_HELIUM_MASS_KG   # known to be sufficient

best_mass_kg  = high_mass_kg
best_rate_mps = max_rate_mps
best_gage_N   = max_gage_force

for _ in range(MAX_BINARY_ITERS):

    mid_mass_kg = 0.5 * (low_mass_kg + high_mass_kg)

    mid_rate_mps, mid_gage_N, mid_failed = simulate_ascent_rate(mid_mass_kg)

    # If ascent rate is insufficient, increase helium mass
    if mid_failed or mid_rate_mps < target_ascent_rate_mps:
        low_mass_kg = mid_mass_kg
        continue

    # Otherwise, record solution and try reducing mass
    high_mass_kg = mid_mass_kg
    best_mass_kg = mid_mass_kg
    best_rate_mps = mid_rate_mps
    best_gage_N = mid_gage_N

    # Stop when ascent rate matches desired precision
    if round(best_rate_mps, RATE_DECIMALS) == round(target_ascent_rate_mps, RATE_DECIMALS):
        break

    # Stop when mass resolution no longer affects printed result
    if (high_mass_kg - low_mass_kg) < 0.5 * 10**(-RATE_DECIMALS):
        break

#######################################################################
# FINAL OUTPUT
#######################################################################

print("Mass for target rate [kg]:")
print(f"{best_mass_kg:.4f}")

print("Initial net force for target rate [N]:")
print(f"{best_gage_N:.4f}")

print("Final achieved ascent rate [m/s]:")
print(f"{best_rate_mps:.4f}")


#######################################################################
# Detailed Ascent Profile for Final Helium Mass
#######################################################################

PLOT_LOG_SCALE = True   # [-] set True for log-scale plots

ascent_profile_results = simulate_ascent_motion_f(
    helium_mass_kg   = best_mass_kg,        # [kg]
    start_altitude_m = start_altitude_m,    # [m]
    max_altitude_m   = burst_altitude_m,    # [m]
    time_step_s      = time_step_s,          # [s]
    constant_mass_kg = CONSTANT_MASS_KG,    # [kg]
    make_plots       = True,                 # [-]
    log_scale_plots  = PLOT_LOG_SCALE        # [-]
)

# Sanity check output
if ascent_profile_results["had_error"]:
    print("\nWARNING: Detailed ascent simulation encountered an issue.")
    print("Reason:")
    print(ascent_profile_results["error_reason"])
else:
    print("\nDetailed ascent simulation completed successfully.")
    print("Mean ascent rate from profile [m/s]:")
    print(f"{ascent_profile_results['mean_ascent_rate_mps']:.4f}")
