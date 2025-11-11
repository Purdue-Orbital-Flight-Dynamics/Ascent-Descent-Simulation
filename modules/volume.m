function vol = volume(altitude, helium_mass)
%{
Calculates volume of the balloon using density and mass.

Aanand Shah
%}

density_b = density_balloon(altitude); % [kg/m^3]
vol = helium_mass / density_b; % [m^3]
end
