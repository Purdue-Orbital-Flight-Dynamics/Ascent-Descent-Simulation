from modules.atmosphere_f import atmosphere_m
from modules.balloon_cross_sectional_area_f import balloon_cross_sectional_area_f

def drag_force_descent_f(velocity: float, altitude: float, mass: float) -> float:
    """
    Computes the drag force acting on the balloon during descent.

    Parameters
    ----------
    velocity : float
        Descent velocity of balloon (m/s).
    altitude : float
        Geometric altitude (m), positive upward.

    Returns
    -------
    float
        Drag force on balloon (N).
    """

    # Get air density from standard atmosphere (geometric altitude in meters)
    atm = atmosphere_m(altitude, geometric=True, output="dict")
    air_density = atm["rho_kgm3"]  # kg/m^3

    # Get balloon cross-sectional area
    cross_sec_area = balloon_cross_sectional_area_f(altitude, mass, atm=atm)  # m^2

    # Drag coefficient of balloon/parachute
    DRAG_COEFFICIENT = 1.75  # dimensionless

    # Compute drag force
    drag_force = (
        0.5
        * DRAG_COEFFICIENT
        * air_density
        * cross_sec_area
        * velocity**2
    )  # N

    return drag_force
