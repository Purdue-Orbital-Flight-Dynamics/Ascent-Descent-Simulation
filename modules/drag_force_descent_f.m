function f_d = dragForceDescent(velocity, altitude)
%{
Calculates drag force on balloon using the standard drag coefficient of a sphere.
Assumes the balloon to be a perfect sphere.
Assumes a drag coefficient of 0.47, when the true value can range from 0.07 to 0.5.

https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/
https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/rktvrecv.html

Jack Triglianos
Samuel Landers
Aanand Shah
%}

% (1) get the air density
air_density = density_air(altitude);

% (2) get the cross sectional area of the balloon
cross_sec_area = cross_sectional_area_parachute();

% (3) calculate drag force
% typical values of drag coefficient for a parachute is about 1.75
DRAG_COEFFICIENT = 1.75; 
f_d = 0.5 * DRAG_COEFFICIENT * air_density * cross_sec_area * velocity^2;
end