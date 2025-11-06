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

<<<<<<< HEAD:modules/densityAir.m
function densityAir = densityAir(pressure, temp)
    molecularWeight = molecularWeightAir();
    gas_const = 8.31432e3; % N * m / (kmol * k)
=======
function air_density = density_air(pressure, temp)
molecular_weight = molecular_weight_air();
gas_const = 8.31432e3;                                            % [N * m / (kmol * k)]

air_density = (pressure * molecular_weight) / (gas_const * temp); % [kg/m^3]
>>>>>>> 8f00067dcd6f36c8a07522b1733ff699313b6b54:modules/density_air.m

    densityAir = (pressure * molecularWeight) / (gas_const * temp); % in kg/m^3
end