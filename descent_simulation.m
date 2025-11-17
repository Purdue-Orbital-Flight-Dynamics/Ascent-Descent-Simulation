%{

Simulation driver and entry point.
Calculates the vertical postion over time of the HAB after burst.
Determines the rate of descent of the system.
Assumes buoyancy force on balloon is constant.

Samuel Landers
Aanadn Shah

%}

% Ensure modules are accessible
startup()

% --- Inputs
burst_altitude = input("Enter balloon burst altitude (m)    : ");
ground_level   = input("Enter ground level (m)              : ");
burst_velocity  = input("Enter velocity at burst (m/s)     : ");

% --- Initial conditions
cur_time      = 0;                    % [s]
position      = burst_altitude;       % [m]
velocity      = burst_velocity;       % [m/s]
acceleration  = 0;                    % [m/s^2]
total_mass    = system_mass(0, 0);    % [kg]
dt         = 1;                       % [s]
stop_steps = 1000;                    % [s]

% --- Statistics
avg_descent_rate = 0; % [m/s]

% --- Build and initialize vectors with state data
t  = cur_time;
x  = position;
v  = velocity;
a  = acceleration;
k = 2;

% --- Run simulation step loop
while (position > ground_level) 

    % --- Exit if taking too long
    if (k >= stop_steps)
        break;
    end

    % --- Forces
    drag_force = dragForceDescent(velocity, position);
    gravitational_force = gravitationalForce(position, total_mass);
    net_force = drag_force + gravitational_force;

    % --- Update state
    acceleration = net_force / total_mass;
    velocity     = velocity + acceleration * dt;
    position     = position + velocity * dt;   

    % --- Update vector logs
    t(k) = cur_time;
    x(k) = position;
    v(k) = velocity;
    a(k) = acceleration;
  
    % --- Update statistics
    avg_ascent_rate = mean(v);

    % --- Progress time
    k = k + 1;
    cur_time = cur_time + dt;
end
disp("Average descent rate: " + avg_descent_rate + " m/s");

