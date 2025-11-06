%{

Contributors:
Garion, Eric, Jack

Created:
11/5/2025

Updated:
11/5/2025

Description:
    Calculates mass of helium

INPUTS: 
-   Initial Altitude                [m]
-   Initial Buoyancy Force          [N]

OUTPUTS: 
- Mass of Helium                    [kg]

%}

function mass = helium_mass(initial_altitude, initial_buoyancy_f)

    temp_data = temperature(initial_altitude);
    temp = temp_data(1);
    temp_inital = temp_data(2);
    slope = temp_data(3);
    pressure = external_pressure(initial_altitude, temp, temp_inital, slope);
    mol_weight = molecular_weight_air();

    density_b = density_balloon(pressure, temp); % in kg/m^3
    density_a = density_air(pressure, mol_weight, temp);
    gravity = gravitational_acceleration(initial_altitude); % in m/s^2

    volume = initial_buoyancy_f / (density_a - density_b) / gravity;
    mass = density_b * volume;
