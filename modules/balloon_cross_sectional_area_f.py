########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: balloon_cross_sectional_area_f
# File Name: balloon_cross_sectional_area_f.py
#
# Contributors: Garion Cheng, Samuel Landers
# Date Created: 10/??/2025
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes cross-sectional area of a high-altitude balloon assuming:
#     - Balloon is a perfect sphere
#     - Ideal gas behavior
#     - Internal pressure equals external pressure
#     - Internal temperature equals external temperature
#
# Notes:
#   Updated to accept a precomputed `atm` dict from modules.atmosphere
#   to avoid recomputing temperature/pressure repeatedly inside timestep loops.
#
# References:
#   None
#
# Input variables:
# - altitude_m: geometric altitude, m, non-negative
# - helium_mass_kg: helium mass, kg, non-negative
# - atm: atmosphere dict (SI) from modules.atmosphere.atmosphere_m, must include:
#       - T_K (K)
#       - p_Pa (Pa)
#
# Output variables:
# - area_m2: balloon cross-sectional area, m^2, positive
#
########################################################################

from __future__ import annotations

import math

GAS_CONSTANT = 8.314462618      # [J/(mol*K)]
HELIUM_MOLAR_MASS = 0.00400261  # [kg/mol]


def balloon_cross_sectional_area_f(altitude_m: float, helium_mass_kg: float, *, atm: dict) -> float:
    """Return balloon cross-sectional area (m^2)."""
    temperature_K = float(atm["T_K"])  # [K]
    pressure_Pa = float(atm["p_Pa"])   # [Pa]

    helium_moles_mol = helium_mass_kg / HELIUM_MOLAR_MASS  # [mol]

    # Ideal gas: V = n R T / p
    volume_m3 = helium_moles_mol * GAS_CONSTANT * temperature_K / pressure_Pa  # [m^3]

    # Sphere radius then cross-sectional area
    radius_m = (3.0 * volume_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)  # [m]
    area_m2 = math.pi * radius_m * radius_m  # [m^2]
    return float(area_m2)
