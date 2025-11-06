
%{

TODO add detailed description of what the file does here
Function: This calculates the bouyant force acting on the balloon. Pulls in
 density of the balloon from densityBalloon module, density of air is pulled from densityAir module, 
 universal gas constant and molar mass of helium are defined here.

Contributors: Aanand Shah, Jack

%}

function F_buoyant = buoyant_force(altitude)

    temp_data = temperature(altitude);
    temp = temp_data(1);
    temp_inital = temp_data(2);
    slope = temp_data(3);
    pressure = external_pressure(altitude, temp, temp_inital, slope);
    mol_weight = molecular_weight_air();

    density_b = density_balloon(pressure, temperature);  % [kg/m^3] 
    density_a = density_air(pressure, mol_weight, temp);           % [kg/m^3]

    g = gravitational_acceleration(altitude);                     % [m/s^2]
    vol =  volume();                                              % [m^3]

    % Calculate the buoyant force using Archimedes' principle
    F_buoyant = (density_a - density_b) * vol * g;                % [N]

end