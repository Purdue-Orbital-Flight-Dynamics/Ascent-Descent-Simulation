def ideal_gas(mass, molar_mass=0.0040026, temp=294.26, pressure=1):
    # returns ft^3
    
    R_s = (8.2057e-5 * 35.3147) / molar_mass  # ft^3·atm/(kg·K)
    return mass * R_s * temp / pressure