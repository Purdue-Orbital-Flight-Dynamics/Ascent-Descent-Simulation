from ascent_simulation import ascent_solver

data = ascent_solver(start_alt_m=0, burst_alt_m=10000, target_rate_mps=5.0)

for section, contents in data.items():
    print(f"\n[{section}]")

    if not isinstance(contents, dict):
        print(contents)
        continue

    for k, v in contents.items():
        print(f"{k:30s} {v}")