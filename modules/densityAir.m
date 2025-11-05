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

function densityAir = densityAir(pressure, temp)
molecularWeight = molecularWeightAir();
gas_const = 8.31432e3; % N * m / (kmol * k)

densityAir = (pressure * molecularWeight) / (gas_const * temp); % in kg/m^3

end