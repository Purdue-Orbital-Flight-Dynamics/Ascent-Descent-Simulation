########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: volume_balloon_f
# File Name: volume_balloon_f.py
#
# Contributors: Purdue Orbital Flight Dynamics Team
# Date Created: Unknown
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes the helium balloon volume using the helium density at altitude:
#       V = m_he / rho_he
#
# References:
#   None
#
# Input variables:
# - altitude_m: geometric altitude, m, non-negative
# - helium_mass_kg: helium mass, kg, non-negative
# - atm: atmosphere dict (SI) from modules.atmosphere.atmosphere_m, must include:
#       - T_K (K), p_Pa (Pa)
#
# Output variables:
# - volume_m3: balloon volume, m^3, non-negative
#
########################################################################

from __future__ import annotations

from modules.balloon_density_f import balloon_density_f


def volume_balloon_f(altitude_m: float, helium_mass_kg: float, *, atm: dict) -> float:
    """Return balloon volume (m^3) for a given helium mass and atmosphere."""
    helium_density_kgm3 = balloon_density_f(altitude_m, atm=atm)  # [kg/m^3]
    volume_m3 = helium_mass_kg / helium_density_kgm3              # [m^3]
    return float(volume_m3)
