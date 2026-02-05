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
# Last Updated: 01/28/2026
#
# Script Description:
#   Simulates vertical ascent for a single helium mass case, integrating
#   position/velocity/acceleration from a starting altitude up to a max
#   altitude using buoyant, drag, and gravity forces.
#
#   Generates graphs of:
#       - position vs time
#       - velocity vs time
#       - acceleration vs time
#
# References:
#######################################################################

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

    Inputs:
        helium_mass_kg  : float   [kg] helium mass
        start_altitude_m: float   [m]  starting altitude
        max_altitude_m  : float   [m]  maximum (burst) altitude
        time_step_s     : float   [s]  integration time step
        constant_mass_kg: float   [kg] payload + structure mass (constant)
        make_plots      : bool    [-]  generate plots if True
        hard_stop_on_nonpositive_net_force : bool [-]
            If True, abort simulation when net_force_N <= 0 (matches original behavior)

    Outputs:
        results : dict containing:
            "time_s"                 : np.ndarray [s]
            "position_m"             : np.ndarray [m]
            "velocity_mps"           : np.ndarray [m/s]
            "acceleration_mps2"      : np.ndarray [m/s^2]
            "mean_ascent_rate_mps"   : float [m/s]
            "gage_force_N"           : float [N] (first-step buoyant - correction)
            "had_error"              : bool [-]
            "error_reason"           : str  [-]
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

    time_history_s            = []   # [s]
    position_history_m        = []   # [m]
    velocity_history_mps      = []   # [m/s]
    acceleration_history_mps2 = []   # [m/s^2]

    gage_force_N = np.nan            # [N] first-step buoyant - correction
    had_error    = False
    error_reason = ""

    step_index = 1                   # [-]
    time_s = 0.0                     # [s]

    #######################################################################
    # Integration Loop
    #######################################################################

    while position_m < max_altitude_m:

        # Compute buoyant force safely
        try:
            buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg)  # [N]
        except Exception:
            had_error = True
            error_reason = "Exception in buoyant_force_f(...)"
            break

        drag_force_N       = drag_force_f(velocity_mps, helium_mass_kg, position_m)  # [N]
        gravity_force_N    = gravity_force_f(position_m, total_mass_kg)              # [N]
        correction_force_N = force_correction_f(helium_mass_kg, position_m)          # [N]

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N               # [N]

        # Save FIRST net force only (matches original intent)
        if step_index == 1:
            gage_force_N = buoyant_force_N - correction_force_N

        # Abort if net force cannot sustain ascent (matches original behavior)
        if hard_stop_on_nonpositive_net_force and net_force_N <= 0:
            had_error = True
            error_reason = "net_force_N <= 0"
            break

        # Update state (explicit Euler)
        acceleration_mps2 = net_force_N / total_mass_kg                  # [m/s^2]
        velocity_mps      = velocity_mps + acceleration_mps2 * time_step_s  # [m/s]
        position_m        = position_m + velocity_mps * time_step_s         # [m]

        # Log histories
        time_history_s.append(time_s)
        position_history_m.append(position_m)
        velocity_history_mps.append(velocity_mps)
        acceleration_history_mps2.append(acceleration_mps2)

        # Advance
        time_s += time_step_s
        step_index += 1

        # Safety guard (prevents infinite loops if something goes weird)
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

        # Position vs Time
        plt.figure()
        plt.plot(results["time_s"], results["position_m"])
        plt.xlabel("Time [s]")
        plt.ylabel("Position [m]")
        plt.title(f"Position vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.xscale("log")

        # Velocity vs Time
        plt.figure()
        plt.plot(results["time_s"], results["velocity_mps"])
        plt.xlabel("Time [s]")
        plt.ylabel("Velocity [m/s]")
        plt.title(f"Velocity vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.xscale("log")

        # Acceleration vs Time
        plt.figure()
        plt.plot(results["time_s"], results["acceleration_mps2"])
        plt.xlabel("Time [s]")
        plt.ylabel("Acceleration [m/s^2]")
        plt.title(f"Acceleration vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.xscale("log")

        # Velocity vs Position
        plt.figure()
        plt.plot(results["position_m"], results["velocity_mps"])
        plt.xlabel("Position [m]")
        plt.ylabel("Velocity [m/s]")
        plt.title(f"Velocity vs Position (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.xscale("log")

        # Acceleration vs Position
        plt.figure()
        plt.plot(results["position_m"], results["acceleration_mps2"])
        plt.xlabel("Position [m]")
        plt.ylabel("Acceleration [m/s^2]")
        plt.title(f"Acceleration vs Position (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.xscale("log")

        plt.show()
    
    return results
