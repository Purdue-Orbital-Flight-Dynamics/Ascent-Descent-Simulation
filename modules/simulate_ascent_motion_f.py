import numpy as np
import matplotlib.pyplot as plt

#######################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Script Name: ascent_profile_plot
# File Name: ascent_profile_plot.py
#
# Contributors: Cayden Varno (original logic), <your name here> (extracted)
# Date Created: 11/20/2025
# Last Updated: 02/09/2026
#
# Script Description:
#   Simulates vertical ascent for a single helium mass case, integrating
#   position/velocity/acceleration from a starting altitude up to a max
#   altitude using buoyant, drag, and gravity forces.
#
#   Updated:
#     - Uses modules.atmosphere.atmosphere_m(...) once per timestep
#     - Passes atm=... into buoyant_force_f and drag_force_f (and any other
#       modules that are now atmosphere-driven)
#
#######################################################################

from modules.atmosphere import atmosphere_m
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f


def simulate_ascent_motion_f(helium_mass_kg, start_altitude_m, max_altitude_m,
                             time_step_s=0.1, constant_mass_kg=8.8,
                             make_plots=True,
                             log_scale_plots=False,   # [-] log-scale toggle
                             hard_stop_on_nonpositive_net_force=True):
    """
    Simulates ascent dynamics for a single helium mass case.

    Outputs a dict containing time histories plus summary stats.
    """

    #######################################################################
    # Input Checks
    #######################################################################

    if start_altitude_m < 0:
        return {
            "time_s": np.array([]),
            "position_m": np.array([]),
            "velocity_mps": np.array([]),
            "acceleration_mps2": np.array([]),
            "mean_ascent_rate_mps": 0.0,
            "gage_force_N": np.nan,
            "had_error": True,
            "error_reason": "start_altitude_m < 0"
        }

    if max_altitude_m <= start_altitude_m:
        return {
            "time_s": np.array([]),
            "position_m": np.array([]),
            "velocity_mps": np.array([]),
            "acceleration_mps2": np.array([]),
            "mean_ascent_rate_mps": 0.0,
            "gage_force_N": np.nan,
            "had_error": True,
            "error_reason": "max_altitude_m <= start_altitude_m"
        }

    if helium_mass_kg < 0:
        return {
            "time_s": np.array([]),
            "position_m": np.array([]),
            "velocity_mps": np.array([]),
            "acceleration_mps2": np.array([]),
            "mean_ascent_rate_mps": 0.0,
            "gage_force_N": np.nan,
            "had_error": True,
            "error_reason": "helium_mass_kg < 0"
        }

    #######################################################################
    # Initialization
    #######################################################################

    total_mass_kg = constant_mass_kg + helium_mass_kg   # [kg]

    position_m   = start_altitude_m   # [m]
    velocity_mps = 0.0               # [m/s]

    time_history_s            = []
    position_history_m        = []
    velocity_history_mps      = []
    acceleration_history_mps2 = []

    gage_force_N = np.nan
    had_error    = False
    error_reason = ""

    step_index = 1
    time_s = 0.0

    #######################################################################
    # Integration Loop
    #######################################################################

    while position_m < max_altitude_m:

        # One atmosphere call per timestep
        atm = atmosphere_m(position_m, geometric=True)

        try:
            buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg, atm=atm)
            drag_force_N    = drag_force_f(velocity_mps, helium_mass_kg, position_m, atm=atm)
        except Exception:
            had_error = True
            error_reason = "Exception in buoyant_force_f(...) or drag_force_f(...)"
            break

        gravity_force_N    = gravity_force_f(position_m, total_mass_kg)
        correction_force_N = force_correction_f(helium_mass_kg, position_m)

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N

        if step_index == 1:
            gage_force_N = buoyant_force_N - correction_force_N

        if hard_stop_on_nonpositive_net_force and net_force_N <= 0:
            had_error = True
            error_reason = "net_force_N <= 0"
            break

        # Explicit Euler integration
        acceleration_mps2 = net_force_N / total_mass_kg
        velocity_mps      = velocity_mps + acceleration_mps2 * time_step_s
        position_m        = position_m + velocity_mps * time_step_s

        # Log histories
        time_history_s.append(time_s)
        position_history_m.append(position_m)
        velocity_history_mps.append(velocity_mps)
        acceleration_history_mps2.append(acceleration_mps2)

        time_s += time_step_s
        step_index += 1

        if step_index > 10_000_000:
            had_error = True
            error_reason = "Safety stop: too many integration steps"
            break

    #######################################################################
    # Post-Processing
    #######################################################################

    if len(velocity_history_mps) == 0:
        mean_ascent_rate_mps = 0.0
        if not had_error:
            had_error = True
            error_reason = "No samples recorded"
    else:
        mean_ascent_rate_mps = float(np.mean(velocity_history_mps))

    results = {
        "time_s": np.asarray(time_history_s),
        "position_m": np.asarray(position_history_m),
        "velocity_mps": np.asarray(velocity_history_mps),
        "acceleration_mps2": np.asarray(acceleration_history_mps2),
        "mean_ascent_rate_mps": mean_ascent_rate_mps,
        "gage_force_N": float(gage_force_N) if np.isfinite(gage_force_N) else gage_force_N,
        "had_error": had_error,
        "error_reason": error_reason
    }

    #######################################################################
    # Plotting
    #######################################################################

    if make_plots and len(results["time_s"]) > 0:

        # Position
        plt.figure()
        plt.plot(results["time_s"], results["position_m"])
        plt.xlabel("Time [s]")
        plt.ylabel("Position [m]")
        plt.title(f"Position vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)
        if log_scale_plots:
            plt.xscale("log")

        # Velocity
        plt.figure()
        plt.plot(results["time_s"], results["velocity_mps"])
        plt.xlabel("Time [s]")
        plt.ylabel("Velocity [m/s]")
        plt.title(f"Velocity vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)
        if log_scale_plots:
            plt.xscale("log")

        # Acceleration
        plt.figure()
        plt.plot(results["time_s"], results["acceleration_mps2"])
        plt.xlabel("Time [s]")
        plt.ylabel("Acceleration [m/s^2]")
        plt.title(f"Acceleration vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)
        if log_scale_plots:
            plt.xscale("log")

        plt.show()

    return results
