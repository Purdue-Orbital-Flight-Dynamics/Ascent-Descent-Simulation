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
        Geometric altitude (km). Default path.
    alt_geopot : float | None
        Geopotential altitude (km).
    output : {"dict", "tuple"}
        - "dict" (default): return a dict of values
        - "tuple": return values in a fixed order (documented below)

    Returns (SI)
    ------------
    T      : K
    p      : Pa
    rho    : kg/m^3
    a      : m/s (speed of sound)
    mu     : kg/(m*s) dynamic viscosity
    nu     : m^2/s kinematic viscosity
    plus ratios: sigma, delta, theta
    """

    # --- input validation ---
    if (alt_geom is None) == (alt_geopot is None):
        raise ValueError("Exactly one of alt_geom or alt_geopot must be specified (in km).")

    # --- atmosphere layer data ---
    REARTH = 6356.766   # km
    GMR = 34.163195     # K/km

    htab = [0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852]
    ttab = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946]
    ptab = [1.0, 2.2336110E-1, 5.4032950E-2, 8.5666784E-3, 1.0945601E-3,
            6.6063531E-4, 3.9046834E-5, 3.68501E-6]
    gtab = [-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0, 0.0]

    # --- compute geopotential altitude h (km) ---
    if alt_geom is not None:
        h = alt_geom * REARTH / (alt_geom + REARTH)  # geometric -> geopotential
        alt_in = alt_geom
        alt_kind = "geometric"
    else:
        h = alt_geopot
        alt_in = alt_geopot
        alt_kind = "geopotential"

    # --- locate layer via binary search ---
    i = 0
    j = len(htab) - 1
    while j > i + 1:
        k = (i + j) // 2
        if h < htab[k]:
            j = k
        else:
            i = k

    # --- temperature ratio theta ---
    tgrad = gtab[i]
    tbase = ttab[i]
    deltah = h - htab[i]
    tlocal = tbase + tgrad * deltah
    theta = tlocal / ttab[0]

    # --- pressure ratio delta ---
    if tgrad == 0.0:
        delta = ptab[i] * math.exp(-GMR * deltah / tbase)
    else:
        delta = ptab[i] * math.pow(tbase / tlocal, GMR / tgrad)

    # --- density ratio sigma ---
    sigma = delta / theta

    # --- raw SI values derived like in Tables.py ---
    T = TZERO * theta               # K
    p = PZERO * delta               # Pa
    rho = RHOZERO * sigma           # kg/m^3
    a = AZERO * math.sqrt(theta)    # m/s

    mu = MetricViscosity(theta)     # kg/(m*s)
    nu = mu / rho                   # m^2/s

    if output == "dict":
        return {
            "alt_km": alt_in,
            "alt_type": alt_kind,
            "h_geopot_km": h,

            "T_K": T,
            "p_Pa": p,
            "rho_kgm3": rho,
            "a_ms": a,
            "mu_kgms": mu,
            "nu_m2s": nu,

            "sigma": sigma,
            "delta": delta,
            "theta": theta,
        }

    if output == "tuple":
        # Fixed order:
        # (T, p, rho, a, mu, nu, sigma, delta, theta, h)
        return (T, p, rho, a, mu, nu, sigma, delta, theta, h)

    raise ValueError('output must be "dict" or "tuple"')
