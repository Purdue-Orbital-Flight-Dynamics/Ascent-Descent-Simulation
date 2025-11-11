function pressure = external_pressure(altitude, T_calculated, T_initial, Lmb)
<<<<<<< HEAD

% *************************************************************************
% Purdue Orbital, Flight Dynamics, Ascent Modeling
% 
% Function Name: external_pressure
% File Name: external_pressure.m
%
% Contributors: Garion, Liam
% Date Started: 10/?/2025
% Last Updated: 11/10/2025
%
% Function Description: This function will accept an input altitude (in 
% geopotential meters) and return a pressure (in Pascals) for altitudes 
% between 0 and 100000 geometric meters. Pressure and altitude values 
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
% - altitude: alitutude in geometric meters
% - T_calculated: calculated temperature at above altitude
% - T_initial: initial temperature the atmospheric layer
% - Lmb: lapse rate
% 
% Output variables: 
% - pressure: calculated pressure
%
% *************************************************************************
=======
%{
Calculates the environmental pressure based on temperature data.

Garion Cheng
Liam Shepard
Samuel Landers
%}

R = 287;
G_0 = 9.80665;
>>>>>>> d7cc8e004ef7ac3d8cbb8f9197f1ecf03be6a493

if altitude < 11100 % first gradient
    pressure_initial = 1.01325*10^3; % mBar
    pressure = pressure_initial*(T_calculated/T_initial)^-(G_0/Lmb/R);
elseif altitude < Z2H(20000) % first pause
    pressure_initial = 2.2346*10^2;
    pressure = pressure_initial * e.^-((G_0/R/216.65)*(altitude*1000-11100)); % 216 is the pause temp
elseif altitude < Z2H(47400) % second gradient
    pressure_initial = 5.5292*10;
    pressure = pressure_initial*(T_calculated/T_initial)^-(G_0/Lmb/R);
elseif altitude < Z2H(51000) % second pause
    pressure_initial = 7.0458 * 10^-1;
    pressure = pressure_initial * e.^-((G_0/R/270.65)*(altitude*1000-11100)); % 270.65is the pause temp
end
end



