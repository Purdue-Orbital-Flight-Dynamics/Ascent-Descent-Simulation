function [helium_mass] = helium_mass_f(altitude, net_buoyancy_force)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: helium_mass_f
% File Name: helium_mass_f.m
%
% Contributors: Garion Cheng, Eric Umminger, Jack Triglianos, Samuel Landers
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function will calculate the mass of helium given 
% an altitude and buoyancy force.
% 
% References: N/A
%
% Input variables:
% - altitude: altitude, in meters, positive
% - net_buoyancy_force: force measured from force meter, in Newtons, positive
%
% Output variables: 
% - helium_mass: helium mass, in kilograms, positive
% 
%************************************************************************

% Calculations

% Other mass
BALLOON_MASS = 0; % in kg
NECK_MASS = 0; % in kg, neck closure system only
ROPE_MASS = 0; % in kg, rope slack when inflating balloon
OTHER_MASS = BALLOON_MASS + NECK_MASS + ROPE_MASS;

% Densities
balloon_density = balloon_density_f(altitude); % in kg/m^3
air_density = air_density_f(altitude); % in kg/m^3

% Acceleration
gravity_acceleration = gravity_acceleration_f(altitude); % in m/s^2

% Other weight
other_weight = OTHER_MASS * gravity_acceleration;

% Helium mass
helium_mass = (balloon_density * (net_buoyancy_force + other_weight)) / (gravity_acceleration * (air_density - balloon_density)); % in kg

