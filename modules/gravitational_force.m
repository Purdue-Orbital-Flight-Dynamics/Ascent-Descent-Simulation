function g_f = gravitational_force(altitude, sys_mass)
%{
Calculates the force due to gravity at a given altitude.

Jack Triglianos
Samuel Landers
%}

g_f = gravitational_acceleration(altitude) * sys_mass;
end