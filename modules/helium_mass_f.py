from modules.atmosphere_f import atmosphere_m


def helium_mass_f(altitude: float, net_buoyancy_force: float) -> float:
    """
    Calculates helium mass given altitude and net buoyancy force.

    Parameters
    ----------
    altitude : float
        Altitude in meters (geometric), positive.
    net_buoyancy_force : float
        Net buoyancy force in Newtons, positive.

    Returns
    -------
    float
        Helium mass in kilograms, positive.
    """

    # Other mass
    BALLOON_MASS = 0.0  # kg
    NECK_MASS = 0.0     # kg
    ROPE_MASS = 0.0     # kg
    OTHER_MASS = BALLOON_MASS + NECK_MASS + ROPE_MASS

    # Get atmospheric properties at altitude
    atm = atmosphere_m(altitude, geometric=True, output="dict")

    air_density = atm["rho_kgm3"]  # kg/m^3

    # Standard gravity used in USSA76 (constant)
    gravity_acceleration = 9.80665  # m/s^2

    # Helium density approximation using ideal gas law:
    # ρ = p / (R_specific * T)
    R_HE = 2077.0  # J/(kg·K), specific gas constant for helium
    helium_density = atm["p_Pa"] / (R_HE * atm["T_K"])  # kg/m^3

    # Other weight
    other_weight = OTHER_MASS * gravity_acceleration

    # Helium mass
    helium_mass = (
        helium_density * (net_buoyancy_force + other_weight)
    ) / (
        gravity_acceleration * (air_density - helium_density)
    )  # kg

    return helium_mass
