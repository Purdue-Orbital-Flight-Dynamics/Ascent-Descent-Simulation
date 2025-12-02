########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: drag_force_f
# File Name: drag_force_f.m
#
# Contributors: Jack Triglianos, Samuel Landers
# Date Created: 11/??/2025
# Last Updated: 11/17/2025
#
# Function Description:
#   Computes the drag force acting on the balloon assuming the balloon
#   behaves as a sphere with a typical drag coefficient. Uses the standard
#   drag equation and atmospheric density as a function of altitude.
#
# References:
#   NASA Glenn Research Center. (n.d.). *Drag of a sphere*. 
#       https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/
#   NASA Glenn Research Center. (n.d.). *Drag coefficient*.
#       https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/
#
# Input variables:
# - velocity: descent or ascent velocity of balloon, m/s, magnitude varies
# - helium_mass: mass of helium inside balloon, kg, positive
# - altitude: geometric altitude above sea level, m, positive
#
# Output variables:
# - drag_force: aerodynamic drag force acting on balloon, N
#
########################################################################

from modules.air_density_f import air_density_f
from modules.balloon_cross_sectional_area_f import balloon_cross_sectional_area_f

def drag_force_f(velocity, helium_mass, altitude):

    # Air density at altitude
    air_density = air_density_f(altitude)  # kg/m^3

    # Balloon cross-sectional area
    cross_sectional_area = balloon_cross_sectional_area_f(altitude, helium_mass)  # m^2

    # Drag coefficient (sphere approximation)
    DRAG_COEFFICIENT = 0.47  # dimensionless

    # Drag force
    drag_force = 0.5 * DRAG_COEFFICIENT * air_density * cross_sectional_area * velocity**2  # N

    return drag_force
