########################################################################
# Purdue Orbital, Flight Dynamics
# Project Name: Ascent Modeling
#
# File Name: ascent_simulation.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 03/02/2026
#
# Script Description:
#   Solves for the helium mass required to achieve a target mean ascent
#   rate between a starting altitude and a burst altitude using a
#   time-marching ascent simulation.
#
#   The script:
#     - Uses the 1976 Standard Atmosphere (modules.atmosphere_f)
#     - Performs a binary search on helium mass
#     - Optionally runs a full ascent simulation for verification
#
# References:
# None
#
# Input variables:
# - start_altitude: starting altitude, m, >= 0
# - burst_altitude: burst altitude, m, > start_altitude
# - target_rate: desired ascent rate, m/s, > 0
#
# Output variables:
# - summary: dictionary containing solution results and diagnostics
########################################################################

from __future__ import annotations

import numpy as np

from modules.atmosphere_f import atmosphere_m
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.simulate_ascent_motion_f import simulate_ascent_motion_f


# --------------------------- CONSTANTS --------------------------------
TIME_STEP = 0.1                     # s
BALLOON_MASS_KG = 2.0              # kg
NECK_MASS_KG = 0.0                 # kg
ROPE_MASS_KG = 0.0                 # kg
OTHER_MASS_KG = 0.0                # kg
PAYLOAD_MASS_KG = 10.0             # kg

CONSTANT_MASS = (
    BALLOON_MASS_KG
    + NECK_MASS_KG
    + ROPE_MASS_KG
    + OTHER_MASS_KG
    + PAYLOAD_MASS_KG
)                                   # kg

GAGE_MASS_KG = (
    BALLOON_MASS_KG
    + NECK_MASS_KG
    + ROPE_MASS_KG
    + OTHER_MASS_KG
)                                   # kg

MAX_HELIUM_MASS = 50.0             # kg
MAX_BINARY_ITERATIONS = 80         # unitless
RATE_DECIMALS = 5                  # unitless
MAX_ATMOSPHERE_ALTITUDE = 84_852.0 # m
# ---------------------------------------------------------------------


def validate_inputs_f(
    start_altitude: float,
    burst_altitude: float,
    target_rate: float,
) -> str | None:
    """
    Validate solver inputs.

    Returns error string if invalid, otherwise None.
    """
    if start_altitude < 0.0:
        return "start_altitude must be non-negative"

    if burst_altitude <= start_altitude:
        return "burst_altitude must be greater than start_altitude"

    if target_rate <= 0.0:
        return "target_rate must be positive"

    if burst_altitude > MAX_ATMOSPHERE_ALTITUDE:
        return "burst_altitude exceeds standard atmosphere ceiling"

    return None


def atmosphere_at_altitude_f(altitude: float) -> dict:
    """
    Wrapper for atmosphere model.

    Inputs:
    - altitude: altitude, m

    Outputs:
    - atmosphere: dictionary of atmospheric properties
    """
    return atmosphere_m(altitude, geometric=True)


def simulate_ascent_rate_f(
    start_altitude: float,
    burst_altitude: float,
    helium_mass: float,
) -> tuple[float, bool, list[dict]]:
    """
    Simulate ascent and compute mean ascent rate.

    Returns:
    - mean_rate: mean ascent velocity, m/s
    - failed: True if ascent fails
    - history: list of state dictionaries
    """

    total_mass = CONSTANT_MASS + helium_mass  # kg

    altitude = start_altitude                 # m
    velocity = 0.0                            # m/s

    history: list[dict] = []

    while altitude < burst_altitude:
        atmosphere = atmosphere_at_altitude_f(altitude)

        buoyant_force = buoyant_force_f(altitude, helium_mass, atm=atmosphere)  # N
        drag_force = drag_force_f(velocity, helium_mass, altitude, atm=atmosphere)  # N
        gravity_force = gravity_force_f(altitude, total_mass)  # N

        net_force = buoyant_force - drag_force - gravity_force  # N

        if net_force <= 0.0:
            return 0.0, True, history

        acceleration = net_force / total_mass  # m/s^2

        velocity += acceleration * TIME_STEP   # m/s
        altitude += velocity * TIME_STEP       # m

        history.append({
            "altitude": altitude,
            "velocity": velocity,
        })

    if len(history) == 0:
        return 0.0, True, history

    mean_rate = float(np.mean([step["velocity"] for step in history]))  # m/s

    return mean_rate, False, history


