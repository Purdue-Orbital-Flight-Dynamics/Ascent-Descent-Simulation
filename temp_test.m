max = 1000;

temps = []

for alt = 0:100:max
    temps = [temps, temperature(alt)];
end

disp(temps)