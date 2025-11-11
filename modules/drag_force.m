function f_d = drag_force(velocity, helium_mass, altitude)
%{
Calculates drag force on balloon using the standard drag coefficient of a sphere.
Assumes the balloon to be a perfect sphere.
Assumes a drag coefficient of 0.47, when the true value can range from 0.07 to 0.5.

https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/

Jack Triglianos
Samuel Landers
%}

% (1) get the air density
air_density = density_air(altitude);

% (2) get the cross sectional area of the balloon
cross_sec_area = cross_sectional_area(altitude, helium_mass);

% (3) calculate drag force
DRAG_COEFFICIENT = 0.47;
f_d = 0.5 * DRAG_COEFFICIENT * air_density * cross_sec_area * velocity;
end