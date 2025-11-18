function [density] = air_density_f(altitude)
%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: air_density_f
% File Name: air_density_f.m
%
% Contributors: Cayden Varno, Jack Triglianos, Samuel Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description:
%   Computes atmospheric density at a given geometric altitude using the
%   equation of state for an ideal gas. Temperature and pressure are 
%   obtained from standard-atmosphere helper functions.
%
% References: N/A   
%
% Input variables:
% - altitude: geometric altitude, meters, positive
%
% Output variables:
% - density: air density at the specified altitude, kg/m^3, positive
%
%************************************************************************

% Constants
GAS_CONSTANT = 8.31432e3;  % Universal gas constant, N*m/(kmol*K)

molecular_weight = molecular_weight_air_f(); % kmol/kg
[temperature, initial_temperature, slope] = temperature_f(altitude);  % K, K, K/m
pressure = pressure_f(altitude, temperature, initial_temperature, slope); % Pa

density = (pressure * molecular_weight) / (GAS_CONSTANT * temperature); % kg/m^3
