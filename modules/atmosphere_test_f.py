#########################################################################
# Purdue Orbital, Flight Dynamics
#
# Project: Ascent Modeling
# 
# Function Name: 
# File Name: atmosphere_test_f.py
#
# Contributors: Eric Umminger
# Date Started: 2/4/2026
# Last Updated: 2/4/2026
#
# Function Description: 
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
# - 
#
# Output variables: 
# -
# 
#########################################################################

import math

#########################################################################
# 
# Constants
# 
#########################################################################

molecular_weight = 0.02897

# T7 constants (elliptical)
T_C = 263.1905  # in Kelvin, from NASA
C1 = -76.3232   # in Kelvin, from NASA
C2 = 19.9429    # in km, from NASA

# Temperature divides
T1_INITIAL = 288.150  # start of gradient
T1_FINAL = 216.650    # end of gradient
T2_INITIAL = T1_FINAL  # start of pause
T2_FINAL = T2_INITIAL  # end of pause
T3a_INITIAL = T2_FINAL  # start of gradient
T3a_FINAL = 228.650    # midpoint of gradient
T3b_INITIAL = T3a_FINAL  # midpoint of gradient
T3b_FINAL = 270.650    # end of gradient
T4_INITIAL = T3b_FINAL  # start of pause
T4_FINAL = T4_INITIAL   # end of pause
T5a_INITIAL = T4_FINAL  # start of gradient
T5a_FINAL = 214.650    # midpoint 1 of gradient
T5b_INITIAL = T5a_FINAL  # midpoint 2 of gradient
T5b_FINAL = 186.946    # end of gradient -----------------From wikipedia welknlesKNLREN
T6_INITIAL = T5b_FINAL  # start of pause
T6_FINAL = T6_INITIAL   # end of pause
T7_INITIAL = T6_FINAL   # start of gradient
# T7_FINAL = 197.16; % end of graph

# Altitude divides
A1_INITIAL = 0        # start of gradient
A1_FINAL = 11000      # end of gradient
A2_INITIAL = A1_FINAL  # start of pause
A2_FINAL = 20000      # end of pause
A3a_INITIAL = A2_FINAL  # start of gradient
A3a_FINAL = 32000     # midpoint of gradient
A3b_INITIAL = A3a_FINAL  # midpoint of gradient
A3b_FINAL = 47000     # end of gradient
A4_INITIAL = A3b_FINAL  # start of pause
A4_FINAL = 51000      # end of pause
A5a_INITIAL = A4_FINAL  # start of gradient
A5a_FINAL = 71000     # midpoint 1 of gradient
A5b_INITIAL = A5a_FINAL  # midpoint 2 of gradient
A5b_FINAL = 84852     # end of gradient
A6_INITIAL = A5b_FINAL  # start of pause
A6_FINAL = 89716      # end of pause
A7_INITIAL = A6_FINAL  # start of gradient (ellipse)
A7_FINAL = 100000     # end of graph

# Slopes
D1 = (T1_FINAL - T1_INITIAL) / (A1_FINAL - A1_INITIAL)     # in K/m
D3a = (T3a_FINAL - T3a_INITIAL) / (A3a_FINAL - A3a_INITIAL)  # in K/m
D3b = (T3b_FINAL - T3b_INITIAL) / (A3b_FINAL - A3b_INITIAL)  # in K/m
D5a = (T5a_FINAL - T5a_INITIAL) / (A5a_FINAL - A5a_INITIAL)  # in K/m
D5b = (T5b_FINAL - T5b_INITIAL) / (A5b_FINAL - A5b_INITIAL)  # in K/m

#########################################################################
# 
# Main program
# 
#########################################################################

# Converting to geopotential altitude
altitude_H = float(input("Enter geopotential altitude in meters -> "))
a7_initial_H = A7_INITIAL * 6356766 / (6356766 + A7_INITIAL)

# Layer 1 (gradient)
if altitude_H >= A1_INITIAL and altitude_H < A1_FINAL:
    temperature = D1 * (altitude_H - A1_INITIAL) + T1_INITIAL  # in K
    initial_temperature = T1_INITIAL  # in K
    slope_variable = D1  # unitless

# Layer 2 (pause)
elif altitude_H >= A2_INITIAL and altitude_H < A2_FINAL:
    temperature = T2_INITIAL  # in K
    initial_temperature = T2_INITIAL  # in K
    slope_variable = 0  # unitless

