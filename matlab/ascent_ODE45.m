function dxdt = ascent_ODE(t, x, helium_mass, system_mass)

    % t = time
    
    % x = state vector
    % x(1) = position (altitude) [m]
    % x(2) = velocity [m/s]
    
    % u = initial conditions
    % u(1) = initial position (initial altitude) [m]
    % u(2) = initial velocity [m/s]
        
    % helium_mass [kg]
    % system_mass [kg]
    
    % Extracting values from the state vector
    position = x(1); % [m]
    velocity = x(2); % [m/s]

    % Atmosphere calculations
    atm = atmosphere_m(position);
    temperature = atm.T_K; % [K]
    pressure = atm.p_Pa; % [Pa]
    air_density = atm.rho_kgm3; % [kg/m^3]
    
    % Constants
    HELIUM_MOLAR_MASS = 0.00400261; % [kg/mol]
    UNIVERSAL_GAS_CONSTANT = 8.314462618; % [J/mol-K]
    DRAG_COEFFICIENT_SPHERE = 0.47; % [unitless]
    STANDARD_GRAVITY = 9.80665; % [m/s^2]
    EARTH_RADIUS_AVERAGE = 6371009; % [m]
    
    % Physics equations
    gravity = STANDARD_GRAVITY * (EARTH_RADIUS_AVERAGE / (EARTH_RADIUS_AVERAGE + position)) ^ 2; % [m/s^2]
    helium_density = (pressure * HELIUM_MOLAR_MASS) / (UNIVERSAL_GAS_CONSTANT * temperature); % [kg/m^3]
    volume = helium_mass / helium_density; % [m^3]
    buoyant_force = air_density * volume * gravity; % [N]
    balloon_radius = (3 * volume / (4 * pi)) ^ (1 / 3); % [m]
    balloon_cross_sectional_area = pi * balloon_radius ^ 2; % [m^2]
    drag_force = 0.5 * DRAG_COEFFICIENT_SPHERE * air_density * balloon_cross_sectional_area * velocity ^ 2; % [N]
    gravity_force = gravity * system_mass; % [N]

    % Governing ODE
    acceleration = (buoyant_force - drag_force - gravity_force) / system_mass; % [m/s^2]
    
    % Derivative of the state vector
    dxdt = [velocity; acceleration];

end

% Initial conditions
u = [0 0];
helium_mass = 2; % [kg]
system_mass = 12; % [kg]
burst_altitude = 1000; % [m]
target_ascent_rate = 5; % [m/s]

% Time interval -> ODE45 runs based on time interval, should change, maybe
% set a fixed interval
end_time = (burst_altitude - u(1)) / target_ascent_rate; % [s]

% ODE45 function call
[t, x] = ode45(@(t, x) ascent_ODE(t, x, helium_mass, system_mass), [0, end_time], u);

% ---------------------------------------------------------------------
% Atmosphere function (AI generated)

function result = atmosphere_m(altitude_m, varargin)
    % Convenience wrapper around Atmosphere(...) using meters.
    % 
    % Usage:
    %   result = atmosphere_m(altitude_m)
    %   result = atmosphere_m(altitude_m, 'geometric', false)
    
    % Default parameters
    p = inputParser;
    addRequired(p, 'altitude_m');
    addParameter(p, 'geometric', true);
    addParameter(p, 'output', 'struct'); % MATLAB uses 'struct' instead of 'dict'
    parse(p, altitude_m, varargin{:});
    
    alt_km = altitude_m / 1000.0;
    
    if p.Results.geometric
        result = Atmosphere(alt_km, [], p.Results.output);
    else
        result = Atmosphere([], alt_km, p.Results.output);
    end
end

