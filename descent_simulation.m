%{

Simulation driver and entry point.
Calculates the vertical postion over time of the HAB after burst.
Determines the rate of descent of the system.
Assumes buoyancy force on balloon is constant.

Samuel Landers

%}

% Ensure modules are accessible
startup()

% --- Inputs
burst_altitude = input("Enter balloon burst altitude (m)    : ");

