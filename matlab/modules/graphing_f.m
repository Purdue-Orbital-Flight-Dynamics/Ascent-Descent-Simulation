function graphing_f(helium_mass_kg, start_altitude_m, burst_altitude_m, total_mass_kg)

%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Function Name: graphing_f
% File Name: graphing_f.m
%
% Contributors: Eric Umminger
% Date Created: 1/28/2026
% Last Updated: 1/28/2026
%
% Function Description:
%   Recalculates the position, velocity, and acceleration of the balloon
%   with the required helium mass.
%
% References:
%
% Input variables:
% - helium_mass_kg
% - start_altitude_m
% - burst_altitude_m
% - total_mass_kg
%
% Output variables:
% - None
%
%************************************************************************

% Initializing variables and matrices
time_step_s = 0.005;   % [s] integration time step
position_m  = start_altitude_m;   % [m]
velocity_mps = 0;                 % [m/s]

position_history_m      = [];     % [m]
velocity_history_mps    = [];     % [m/s]
acceleration_history_mps2 = [];   % [m/s^2]
time_history_s          = [];     % [s]

had_error   = false;
step_index  = 1;

while position_m < burst_altitude_m
    % fprintf("Height: %.3f m ", position_m)

    % Compute buoyant force safely
    try
        buoyant_force_N = buoyant_force_f(position_m, helium_mass_kg); % [N]
    catch ME
        fprintf("Error in buoyant_force_f at position %.3f m: %s\n", ...
                position_m, ME.message);
        had_error = true;
        break
    end

    % Calculating relevant values
    drag_force_N    = drag_force_f(velocity_mps, helium_mass_kg, position_m); % [N]
    gravity_force_N = gravity_force_f(position_m, total_mass_kg);             % [N]

    net_force_N = buoyant_force_N - drag_force_N - gravity_force_N;           % [N]

    % Update state
    net_accel_mps2    = net_force_N / total_mass_kg;      % [m/s^2]
    acceleration_mps2 = net_accel_mps2;                   % [m/s^2]
    velocity_mps      = velocity_mps + acceleration_mps2 * time_step_s; % [m/s]
    position_m        = position_m + velocity_mps * time_step_s;        % [m]

    % Log histories
    position_history_m(step_index)       = position_m;
    velocity_history_mps(step_index)     = velocity_mps;
    acceleration_history_mps2(step_index) = acceleration_mps2;
    if step_index == 1
        time_history_s(step_index)       = 0;
    else
    time_history_s(step_index)           = time_history_s(step_index - 1) + time_step_s;
    end

    if net_force_N <= 0
        fprintf("Net force became non-positive after %d steps\n", step_index);
        had_error = true;
        break
    end

    step_index = step_index + 1;
end

figure(1)
plot(position_history_m, time_history_s, 'Color', 'g')
title("Position vs. Time")
xlabel("Time [s]")
ylabel("Position [m]")
grid on
xlim([0, max(time_history_s)])
ylim([0, max(position_history_m)])

figure(2)
plot(velocity_history_mps, time_history_s, 'Color', 'b')
title("Velocity vs. Time")
xlabel("Time [s]")
ylabel("Velocity [m/s]")
grid on
xlim([0,max(time_history_s)])
ylim([0, max(velocity_history_mps)])

figure(3)
plot(acceleration_history_mps2, time_history_s, 'Color', 'r')
title("Acceleration vs. Time")
xlabel("Time [s]")
ylabel("Acceleration [m/s^2]")
grid on
xlim([0,max(time_history_s)])
ylim([0, max(acceleration_history_mps2)])

fprintf("Three graphs generated.\n")
