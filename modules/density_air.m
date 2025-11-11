function air_density = density_air(altitude)
%{
Calculates the density of the air.

Cayden Varno
Jack Triglianos
Samuel Landers
%}

% (1) get the molecular weight of the air
molecular_weight = molecular_weight_air();

% (2) calculate temperature and pressure
temp_data = temperature(altitude);
temp = temp_data(1);
temp_initial = temp_data(2);
slope = temp_data(3);
pressure = external_pressure(altitude, temp, temp_initial, slope);

% (3) calculate density of air
GAS_CONSTANT = 8.31432e3; % [N * m / (kmol * k)]
air_density = (pressure * molecular_weight) / (GAS_CONSTANT * temp); % [kg/m^3]
end