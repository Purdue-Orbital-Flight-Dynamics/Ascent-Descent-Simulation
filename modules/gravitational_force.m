%{

Takes altitude in meters and mass in kg: calculates force due to gravity at given altitude.

Sources
https://www.vcalc.com/wiki/gravity-acceleration-by-altitude

Contributors
Jack Triglianos
Sam Landers

%}

function g_f = gravitational_force(altitude, mass)

    % Gravity at sea level 
    g = 9.80665;                        % [m/s^2]
    % Mean radius of Earth 
    r = 6371009;                        % [m]

    gravitational_acceleration = g * (r / (r + altitude))^2; % [m/s^2]

    g_f = gravitational_acceleration * mass;
end