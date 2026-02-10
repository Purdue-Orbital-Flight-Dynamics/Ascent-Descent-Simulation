from modules.atmosphere import Atmosphere

def balloon_density_f(altitude, *, atm):

    T = atm["T_K"]
    p = atm["p_Pa"]

    # Constants (SI mol-based)
    GAS_CONSTANT = 8.314462618      # J/(mol·K)
    HELIUM_MOLAR_MASS = 0.00400261  # kg/mol

    return (p * HELIUM_MOLAR_MASS) / (GAS_CONSTANT * T)
