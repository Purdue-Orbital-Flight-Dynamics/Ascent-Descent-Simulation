function g = gravitational_acceleration(altitude)
%{
Calculates the acceleration due to gravity at a given altitude.

https://www.vcalc.com/wiki/gravity-acceleration-by-altitude

Jack Triglianos
Samuel Landers
%}

G_0 = 9.80665; % [m/s^2] gravity at sea level
R_AVG = 6371009; % [m] avg. radius of the earth
g = G_0 * (R_AVG / (R_AVG + altitude))^2; % [m/s^2]
end
