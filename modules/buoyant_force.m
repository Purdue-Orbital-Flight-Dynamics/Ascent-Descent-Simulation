
%{

TODO add detailed description of what the file does here
Function: This calculates the bouyant force acting on the balloon. Pulls in
 density of the balloon from densityBalloon module, density of air is pulled from densityAir module, 
 universal gas constant and molar mass of helium are defined here.

Contributors: Aanand Shah

%}

function F_buoyant = buoyant_force(external_pressure, temperature, pressure, molWeight, temp, altitude)

    density_b = density_balloon(external_pressure, temperature);  % [kg/m^3] 
    density_a = density_air(pressure, molWeight, temp);           % [kg/m^3]

    g = gravitational_acceleration(altitude);                     % [m/s^2]
    vol =  volume();                                              % [m^3]

    % Calculate the buoyant force using Archimedes' principle
    F_buoyant = (density_a - density_b) * vol * g;                % [N]

end