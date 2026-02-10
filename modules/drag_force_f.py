# drag_force_f.py
from modules.balloon_cross_sectional_area_f import balloon_cross_sectional_area_f

def drag_force_f(velocity, helium_mass, altitude, *, atm):

    rho = atm["rho_kgm3"]

    area = balloon_cross_sectional_area_f(altitude, helium_mass, atm=atm)  # m^2
    CD = 0.47

    return 0.5 * CD * rho * area * velocity**2
