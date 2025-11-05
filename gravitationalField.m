%{

Description:
Takes altitude in meters and calculates acceleration due to gravity at given altitude.

Contributors:
Jack Triglianos

Source:
https://www.vcalc.com/wiki/gravity-acceleration-by-altitude

%}

function g_alt = gravitationalField(altitude) % altitude in m

    format long
    g = 9.80665; % gravity at sea level (m/s^2)
    r = 6371009; % mean radius of Earth (m)

    g_alt = g * (r / (r + altitude))^2; % m/s^2

end
