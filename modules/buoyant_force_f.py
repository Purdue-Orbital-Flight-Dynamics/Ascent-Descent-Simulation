# buoyant_force_f.py
from modules.gravity_acceleration_f import gravity_acceleration_f
from modules.volume_balloon_f import volume_balloon_f

def buoyant_force_f(altitude, helium_mass, *, atm):
    # Density

    rho = atm["rho_kgm3"]

    # g
    g = gravity_acceleration_f(altitude)

    # Volume
    V = volume_balloon_f(altitude, helium_mass, atm=atm)

    return rho * V * g
