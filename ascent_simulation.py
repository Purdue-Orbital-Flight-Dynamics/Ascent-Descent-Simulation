from __future__ import annotations
import time

# Updated Imports
from modules.fast_atmosphere import FastAtmosphere
from modules.logger_f import log_entry_f
from modules.buoyant_force_f import buoyant_force_f
from modules.drag_force_f import drag_force_f
from modules.gravity_force_f import gravity_force_f

# --------------------------- CONSTANTS --------------------------------
TIME_STEP = 0.1 
BALLOON_MASS_KG = 2.0
NECK_MASS_KG = 0.0
ROPE_MASS_KG = 0.0
OTHER_MASS_KG = 0.0
PAYLOAD_MASS_KG = 10.0

CONSTANT_MASS = (
    BALLOON_MASS_KG + NECK_MASS_KG + ROPE_MASS_KG + OTHER_MASS_KG + PAYLOAD_MASS_KG
)
GAGE_MASS_KG = BALLOON_MASS_KG + NECK_MASS_KG + ROPE_MASS_KG + OTHER_MASS_KG

MAX_HELIUM_MASS = 50.0
MAX_BINARY_ITERATIONS = 80
RATE_TOLERANCE = 1e-4 
MAX_ATMOSPHERE_ALTITUDE = 84_852.0

ATM_CACHE = FastAtmosphere(max_alt=MAX_ATMOSPHERE_ALTITUDE)
# ---------------------------------------------------------------------

def validate_inputs_f(start_altitude: float, burst_altitude: float, target_rate: float) -> str | None:
    if start_altitude < 0.0: return "start_altitude must be non-negative"
    if burst_altitude <= start_altitude: return "burst_altitude must be greater than start_altitude"
    if target_rate <= 0.0: return "target_rate must be positive"
    if burst_altitude > MAX_ATMOSPHERE_ALTITUDE: return "burst_altitude exceeds ceiling"
    return None

def simulate_ascent_rate_f(start_alt, burst_alt, helium_mass, keep_history=False):
    total_mass = CONSTANT_MASS + helium_mass
    altitude, velocity, elapsed_time = start_alt, 0.0, 0.0
    history = []

    while altitude < burst_alt:
        atm = ATM_CACHE.get_atm(altitude)
        buoyant = buoyant_force_f(altitude, helium_mass, atm=atm)
        drag = drag_force_f(velocity, helium_mass, altitude, atm=atm)
        gravity = gravity_force_f(altitude, total_mass)

        net_force = buoyant - drag - gravity
        if net_force <= 0.0: return 0.0, True, history

        acceleration = net_force / total_mass
        velocity += acceleration * TIME_STEP
        altitude += velocity * TIME_STEP
        elapsed_time += TIME_STEP

        if keep_history:
            history.append({"altitude": altitude, "velocity": velocity})

    mean_rate = (altitude - start_alt) / elapsed_time if elapsed_time > 0 else 0.0
    return mean_rate, False, history

def solve_helium_mass_f(start_alt: float, burst_alt: float, target_rate: float):
    lower_mass, upper_mass = 0.0, MAX_HELIUM_MASS
    best_mass, best_rate = upper_mass, 0.0

    for _ in range(MAX_BINARY_ITERATIONS):
        test_mass = 0.5 * (lower_mass + upper_mass)
        rate, failed, _ = simulate_ascent_rate_f(start_alt, burst_alt, test_mass)

        if failed or rate < target_rate:
            lower_mass = test_mass
        else:
            upper_mass = test_mass
            best_mass, best_rate = test_mass, rate
            
        if abs(best_rate - target_rate) < RATE_TOLERANCE:
            break
    return best_mass, best_rate

def ascent_solver_f(start_altitude: float, burst_altitude: float, target_rate: float) -> dict:
    start_time = time.perf_counter() # Start high-precision timer

    summary = {
        "inputs": {"start_altitude": start_altitude, "burst_altitude": burst_altitude, "target_rate": target_rate},
        "results": {
            "helium_mass": None, 
            "achieved_rate": 0.0, 
            "initial_gage_force": 0.0, 
            "success": False, 
            "history": [],
            "calculation_time": 0.0 # Placeholder
        },
        "limits": {"max_helium_mass": MAX_HELIUM_MASS, "atmosphere_ceiling": MAX_ATMOSPHERE_ALTITUDE},
        "forces_at_launch": None,
        "status": {"solution_found": False, "error": None},
    }

    error = validate_inputs_f(start_altitude, burst_altitude, target_rate)
    if error:
        summary["status"]["error"] = error
        summary["results"]["calculation_time"] = time.perf_counter() - start_time
        return summary

    # Core logic (Binary search + final history run)
    helium_mass, rate = solve_helium_mass_f(start_altitude, burst_altitude, target_rate)
    _, failed, final_history = simulate_ascent_rate_f(start_altitude, burst_altitude, helium_mass, keep_history=True)

    if failed and rate < target_rate:
        summary["status"]["error"] = "Target ascent rate not achievable"
        summary["results"]["calculation_time"] = time.perf_counter() - start_time
        return summary

    # Physics calculations
    atm_launch = ATM_CACHE.get_atm(start_altitude)
    buoyant = buoyant_force_f(start_altitude, helium_mass, atm=atm_launch)
    gravity = gravity_force_f(start_altitude, CONSTANT_MASS + helium_mass)
    gage_gravity = gravity_force_f(start_altitude, GAGE_MASS_KG)
    
    summary["forces_at_launch"] = {
        "buoyant_force": buoyant,
        "gravity_force": gravity,
        "net_force": buoyant - gravity,
        "initial_acceleration": (buoyant - gravity) / (CONSTANT_MASS + helium_mass),
    }

    # Finalize results
    summary["results"].update({
        "helium_mass": helium_mass,
        "achieved_rate": rate,
        "initial_gage_force": buoyant - gage_gravity,
        "success": True,
        "history": final_history
    })
    summary["status"]["solution_found"] = True

    # Stop timer and store result
    summary["results"]["calculation_time"] = time.perf_counter() - start_time
    return summary

def main():
    try:
        b_alt = float(input("Burst Altitude [m]: "))
        s_alt = float(input("Starting Altitude [m]: "))
        t_rate = float(input("Desired Ascent Rate [m/s]: "))
        v_check_str = input("Altitude for velocity check [m] (Leave blank to skip): ")

        summary = ascent_solver_f(s_alt, b_alt, t_rate)

        if not summary["results"]["success"]:
            log_entry_f("ERROR", summary, error=summary["status"]["error"])
            print(f"Error: {summary['status']['error']}")
            return

        res = summary["results"]
        closest_step = None
        if v_check_str.strip():
            check_alt = float(v_check_str)
            closest_step = min(res["history"], key=lambda x: abs(x["altitude"] - check_alt))

        # Outputs
        print(f"\nHelium mass required [kg]: {res['helium_mass']:.4f}")
        print(f"Initial gage force [N]: {res['initial_gage_force']:.4f}")
        print(f"Achieved ascent rate [m/s]: {res['achieved_rate']:.4f}")
        if closest_step:
            print(f"Velocity at {closest_step['altitude']:.2f} m: {closest_step['velocity']:.4f} m/s")
        
        # New console output
        print(f"Calculation time: {res['calculation_time']:.6f} seconds")

        log_entry_f("SUCCESS", summary, closest_step)

    except ValueError as e:
        print(f"Input Error: Please enter numeric values. ({e})")

if __name__ == "__main__":
    main()