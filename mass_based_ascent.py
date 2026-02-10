# mass_based_ascent.py
import numpy as np

from modules.atmosphere import atmosphere_m
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f
from modules.force_correction_f import force_correction_f

# ----------------- config -----------------
TIME_STEP_S = 0.1
CONSTANT_MASS_KG = 8.8
MAX_HELIUM_MASS_KG = 50.0
MAX_BINARY_ITERS = 80
RATE_DECIMALS = 5
# ------------------------------------------

def atmosphere_at_position(position_m: float) -> dict:
    return atmosphere_m(position_m, geometric=True)

def simulate_ascent_rate(start_alt_m: float, burst_alt_m: float, helium_mass_kg: float):
    total_mass_kg = CONSTANT_MASS_KG + helium_mass_kg
    pos_m = start_alt_m
    vel_mps = 0.0
    v_hist = []
    gage_force_N = np.nan

    step = 0
    while pos_m < burst_alt_m:
        atm = atmosphere_at_position(pos_m)

        buoy_N = buoyant_force_f(pos_m, helium_mass_kg, atm=atm)
        drag_N = drag_force_f(vel_mps, helium_mass_kg, pos_m, atm=atm)
        grav_N = gravity_force_f(pos_m, total_mass_kg)
        corr_N = force_correction_f(helium_mass_kg, pos_m)

        net_N = buoy_N - drag_N - grav_N

        if step == 0:
            gage_force_N = buoy_N - corr_N

        if net_N <= 0:
            return 0.0, gage_force_N, True

        acc = net_N / total_mass_kg
        vel_mps += acc * TIME_STEP_S
        pos_m += vel_mps * TIME_STEP_S
        v_hist.append(vel_mps)
        step += 1

    if not v_hist:
        return 0.0, gage_force_N, True

    return float(np.mean(v_hist)), gage_force_N, False

def solve_helium_mass(start_alt_m: float, burst_alt_m: float, target_rate_mps: float):
    max_rate, max_gage, max_failed = simulate_ascent_rate(
        start_alt_m, burst_alt_m, MAX_HELIUM_MASS_KG
    )
    if max_failed or max_rate < target_rate_mps:
        return None, max_rate, max_gage

    lo, hi = 0.0, MAX_HELIUM_MASS_KG
    best_m, best_rate, best_gage = hi, max_rate, max_gage

    for _ in range(MAX_BINARY_ITERS):
        mid = 0.5 * (lo + hi)
        rate, gage, failed = simulate_ascent_rate(start_alt_m, burst_alt_m, mid)

        if failed or rate < target_rate_mps:
            lo = mid
            continue

        hi = mid
        best_m, best_rate, best_gage = mid, rate, gage

        if round(best_rate, RATE_DECIMALS) == round(target_rate_mps, RATE_DECIMALS):
            break
        if (hi - lo) < 0.5 * 10 ** (-RATE_DECIMALS):
            break

    return best_m, best_rate, best_gage

def main():
    burst_alt_m = float(input("Burst Altitude [m]: "))
    start_alt_m = float(input("Starting Altitude [m]: "))
    target_rate = float(input("Desired Ascent Rate [m/s]: "))

    # 1976 std-atm tables in modules/atmosphere.py top out at 84.852 km
    if start_alt_m < 0 or burst_alt_m <= start_alt_m or target_rate <= 0 or burst_alt_m > 84852:
        raise SystemExit("Invalid inputs.")

    best_m, best_rate, best_gage = solve_helium_mass(start_alt_m, burst_alt_m, target_rate)

    if best_m is None:
        print("\nMAX helium insufficient.")
        print(f"MAX helium mass [kg]: {MAX_HELIUM_MASS_KG:.4f}")
        print(f"MAX achieved ascent rate [m/s]: {best_rate:.4f}")
        print(f"Initial net force at MAX mass [N]: {best_gage:.4f}")
        return

    print(f"\nMass for target rate [kg]: {best_m:.4f}")
    print(f"Initial net force for target rate [N]: {best_gage:.4f}")
    print(f"Final achieved ascent rate [m/s]: {best_rate:.4f}")

if __name__ == "__main__":
    main()
