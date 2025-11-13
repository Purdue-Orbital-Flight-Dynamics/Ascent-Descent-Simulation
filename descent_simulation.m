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
ground_level   = input("Enter ground level (m)              : ");
burst_velocity   = input("Enter velocity at burst (m/s)              : ");

% --- Initial conditions
cur_time      = 0;                    % [s]
position      = burst_altitude;       % [m]
velocity      = burst_velocity;       % [m/s]
acceleration  = 0;                    % [m/s^2]

% --- Statistics
avg_descent_rate = 0; % [m/s]

% --- Build and initialize vectors with state data
t  = cur_time;
x  = position;
v  = velocity;
a  = acceleration;
k = 2;

% --- Run simulation step loop
while () {

}

