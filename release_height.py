import math

PI = math.pi

def to_rad(deg):
    return deg * PI / 180

def to_deg(rad):
    return rad * 180 / PI

h_0 = 4 # ft, payload height above ground
L = 40 # ft, rope length

m_He = 2.7527
rho_air = 1.2050
rho_He = 0.1786
m_prime = 13
C_d = .25
g = -9.81

# angle from the horizontal. Smaller number is more permitting.
theta_cr = math.asin(1 - h_0 / L) # rad

print(to_deg(theta_cr))

numerator = 2 * g * (m_He * (rho_air * rho_He - 1) - m_prime) * (1 / math.tan(theta_cr))

denominator = (
    math.pi
    * ((3 * m_He * rho_He) / (4 * math.pi)) ** (2 / 3)
    * rho_air
    * C_d
)

V_inf_cr = math.sqrt(numerator / denominator)

print(V_inf_cr)