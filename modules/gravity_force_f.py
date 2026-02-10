########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent Modeling
#
# Function Name: gravity_force_f
# File Name: gravity_force_f.py
#
# Contributors: Jack Triglianos, Samuel Landers
# Date Created: 10/??/2025
# Last Updated: 02/09/2026
#
# Function Description:
#   Calculates gravitational force magnitude:
#       F_g = m * g(h)
#
# References:
#   None
#
# Input variables:
# - altitude_m: geometric altitude, m, non-negative
# - system_mass_kg: total system mass, kg, positive
#
# Output variables:
# - gravity_force_N: gravitational force magnitude, N, positive
#
########################################################################

from __future__ import annotations

from modules.gravity_acceleration_f import gravity_acceleration_f


def gravity_force_f(altitude_m: float, system_mass_kg: float) -> float:
    """Return gravitational force magnitude (N)."""
    gravity_force_N = gravity_acceleration_f(altitude_m) * system_mass_kg  # [N]
    return float(gravity_force_N)
