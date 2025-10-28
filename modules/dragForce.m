%{

TODO: Estimate drag coefficient, potentially require Reynolds number as an argument to calculate drag coefficient

Contributors:
Jack Triglianos

Created:
10/15/2025

Updated:
10/15/2025

INPUTS: Current air density in kilograms / meters ^ 3, cross sectional area of ballon in meters ^ 2, velocity in meters / second ^ 2

OUTPUTS: Drag force

Sources:
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/ 

%}



function f_d = calc_drag_force(air_density, cross_sec_area, velocity)
    
    % Can change in future if necessary
    % Should be around 0.07 - 0.5
    DRAG_COEFFICIENT = 0.47; % Drag coefficient for a sphere (approximate for balloon)

    f_d = 0.5 * DRAG_COEFFICIENT * air_density * cross_sec_area * velocity;