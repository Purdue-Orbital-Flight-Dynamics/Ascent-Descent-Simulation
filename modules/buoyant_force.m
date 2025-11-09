function F_buoyant = buoyant_force(altitude, helium_mass)
%{
Calculates the density of helium within the balloon.

Aanand Shah
Jack Triglianos
%}

% (1) calculate temperature and pressure
temp_data = temperature(altitude);
temp = temp_data(1);
temp_inital = temp_data(2);
slope = temp_data(3);
pressure = external_pressure(altitude, temp, temp_inital, slope);

% (2) calculate density of the air and of the balloon
density_b = density_balloon(pressure, temperature);
density_a = density_air(altitude);

% (3) calculate the gravitational acceleration
g = gravitational_acceleration(altitude);

% (4) calculate the volume of the balloon
vol = volume(altitude, helium_mass);

% (5) Calculate the buoyant force using Archimedes' principle
F_buoyant = (density_a - density_b) * vol * g;
end