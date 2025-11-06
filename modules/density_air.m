% *************************************************************************
% Purdue Orbital, Flight Dynamics, Ascent Modeling
% 
% Function Name: density
% File Name: density.m
%
% Contributors: Cayden
% Date Started: 10/20/2025
% Last Updated: 10/20/2025
%
% Function Description: This function accepts an input of pressure,
% molecular weight, and temperature. Gas constant is hardcoded internally.
% Density is returned in kg/m^3.
%
% Output variables: 
% - density
% 
% *************************************************************************

% *************************************************************************
% 
% Constants
% - Gas Constant = 8.31432e3 N * m / (kmol * k)
% 
% *************************************************************************

function air_density = density_air(altitude)
    
    gas_const = 8.31432e3;                                            % [N * m / (kmol * k)]
    molecular_weight = molecular_weight_air();

    temp_data = temperature(altitude);
    temp = temp_data(1);
    temp_initial = temp_data(2);
    slope = temp_data(3);
    
    pressure = external_pressure(altitude, temp, temp_initial, slope);

    air_density = (pressure * molecular_weight) / (gas_const * temp); % [kg/m^3]