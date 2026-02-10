########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: balloon_density_f
# File Name: balloon_density_f.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes helium density using the ideal gas law:
#       rho = (p * M) / (R * T)
#
# References:
#   None
#
# Input variables:
# - altitude_m: geometric altitude, m, non-negative (unused except for consistency)
# - atm: atmosphere dict (SI) from modules.atmosphere.atmosphere_m, must include:
#       - T_K (K)
#       - p_Pa (Pa)
#
# Output variables:
# - helium_density_kgm3: helium density, kg/m^3, positive
#
########################################################################

from __future__ import annotations

GAS_CONSTANT = 8.314462618      # [J/(mol*K)]
HELIUM_MOLAR_MASS = 0.00400261  # [kg/mol]


def balloon_density_f(altitude_m: float, *, atm: dict) -> float:
    """Return helium density (kg/m^3) assuming ideal gas behavior."""
    temperature_K = float(atm["T_K"])  # [K]
    pressure_Pa = float(atm["p_Pa"])   # [Pa]

    helium_density_kgm3 = (pressure_Pa * HELIUM_MOLAR_MASS) / (GAS_CONSTANT * temperature_K)  # [kg/m^3]
    return float(helium_density_kgm3)
