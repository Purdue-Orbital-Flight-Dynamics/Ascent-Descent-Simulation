function gravity_force = gravity_force_f(altitude, system_mass)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: gravity_force_f
% File Name: gravity_force_f
%
% Contributors: Jack Triglianos, Samuel Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function will calculate the magnitude of 
% gravitational force.
% 
% References: N/A
%
% Input variables:
% - altitude: altitude, in meters, positive
% - system_mass: total mass of system, in kilograms, positive
%
% Output variables: 
% - gravity_force: force of gravity, in Newtons, ALWAYS POSITIVE
% 
%************************************************************************

% Calculation
gravity_force = gravity_acceleration_f(altitude) * system_mass; % in N, magnitude of force

% THIS OUTPUTS A MAGNITUDE OF FORCE