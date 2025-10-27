%{

Place to hard-code all the mass measurements so it's not necesary to recalculate weight everytime.
All mass measurements are in terms of grams.

Contributors:
Samuel Landers

%}

function mass = system_mass()

    % Launch Structure masses
    launch_structure_mass = 10;

    % Flight operations masses
    flight_operations_mass = 10;

    % Avionics masses
    avionics_mass = 10;

    % Non-team associated masses
    misc_mass = 10;

    mass = launch_structure_mass + flight_operations_mass + avionics_mass + misc_mass;
end