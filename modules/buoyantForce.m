
%{

TODO add detailed description of what the file does here
Function: This calculates the bouyant force acting on the balloon. Pulls in
 density of the balloon from densityBalloon module, density of air is pulled from densityAir module, 
 universal gas constant and molar mass of helium are defined here.

Contributors: Aanand Shah

%}
function F_buoyant = buoyantForce(external_pressure, temperature, pressure, molWeight, temp, altitude)
    % volume in m^3
    % fluidDensity in kg/m^3
    % gravity in m/s^2


    densityB = densityBalloon(external_pressure,temperature); % in kg/m^3 
    densityA = densityAir(pressure, molWeight, temp); % in kg/m^3
    gravityA = gravitationalAcceleration(altitude); % in m/s^2
    volume =  volume(); % in m^3 placeholder for now

    % Calculate the buoyant force using Archimedes' principle
    F_buoyant = (densityA-densityB) * volume * gravityA; % in Newtons (N)

end