import os
from datetime import datetime

def log_entry_f(status: str, summary: dict, closest_step: dict = None, error: str = None) -> None:
    log_dir = "log"
    log_file = os.path.join(log_dir, "ascent_log.txt")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calc_time = summary.get('results', {}).get('calculation_time', 0.0)
    
    with open(log_file, "a") as f:
        f.write(f"--- Run at {timestamp} | Status: {status} ---\n")
        
        if error:
            f.write(f"Error: {error}\n")
        else:
            inputs = summary.get('inputs', {})
            results = summary.get('results', {})
            
            f.write(
                f"Inputs: Start={inputs.get('start_altitude')}m, "
                f"Burst={inputs.get('burst_altitude')}m, "
                f"Target={inputs.get('target_rate')}m/s\n"
            )
            
            f.write(
                f"Outputs: Helium={results.get('helium_mass', 0):.4f}kg, "
                f"Mean Rate={results.get('achieved_rate', 0):.4f}m/s, "
                f"Gage Force={results.get('initial_gage_force', 0):.4f}N\n"
            )
            
            if closest_step:
                f.write(
                    f"Point Check: Alt={closest_step.get('altitude', 0):.2f}m, "
                    f"Vel={closest_step.get('velocity', 0):.4f}m/s\n"
                )
            
            # New log line for timing
            f.write(f"Performance: Calculation Time = {calc_time:.6f}s\n")
                
        f.write("-" * 50 + "\n\n")