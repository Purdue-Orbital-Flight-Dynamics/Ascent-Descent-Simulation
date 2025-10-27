
%{

TODO add detailed description of what the file does here

Contributors:

%}
function F_buoyant = buoyantForce(volume, densityAir, gravity, external_pressure, temperature,)
    % volume in m^3
    % fluidDensity in kg/m^3
    % gravity in m/s^2

    universal_gas_constant = 8.314462618; % J/(mol·K)
    molar_mass_gas = 0.004002602; % kg/mol for Helium
    densityBalloon = densityBalloon(external_pressure,temperature); % in kg/m^3 

    % Calculate the buoyant force using Archimedes' principle
    F_buoyant = (densityAir-densityBalloon) * volume * gravity; % in Newtons (N)

end