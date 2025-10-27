function H = Z2H(Z)
    r0 = 6356766;
    H = Z*r0/(r0+Z);