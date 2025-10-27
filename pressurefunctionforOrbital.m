%pressurefunctionforOrbital 
%Authors: Garion, Liam


R = 287;   

%lmb is 'a', or the slope

% Find what gradient we are in:

if altitude < 11100 %gradient 1
    
    pressure_initial = 1.01325*10^3; % mBar
    pgradient = pressure_initial*(T_calculated/T_initial)^-(g0/Lmb/R);

elseif altitude < 20000 % Pause one
    pressure_initial = 2.2346*10^2;
    ppause = pressure_initial * e.^-((g0/R/216.65)*(altitude*1000-11100)); % 216 is the pause temp

elseif altitude < 47400 %Gradient 2
    pressure_initial = 5.5292*10;
    pgradient = pressure_initial*(T_calculated/T_initial)^-(g0/Lmb/R);

elseif altitude < 51000 % Pause 2
    pressure_initial = 7.0458 * 10^-1;
    ppause = pressure_initial * e.^-((g0/R/270.65)*(altitude*1000-11100)); % 270.65is the pause temp
    
end



