function [system_mass, helium_mass] = system_mass_f(initial_altitude, initial_buoyancy_force)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: system_mass_f
% File Name: system_mass_f.m
%
% Contributors: Sam Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function will calculate the total system 
% mass of the balloon-rocket system.
% 
% References: N/A
%
% Input variables:
% - initial_altitude: initial launch altitude, in meters, positive
% - initial_buoyancy_force: initial buoyancy force, in Newtons, positive
%
% Output variables: 
% - system_mass: total system mass, in kilograms, positive
% - helium_mass: calculated helium mass, in kilograms, positive
% 
%************************************************************************

% Constants
LAUNCH_STRUCTURE_MASS = 2.2; % in kg
FLIGHT_OPERATIONS_MASS = 2.2; % in kg, does not include helium mass
AVIONICS_MASS = 2.2; % in kg
MISCELLANEOUS_MASS = 2.2; % in kg

% Calculations
helium_mass = helium_mass_f(initial_altitude, initial_buoyancy_force); % in kg

system_mass = LAUNCH_STRUCTURE_MASS + FLIGHT_OPERATIONS_MASS + AVIONICS_MASS + MISCELLANEOUS_MASS + helium_mass; % in kg