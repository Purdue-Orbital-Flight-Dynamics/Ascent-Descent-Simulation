%{

Description:
Calculates an updated altitude based on previous altitude, current velocity, and change in time since previous altitude update.

Contributors:
Jack Triglianos

Created:
10/15/2025

Updated:
10/15/2025

INPUTS: Initial altitude in meters, velocity in meters / second, change in time since last update

OUTPUTS: Updated altitude

%}

function v = update_altitude(initial_altitude, velocity, delta_T)

    v = initial_altitude + (velocity * delta_T);
    