%{

TODO add detailed description of what the file does here
This function calculates the volume of the balloon based on its density and the mass 
which is pulled from system mass.

Contributors: Aanand Shah

%}
function volume = volume()
    mass = system_mass(); % in kg placeholder for now
    densityB = densityBalloon(external_pressure, temperature); % in kg/m^3 placeholder for now

    volume = mass / densityB; % in m^3
end
