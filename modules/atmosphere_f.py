# atmosphere.py
import math

# --- Sea-level and viscosity constants (from your Tables.py) ---
TZERO   = 288.15        # K
PZERO   = 101325.0      # Pa (N/m^2)
RHOZERO = 1.225         # kg/m^3
AZERO   = 340.294       # m/s
BETAVISC = 1.458E-6     # kg/(m*s*sqrt(K)) style constant used in this form
SUTH    = 110.4         # K

def MetricViscosity(theta):
    """Dynamic viscosity (kg/m-s) via Sutherland's law form used in Tables.py."""
    t = theta * TZERO
    return BETAVISC * math.sqrt(t*t*t) / (t + SUTH)

def Atmosphere(alt_geom=None, alt_geopot=None, *, output="dict"):
    """1976 standard atmosphere (to ~86 km), returning raw SI properties at one altitude.

    Exactly one of alt_geom or alt_geopot must be supplied (km).

    Parameters
    ----------
    alt_geom : float | None
        Geometric altitude (km).
    alt_geopot : float | None
        Geopotential altitude (km).
    output : str
        "dict" (default) or "tuple".

    Returns
    -------
    dict | tuple
        Includes keys:
        - h_geom_km, h_geopot_km
        - T_K, p_Pa, rho_kgm3
        - a_mps (speed of sound)
        - mu_Pas (dynamic viscosity)
        - theta (T/T0), delta (p/p0), sigma (rho/rho0)

    Notes
    -----
    This is a cleaned single-point version of the classic 1976 Standard Atmosphere tables
    approach (layered lapse rates), matching the style used in typical aerospace Tables.py.
    """

    if (alt_geom is None) == (alt_geopot is None):
        raise ValueError("Provide exactly one of alt_geom or alt_geopot (km).")

    # --- Constants ---
    REARTH_KM = 6356.766  # effective Earth radius used in USSA76 (km)
    GMR = 34.163195       # g0*M/R*1000 (dimensionless in table form)
    RSTAR = 8.31432e3     # J/(kmol·K)
    MW_AIR = 28.9644      # kg/kmol
    RGAS = RSTAR / MW_AIR # J/(kg·K)
    GAMMA = 1.4

    # Layer base geopotential altitudes (km), base temps (K), base pressure ratios, lapse rates (K/km)
    # Standard USSA76 up to 84.852 km
    hb = [0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852]
    Lb = [-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0]  # K/km for each layer (len = len(hb)-1)
    Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946]  # K
    pb = [1.0, 0.223361105092, 0.054032950695, 0.008566678359, 0.001094560133,
          0.00066063531, 0.000039046, 0.00000368501]  # pressure ratio at base (p/p0)

    # Convert geom<->geopot as needed
    if alt_geopot is None:
        h_geom = float(alt_geom)
        h_geopot = (REARTH_KM * h_geom) / (REARTH_KM + h_geom)
    else:
        h_geopot = float(alt_geopot)
        h_geom = (REARTH_KM * h_geopot) / (REARTH_KM - h_geopot)

    # Clamp to table range (optional: could raise instead; keeping clamp avoids crashes)
    if h_geopot < hb[0]:
        h_geopot = hb[0]
    if h_geopot > hb[-1]:
        h_geopot = hb[-1]

    # Find layer index i such that hb[i] <= h < hb[i+1]
    i = 0
    for k in range(len(hb) - 1):
        if hb[k] <= h_geopot <= hb[k+1]:
            i = k
            break

    h0 = hb[i]
    T0 = Tb[i]
    p0_ratio = pb[i]
    L = Lb[i]

    dh = h_geopot - h0

    # Temperature
    T = T0 + L * dh  # K

    # Pressure ratio
    if abs(L) < 1e-12:
        # isothermal
        p_ratio = p0_ratio * math.exp(-GMR * dh / T0)
    else:
        p_ratio = p0_ratio * (T0 / T) ** (GMR / L)

    # Density ratio
    rho_ratio = p_ratio / (T / TZERO)

    # Absolute pressure/density
    p = p_ratio * PZERO
    rho = rho_ratio * RHOZERO

    # Speed of sound
    a = math.sqrt(GAMMA * RGAS * T)

    # Viscosity (using same form as Tables.py helpers; requires theta=T/T0)
    theta = T / TZERO
    mu = MetricViscosity(theta)

    if output == "tuple":
        return (h_geom, h_geopot, T, p, rho, a, mu, theta, p_ratio, rho_ratio)

    return {
        "h_geom_km": h_geom,
        "h_geopot_km": h_geopot,
        "T_K": T,
        "p_Pa": p,
        "rho_kgm3": rho,
        "a_mps": a,
        "mu_Pas": mu,
        "theta": theta,
        "delta": p_ratio,
        "sigma": rho_ratio,
    }

def atmosphere_m(altitude_m: float, *, geometric: bool = True, output: str = "dict"):
    """Convenience wrapper around Atmosphere(...) using meters.

    Parameters
    ----------
    altitude_m : float
        Altitude in meters.
    geometric : bool
        If True, interpret altitude_m as geometric altitude. If False, geopotential.
    output : str
        Passed through to Atmosphere(...).

    Returns
    -------
    dict | tuple
        Same as Atmosphere(...).
    """
    alt_km = altitude_m / 1000.0
    if geometric:
        return Atmosphere(alt_geom=alt_km, output=output)
    return Atmosphere(alt_geopot=alt_km, output=output)
