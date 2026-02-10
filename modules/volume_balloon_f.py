from modules.balloon_density_f import balloon_density_f

def volume_balloon_f(altitude, helium_mass, *, atm):
    rho_he = balloon_density_f(altitude, atm=atm)
    return helium_mass / rho_he
