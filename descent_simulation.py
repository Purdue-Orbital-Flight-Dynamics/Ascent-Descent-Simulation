import numpy as np

#{Simulation driver and entry point.
#Calculates the vertical postion over time of the HAB after burst.
#Determines the rate of descent of the system.
#Assumes buoyancy force on balloon is constant.

#Samuel Landers
#Aanadn Shah
#Garion Cheng: 2/4/2026 Converted to Python

from modules.drag_force_descent_f import drag_force_descent_f
from modules.gravitational_force_f import gravitational_force_f
from modules.system_mass_f import system_mass_f

# --- Inputs
burst_altitude = float(input("Enter balloon burst altitude (m)    : "))
ground_level   = float(input("Enter ground level (m)              : "))
burst_velocity = float(input("Enter velocity at burst (m/s)       : "))

# --- Initial conditions
cur_time      = 0                     # [s]
position      = burst_altitude        # [m]
velocity      = burst_velocity        # [m/s]
acceleration  = 0                     # [m/s^2]
total_mass, helium_mass = system_mass_f(0, 0)   # [kg]
dt         = 1                        # [s]
stop_steps = 1000                     # [s]

# --- Statistics
avg_descent_rate = 0  # [m/s]

# --- Build and initialize vectors with state data
t  = cur_time
x  = position
v  = velocity
a  = acceleration
k = 2

# --- Run simulation step loop
while position > ground_level: 

    # --- Exit if taking too long
    if k >= stop_steps:
        break
    

    # --- Forces
    drag_force = drag_force_descent_f(velocity, position)
    gravitational_force = gravitational_force_f(position, total_mass)
    net_force = drag_force + gravitational_force

    # --- Update state
    acceleration = net_force / total_mass
    velocity     = velocity + acceleration * dt
    position     = position + velocity * dt   

    # --- Update vector logs
    t(k) = cur_time
    x(k) = position
    v(k) = velocity
    a(k) = acceleration
  
    # --- Update statistics
    avg_ascent_rate = np.mean(v)

    # --- Progress time
    k += 1
    cur_time +=  dt

print(f"Average descent rate: {avg_descent_rate:.2f} m/s")

