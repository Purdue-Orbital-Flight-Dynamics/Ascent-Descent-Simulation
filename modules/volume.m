%{

TODO add detailed description of what the file does here
This function calculates the volume of the balloon based on its density and the mass 
which is pulled from system mass.

Contributors: Aanand Shah

%}
function vol = volume(altitude)

    mass = helium_mass();                                        % [kg]

    temp_data = temperature(altitude);
    temp = temp_data(1);
    temp_inital = temp_data(2);
    slope = temp_data(3);
    pressure = external_pressure(altitude, temp, temp_inital, slope);

    density_b = density_balloon(pressure, temp); % [kg/m^3]

    vol = mass / density_b;                                      % [m^3]
end
