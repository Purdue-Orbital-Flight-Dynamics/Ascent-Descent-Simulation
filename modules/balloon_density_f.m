function density_b = balloon_density_f(altitude)

%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: balloon_density_f
% File Name: balloon_density_f.m
%
% Contributors: Aanand Shah, Samuel Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description:
%   Computes the density of helium inside the balloon assuming ideal gas
%   behavior and equilibrium between internal and external temperature
%   and pressure.
%
% Input variables:
% - altitude: geometric altitude, m, positive
%
% Output variables:
% - density_b: helium density inside the balloon, kg/m^3, positive
%
%************************************************************************

% Compute temperature and pressure
[temperature, temperature_initial, lapse_rate] = temperature_f(altitude); % K, K, K/m
pressure = external_pressure(altitude, temperature, temperature_initial, lapse_rate); % Pa

% Constants (SI mol-based)
GAS_CONSTANT = 8.314462618; % J/(mol·K)
HELIUM_MOLAR_MASS = 0.00400261; % kg/mol

% Density from ideal gas law
density_b = (pressure * HELIUM_MOLAR_MASS) / (GAS_CONSTANT * temperature); % kg/m^3
