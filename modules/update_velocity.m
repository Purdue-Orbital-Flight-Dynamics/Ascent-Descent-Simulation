%{

Description:
Calculates an updated velocity based on previous velocity, current acceleration, and change in time since previous velocity update.

Contributors:
Jack Triglianos

Created:
10/15/2025

Updated:
10/15/2025

INPUTS: Initial velocity in meters / second, acceleration in meters / second ^ 2, change in time since last update

OUTPUTS: Updated velocity

%}

function v = update_velocity(initial_velocity, acceleration, delta_T)

    v = initial_velocity + (acceleration * delta_T);