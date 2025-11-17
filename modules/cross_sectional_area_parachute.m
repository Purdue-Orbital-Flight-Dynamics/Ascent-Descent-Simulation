function area = cross_sectional_area_parachute()
%{
Calculates the cross sectional area of the parachute.

Samuel Landers
%}

% there are multiple parachute sizes we will use
% those are hardcoded here

area = 15; % ft^2

% convert to metric units
area = area / 10.764;

end