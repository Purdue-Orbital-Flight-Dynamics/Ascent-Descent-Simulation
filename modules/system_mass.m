function [sys_mass, required_helium_mass] = system_mass(initial_altitude, buoyancy_force)
%{
Returns the mass of the entire system.

Sam Landers
%}

% (1) calculate launch strucutre mass
launch_structure_mass = 10;

% (2) calculate flight operations mass
flight_operations_mass = 10;
required_helium_mass = helium_mass(initial_altitude, buoyancy_force);
flight_operations_mass = flight_operations_mass + helium_mass;

% (3) calculate avionics mass
avionics_mass = 10;

% (4) account for any other mass on the system
misc_mass = 0;

% (5) sum masses to attain system mass
sys_mass = launch_structure_mass + flight_operations_mass + avionics_mass + misc_mass;
end