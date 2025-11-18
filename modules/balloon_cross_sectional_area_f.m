function [area] = balloon_cross_sectional_area_f(altitude, helium_mass)

%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: balloon_cross_sectional_area_f
% File Name: balloon_cross_sectional_area_f.m
%
% Contributors: Garion Cheng, Samuel Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description:
%   Computes the cross-sectional area of a high-altitude balloon assuming:
%   - Balloon is a perfect sphere
%   - Ideal gas behavior
%   - Internal pressure equals external pressure
%   - Internal temperature equals external temperature
%
% References: N/A
%
% Input variables:
% - altitude: geometric altitude, meters, positive
% - helium_mass: mass of helium in the balloon, kilograms, positive
%
% Output variables:
% - area: balloon cross-sectional area, m^2, positive
%
%************************************************************************

% Calculate temperature and external pressure at altitude
[temperature, initial_temperature, lapse_rate] = temperature_f(altitude); % K, K, K/m
pressure = external_pressure(altitude, temperature, initial_temperature, lapse_rate); % Pa

% Calculate amount of helium
HELIUM_MOLAR_MASS = 4.00261; % kg/kmol
helium_amount = helium_mass / HELIUM_MOLAR_MASS; % kmol

% Ideal gas law for volume
GAS_CONSTANT = 8.314e3; % J/(kmol·K)
gas_volume = helium_amount * GAS_CONSTANT * temperature / pressure; % m^3

% Convert volume to radius, then cross-sectional area
radius = (3 * gas_volume / (4 * pi))^(1/3); % m
area = pi * radius^2; % m^2
