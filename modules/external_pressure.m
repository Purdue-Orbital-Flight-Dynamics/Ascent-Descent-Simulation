function pressure = external_pressure(altitude, T_calculated, T_initial, Lmb)
%{
Calculates the environmental pressure based on temperature data.

Garion Cheng
Liam Shepard
Samuel Landers
%}

R = 287;
G_0 = 9.80665;

if altitude < 11100 % first gradient
    pressure_initial = 1.01325*10^3; % mBar
    pressure = pressure_initial*(T_calculated/T_initial)^-(G_0/Lmb/R);
elseif altitude < Z2H(20000) % first pause
    pressure_initial = 2.2346*10^2;
    pressure = pressure_initial * e.^-((G_0/R/216.65)*(altitude*1000-11100)); % 216 is the pause temp
elseif altitude < Z2H(47400) % second gradient
    pressure_initial = 5.5292*10;
    pressure = pressure_initial*(T_calculated/T_initial)^-(G_0/Lmb/R);
elseif altitude < Z2H(51000) % second pause
    pressure_initial = 7.0458 * 10^-1;
    pressure = pressure_initial * e.^-((G_0/R/270.65)*(altitude*1000-11100)); % 270.65is the pause temp
end
end



