%Helium Mass Calculator 
%Authors: Garion, Eric

% inputs: Buoyancy Force, Density of Air Initial, Gravitational
% Acceleration

function mass = HeliumMass(external_pressure, temperature, pressure, molWeight, temp, alt, Fb)

    densityB = densityBalloon(external_pressure,temperature); % in kg/m^3
    densityA = densityAir(pressure,molWeight,temp);
    gravityA = gravitationalAcceleration(altitude); % in m/s^2
    volume = F_buoyant/(densityA-densityB)/gravityA;
    mass = densityB*volume;




    