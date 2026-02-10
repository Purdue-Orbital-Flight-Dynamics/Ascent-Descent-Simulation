########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: buoyant_force_f
# File Name: buoyant_force_f.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes buoyant force magnitude (Archimedes principle):
#       F_b = rho_air * V_balloon * g
#
# Notes:
#   - Returns magnitude (always non-negative).
#
# References:
#   None
#
# Input variables:
# - altitude_m: geometric altitude, m, non-negative
# - helium_mass_kg: helium mass in balloon, kg, non-negative
# - atm: atmosphere dict (SI) from modules.atmosphere.atmosphere_m, must include:
#       - rho_kgm3 (kg/m^3)
#
# Output variables:
# - buoyant_force_N: buoyant force magnitude, N, non-negative
#
########################################################################

from __future__ import annotations

from modules.gravity_acceleration_f import gravity_acceleration_f
from modules.volume_balloon_f import volume_balloon_f


def buoyant_force_f(altitude_m: float, helium_mass_kg: float, *, atm: dict) -> float:
    """Return buoyant force magnitude (N)."""
    air_density_kgm3 = float(atm["rho_kgm3"])  # [kg/m^3]
    gravity_mps2 = gravity_acceleration_f(altitude_m)  # [m/s^2]
    volume_m3 = volume_balloon_f(altitude_m, helium_mass_kg, atm=atm)  # [m^3]

    buoyant_force_N = air_density_kgm3 * volume_m3 * gravity_mps2  # [N]
    return float(buoyant_force_N)
