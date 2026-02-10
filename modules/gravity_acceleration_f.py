########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: gravity_acceleration_f
# File Name: gravity_acceleration_f.py
#
# Contributors: Jack Triglianos, Samuel Landers
# Date Created: 11/??/2025
# Last Updated: 02/09/2026
#
# Function Description:
#   Computes gravitational acceleration at a given geometric altitude using
#   an inverse-square law based on Earth's mean radius:
#       g(h) = g0 * (R / (R + h))^2
#
# References:
#   vCalc. (n.d.). Gravity acceleration by altitude.
#   https://www.vcalc.com/wiki/gravity-acceleration-by-altitude
#
# Input variables:
# - altitude_m: geometric altitude above Earth's surface, m, non-negative
#
# Output variables:
# - gravity_mps2: gravitational acceleration, m/s^2, positive
#
########################################################################

from __future__ import annotations

STANDARD_GRAVITY_MPS2 = 9.80665   # [m/s^2]
EARTH_RADIUS_M = 6_371_009.0      # [m] mean Earth radius


def gravity_acceleration_f(altitude_m: float) -> float:
    """Return gravitational acceleration magnitude (m/s^2)."""
    gravity_mps2 = STANDARD_GRAVITY_MPS2 * (EARTH_RADIUS_M / (EARTH_RADIUS_M + altitude_m)) ** 2  # [m/s^2]
    return float(gravity_mps2)
