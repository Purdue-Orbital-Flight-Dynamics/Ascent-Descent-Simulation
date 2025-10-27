function Z = H2Z(H)
    r0 = 6356766;
    Z = r0*H/(r0-H);