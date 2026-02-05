########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project Name: Ascent/Descent Modeling
#
# Function Name: pressure_f
# File Name: pressure_f.py
#
# Contributors: Garion Cheng, Liam Shepard, Samuel Landers, Eric Umminger
# Date Created: 10/??/2025
# Last Updated: 1/28/2026
#
# Function Description:
#   Computes the environmental (external) pressure as a function of
#   altitude and temperature using piecewise standard-atmosphere
#   relations. Valid for altitudes between 0 and 100000 geometric meters.
#
# References:
#   United States National Oceanic and Atmospheric Administration. (1976).
#   U.S. Standard Atmosphere, 1976: NOAA-S/T 76-1562. U.S. Government
#   Printing Office. https://www.ngdc.noaa.gov/stp/space-weather/
#   online-publications/miscellaneous/us-standard-atmosphere-1976/
#   us-standard-atmosphere_st76-1562_noaa.pdf
#
# Input variables:
# - altitude: geometric altitude, m, 0 ≤ altitude ≤ 100000
# - temperature_calculated: temperature at altitude, K, varies
# - temperature_initial: base-layer temperature, K, varies
# - lapse_rate: temperature lapse rate in layer, K/m, can be negative/zero
#
# Output variables:
# - pressure: external static pressure, Pa, positive
#
########################################################################

import math
from modules.geometric_to_geopotential_f import geometric_to_geopotential_f

def pressure_f(altitude_z, temperature_calculated, temperature_initial, lapse_rate):

    altitude = geometric_to_geopotential_f(altitude_z)
    GAS_CONSTANT = 287  # J/(kg·K)
    G_0 = 9.80665       # m/s^2

    if altitude < 11000:  # first gradient region
        pressure_initial = 1.01325e3  # mbar
        pressure_layer = pressure_initial * (temperature_calculated / temperature_initial) ** (-G_0 / (lapse_rate * GAS_CONSTANT))  # mbar

    elif altitude < 20000:  # first isothermal (pause) region
        pressure_initial = 2.2632e2  # mbar
        pressure_layer = pressure_initial * math.exp(-(G_0 / (GAS_CONSTANT * 216.65)) * (altitude - 11000))  # mbar

    elif altitude < 32000: # second gradient region a
        pressure_initial = 54.7489  # mbar
        pressure_layer = pressure_initial * (temperature_calculated / temperature_initial) ** (-G_0 / (lapse_rate * GAS_CONSTANT))  # mbar

    elif altitude < 47000:  # second gradient region b
        pressure_initial = 8.68019 # mbar
        pressure_layer = pressure_initial * (temperature_calculated / temperature_initial) ** (-G_0 / (lapse_rate * GAS_CONSTANT))  # mbar

    elif altitude < 51000:  # second isothermal (pause) region
        pressure_initial = 1.1090  # mbar
        pressure_layer = pressure_initial * math.exp(-(G_0 / (GAS_CONSTANT * 270.65)) * (altitude - 11000))  # mbar

    else:
        # Optional: handle out-of-range altitudes; here we simply set NaN
        pressure_layer = float('nan')  # mbar

    # x 100 to put in pascals
    pressure = pressure_layer * 100  # Pa

    return pressure
