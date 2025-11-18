function [area] = parachute_cross_sectional_area_f()

%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: parachute_cross_sectional_area_f
% File Name: parachute_cross_sectional_area_f.m
%
% Contributors: Samuel Landers
% Date Created: 11/??/2025
% Last Updated: 11/17/2025
%
% Function Description:
%   Returns the cross-sectional area of the parachute. The parachute size
%   is currently hardcoded based on expected mission design options.
%
% References:
%
% Input variables:
%   None
%
% Output variables:
% - area: parachute cross-sectional area, m^2, positive
%
%************************************************************************

PARACHUTE_AREA_FT2 = 15; % ft^2, parachute planform area
FT2_TO_M2 = 1 / 10.764; % m^2/ft^2

area = PARACHUTE_AREA_FT2 * FT2_TO_M2; % m^2
