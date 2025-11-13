clear
%{

Simulation driver and entry point.
Calculates the vertical postion over time of the HAB.
Assumes buoyancy force on balloon is constant.

Samuel Landers

%}

% Ensure modules are accessible
startup()

best_buoyancy_force = NaN;
closest_ascent_rate = Inf;
buoyant_force_start_index = 200; % [N]
buoyant_force_end_index = 600; % [N]
dt         = 1;      % [s]
stop_steps = 1000; % [s]
bouyant_step = 10;

% --- Inputs
burst_altitude     = input("Enter balloon burst altitude (m)    : ");
start_altitude     = input("Enter starting altitude (m)         : ");
target_ascent_rate = input("Enter desired ascent rate (m/s)     : ");

for initial_buoyant_force = buoyant_force_start_index:bouyant_step:buoyant_force_end_index

    % --- Initial conditions
    cur_time      = 0;                    % [s]
    position      = start_altitude;                    % [m]
    velocity      = 0;                    % [m/s]
    acceleration  = 0;                    % [m/s^2]
    total_mass    = system_mass(start_altitude, initial_buoyant_force) % [kg]
    helium_mass   = heliumMass(start_altitude, initial_buoyant_force)

    % --- Statistics
    avg_ascent_rate = 0; % [m/s]

    % --- Build and initialize vectors with state data
    t  = cur_time;
    x  = position;
    v  = velocity;
    a  = acceleration;
    k = 2;

    % --- Loop until balloon reaches burst altitude
    while position < burst_altitude

        % --- Exit if taking too long
        if (k >= stop_steps)
            break;
        end

        % --- Forces
        drag_force          = dragForce(velocity, helium_mass, position)
        gravitational_force = -gravitationalForce(position, total_mass)
        buoyant_force       = buoyantForce(position, helium_mass)
        
        net_force           = buoyant_force - drag_force + gravitational_force;
        if net_force < 0
            break
        end

        % --- Update state
        acceleration = net_force / total_mass;
        velocity     = velocity + acceleration * dt
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
    
    if abs(avg_ascent_rate) < abs(closest_ascent_rate)
        closest_ascent_rate = avg_ascent_rate;
        best_buoyancy_force = buoyant_force;
    end
end

disp(best_buoyancy_force + " N buoyancy force results in an avg. velocity of " + closest_ascent_rate + " m/s");
