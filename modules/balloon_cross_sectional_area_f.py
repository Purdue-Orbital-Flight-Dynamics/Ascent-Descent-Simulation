# balloon_cross_sectional_area_f.py
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
#   Computes the cross-sectional area of a high-altitude balloon assuming:
#   - Balloon is a perfect sphere
#   - Ideal gas behavior
#   - Internal pressure equals external pressure
#   - Internal temperature equals external temperature
#
# Notes:
#   - Updated to optionally accept a precomputed `atm` dict from modules.atmosphere.Atmosphere
#     to avoid recomputing temperature/pressure repeatedly inside the timestep loop.
#
# Input variables:
# - altitude: geometric altitude, meters, positive
# - helium_mass: mass of helium in the balloon, kilograms, positive
# - atm: (optional) atmosphere dict (SI) from Atmosphere(...), containing T_K and p_Pa
#
# Output variables:
# - area: balloon cross-sectional area, m^2, positive
#
########################################################################

import math

def balloon_cross_sectional_area_f(altitude_m, helium_mass_kg, *, atm):
    """Return balloon cross-sectional area (m^2).

    Parameters
    ----------
    altitude_m : float
        Geometric altitude in meters.
    helium_mass_kg : float
        Helium mass in kilograms.
    atm : dict | None
        Optional atmosphere dict from modules.atmosphere.Atmosphere(...).
        Must contain keys: "T_K", "p_Pa".
    """

    # External conditions (assume internal equals external)
    T = float(atm["T_K"])      # K
    p = float(atm["p_Pa"])     # Pa

    # Amount of helium
    HELIUM_MOLAR_MASS = 0.00400261  # kg/mol
    n_mol = helium_mass_kg / HELIUM_MOLAR_MASS  # mol

    # Ideal gas law for volume: V = n R T / p
    GAS_CONSTANT = 8.314462618  # J/(mol·K)
    V = n_mol * GAS_CONSTANT * T / p  # m^3

    # Sphere radius and cross-sectional area
    r = (3.0 * V / (4.0 * math.pi)) ** (1.0 / 3.0)  # m
    return math.pi * r * r
