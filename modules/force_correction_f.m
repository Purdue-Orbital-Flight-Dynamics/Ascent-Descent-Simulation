function [correction_force_N] = force_correction_f(helium_mass_kg, position_m)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: force_correction_f
% File Name: force_correction_f
%
% Contributors: Eric Umminger
% Date Created: 12/1/2025
% Last Updated: 12/1/2025
%
% Function Description: This function will calculate the force due to the masses
% of helium, the balloon, the neck system, and other miscellaneous masses.
% 
% References: N/A
%
% Input variables:
% - helium_mass_kg: altitude, in meters, positive
% - position_m: force measured from force meter, in Newtons, positive
%
% Output variables: 
% - helium_mass: helium mass, in kilograms, positive
% 
%************************************************************************

% Constants
BALLOON_MASS_KG = 0; % in kg
NECK_MASS_KG = 0; % in kg, neck closure system only
ROPE_MASS_KG = 0; % in kg, rope slack when inflating balloon
OTHER_MASS_KG = 0; % in kg, any other masses to include

% Calculations
correction_mass_kg = BALLOON_MASS_KG + NECK_MASS_KG + ROPE_MASS_KG + OTHER_MASS_KG + helium_mass_kg; % in kg
gravity_acceleration_mps2 = gravity_acceleration_f(position_m); % in m/s^2

correction_force_N = correction_mass_kg * gravity_acceleration_mps2; % in N


