%crosssectionalArea 
%Authors: Garion

% This function assumes that the balloon is a perfect sphere, and that
% ideal gas laws apply, and that external temperature is equal to internal
% balloon temperature, and that the pressure external = pressure internal

% inputs: pressure external, temperature external, mass

function Area = cross_sectional_area(T,P,mass)

    n = mass/.00400261; %.004 is the molar mass of helium, mass is in kg

    R = 8.314; %J/(mol*k)

    V = n*R*T/P; %Ideal gas law

    radius = (3*V/(4*pi))^(1/3);

    Area = pi*radius^2;

end