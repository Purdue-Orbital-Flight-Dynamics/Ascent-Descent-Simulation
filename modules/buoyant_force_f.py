#######################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: buoyant_force_f
# File Name: buoyant_force_f.py
#
# Contributors: Aanand Shah, Jack Triglianos
# Date Created: 11/??/2025
# Last Updated: 11/17/2025
#
# Function Description:
#   Computes the buoyant force acting on the balloon using Archimedes'
#   principle. Assumes ideal gas behavior and equilibrium between internal
#   and external pressure and temperature.
#
# References: 
#
# Input variables:
# - altitude: geometric altitude, m, positive
# - helium_mass: mass of helium in the balloon, kg, positive
#
# Output variables:
# - F_buoyant: buoyant force on the balloon, N
#
#######################################################################

from modules.air_density_f import air_density_f
from modules.gravity_acceleration_f import gravity_acceleration_f
from modules.volume_balloon_f import volume_balloon_f

def buoyant_force_f(altitude, helium_mass):

    # Compute density
    air_density = air_density_f(altitude)  # in kg/m^3

    # Compute gravitational acceleration
    gravity_acceleration = gravity_acceleration_f(altitude)  # in m/s^2

    # Compute balloon volume
    volume = volume_balloon_f(altitude, helium_mass)  # in m^3

    # Buoyant force (Archimedes)
    buoyant_force = (air_density) * volume * gravity_acceleration  # in N

    return buoyant_force
