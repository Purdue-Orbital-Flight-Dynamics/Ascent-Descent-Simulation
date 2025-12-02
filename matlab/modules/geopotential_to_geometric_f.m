function geometric_altitude = geopotential_to_geometric_f(geopotential_altitude)

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: geopotential_to_geometric_f
% File Name: geopotential_to_geometric_f.m
%
% Contributors: Cayden
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function will convert geopotential altitude into
% geometric altitude.
% 
% References: 
%
% United States. National Oceanic and Atmospheric Administration. (1976). 
% U.S. Standard Atmosphere, 1976: NOAA-S/T 76-1562. U.S. Government
% Printing Office. Retrieved from https://www.ngdc.noaa.gov/stp/space-weat
% her/online-publications/miscellaneous/us-standard-atmosphere-1976/us-stan
% dard-atmosphere_st76-1562_noaa.pdf
%
% Input variables:
% - geopotential_altitude: geopotential altitude, in geopotential meters, positive
%
% Output variables: 
% - geopmetric_altitude: geometric altitude, in geometric meters, positive
% 
%************************************************************************

% Constant
RADIUS_EARTH = 6356766; % in m, from NASA

% Conversion
geometric_altitude = (geopotential_altitude * RADIUS_EARTH) / (RADIUS_EARTH - geopotential_altitude);