# Layer 3a (gradient)
elif altitude_H >= A3a_INITIAL and altitude_H < A3a_FINAL:
    temperature = D3a * (altitude_H - A3a_INITIAL) + T3a_INITIAL  # in K
    initial_temperature = T3a_INITIAL  # in K
    slope_variable = D3a  # unitless

# Layer 3a (gradient)
elif altitude_H >= A3b_INITIAL and altitude_H < A3b_FINAL:
    temperature = D3b * (altitude_H - A3b_INITIAL) + T3b_INITIAL  # in K
    initial_temperature = T3b_INITIAL  # in K
    slope_variable = D3b  # unitless

# Layer 4 (pause)
elif altitude_H >= A4_INITIAL and altitude_H < A4_FINAL:
    temperature = T4_INITIAL  # in K
    initial_temperature = T4_INITIAL  # in K
    slope_variable = 0  # unitless

# Layer 5a (gradient)
elif altitude_H >= A5a_INITIAL and altitude_H < A5a_FINAL:
    temperature = D5a * (altitude_H - A5a_INITIAL) + T5a_INITIAL  # in K
    initial_temperature = T5a_INITIAL  # in K
    slope_variable = D5a  # unitless

# Layer 5b (gradient)
elif altitude_H >= A5b_INITIAL and altitude_H < A5b_FINAL:
    temperature = D5b * (altitude_H - A5b_INITIAL) + T5b_INITIAL  # in K
    initial_temperature = T5b_INITIAL  # in K
    slope_variable = D5b  # unitless

# Layer 6 (pause)
elif altitude_H >= A6_INITIAL and altitude_H < A6_FINAL:
    temperature = T6_INITIAL  # in K
    initial_temperature = T6_INITIAL  # in K
    slope_variable = 0  # unitless

# Layer 7 (gradient, ellipse)
#elif altitude_H >= A7_INITIAL and altitude_H <= A7_FINAL:  # end of graph
#    temperature = T_C + C1 * (1 - ((altitude_Z - a7_initial_H) / C2) ** 2) ** 0.5  # in K
#    initial_temperature = T7_INITIAL  # in K
#    slope_variable = 0  # unitless

# All altitudes not within the range
else:
    print('Error: temperature function failed--altitude out of acceptable range')

GAS_CONSTANT = 287  # J/(kg·K)
G_0 = 9.80665       # m/s^2

if altitude_H < 11000:  # first gradient region
    pressure_initial = 1.01325e3  # mbar
    pressure_layer = pressure_initial * (temperature / initial_temperature) ** (-G_0 / (slope_variable * GAS_CONSTANT))  # mbar

elif altitude_H < 20000:  # first isothermal (pause) region
    pressure_initial = 2.2632e2  # mbar
    pressure_layer = pressure_initial * math.exp(-(G_0 / (GAS_CONSTANT * 216.65)) * (altitude_H - 11000))  # mbar

elif altitude_H < 32000: # second gradient region a
    pressure_initial = 54.7489  # mbar
    pressure_layer = pressure_initial * (temperature / initial_temperature) ** (-G_0 / (slope_variable * GAS_CONSTANT))  # mbar

elif altitude_H < 47000:  # second gradient region b
    pressure_initial = 8.68019 # mbar
    pressure_layer = pressure_initial * (temperature / initial_temperature) ** (-G_0 / (slope_variable * GAS_CONSTANT))  # mbar

elif altitude_H < 51000:  # second isothermal (pause) region
    pressure_initial = 1.1090  # mbar
    pressure_layer = pressure_initial * math.exp(-(G_0 / (GAS_CONSTANT * 270.65)) * (altitude_H - 47000))  # mbar

else:
    # Optional: handle out-of-range altitudes; here we simply set NaN
    pressure_layer = float('nan')  # mbar

# x 100 to put in pascals
pressure = pressure_layer * 100 # Pa

density = (pressure * molecular_weight) / (8.31432 * temperature)  # kg/m^3

pressure = pressure / 100

print(f"Temperature [K]:           {temperature:.4f}")
print(f"Pressure [mbar]:           {pressure:.5e}")
print(f"Air Density [kg/m^3]:      {density:.5e}")
