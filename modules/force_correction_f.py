########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent Modeling
#
# Function Name: force_correction_f
# File Name: force_correction_f.py
#
# Contributors: Eric Umminger
# Date Created: 12/01/2025
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes the correction force to convert buoyant force into an initial
#   gage force during inflation/measurement, accounting for helium mass and
#   additional attached masses (balloon, neck system, rope slack, etc.):
#       F_corr = (m_misc + m_He) * g(h)
#
# References:
#   None
#
# Input variables:
# - helium_mass_kg: helium mass, kg, non-negative
# - position_m: geometric altitude, m, non-negative
#
# Output variables:
# - correction_force_N: correction force magnitude, N, non-negative
#
########################################################################

from __future__ import annotations

from modules.gravity_acceleration_f import gravity_acceleration_f

# NOTE: These are placeholders until measured values are provided.
BALLOON_MASS_KG = 0.0  # [kg]
NECK_MASS_KG = 0.0     # [kg] neck closure system only
ROPE_MASS_KG = 0.0     # [kg] rope slack when inflating balloon
OTHER_MASS_KG = 0.0    # [kg] any other masses to include


def force_correction_f(helium_mass_kg: float, position_m: float) -> float:
    """Return correction force magnitude (N)."""
    correction_mass_kg = BALLOON_MASS_KG + NECK_MASS_KG + ROPE_MASS_KG + OTHER_MASS_KG + helium_mass_kg  # [kg]
    gravity_mps2 = gravity_acceleration_f(position_m)  # [m/s^2]
    correction_force_N = correction_mass_kg * gravity_mps2  # [N]
    return float(correction_force_N)
