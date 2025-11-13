function g_f = gravitationalForce(altitude, sys_mass)
%{
Calculates the force due to gravity at a given altitude.

Jack Triglianos
Samuel Landers
%}

g_f = gravitationalAcceleration(altitude) * sys_mass;
end