import os
from datetime import datetime

def log_descent_entry(status: str, summary: dict, error: str = None) -> None:
    log_dir = "log"
    log_file = os.path.join(log_dir, "descent_log.txt")

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
                f"Inputs: Burst Alt={inputs.get('burst_altitude', 0)}m, "
                f"Payload Mass={inputs.get('payload_mass', 0)}kg, "
                f"Chute Deploy Time={inputs.get('parachute_deploy_time', 0)}s\n"
            )
            
            # Handle terminal velocity formatting safely if it wasn't reached
            term_vel = results.get('terminal_velocity_value')
            term_str = f"{term_vel:.2f}m/s" if term_vel is not None else "Not reached"
            
            f.write(
                f"Outputs: Final Time={results.get('final_time', 0):.2f}s, "
                f"Final Velocity={results.get('final_velocity', 0):.2f}m/s, "
                f"Terminal Velocity={term_str}\n"
            )
            
            # Log calculation performance
            f.write(f"Performance: Calculation Time = {calc_time:.6f}s\n")
                
        f.write("-" * 50 + "\n\n")