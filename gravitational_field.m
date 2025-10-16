%{

Description:
Takes altitude in meters and calculates acceleration due to gravity at given altitude.

Contributors:
Jack Triglianos

Created:
10/15/2025

Updated:
10/15/2025

INPUTS: Altitude in meters

OUTPUTS: Gravity at an altitude in meters / second ^ 2

Source:
https://www.vcalc.com/wiki/gravity-acceleration-by-altitude

%}

function g_alt = gravitational_field(altitude)

    format long
    g = 9.80665; % gravity at sea level (m/s^2)
    r = 6371009; % mean radius of Earth (m)

    g_alt = g * (r / (r + altitude))^2; % m/s^2

end
