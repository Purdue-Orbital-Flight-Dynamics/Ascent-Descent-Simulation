function [temperature_K, t_initial, slope_variable] = temperature(altitude_m)

% *************************************************************************
% Purdue Orbital, Flight Dynamics, Ascent Modeling
% 
% Function Name: temperature
% File Name: temperature.m
%
% Contributors: Eric, Cayden, Garion
% Date Started: 10/8/2025
% Last Updated: 10/9/2025
%
% Function Description: This function will accept an input altitude (in 
% meters) and return a temperature (in Kelvin) for altitudes between 0 and 
% 100 km. Temperature and altitude values and equations are taken from 
% NASA's 1976 US standard atmosphere. 
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

T_C = 263.1905; % in Kelvin, from NASA
C1 = -76.3232; % in Kelvin, from NASA
C2 = 19.9429; % in km, from NASA


% Temperature divides
T1_INITIAL = 288.150; % start of gradient
T1_FINAL = 216.650; % end of gradient
T2_INITIAL = T1_FINAL; % start of pause
T2_FINAL = T2_INITIAL; % end of pause
T3a_INITIAL = T2_FINAL; % start of gradient
T3a_FINAL = 228.756; % midpoint of gradient 
T3b_INITIAL = T3a_FINAL; % midpoint of gradient
T3b_FINAL = 270.650; % end of gradient
T4_INITIAL = T3_FINAL; % start of pause
T4_FINAL = T4_INITIAL; % end of pause
T5a_INITIAL = T4_FINAL; % start of gradient
T5a_FINAL = 270.409; % midpoint 1 of gradient
T5b_INITIAL = T5a_FINAL; % midpoint 1 of gradient
T5b_FINAL = 215.477; % midpoint 2 of gradient
T5c_INITIAL = T5b_FINAL; % midpoint 2 of gradient
T5c_FINAL = 186.870; % end of gradient
T6_INITIAL = T5c_FINAL; % start of pause
T6_FINAL = T6_INITIAL; % end of pause
T7_INITIAL = T6_FINAL; % start of gradient
T7_FINAL = 195.08; % end of graph

% Altitude divides
A1_INITIAL = 0; % start of gradient
A1_FINAL = 11100; % end of gradient
A2_INITIAL = A1_FINAL; % start of pause
A2_FINAL = 20000; % end of pause
A3a_INITIAL = A2_FINAL; % start of gradient
A3a_FINAL = 32200; % midpoint of gradient
A3b_INITIAL = A3a_FINAL; % midpoint of gradient
A3b_FINAL = 47400; % end of gradient
A4_INITIAL = A3_FINAL; % start of pause
A4_FINAL = 51000; % end of pause
A5a_INITIAL = A4_FINAL; % start of gradient
A5a_FINAL = 51500; % midpoint 1 of gradient
A5b_INITIAL = A5a_FINAL; % midpoint 1 of gradient
A5b_FINAL = 71500; % midpoint 2 of gradient
A5c_INITIAL = A5b_FINAL; % midpoint 2 of gradient
A5c_FINAL = 86000; % end of gradient
A6_INITIAL = A5c_FINAL; % start of pause
A6_FINAL = 91000; % end of pause
A7_INITIAL = A6_FINAL; % start of gradient (ellipse)
A7_FINAL = 100000; % end of graph

% Slopes
D1 = (T1_FINAL - T1_INITIAL) / (A1_FINAL - A1_INITIAL);
D3a = (T3a_FINAL - T3a_INITIAL) / (A3a_FINAL - A3a_INITIAL);
D3b = (T3b_FINAL - T3b_INITIAL) / (A3b_FINAL - A3b_INITIAL);
D5a = (T5a_FINAL - T5a_INITIAL) / (A5a_FINAL - A5a_INITIAL);
D5b = (T5b_FINAL - T5b_INITIAL) / (A5b_FINAL - A5b_INITIAL);
D5c = (T5c_FINAL - T5c_INITIAL) / (A5c_FINAL - A5c_INITIAL);

% *************************************************************************
% 
% Main program
% 
% *************************************************************************

% Layer 1 (gradient)
if altitude_m >= A1_INITIAL && altitude_m < A1_FINAL
    temperature_K = D1 * (altitude_m - A1_INITIAL) + T1_INITIAL;
    t_initial = T1_INITIAL;
    slope_variable = D1;

% Layer 2 (pause)
elseif altitude_m >= A2_INITIAL && altitude_m < A2_FINAL
    temperature_K = T2_INITIAL;
    t_initial = T2_INITIAL;
    slope_variable = 0;

% Layer 3a (gradient)
elseif altitude_m >= A3a_INITIAL && altitude_m < A3a_FINAL
    temperature_K = D3a * (altitude_m - A3_INITIAL) + T3_INITIAL;
    t_initial = T3a_INITIAL;
    slope_variable = D3a;

% Layer 3a (gradient)
elseif altitude_m >= A3b_INITIAL && altitude_m < A3b_FINAL
    temperature_K = D3b * (altitude_m - A3b_INITIAL) + T3b_INITIAL;
    t_initial = T3b_INITIAL;
    slope_variable = D3b;

% Layer 4 (pause)
elseif altitude_m >= A4_INITIAL && altitude_m < A4_FINAL
    temperature_K = T4_INITIAL;
    t_initial = T4_INITIAL;
    slope_variable = 0;

% Layer 5 (gradient)
elseif altitude_m >= A5_INITIAL && altitude_m < A5_FINAL
    temperature_K = D5 * (altitude_m - A5_INITIAL) + T5_INITIAL;
    t_initial = T5_INITIAL;
    slope_variable = D5;

% Layer 6 (pause)
elseif altitude_m >= A6_INITIAL && altitude_m < A6_FINAL
    temperature_K = T6_INITIAL;
    t_initial = T6_INITIAL;
    slope_variable = 0;

% Layer 7 (gradient, ellipse)
elseif altitude_m >= A7_INITIAL && altitude_m <= A7_FINAL % end of graph
    temperature_K = T_C + C1 * (1 - ((altitude_m - A7_INITIAL) / C2) ^ 2) ^ 0.5;
    t_initial = T7_INITIAL;
    slope_variable = 0;

% All altitudes not within the range 
else
    fprintf(['* * * * * ERROR * * * * *\n\nAltitude out of acceptable ' ...
        'range\nTemperature not calculated\n']);

end

% Got stuck, NASA and Anderson do not agree, will go with NASA