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

function density = density(pressure, molWeight, temp)

gas_const = 8.31432e3;

density = pressure * molWeight / gas_const / temp;

end