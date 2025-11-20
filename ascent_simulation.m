%{

Simulation driver and entry point.
Calculates the vertical postion over time of the HAB.
Assumes buoyancy force on balloon is constant.

Samuel Landers

%}

% Clear environment variables from previous runs
clear

% Ensure modules are accessible
startup()

best_buoyancy_force = NaN;
closest_ascent_rate = Inf;
buoyant_force_start_index = 200; % [N]
buoyant_force_end_index = 600; % [N]
dt         = 1;      % [s]
stop_steps = 1000; % [s]
buoyant_step = 50;

% --- Inputs
burst_altitude     = input("Enter balloon burst altitude (m)    : ");
start_altitude     = input("Enter starting altitude (m)         : ");
target_ascent_rate = input("Enter desired ascent rate (m/s)     : ");
initial_buoyant_force = buoyant_force_start_index;

%for initial_buoyant_force = buoyant_force_start_index:buoyant_step:buoyant_force_end_index

    % --- Initial conditions
    cur_time      = 0;                    % [s]
    position      = start_altitude;                    % [m]
    velocity      = 0;                    % [m/s]
    acceleration  = 0;                    % [m/s^2]
    total_mass    = system_mass_f(start_altitude, initial_buoyant_force); % [kg]
    helium_mass   = helium_mass_f(start_altitude, initial_buoyant_force);

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
        drag_force          = drag_force_f(velocity, helium_mass, position);
        gravitational_force = -gravity_force_f(position, total_mass);
        buoyant_force       = buoyant_force_f(position, helium_mass);
        
        net_force           = buoyant_force - drag_force + gravitational_force;
        if net_force < 0
            break
        end

        % --- Sanity checks
        if net_force < 0
            % Balloon should always be going up
            break
        elseif gravitational_force > 0
            % Gravity should always be negative
            disp("Error: gravity was positive");
            return;
        end
       
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

        possssssss = x(end);
    end
    
    if abs(avg_ascent_rate - target_ascent_rate) < abs(closest_ascent_rate - target_ascent_rate)
        closest_ascent_rate = avg_ascent_rate;
        best_buoyancy_force = initial_buoyant_force;
    end
%end

disp(best_buoyancy_force + " N buoyancy force results in an avg. velocity of " + closest_ascent_rate + " m/s");