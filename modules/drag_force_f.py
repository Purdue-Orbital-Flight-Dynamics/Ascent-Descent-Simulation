########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: drag_force_f
# File Name: drag_force_f.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes aerodynamic drag magnitude on the balloon using:
#       D = 0.5 * C_D * rho * A * v^2
#
# Notes:
#   - Returns magnitude (always non-negative). Direction must be applied by
#     the calling code based on velocity sign.
#
# References:
#   None
#
# Input variables:
# - velocity_mps: vertical velocity, m/s, sign varies
# - helium_mass_kg: helium mass in balloon, kg, non-negative
# - altitude_m: geometric altitude, m, non-negative
# - atm: atmosphere dict (SI) from modules.atmosphere.atmosphere_m, must include:
#       - rho_kgm3 (kg/m^3)
#
# Output variables:
# - drag_force_N: drag force magnitude, N, non-negative
#
########################################################################

from __future__ import annotations

from modules.balloon_cross_sectional_area_f import balloon_cross_sectional_area_f

DRAG_COEFF_SPHERE = 0.47  # [-] representative sphere drag coefficient


def drag_force_f(velocity_mps: float, helium_mass_kg: float, altitude_m: float, *, atm: dict) -> float:
    """Return drag magnitude in newtons."""
    air_density_kgm3 = float(atm["rho_kgm3"])  # [kg/m^3]
    area_m2 = balloon_cross_sectional_area_f(altitude_m, helium_mass_kg, atm=atm)  # [m^2]

    drag_force_N = 0.5 * DRAG_COEFF_SPHERE * air_density_kgm3 * area_m2 * (velocity_mps ** 2)  # [N]
    return float(drag_force_N)
