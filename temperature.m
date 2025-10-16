function [temperature_K] = temperature(altitude_m)

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
T3_INITIAL = T2_FINAL; % start of gradient
T3_FINAL = 270.650; % end of gradient 
T4_INITIAL = T3_FINAL; % start of pause
T4_FINAL = T4_INITIAL; % end of pause
T5_INITIAL = T4_FINAL; % start of gradient
T5_FINAL = 186.870; % end of gradient
T6_INITIAL = T5_INITIAL; % start of pause
T6_FINAL = T6_INITIAL; % end of pause
T7_INITIAL = T6_FINAL; % start of gradient
T7_FINAL = 195.08; % end of graph

% Altitude divides
A1_INITIAL = 0; % start of gradient
A1_FINAL = 11100; % end of gradient
A2_INITIAL = A1_FINAL; % start of pause
A2_FINAL = 20000; % end of pause
A3_INITIAL = A2_FINAL; % start of gradient
A3_FINAL = 47400; % end of gradient
A4_INITIAL = A3_FINAL; % start of pause
A4_FINAL = 51000; % end of pause
A5_INITIAL = A4_FINAL; % start of gradient
A5_FINAL = 86000; % end of gradient
A6_INITIAL = A5_FINAL; % start of pause
A6_FINAL = 91000; % end of pause
A7_INITIAL = A6_FINAL; % start of gradient (ellipse)
A7_FINAL = 100000; % end of graph

% Slopes
D1 = (T1_FINAL - T1_INITIAL) / (A1_FINAL - A1_INITIAL);
D3 = (T3_FINAL - T3_INITIAL) / (A3_FINAL - A3_INITIAL);
D5 = (T5_FINAL - T5_INITIAL) / (A5_FINAL - A5_INITIAL);

% *************************************************************************
% 
% Main program
% 
% *************************************************************************

% If-elseif statements to determine temperature

% Layer 1 (gradient)
if altitude_m >= A1_INITIAL && altitude_m < A1_FINAL
    temperature_K = D1 * (altitude_m - A1_INITIAL) + T1_INITIAL;

% Layer 2 (pause)
elseif altitude_m >= A2_INITIAL && altitude_m < A2_FINAL
    temperature_K = T2_INITIAL;

% Layer 3 (gradient)
elseif altitude_m >= A3_INITIAL && altitude_m < A3_FINAL
    temperature_K = D3 * (altitude_m - A3_INITIAL) + T3_INITIAL;

% Layer 4 (pause)
elseif altitude_m >= A4_INITIAL && altitude_m < A4_FINAL
    temperature_K = T4_INITIAL;

% Layer 5 (gradient)
elseif altitude_m >= A5_INITIAL && altitude_m < A5_FINAL
    temperature_K = D5 * (altitude_m - A5_INITIAL) + T5_INITIAL;

% Layer 6 (pause)
elseif altitude_m >= A6_INITIAL && altitude_m < A6_FINAL
    temperature_K = T6_INITIAL;

% Layer 7 (gradient, ellipse)
elseif altitude_m >= A7_INITIAL && altitude_m <= A7_FINAL % end of graph
    temperature_K = T_C + C1 * (1 - ((altitude_m - A7_INITIAL) / C2) ^ 2) ^ 0.5;

% All altitudes not within the range 
else
    fprintf(['* * * * * ERROR * * * * *\n\nAltitude out of acceptable ' ...
        'range\nTemperature not calculated\n']);

end

% Got stuck, NASA and Anderson do not agree, will go with NASA
% 91-100 km use ellipse equation
