from typing import Union
from functools import lru_cache
from math import sqrt as math_sqrt

from CI_methods_analyser.math_functions import normal_z_score_two_tailed


@lru_cache(100_000)
def wald_interval(x: int, n: int, conflevel: float = 0.95):
    # LaTeX: $$(w^-, w^+) = \hat{p}\,\pm\,z\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$
    """Calculates confidence interval for proportions using Wald Interval method

    `x` - succeeded trials

    `n` - total trials

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    if x > n:
        raise ValueError(f"Number of succeeded trials (x) has to be no more than number of total trials (n). x = {x} and n = {n} were passed")

    z = normal_z_score_two_tailed(conflevel)

    p = float(x)/n
    sd = math_sqrt((p*(1-p))/n)
    z_sd = z*sd
    ci = (
        p - z_sd,
        p + z_sd
    )
    return ci


@lru_cache(100_000)
def wilson_score_interval(x: int, n: int, conflevel: Union[float, None] = 0.95, z: Union[float, None] = None):
    # LaTeX: $$(w^-, w^+) = \frac{p + z^2/2n \pm z\sqrt{p(1-p)/n + z^2/4n^2}}{1+z^2/n}$$
    """Calculates confidence interval for proportions using Wilson Score Interval method

    `x` - succeeded trials

    `n` - total trials

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    if x > n:
        raise ValueError(f"Number of succeeded trials (x) has to be no more than number of total trials (n). x = {x} and n = {n} were passed")

    z = normal_z_score_two_tailed(conflevel)

    p = float(x)/n
    denom = 1 + ((z**2) / n)
    mean = p + ((z**2)/(2*n))
    diff = z * math_sqrt(p*(1-p)/n + (z**2)/(4*n**2))
    ci = (
        (mean-diff)/denom,
        (mean+diff)/denom
    )
    return ci


@lru_cache(100_000)
def wilson_score_interval_continuity_corrected(x: int, n: int, conflevel: Union[float, None] = 0.95, z: Union[float, None] = None):
    # LaTeX:
    # $$w_{cc}^- = \frac{2np + z^2 - (z\sqrt{z^2 - 1/n + 4np(1-p) + (4p-2)} + 1)}{2(n+z^2)}$$
    # $$w_{cc}^+ = \frac{2np + z^2 + (z\sqrt{z^2 - 1/n + 4np(1-p) - (4p-2)} + 1)}{2(n+z^2)}$$
    # or, simplified:
    # $$e = 2np + z^2;\,\,\, f = z^2 - 1/n + 4np(1-p);\,\,\, g = (4p - 2);\,\,\, h = 2(n+z^2)$$
    # $$w_{cc}^- = \frac{e - (z\sqrt{f+g} + 1)}{h}$$
    # $$w_{cc}^+ = \frac{e + (z\sqrt{f-g} + 1)}{h}$$
    """Calculates confidence interval for proportions using Wilson Score Interval method with correction for continuity

    `x` - succeeded trials

    `n` - total trials

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    if x > n:
        raise ValueError(f"Number of succeeded trials (x) has to be no more than number of total trials (n). x = {x} and n = {n} were passed")

    z = normal_z_score_two_tailed(conflevel)

    p = float(x)/n
    e = 2*n*p + z**2
    f = z**2 - 1/n + 4*n*p*(1-p)
    g = (4*p - 2)
    h = 2*(n+z**2)
    ci = (
        (e - (z*math_sqrt(f+g) + 1))/h,
        (e + (z*math_sqrt(f-g) + 1))/h
    )
    return ci


@lru_cache(100_000)
def wilson_score_interval_continuity_semicorrected(x: int, n: int, conflevel: Union[float, None] = 0.95, z: Union[float, None] = None):
    """Calculates confidence interval for proportions using two Wilson Score Interval methods
    (arithmetic mean of ordinary and continuity-corrected methods)

    `x` - succeeded trials

    `n` - total trials

    `conflevel` - confidence level (0 < float < 1). Defaults to 0.95 if its unset and *z* is unset

    `z` - z score. If unset, calculated form the given *conflevel*
    """
    if x > n:
        raise ValueError(
            f"Number of succeeded trials (x) has to be no more than number of total trials (n). x = {x} and n = {n} were passed")

    z = normal_z_score_two_tailed(conflevel)

    uncorrected = wilson_score_interval(x, n, conflevel, z)
    corrected   = wilson_score_interval_continuity_corrected(x, n, conflevel, z)
    ci = (
        (corrected[0]+uncorrected[0])/2,
        (corrected[1]+uncorrected[1])/2
    )
    return ci
