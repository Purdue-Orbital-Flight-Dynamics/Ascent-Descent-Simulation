########################################################################
# Purdue Orbital, Flight Dynamics
# 
# Project Name: Ascent Modeling
# 
# Function Name: geometric_to_geopotential_f
# File Name: geometric_to_geopotential_f.py
#
# Contributors: Cayden
# Date Created: 10/??/2025
# Last Updated: 11/17/2025
#
# Function Description: This function will convert geometric altitude into
# geopotential altitude.
# 
# References:
#
# United States. National Oceanic and Atmospheric Administration. (1976). 
# U.S. Standard Atmosphere, 1976: NOAA-S/T 76-1562. U.S. Government
# Printing Office. Retrieved from https://www.ngdc.noaa.gov/stp/space-weat
# her/online-publications/miscellaneous/us-standard-atmosphere-1976/us-stan
# dard-atmosphere_st76-1562_noaa.pdf
#
# Input variables:
# - geometric_altitude: geometric altitude, in geometric meters, positive
#
# Output variables: 
# - geopotential_altitude: geopotential altitude, in geopotential meters, positive
# 
########################################################################

def geometric_to_geopotential_f(geometric_altitude):

    # Constant
    RADIUS_EARTH = 6356766  # in m, from NASA

    # Conversion
    geopotential_altitude = (geometric_altitude * RADIUS_EARTH) / (RADIUS_EARTH + geometric_altitude)

    return geopotential_altitude
