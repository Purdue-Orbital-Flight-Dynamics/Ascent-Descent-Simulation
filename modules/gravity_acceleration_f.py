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
# Last Updated: 11/17/2025
#
# Function Description:
#   Computes gravitational acceleration at a given geometric altitude using
#   the inverse square law based on Earth's average radius.
#
# References:
#   vCalc. (n.d.). *Gravity acceleration by altitude*.
#   https://www.vcalc.com/wiki/gravity-acceleration-by-altitude
#
# Input variables:
# - altitude: geometric altitude above Earth's surface, m, positive
#
# Output variables:
# - g: gravitational acceleration at altitude, m/s^2, positive
#
########################################################################

def gravity_acceleration_f(altitude):

    G_0 = 9.80665  # m/s^2, standard gravity at sea level
    R_EARTH = 6371009  # m, average Earth radius

    gravity = G_0 * (R_EARTH / (R_EARTH + altitude)) ** 2  # m/s^2

    # THIS RETURNS A MAGNITUDE

    return gravity
