function pressure = externalPressure(altitude, T_calculated, T_initial, Lmb)
% alt in geopot


%pressurefunctionforOrbital 
%Authors: Garion, Liam


R = 287;   
g0 = 9.80665;

%lmb is 'a', or the slope

% Find what gradient we are in:

if altitude < 11100 %gradient 1
    
    pressure_initial = 1.01325*10^3; % mBar
    pressure = pressure_initial*(T_calculated/T_initial)^-(g0/Lmb/R);

elseif altitude < Z2H(20000) % Pause one
    pressure_initial = 2.2346*10^2;
    pressure = pressure_initial * e.^-((g0/R/216.65)*(altitude*1000-11100)); % 216 is the pause temp

elseif altitude < Z2H(47400) %Gradient 2
    pressure_initial = 5.5292*10;
    pressure = pressure_initial*(T_calculated/T_initial)^-(g0/Lmb/R);

elseif altitude < Z2H(51000) % Pause 2
    pressure_initial = 7.0458 * 10^-1;
    pressure = pressure_initial * e.^-((g0/R/270.65)*(altitude*1000-11100)); % 270.65is the pause temp
    
end



