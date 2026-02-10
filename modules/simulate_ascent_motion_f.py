########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: simulate_ascent_motion_f
# File Name: simulate_ascent_motion_f.py
#
# Contributors: Cayden Varno (original logic), Purdue Orbital Flight Dynamics Team (refactor)
# Date Created: 11/20/2025
# Last Updated: 02/09/2026
#
# Function Description:
#   Simulates 1-D vertical ascent for a single helium mass case, integrating
#   position/velocity/acceleration from a starting altitude up to a maximum
#   altitude using buoyant, drag, and gravity forces.
#
# Notes:
#   - Calls modules.atmosphere.atmosphere_m(...) once per timestep and passes
#     the resulting atm dict into buoyant_force_f and drag_force_f.
#   - Integration uses explicit Euler.
#
# References:
#   None
#
# Input variables:
# - helium_mass_kg: helium mass, kg, non-negative
# - start_altitude_m: starting altitude, m, non-negative
# - max_altitude_m: max altitude, m, > start_altitude_m
# - time_step_s: integration time step, s, positive
# - constant_mass_kg: non-helium mass, kg, non-negative
# - make_plots: plot time histories, bool
# - log_scale_plots: toggle log x-axis for plots, bool
# - hard_stop_on_nonpositive_net_force: stop if net force <= 0, bool
#
# Output variables (returned dict):
# - time_s: time history, s
# - position_m: altitude history, m
# - velocity_mps: velocity history, m/s
# - acceleration_mps2: acceleration history, m/s^2
# - mean_ascent_rate_mps: mean of velocity history, m/s
# - gage_force_N: initial gage force (buoyant - correction), N
# - had_error: error flag, bool
# - error_reason: error description, str
#
########################################################################

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from modules.atmosphere_f import atmosphere_m
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f


def _empty_error_result(error_reason: str) -> dict:
    """Return a standardized empty results dict."""
    return {
        "time_s": np.array([]),
        "position_m": np.array([]),
        "velocity_mps": np.array([]),
        "acceleration_mps2": np.array([]),
        "mean_ascent_rate_mps": 0.0,
        "gage_force_N": np.nan,
        "had_error": True,
        "error_reason": error_reason,
    }


def simulate_ascent_motion_f(
    helium_mass_kg: float,
    start_altitude_m: float,
    max_altitude_m: float,
    time_step_s: float = 0.1,
    constant_mass_kg: float = 8.8,
    make_plots: bool = True,
    log_scale_plots: bool = False,
    hard_stop_on_nonpositive_net_force: bool = True,
) -> dict:
    """Simulate ascent dynamics for a single helium mass case."""

    if start_altitude_m < 0.0:
        return _empty_error_result("start_altitude_m < 0")
    if max_altitude_m <= start_altitude_m:
        return _empty_error_result("max_altitude_m <= start_altitude_m")
    if helium_mass_kg < 0.0:
        return _empty_error_result("helium_mass_kg < 0")
    if time_step_s <= 0.0:
        return _empty_error_result("time_step_s <= 0")
    if constant_mass_kg < 0.0:
        return _empty_error_result("constant_mass_kg < 0")

    total_mass_kg = constant_mass_kg + helium_mass_kg  # [kg]

    position_m = start_altitude_m  # [m]
    velocity_mps = 0.0             # [m/s]
    time_s = 0.0                   # [s]

    time_history_s: list[float] = []
    position_history_m: list[float] = []
    velocity_history_mps: list[float] = []
    acceleration_history_mps2: list[float] = []

    gage_force_N = float("nan")
    had_error = False
    error_reason = ""

    step_index = 1

    while position_m < max_altitude_m:
        atm = atmosphere_m(position_m, geometric=True)

        try:
            buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg, atm=atm)  # [N]
            drag_force_N = drag_force_f(velocity_mps, helium_mass_kg, position_m, atm=atm)  # [N]
        except Exception:
            had_error = True
            error_reason = "Exception in buoyant_force_f(...) or drag_force_f(...)"
            break

        gravity_force_N = gravity_force_f(position_m, total_mass_kg)  # [N]
        correction_force_N = force_correction_f(helium_mass_kg, position_m)  # [N]

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N  # [N]

        if step_index == 1:
            gage_force_N = buoyant_force_N - correction_force_N  # [N]

        if hard_stop_on_nonpositive_net_force and net_force_N <= 0.0:
            had_error = True
            error_reason = "net_force_N <= 0"
            break

        acceleration_mps2 = net_force_N / total_mass_kg  # [m/s^2]
        velocity_mps = velocity_mps + acceleration_mps2 * time_step_s  # [m/s]
        position_m = position_m + velocity_mps * time_step_s  # [m]

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
        "error_reason": error_reason,
    }

    if make_plots and len(results["time_s"]) > 0:
        plt.figure()
        plt.plot(results["time_s"], results["position_m"])
        plt.xlabel("Time [s]")
        plt.ylabel("Position [m]")
        plt.title(f"Position vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)
        if log_scale_plots:
            plt.xscale("log")

        plt.figure()
        plt.plot(results["time_s"], results["velocity_mps"])
        plt.xlabel("Time [s]")
        plt.ylabel("Velocity [m/s]")
        plt.title(f"Velocity vs Time (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)
        if log_scale_plots:
            plt.xscale("log")

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
            plt.yscale("log")

        # Acceleration vs Position
        plt.figure()
        plt.plot(results["position_m"], results["acceleration_mps2"])
        plt.xlabel("Position [m]")
        plt.ylabel("Acceleration [m/s^2]")
        plt.title(f"Acceleration vs Position (He Mass = {helium_mass_kg:.4f} kg)")
        plt.grid(True)

        if log_scale_plots:
            plt.yscale("log")

        plt.show()

    return results
