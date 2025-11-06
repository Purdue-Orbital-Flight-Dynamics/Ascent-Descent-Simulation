%{

TODO add detailed description of what the file does here
This function calculates the density of the balloon based on internal pressure and temperature.
It pulls the temperature and pressure values from the main scirpts and uses the ideal gas law to calculate the 
denisity in kg/m^3. 

Molar mass and universal gas constant are defined here. 

Contributors: Aanand Shah

%}

function density_b = density_balloon(external_pressure, temperature)

    universal_gas_constant = 8.314462618;   % [J/(mol·K)]
    molar_mass_gas = 0.004002602;           % [kg/mol] for Helium
    density_b = (external_pressure * molar_mass_gas) / (universal_gas_constant * temperature); % [kg/m^3]

end