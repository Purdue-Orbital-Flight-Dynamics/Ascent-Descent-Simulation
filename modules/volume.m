%{

TODO add detailed description of what the file does here
This function calculates the volume of the balloon based on its density and the mass 
which is pulled from system mass.

Contributors: Aanand Shah

%}
function vol = volume()

    mass = system_mass();                                        % [kg]
    density_b = density_balloon(external_pressure, temperature); % [kg/m^3]

    vol = mass / density_b;                                      % [m^3]
end
