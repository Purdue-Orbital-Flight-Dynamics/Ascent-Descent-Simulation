clear
%************************************************************************
% Purdue Orbital, Flight Dynamics
%
% Project Name: Ascent/Descent Modeling
%
% Script Name: mass_based_ascent
% File Name: mass_based_ascent.m
%
% Contributors: Cayden Varno
% Date Created: 11/??/2025
% Last Updated: 11/20/2025
%
% Script Description:
%   Iteratively determines the helium mass required to achieve a target
%   mean ascent rate between a starting altitude and a specified burst
%   altitude. For each helium mass, this script integrates the vertical
%   motion using buoyant, drag, and gravity forces, and records the first
%   net force for the final (target) case.
%
% References:
%
% Input (via user prompt):
% - burst_altitude_m: burst altitude, meters, positive
% - start_altitude_m: starting altitude, meters, positive
% - target_ascent_rate_mps: desired average ascent rate, m/s, positive
%
% Outputs (printed to command window):
% - helium_mass_kg: helium mass required to reach target ascent rate, kg
% - first_net_force_N: initial net force at start altitude for that mass, N
%
%************************************************************************

time_step_s = 0.01;   % [s] integration time step

burst_altitude_m = input("Burst Altitude [m]: ");           % [m]
start_altitude_m = input("Starting Altitude [m]: ");        % [m]
target_ascent_rate_mps = input("Desired Ascent Rate [m/s]: ");                 % [m/s]

MASS_STEP_KG       = 0.005;   % [kg] helium mass increment per iteration
helium_mass_kg     = -MASS_STEP_KG;  % [kg] so first loop adds to 0
CONSTANT_MASS_KG   = 8.8;     % [kg] payload + structure, assumed constant
ascent_rate_mps    = 0;       % [m/s] current mean ascent rate estimate

MAX_HELIUM_MASS_KG = 50;      % [kg] safety limit on helium mass
first_net_force_N  = NaN;     % [N] first net force at start altitude

while ascent_rate_mps < target_ascent_rate_mps && ...
      helium_mass_kg < MAX_HELIUM_MASS_KG

    fprintf("\n")

    % Reset state for this helium mass
    position_m  = start_altitude_m;   % [m]
    velocity_mps = 0;                 % [m/s]

    position_history_m      = [];     % [m]
    velocity_history_mps    = [];     % [m/s]
    acceleration_history_mps2 = [];   % [m/s^2]

    had_error   = false;
    step_index  = 1;

    helium_mass_kg = helium_mass_kg + MASS_STEP_KG;   % [kg]
    % fprintf("Helium mass: %.3f kg\n", helium_mass_kg)

    total_mass_kg = CONSTANT_MASS_KG + helium_mass_kg;   % [kg]

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

        drag_force_N    = drag_force_f(velocity_mps, helium_mass_kg, position_m); % [N]
        gravity_force_N = gravity_force_f(position_m, total_mass_kg);             % [N]

        net_force_N = buoyant_force_N - drag_force_N - gravity_force_N;           % [N]
        % fprintf("    Net Force: %.3f N\n", net_force_N)

        % Save FIRST net force only (for this helium mass)
        if step_index == 1
            first_net_force_N = net_force_N;   % overwrite every run
        end

        % Update state
        net_accel_mps2    = net_force_N / total_mass_kg;      % [m/s^2]
        acceleration_mps2 = net_accel_mps2;                   % [m/s^2]
        velocity_mps      = velocity_mps + acceleration_mps2 * time_step_s; % [m/s]
        position_m        = position_m + velocity_mps * time_step_s;        % [m]

        % Log histories
        position_history_m(step_index)       = position_m;
        velocity_history_mps(step_index)     = velocity_mps;
        acceleration_history_mps2(step_index) = acceleration_mps2;

        if net_force_N <= 0
            fprintf("Net force became non-positive after %d steps\n", step_index);
            had_error = true;
            break
        end

        step_index = step_index + 1;
    end

    if ~had_error && ~isempty(velocity_history_mps)
        ascent_rate_mps = mean(velocity_history_mps);    % [m/s]
        fprintf("Ascent Rate: %.4f m/s\n", ascent_rate_mps)
    end
end

disp("Mass for target rate [kg]:")
disp(helium_mass_kg)

disp("Initial net force for target rate [N]:")
disp(first_net_force_N)