function out = Atmosphere(alt_geom, alt_geopot, output_type)
    % 1976 Standard Atmosphere (to ~86 km) logic
    
    % --- Sea-level and viscosity constants ---
    TZERO    = 288.15;        % K
    PZERO    = 101325.0;      % Pa
    RHOZERO  = 1.225;         % kg/m^3
    REARTH_KM = 6356.766;     % Earth radius
    GMR      = 34.163195;     % g0*M/R*1000
    RGAS     = 8.31432e3 / 28.9644; % J/(kg·K)
    GAMMA    = 1.4;

    % Validation
    if isempty(alt_geom) == isempty(alt_geopot)
        error('Provide exactly one of alt_geom or alt_geopot (km).');
    end

    % Layer data (USSA76)
    hb = [0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852];
    Lb = [-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0];
    Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946];
    pb = [1.0, 0.223361105092, 0.054032950695, 0.008566678359, 0.001094560133, ...
          0.00066063531, 0.000039046, 0.00000368501];

    % Convert geom <-> geopot
    if isempty(alt_geopot)
        h_geom = alt_geom;
        h_geopot = (REARTH_KM * h_geom) / (REARTH_KM + h_geom);
    else
        h_geopot = alt_geopot;
        h_geom = (REARTH_KM * h_geopot) / (REARTH_KM - h_geopot);
    end

    % Clamp to table range
    h_geopot = max(hb(1), min(h_geopot, hb(end)));

    % Find layer index
    idx = find(hb <= h_geopot, 1, 'last');
    if idx >= length(hb), idx = length(hb) - 1; end

    h0 = hb(idx);
    T0 = Tb(idx);
    p0_ratio = pb(idx);
    L = Lb(idx);
    dh = h_geopot - h0;

    % Temperature
    T = T0 + L * dh;

    % Pressure ratio
    if abs(L) < 1e-12
        p_ratio = p0_ratio * exp(-GMR * dh / T0);
    else
        p_ratio = p0_ratio * (T0 / T)^(GMR / L);
    end

    % Ratios
    theta = T / TZERO;
    delta = p_ratio;
    sigma = delta / theta;

    % Absolute values
    p = delta * PZERO;
    rho = sigma * RHOZERO;
    a = sqrt(GAMMA * RGAS * T);
    mu = MetricViscosity(theta, TZERO);

    % Output formatting
    if strcmpi(output_type, 'tuple')
        out = {h_geom, h_geopot, T, p, rho, a, mu, theta, delta, sigma};
    else
        out = struct(...
            'h_geom_km', h_geom, ...
            'h_geopot_km', h_geopot, ...
            'T_K', T, ...
            'p_Pa', p, ...
            'rho_kgm3', rho, ...
            'a_mps', a, ...
            'mu_Pas', mu, ...
            'theta', theta, ...
            'delta', delta, ...
            'sigma', sigma);
    end
end

function mu = MetricViscosity(theta, TZERO)
    % Helper function for Sutherland's Law
    BETAVISC = 1.458E-6;
    SUTH     = 110.4;
    t = theta * TZERO;
    mu = BETAVISC * sqrt(t^3) / (t + SUTH);
end

% ---------------------------------------------------------------------
% Graphing

position = x(:, 1);
velocity = x(:, 2);

% Calculate Acceleration (AI Generated)
% Extracts acceleration from ODE45 somehow
acceleration = zeros(size(t));
for i = 1:length(t)
    % Call the ODE function with the solved states to get the derivatives
    derivs = ascent_ODE(t(i), x(i,:)', helium_mass, system_mass);
    acceleration(i) = derivs(2); % The second derivative is acceleration
end

% Graphs
figure (1)
plot(t, position, 'b', 'LineWidth', 2);
grid on;
title('Balloon Altitude vs Time');
xlabel('Time (s)');
ylabel('Altitude (m)');

figure (2)
plot(t, velocity, 'r', 'LineWidth', 2);
grid on;
title('Balloon Velocity vs Time');
xlabel('Time (s)');
ylabel('Velocity (m/s)');

figure (3)
plot(t, acceleration, 'g', 'LineWidth', 2);
grid on;
title('Balloon Acceleration vs Time');
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');