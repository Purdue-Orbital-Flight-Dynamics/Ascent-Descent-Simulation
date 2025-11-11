function density_b = density_balloon(altitude)
%{
Calculates the density of the helium within the balloon.
Assumes ideal gas law applies.

Aanand Shah
Samuel Landers
%}

% (1) calculate temperature and pressure
[temperature_K, t_initial, slope_variable] = temperature(altitude);
temp_data = [temperature_K, t_initial, slope_variable];
temp = temp_data(1);
temp_inital = temp_data(2);
slope = temp_data(3);
pressure = external_pressure(altitude, temp, temp_inital, slope);

% (2) calculate density of the balloon
GAS_CONSTANT = 8.314462618; % [J/(mol·K)]
HELIUM_MOLAR_MASS = 0.00400261; % [kg/mol]
density_b = (pressure * HELIUM_MOLAR_MASS) / (GAS_CONSTANT * temp); % [kg/m^3]
end