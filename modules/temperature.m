function [temperature_K, t_initial, slope_variable] = temperature(altitude_Z_m)
%{
Calculates the temperature (K) at a given altitude (m).

https://www.ngdc.noaa.gov/stp/space-weather/online-publications/miscellan
eous/us-standard-atmosphere-1976/us-standard-atmosphere_st76-1562_noaa.pdf

Eric Umminger
Cayden Varno
garion Cheng
%}

% *************************************************************************
% Purdue Orbital, Flight Dynamics, Ascent Modeling
% 
% Function Name: temperature
% File Name: temperature.m
%
% Contributors: Eric, Cayden, Garion
% Date Started: 10/27/2025
% Last Updated: 10/27/2025
%
% Function Description: This function will accept an input altitude (in 
% geometric meters) and return a temperature (in Kelvin) for altitudes 
% between 0 and 100000 geometric meters. Temperature and altitude values 
% and equations are taken from NASA's 1976 US standard atmosphere. 
% 
% Source: 
% 
% United States. National Oceanic and Atmospheric Administration. (1976). 
% U.S. Standard Atmosphere, 1976: NOAA-S/T 76-1562. U.S. Government
% Printing Office. Retrieved from https://www.ngdc.noaa.gov/stp/space-weat
% her/online-publications/miscellaneous/us-standard-atmosphere-1976/us-stan
% dard-atmosphere_st76-1562_noaa.pdf
%
% Input variables:
% - altitude_Z_m: altitude in geometric meters
%
% Output variables: 
% - temperature_K: calculated temperature
% - t_initial: Initial temperature for respective layer
% - slope_variable: 0 is pause, any other value is slope
% 
% *************************************************************************

% *************************************************************************
% 
% Constants
% 
% *************************************************************************

% T7 constants (elliptical)
T_C = 263.1905; % in Kelvin, from NASA
C1 = -76.3232; % in Kelvin, from NASA
C2 = 19.9429; % in km, from NASA

% Temperature divides
T1_INITIAL = 288.150; % start of gradient
T1_FINAL = 216.650; % end of gradient
T2_INITIAL = T1_FINAL; % start of pause
T2_FINAL = T2_INITIAL; % end of pause
T3a_INITIAL = T2_FINAL; % start of gradient
T3a_FINAL = 228.650; % midpoint of gradient 
T3b_INITIAL = T3a_FINAL; % midpoint of gradient
T3b_FINAL = 270.650; % end of gradient
T4_INITIAL = T3b_FINAL; % start of pause
T4_FINAL = T4_INITIAL; % end of pause
T5a_INITIAL = T4_FINAL; % start of gradient
T5a_FINAL = 214.650; % midpoint 1 of gradient
T5b_INITIAL = T5a_FINAL; % midpoint 2 of gradient
T5b_FINAL = 186.946; % end of gradient -----------------From wikipedia welknlesKNLREN
T6_INITIAL = T5b_FINAL; % start of pause
T6_FINAL = T6_INITIAL; % end of pause
T7_INITIAL = T6_FINAL; % start of gradient
% T7_FINAL = 197.16; % end of graph

% Altitude divides
A1_INITIAL = 0; % start of gradient
A1_FINAL = 11000; % end of gradient
A2_INITIAL = A1_FINAL; % start of pause
A2_FINAL = 20000; % end of pause
A3a_INITIAL = A2_FINAL; % start of gradient
A3a_FINAL = 32000; % midpoint of gradient
A3b_INITIAL = A3a_FINAL; % midpoint of gradient
A3b_FINAL = 47000; % end of gradient
A4_INITIAL = A3b_FINAL; % start of pause
A4_FINAL = 51000; % end of pause
A5a_INITIAL = A4_FINAL; % start of gradient
A5a_FINAL = 71000; % midpoint 1 of gradient
A5b_INITIAL = A5a_FINAL; % midpoint 2 of gradient
A5b_FINAL = 84852; % end of gradient
A6_INITIAL = A5b_FINAL; % start of pause
A6_FINAL = 89716; % end of pause
A7_INITIAL = A6_FINAL; % start of gradient (ellipse)
A7_FINAL = 100000; % end of graph

% Slopes
D1 = (T1_FINAL - T1_INITIAL) / (A1_FINAL - A1_INITIAL);
D3a = (T3a_FINAL - T3a_INITIAL) / (A3a_FINAL - A3a_INITIAL);
D3b = (T3b_FINAL - T3b_INITIAL) / (A3b_FINAL - A3b_INITIAL);
D5a = (T5a_FINAL - T5a_INITIAL) / (A5a_FINAL - A5a_INITIAL);
D5b = (T5b_FINAL - T5b_INITIAL) / (A5b_FINAL - A5b_INITIAL);

% *************************************************************************
% 
% Main program
% 
% *************************************************************************

% Coverting to geopotential altitude
altitude_H_m = Z2H(altitude_Z_m);
a7_initial_H = A7_INITIAL*6356766/(6356766+ A7_INITIAL);

% Layer 1 (gradient)
if altitude_H_m >= A1_INITIAL && altitude_H_m < A1_FINAL
    temperature_K = D1 * (altitude_H_m - A1_INITIAL) + T1_INITIAL;
    t_initial = T1_INITIAL;
    slope_variable = D1;

% Layer 2 (pause)
elseif altitude_H_m >= A2_INITIAL && altitude_H_m < A2_FINAL
    temperature_K = T2_INITIAL;
    t_initial = T2_INITIAL;
    slope_variable = 0;

% Layer 3a (gradient)
elseif altitude_H_m >= A3a_INITIAL && altitude_H_m < A3a_FINAL
    temperature_K = D3a * (altitude_H_m - A3a_INITIAL) + T3a_INITIAL;
    t_initial = T3a_INITIAL;
    slope_variable = D3a;

% Layer 3a (gradient)
elseif altitude_H_m >= A3b_INITIAL && altitude_H_m < A3b_FINAL
    temperature_K = D3b * (altitude_H_m - A3b_INITIAL) + T3b_INITIAL;
    t_initial = T3b_INITIAL;
    slope_variable = D3b;

% Layer 4 (pause)
elseif altitude_H_m >= A4_INITIAL && altitude_H_m < A4_FINAL
    temperature_K = T4_INITIAL;
    t_initial = T4_INITIAL;
    slope_variable = 0;

% Layer 5a (gradient)
elseif altitude_H_m >= A5a_INITIAL && altitude_H_m < A5a_FINAL
    temperature_K = D5a * (altitude_H_m - A5a_INITIAL) + T5a_INITIAL;
    t_initial = T5a_INITIAL;
    slope_variable = D5a;

% Layer 5b (gradient)
elseif altitude_H_m >= A5b_INITIAL && altitude_H_m < A5b_FINAL
    temperature_K = D5b * (altitude_H_m - A5b_INITIAL) + T5b_INITIAL;
    t_initial = T5b_INITIAL;
    slope_variable = D5b;

% Layer 6 (pause)
elseif altitude_H_m >= A6_INITIAL && altitude_H_m < A6_FINAL
    temperature_K = T6_INITIAL;
    t_initial = T6_INITIAL;
    slope_variable = 0;

% Layer 7 (gradient, ellipse)
elseif altitude_H_m >= A7_INITIAL && altitude_H_m <= A7_FINAL % end of graph
    temperature_K = T_C + C1 * (1 - ((altitude_Z_m - a7_initial_H) / C2) ^ 2) ^ 0.5;
    t_initial = T7_INITIAL;
    slope_variable = 0;

% All altitudes not within the range 
else
    fprintf(['Error: temperature function failed--altitude out of acceptable range']);
end

