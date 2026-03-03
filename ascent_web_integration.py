from ascent_simulation import ascent_solver_f

data = ascent_solver_f(
    start_altitude=0.0,
    burst_altitude=10000.0,
    target_rate=5.0,
)

for section, contents in data.items():
    print(f"\n[{section}]")

    if not isinstance(contents, dict):
        print(contents)
        continue

    for key, value in contents.items():
        print(f"{key:30s} {value}")