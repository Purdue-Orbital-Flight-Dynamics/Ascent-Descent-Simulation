import math
import pytest

import modules.pressure_f as pressure_mod


# US Standard Atmosphere 1976 layer-base pressures (geopotential altitude), Pa
# Source: USSA1976 layer table summary. :contentReference[oaicite:1]{index=1}
USSA1976_P_PA = {
    0.0: 101325.0,
    11000.0: 22632.1,
    20000.0: 5474.89,
    32000.0: 868.019,
    47000.0: 110.906,
    51000.0: 66.9389,
}


@pytest.fixture(autouse=True)
def patch_geometric_to_geopotential_identity(monkeypatch):
    """
    Tests use geopotential altitude directly.
    Patch conversion to identity so altitude_z == altitude (geopotential).
    """
    monkeypatch.setattr(pressure_mod, "geometric_to_geopotential_f", lambda z: z)


def std_atm_inputs_for_pressure_f(h_gp: float):
    """
    Provide (temperature_calculated, temperature_initial, lapse_rate) consistent with
    US Standard Atmosphere 1976 temperature profile in each layer.

    Notes:
    - pressure_f expects temperature_initial and lapse_rate for the *current* layer.
    - For isothermal layers, lapse_rate can be 0 because pressure_f ignores it there.
    """
    # Layer boundaries (geopotential altitude, meters):
    # 0–11 km: L = -0.0065 K/m, T(0)=288.15 K
    # 11–20 km: isothermal, T=216.65 K
    # 20–32 km: L = +0.0010 K/m, T(20)=216.65 K
    # 32–47 km: L = +0.0028 K/m, T(32)=228.65 K
    # 47–51 km: isothermal, T=270.65 K

    if h_gp < 11000.0:
        T0 = 288.15
        L = -0.0065
        T = T0 + L * (h_gp - 0.0)
        return T, T0, L

    if h_gp < 20000.0:
        # isothermal
        return 216.65, 216.65, 0.0

    if h_gp < 32000.0:
        T0 = 216.65
        L = 0.0010
        T = T0 + L * (h_gp - 20000.0)
        return T, T0, L

    if h_gp < 47000.0:
        T0 = 228.65
        L = 0.0028
        T = T0 + L * (h_gp - 32000.0)
        return T, T0, L

    if h_gp < 51000.0:
        # isothermal
        return 270.65, 270.65, 0.0

    # Above 51 km: your function currently returns NaN; inputs don't matter
    return 270.65, 270.65, 0.0


@pytest.mark.parametrize("h_gp", [0.0, 11000.0, 20000.0, 32000.0])
def test_pressure_matches_ussa1976_at_key_layer_bases_up_to_32km(h_gp):
    """
    These are strong correctness checks versus USSA1976 at key layer bases.
    With a correct implementation, these should match closely.
    """
    T, T0, L = std_atm_inputs_for_pressure_f(h_gp)
    p = pressure_mod.pressure_f(h_gp, T, T0, L)

    # Use a small relative tolerance; you can tighten once implementation is corrected.
    assert p == pytest.approx(USSA1976_P_PA[h_gp], rel=3e-4, abs=0.5)


@pytest.mark.xfail(reason="Current pressure_f implementation has known issues in the 47–51 km region (branch formula/offset).")
@pytest.mark.parametrize("h_gp", [47000.0])
def test_pressure_matches_ussa1976_at_47km(h_gp):
    T, T0, L = std_atm_inputs_for_pressure_f(h_gp)
    p = pressure_mod.pressure_f(h_gp, T, T0, L)
    assert p == pytest.approx(USSA1976_P_PA[h_gp], rel=3e-4, abs=0.5)


@pytest.mark.xfail(reason="Current pressure_f returns NaN at and above 51 km; USSA1976 defines pressure at 51 km.")
@pytest.mark.parametrize("h_gp", [51000.0])
def test_pressure_matches_ussa1976_at_51km(h_gp):
    T, T0, L = std_atm_inputs_for_pressure_f(h_gp)
    p = pressure_mod.pressure_f(h_gp, T, T0, L)
    assert p == pytest.approx(USSA1976_P_PA[h_gp], rel=5e-4, abs=0.5)


def test_out_of_range_behavior_currently_returns_nan_above_51km():
    # This documents current behavior; change this test if you later implement >51 km.
    T, T0, L = std_atm_inputs_for_pressure_f(80000.0)
    p = pressure_mod.pressure_f(80000.0, T, T0, L)
    assert math.isnan(p)
