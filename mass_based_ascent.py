########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Script Name: mass_based_ascent
# File Name: mass_based_ascent.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 02/09/2026
#
# Script Description:
#   Solves for the helium mass (kg) required to meet a target mean ascent
#   rate (m/s) between a starting altitude and a burst altitude.
#
#   This script:
#     - Uses the 1976 Standard Atmosphere implementation in modules.atmosphere
#       once per timestep (atm dict passed into dependent functions).
#     - Runs a full ascent simulation/plot using simulate_ascent_motion_f(...)
#       after solving for the helium mass.
#
# References:
#   None
#
# Inputs (via CLI prompts):
# - burst_alt_m: burst altitude, m, positive and > start_alt_m
# - start_alt_m: starting altitude, m, non-negative
# - target_rate_mps: desired mean ascent rate, m/s, positive
#
# Outputs (printed):
# - helium mass for target rate, kg
# - initial gage force (buoyant - correction), N
# - achieved mean ascent rate, m/s
#
########################################################################

from __future__ import annotations

import numpy as np

from modules.atmosphere_f import atmosphere_m
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f
from modules.simulate_ascent_motion_f import simulate_ascent_motion_f

# ----------------- configuration constants -----------------
TIME_STEP_S = 0.1               # [s]
CONSTANT_MASS_KG = 8.8          # [kg] fixed non-helium mass
MAX_HELIUM_MASS_KG = 50.0       # [kg] search upper bound
MAX_BINARY_ITERS = 80           # [-]
RATE_DECIMALS = 5               # [-] rate comparison precision
MAX_USSA76_ALT_M = 84_852.0     # [m] 1976 std-atm table ceiling in atmosphere.py
# -----------------------------------------------------------


def atmosphere_at_position(position_m: float) -> dict:
    """Return an atmosphere dict at a given geometric altitude.

    Parameters
    ----------
    position_m : float
        Geometric altitude, m, non-negative.

    Returns
    -------
    dict
        Atmosphere properties in SI units. Must include:
        - T_K, p_Pa, rho_kgm3
    """
    return atmosphere_m(position_m, geometric=True)


def simulate_ascent_rate(
    start_alt_m: float,
    burst_alt_m: float,
    helium_mass_kg: float,
) -> tuple[float, float, bool]:
    """Simulate ascent and estimate mean ascent rate for one helium mass.

    Parameters
    ----------
    start_alt_m : float
        Starting geometric altitude, m.
    burst_alt_m : float
        Burst geometric altitude, m.
    helium_mass_kg : float
        Helium mass in balloon, kg.

    Returns
    -------
    mean_rate_mps : float
        Mean ascent rate over the run, m/s (0 if non-positive net force).
    gage_force_N : float
        Initial gage force approximation, N (buoyant - correction).
    failed : bool
        True if the run encountered non-positive net force or no samples.
    """
    total_mass_kg = CONSTANT_MASS_KG + helium_mass_kg  # [kg]

    position_m = start_alt_m  # [m]
    velocity_mps = 0.0        # [m/s]

    velocity_history_mps: list[float] = []
    gage_force_N = float("nan")

    step_index = 0
    while position_m < burst_alt_m:
        atm = atmosphere_at_position(position_m)

        buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg, atm=atm)  # [N]
        drag_force_N = drag_force_f(velocity_mps, helium_mass_kg, position_m, atm=atm)  # [N]
        gravity_force_N = gravity_force_f(position_m, total_mass_kg)  # [N]
        correction_force_N = force_correction_f(helium_mass_kg, position_m)  # [N]

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N  # [N]

        if step_index == 0:
            gage_force_N = buoyant_force_N - correction_force_N  # [N]

        if net_force_N <= 0.0:
            return 0.0, gage_force_N, True

        acceleration_mps2 = net_force_N / total_mass_kg  # [m/s^2]
        velocity_mps += acceleration_mps2 * TIME_STEP_S  # [m/s]
        position_m += velocity_mps * TIME_STEP_S         # [m]

        velocity_history_mps.append(velocity_mps)
        step_index += 1

    if len(velocity_history_mps) == 0:
        return 0.0, gage_force_N, True

    return float(np.mean(velocity_history_mps)), gage_force_N, False


def solve_helium_mass(
    start_alt_m: float,
    burst_alt_m: float,
    target_rate_mps: float,
) -> tuple[float | None, float, float]:
    """Binary-search helium mass required to meet target mean ascent rate."""
    max_rate_mps, max_gage_force_N, max_failed = simulate_ascent_rate(
        start_alt_m, burst_alt_m, MAX_HELIUM_MASS_KG
    )
    if max_failed or max_rate_mps < target_rate_mps:
        return None, max_rate_mps, max_gage_force_N

    lower_mass_kg, upper_mass_kg = 0.0, MAX_HELIUM_MASS_KG
    best_mass_kg, best_rate_mps, best_gage_force_N = upper_mass_kg, max_rate_mps, max_gage_force_N

    for _ in range(MAX_BINARY_ITERS):
        mid_mass_kg = 0.5 * (lower_mass_kg + upper_mass_kg)
        rate_mps, gage_force_N, failed = simulate_ascent_rate(start_alt_m, burst_alt_m, mid_mass_kg)

        if failed or rate_mps < target_rate_mps:
            lower_mass_kg = mid_mass_kg
            continue

        upper_mass_kg = mid_mass_kg
        best_mass_kg, best_rate_mps, best_gage_force_N = mid_mass_kg, rate_mps, gage_force_N

        if round(best_rate_mps, RATE_DECIMALS) == round(target_rate_mps, RATE_DECIMALS):
            break
        if (upper_mass_kg - lower_mass_kg) < 0.5 * 10 ** (-RATE_DECIMALS):
            break

    return best_mass_kg, best_rate_mps, best_gage_force_N


def main() -> None:
    """CLI entry point."""
    burst_alt_m = float(input("Burst Altitude [m]: "))
    start_alt_m = float(input("Starting Altitude [m]: "))
    target_rate_mps = float(input("Desired Ascent Rate [m/s]: "))

    if (
        start_alt_m < 0.0
        or burst_alt_m <= start_alt_m
        or target_rate_mps <= 0.0
        or burst_alt_m > MAX_USSA76_ALT_M
    ):
        raise SystemExit("Invalid inputs.")

    best_mass_kg, best_rate_mps, best_gage_force_N = solve_helium_mass(start_alt_m, burst_alt_m, target_rate_mps)

    if best_mass_kg is None:
        print("\nMAX helium insufficient.")
        print(f"MAX helium mass [kg]: {MAX_HELIUM_MASS_KG:.4f}")
        print(f"MAX achieved ascent rate [m/s]: {best_rate_mps:.4f}")
        print(f"Initial net force at MAX mass [N]: {best_gage_force_N:.4f}")
        return

    print(f"\nMass for target rate [kg]: {best_mass_kg:.4f}")
    print(f"Initial net force for target rate [N]: {best_gage_force_N:.4f}")
    print(f"Final achieved ascent rate [m/s]: {best_rate_mps:.4f}")

    simulate_ascent_motion_f(
        helium_mass_kg=best_mass_kg,
        start_altitude_m=start_alt_m,
        max_altitude_m=burst_alt_m,
        time_step_s=TIME_STEP_S,
        constant_mass_kg=CONSTANT_MASS_KG,
        make_plots=True,
        log_scale_plots=False,
        hard_stop_on_nonpositive_net_force=True,
    )


if __name__ == "__main__":
    main()
