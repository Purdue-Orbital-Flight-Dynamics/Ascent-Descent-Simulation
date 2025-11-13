function area = cross_sectional_area_parachute(altitude, helium_mass)
%{
Calculates the cross sectional area of the parachute.
Assumes the balloon is a perfect sphere.
Assumes ideal gas law applies.
Assumes external and internal pressures are equivalent.
Assumes external and internal temperatures are equivalent.

Garion Cheng
Samuel Landers
%}

% (1) calculate temperature and pressure
temp_data = temperature(altitude);
t = temp_data(1);
temp_inital = temp_data(2);
slope = temp_data(3);
p = external_pressure(altitude, T, temp_inital, slope);

% (2) calculate mols of helium
HELIUM_MOLAR_MASS = 0.00400261;
n = helium_mass / HELIUM_MOLAR_MASS;

% (3) utilize ideal gas law to calculate volume of gas
R = 8.314; %J/(mol*k)
v = n*R*t/p;

% (4) use volume to calculate cross setional area of the sphere
radius = (3 * v / (4 * pi))^(1 / 3);
area = pi * (radius^2);
end