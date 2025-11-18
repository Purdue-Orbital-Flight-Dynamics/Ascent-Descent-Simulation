function f_d = drag_force_descent_f(velocity, altitude)

%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: dragForceDescent
% File Name: dragForceDescent.m
%
% Contributors: Jack Triglianos, Samuel Landers, Aanand Shah
% Date Created: 11/??/2025
% Last Updated: 11/17/2025
%
% Function Description:
%   Computes the drag force acting on the balloon during descent. Assumes
%   the balloon behaves as a bluff body with a typical parachute drag
%   coefficient. Uses the standard drag equation.
%
% References:
%   NASA. (2024, July 19). Drag coefficient. NASA. https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/ 
%   NASA. (2025, June 30). Drag of a sphere. NASA. https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/ 
%   NASA. (n.d.). Velocity during recovery. NASA. https://www.grc.nasa.gov/WWW/k-12/VirtualAero/BottleRocket/airplane/rktvrecv.html 
%
% Input variables:
% - velocity: descent velocity of balloon, m/s
% - altitude: geometric altitude, m, positive
%
% Output variables:
% - f_d: drag force on balloon, N
%   
%************************************************************************  

% Get air density
air_density = air_density_f(altitude); % kg/m^3

% Get balloon cross-sectional area
cross_sec_area = cross_sectional_area_parachute_f(); % m^2

% Drag coefficient of balloon/parachute
DRAG_COEFFICIENT = 1.75; % dimensionless

% Compute drag force
f_d = 0.5 * DRAG_COEFFICIENT * air_density * cross_sec_area * velocity^2; % N
