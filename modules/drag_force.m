%{

TODO: Estimate drag coefficient, potentially require Reynolds number as an argument to calculate drag coefficient

Contributors:
Jack Triglianos
Sam Landers

Created:
10/15/2025

Updated:
10/29/2025

Description:
    Calculates drag force on balloon using the standard drag coefficient of a sphere

INPUTS: 
-   Current surrounding air density [kg/m^3]
-   Coss sectional area of ballon   [m^2]
-   Velocity                        [m/s^2]

OUTPUTS: 
- Drag force                        [N]

Sources:
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-coefficient/ 

%}

function f_d = calc_drag_force(cross_sec_area, velocity)
    
    % Can change in future if necessary
    % Should be around 0.07 - 0.5
    DRAG_COEFFICIENT = 0.47; % Drag coefficient for a sphere (approximate for balloon)

    f_d = 0.5 * DRAG_COEFFICIENT * densityAir() * cross_sec_area * velocity;