def solve_helium_mass_f(
    start_altitude: float,
    burst_altitude: float,
    target_rate: float,
) -> tuple[float | None, float]:
    """
    Solve for helium mass using binary search.

    Returns:
    - helium_mass: kg (None if not achievable)
    - achieved_rate: m/s
    """

    max_rate, failed, _ = simulate_ascent_rate_f(
        start_altitude,
        burst_altitude,
        MAX_HELIUM_MASS,
    )

    if failed or max_rate < target_rate:
        return None, max_rate

    lower_mass = 0.0
    upper_mass = MAX_HELIUM_MASS

    best_mass = upper_mass
    best_rate = max_rate

    for _ in range(MAX_BINARY_ITERATIONS):
        test_mass = 0.5 * (lower_mass + upper_mass)

        rate, failed, _ = simulate_ascent_rate_f(
            start_altitude,
            burst_altitude,
            test_mass,
        )

        if failed or rate < target_rate:
            lower_mass = test_mass
            continue

        upper_mass = test_mass
        best_mass = test_mass
        best_rate = rate

        if round(best_rate, RATE_DECIMALS) == round(target_rate, RATE_DECIMALS):
            break

    return best_mass, best_rate


def ascent_solver_f(
    start_altitude: float,
    burst_altitude: float,
    target_rate: float,
    run_simulation: bool = False,
) -> dict:
    """
    High-level ascent solver interface.
    """

    summary = {
        "inputs": {
            "start_altitude": start_altitude,
            "burst_altitude": burst_altitude,
            "target_rate": target_rate,
        },
        "results": {
            "helium_mass": None,
            "achieved_rate": 0.0,
            "initial_gage_force": 0.0,
            "success": False,
        },
        "limits": {
            "max_helium_mass": MAX_HELIUM_MASS,
            "atmosphere_ceiling": MAX_ATMOSPHERE_ALTITUDE,
        },
        "forces_at_launch": None,
        "status": {
            "solution_found": False,
            "error": None,
        },
    }

    error = validate_inputs_f(start_altitude, burst_altitude, target_rate)

    if error is not None:
        summary["status"]["error"] = error
        return summary

    helium_mass, rate = solve_helium_mass_f(
        start_altitude,
        burst_altitude,
        target_rate,
    )

    if helium_mass is None:
        summary["status"]["error"] = "Target ascent rate not achievable"
        return summary

    atmosphere = atmosphere_at_altitude_f(start_altitude)

    buoyant = buoyant_force_f(start_altitude, helium_mass, atm=atmosphere)  # N
    gravity = gravity_force_f(start_altitude, CONSTANT_MASS + helium_mass)  # N
    gage_gravity = gravity_force_f(start_altitude, GAGE_MASS_KG)            # N

    net_force = buoyant - gravity                                           # N
    initial_acceleration = net_force / (CONSTANT_MASS + helium_mass)        # m/s^2
    gage_force = buoyant - gage_gravity                                     # N

    summary["forces_at_launch"] = {
        "buoyant_force": buoyant,
        "gravity_force": gravity,
        "net_force": net_force,
        "initial_acceleration": initial_acceleration,
    }

    summary["results"].update({
        "helium_mass": helium_mass,
        "achieved_rate": rate,
        "initial_gage_force": gage_force,
        "success": True,
    })

    summary["status"]["solution_found"] = True

    if run_simulation:
        simulate_ascent_motion_f(
            helium_mass_kg=helium_mass,
            start_altitude_m=start_altitude,
            max_altitude_m=burst_altitude,
            time_step_s=TIME_STEP,
            constant_mass_kg=CONSTANT_MASS,
            make_plots=False,
            log_scale_plots=False,
            hard_stop_on_nonpositive_net_force=True,
        )

    return summary


def main() -> None:
    """
    Entry point for standalone execution.
    """

    burst_altitude = float(input("Burst Altitude [m]: "))
    start_altitude = float(input("Starting Altitude [m]: "))
    target_rate = float(input("Desired Ascent Rate [m/s]: "))
    target_specific_alt = float(input("Altitude for velocity check [m]: "))

    summary = ascent_solver_f(
        start_altitude=start_altitude,
        burst_altitude=burst_altitude,
        target_rate=target_rate,
        run_simulation=True,
    )

    if not summary["results"]["success"]:
        raise SystemExit(summary["status"]["error"])

    _, _, full_history = simulate_ascent_rate_f(
        start_altitude,
        burst_altitude,
        summary["results"]["helium_mass"],
    )

    closest_step = min(
        full_history,
        key=lambda step: abs(step["altitude"] - target_specific_alt),
    )

    print(f"\nHelium mass required [kg]: {summary['results']['helium_mass']:.4f}")
    print(f"Initial gage force [N]: {summary['results']['initial_gage_force']:.4f}")
    print(f"Achieved ascent rate [m/s]: {summary['results']['achieved_rate']:.4f}")
    print(f"Velocity at {closest_step['altitude']:.2f} m: {closest_step['velocity']:.4f} m/s")


if __name__ == "__main__":
    main()
