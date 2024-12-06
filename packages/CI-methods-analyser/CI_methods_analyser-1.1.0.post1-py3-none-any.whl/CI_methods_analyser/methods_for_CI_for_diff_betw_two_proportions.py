from typing import Tuple
from functools import lru_cache
from math import sqrt as math_sqrt

from numpy import sign, sqrt as np_sqrt, pi, cos, arccos

from CI_methods_analyser.math_functions import normal_z_score_two_tailed


@lru_cache(100_000)
def Z_test_unpooled(xT: int, nT: int, xC: int, nC: int, conflevel: float = 0.95) -> Tuple[float, float]:
    # LATEX: $$ (\delta^-, \delta^+) = \hat{p}_T - \hat{p}_C \pm z_{\alpha}\sqrt{\frac{\hat{p}_T (1 - \hat{p}_T)}{n_T} + \frac{\hat{p}_C (1 - \hat{p}_C)}{n_C}} $$
    """Calculates confidence interval for the difference between two proportions using Z test (unpooled) method

    `xT` - succeeded trials in the experimental (trial) group

    `nT` - total trials in the experimental (trial) group

    `xC` - succeeded trials in the control group

    `nC` - total trials in the control group

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    pT = float(xT)/nT
    pC = float(xC)/nC

    z = normal_z_score_two_tailed(conflevel)

    delta = pC - pT

    sd = math_sqrt((pT*(1-pT))/nT + (pC*(1-pC))/nC)
    z_sd = abs(z*sd)
    ci = (
        delta - z_sd,
        delta + z_sd
    )
    return ci


@lru_cache(100_000)
def Z_test_pooled(xT: int, nT: int, xC: int, nC: int, conflevel: float = 0.95) -> Tuple[float, float]:
    # LATEX: $$ (\delta^-, \delta^+) = \hat{p}_T - \hat{p}_C \pm z_{\alpha}\sqrt{\bar{p}(1-\bar{p})(\frac{1}{n_T}+\frac{1}{n_C})} $$
    # $$ \bar{p} = \frac{n_T\hat{p}_T + n_C\hat{p}_C}{n_T + n_C} $$
    """Calculates confidence interval for the difference between two proportions using Z test (pooled) method

    `xT` - succeeded trials in the experimental (trial) group

    `nT` - total trials in the experimental (trial) group

    `xC` - succeeded trials in the control group

    `nC` - total trials in the control group

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    pT = float(xT)/nT
    pC = float(xC)/nC

    z = normal_z_score_two_tailed(conflevel)

    delta = pC - pT

    p_bar = (nT*pT + nC*pC)/(nT + nC)

    sd = math_sqrt(p_bar*(1-p_bar)*(1/nT + 1/nC))
    z_sd = abs(z*sd)
    ci = (
        delta - z_sd,
        delta + z_sd
    )
    return ci


@lru_cache(100_000)
def Miettinen_and_Nurminen(xT: int, nT: int, xC: int, nC: int, conflevel: float = 0.95) -> Tuple[float, float]:
    """Calculates confidence interval for the difference between two proportions using Miettinen and Nurminen’s Likelihood Score Test

    `xT` - succeeded trials in the experimental (trial) group

    `nT` - total trials in the experimental (trial) group

    `xC` - succeeded trials in the control group

    `nC` - total trials in the control group

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """

    #x11 = xT
    #x21 = xC
    #x12 = yT
    #x22 = yC

    pT = float(xT)/nT # p1
    pC = float(xC)/nC # p2

    yT = nT - xT # x12
    yC = nC - xC # x22

    N = nT + nC  # N
    x = xT + xC  # m1
    y = yT + yT  # m2

    delta = pC - pT  # delta0



    L0 = xC*delta*(1-delta)
    L1 = (nC*delta - N - 2*yT)*delta + x
    L2 = (N + nC)*delta - N - x
    L3 = N

    C = (L2**3)/(27* L3**3) - (L1*L2)/(6* L3**2) + L0/(2*L3)

    B = sign(C) * np_sqrt(abs(L2**2/(9* L3**2) - L1/(3*L3)))

    if B == 0:
        under_arccos = 1
    else:
        under_arccos = C/(B**3)
    A = 1/3 * (pi + arccos(under_arccos - int(under_arccos)))


    pC_tilde = 2*B*cos(A) - L2/(3*L3)
    pT_tilde = pC_tilde + delta

    qC_tilde = 1 - pC_tilde
    qT_tilde = 1 - pT_tilde

    sd = np_sqrt(abs(( (pT_tilde*qT_tilde)/nT + (pC_tilde*qC_tilde)/nC ) *(N/(N-1))))


    z = normal_z_score_two_tailed(conflevel)
    z_sd = abs(z*sd)
    ci = (
        delta - z_sd,
        delta + z_sd
    )
    return ci


@lru_cache(100_000)
def Z_test_combined(xT: int, nT: int, xC: int, nC: int, conflevel: float = 0.95) -> Tuple[float, float]:
    """Calculates confidence interval for the difference between two proportions using Z test (combined) method

    `xT` - succeeded trials in the experimental (trial) group

    `nT` - total trials in the experimental (trial) group

    `xC` - succeeded trials in the control group

    `nC` - total trials in the control group

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    one = Z_test_unpooled(xT, nT, xC, nC, conflevel)
    two =   Z_test_pooled(xT, nT, xC, nC, conflevel)
    ci = (
        (one[0] + two[0])/2,
        (one[1] + two[1])/2
    )
    return ci

