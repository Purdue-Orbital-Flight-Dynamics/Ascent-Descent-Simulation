function volume = volume_balloon_f(altitude, helium_mass)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modelling
% 
% Function Name: volume_balloon_f
% File Name: volume_balloon_f
%
% Contributors: Aanand Shah
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function will calculate the volume of the balloon
% for a given altitude and helium mass.
% 
% References: N/A
%
% Input variables:
% - altitude: geometric altitude, in meters, positive
%
% Output variables: 
% - volume: volume of balloon, in cubic meters, positive
% 
%************************************************************************

% Calculate density
density_balloon = balloon_density_f(altitude); % in kg/m^3

% Calculate volume
volume = helium_mass / density_balloon; % in m^3

