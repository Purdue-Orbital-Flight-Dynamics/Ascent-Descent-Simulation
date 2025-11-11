function mass = helium_mass(initial_altitude, initial_buoyancy_f)
%{
Calculates the required mass of helium to attain a certain bouyant
force at a given altittude.

Garion Cheng
Eric Umminger
Jack Triglianos
Samuel Landers
%}

% (1) calculate temperature and pressure
[temperature_K, t_initial, slope_variable]= temperature(initial_altitude);
temp_data = [temperature_K, t_initial, slope_variable];
temp = temp_data(1);
temp_inital = temp_data(2);
slope = temp_data(3);
pressure = external_pressure(initial_altitude, temp, temp_inital, slope);

% (2) get the molecular weight of the air
mol_weight = molecular_weight_air();

% (3) calculate the density of the air and within the balloon
density_b = density_balloon(pressure, temp); % in kg/m^3
density_a = density_air(pressure, mol_weight, temp);

% (4) get the gravitational acceleration
gravity = gravitational_acceleration(initial_altitude); % in m/s^2

% (5) calculate volume of the balloon
volume = initial_buoyancy_f / (density_a - density_b) / gravity;

% (6) use volume and desnity to determine the mass of the balloon
mass = density_b * volume;
end
