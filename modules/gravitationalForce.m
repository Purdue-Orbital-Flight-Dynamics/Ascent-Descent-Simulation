%{

Takes altitude in meters and mass in kg: calculates force due to gravity at given altitude.

Sources
https://www.vcalc.com/wiki/gravity-acceleration-by-altitude

Contributors
Jack Triglianos
Sam Landers

%}

function gravitational_force = gravitationalForce(altitude, mass)

    g = 9.80665; % gravity at sea level (m/s^2)
    r = 6371009; % mean radius of Earth (m)

    gravitational_acceleration = g * (r / (r + altitude))^2; % m/s^2

    gravitational_force = gravitational_acceleration * mass;
end