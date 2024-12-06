// Copyright (c) 2021 Patricio Cubillos
// Pyrat Bay is open-source software under the GNU GPL-2.0 license (see LICENSE)

#include <math.h>

// Exponential integral of the first order
// Approximation by Abramowitz & Stegun (1970),
// As described by Lavie et al. (2017)

static double expn_abramowitz(double x){
    double expn;

    double A0 = -0.57721566;
    double A1 =  0.99999193;
    double A2 = -0.24991055;
    double A3 =  0.05519968;
    double A4 = -0.00976004;
    double A5 =  0.00107857;

    double B0 = 1.0;
    double B1 = 8.5733287401;
    double B2 = 18.059016973;
    double B3 = 8.6347608925;
    double B4 = 0.2677737343;

    double C0 = 1.0;
    double C1 = 9.5733223454;
    double C2 = 25.6329561486;
    double C3 = 21.0996530827;
    double C4 = 3.9584969228;

    if (x <= 1.0)
        expn = -log(x)
            + A0 + A1*x + A2*x*x
            + A3*pow(x,3.0) + A4*pow(x,4.0) + A5*pow(x,5.0);
    else
        expn = exp(-x) / x
            * (B4 + B3*x + B2*x*x + B1*pow(x,3.0) + B0*pow(x,4.0))
            / (C4 + C3*x + C2*x*x + C1*pow(x,3.0) + C0*pow(x,4.0));
    return expn;
}

