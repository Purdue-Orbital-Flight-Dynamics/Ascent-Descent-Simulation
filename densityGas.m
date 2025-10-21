%{

TODO add detailed description of what the file does here

Contributors:

%}
function density_gas = densityGas(external_pressure, temperature)
    % volume in m^3
    % fluidDensity in kg/m^3
    % gravity in m/s^2

    universal_gas_constant = 8.314462618; % J/(mol·K)
    molar_mass_gas = 0.004002602; % kg/mol for Helium
    density_gas = (external_pressure*molar_mass_gas)/(universal_gas_constant*temperature); % in kg/m^3

end