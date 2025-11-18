function [molecular_weight_air] = molecular_weight_air_f()

%************************************************************************
% Purdue Orbital, Flight Dynamics
% 
% Project Name: Ascent Modeling
% 
% Function Name: molecular_weight_air_f
% File Name: molecular_weight_air_f
%
% Contributors: Cayden Varno
% Date Created: 10/??/2025
% Last Updated: 11/17/2025
%
% Function Description: This function has the NASA way of calculating the 
% molecular weight of air as well as the generally accepted value.
% 
% References: 
%
% United States. National Oceanic and Atmospheric Administration. (1976). 
% U.S. Standard Atmosphere, 1976: NOAA-S/T 76-1562. U.S. Government
% Printing Office. Retrieved from https://www.ngdc.noaa.gov/stp/space-weat
% her/online-publications/miscellaneous/us-standard-atmosphere-1976/us-stan
% dard-atmosphere_st76-1562_noaa.pdf
% 
% Purdue University. (2020). ME 200 Equation Sheet, Spring 2020 [PDF]. 
% Purdue University, Department of Mechanical Engineering. https://eng
% ineering.purdue.edu/ME200/files/current_semester/ME200_Eqn_Spring2020.pdf
%
% Input variables: N/A
%
% Output variables: 
% - molecular_weight_air: molecular weight of air, in kilograms per mole, positive
% 
%************************************************************************

% Previous NASA calculations
% 
% n2 = [28.0134, .78084];
% o2 = [31.9988, .209476];
% ar = [39.948, .00934];
% co2 = [44.00995, .00314];
% ne = [20.183, .00001818];
% he = [4.0026, .00000524];
% kr = [83.80, .00000114];
% xe = [181.30, .000000087];
% ch4 = [16.04303, .000002];
% h2 = [2.01594, .0000005];
%
% gases_matrix = [n2; o2; ar; co2; ne; he; kr; xe; ch4; h2];
% molecular_weight_air = sum(gases_matrix(:,1) .* gases_matrix(:,2));

% Constant value
molecular_weight_air = 0.02897; % kg/mol, from ME 20000 equation sheet