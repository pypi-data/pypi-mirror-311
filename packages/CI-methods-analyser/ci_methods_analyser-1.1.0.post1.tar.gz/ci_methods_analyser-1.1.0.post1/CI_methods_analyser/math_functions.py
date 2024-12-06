from functools import lru_cache
from math import sqrt as math_sqrt

from numpy import floor as np_floor, ceil as np_ceil
from scipy.stats import norm as normal_distribution, binom as binomial_distribution


@lru_cache(1000)
def normal_z_score(p: float = 0.95) -> float:
    """
    Answers the question: "At what point in terms of number of standard deviations from the mean
    the area spanning from -inf to that point on the normal distribution cover `p` of its area

    https://en.wikipedia.org/wiki/Standard_score#/media/File:Z_score_for_Students_A.png
    https://mat117.wisconsin.edu/wp-content/uploads/2014/12/Sec03.-z-score-5.png
    https://cdn1.byjus.com/wp-content/uploads/2017/09/word-image2.png
    """
    return normal_distribution.ppf(p)

@lru_cache(1000)
def normal_z_score_two_tailed(p: float = 0.95) -> float:
    """
    Answers the question: "How many standard deviations from the mean we have to span
    equally in both sides in a normal distribution to cover `p` of the area"

    https://www.freecodecamp.org/news/content/images/2020/08/normal_dist_68_rule.jpg
    https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Standard_deviation_diagram.svg/1920px-Standard_deviation_diagram.svg.png
    """
    return normal_distribution.ppf((1+p)/2)

@lru_cache(1000)
def normal_p_area(z: float) -> float:
    """
    Answers the question: "How much area under the normal distribution curve does
    the range from -inf to `z` cover (`z` - number of standard deviations from the mean)"

    https://en.wikipedia.org/wiki/Standard_score#/media/File:Z_score_for_Students_A.png
    https://mat117.wisconsin.edu/wp-content/uploads/2014/12/Sec03.-z-score-5.png
    https://cdn1.byjus.com/wp-content/uploads/2017/09/word-image2.png
    """
    return normal_distribution.cdf(z)

@lru_cache(1000)
def normal_p_area_two_tailed(z: float) -> float:
    """
    Answers the question: "How much area does the range cover that spans
    `z` standard deviations from the mean in equally both sides in a normal distribution"

    https://www.freecodecamp.org/news/content/images/2020/08/normal_dist_68_rule.jpg
    https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Standard_deviation_diagram.svg/1920px-Standard_deviation_diagram.svg.png
    """
    return (2*normal_distribution.cdf(z)) - 1


@lru_cache(500_000)
def binomial_distribution_two_tailed_range(n: int, p: float, sds: float):
    """
    Calculates range of `x` values that span `sds` standard deviations
    from the mean of a binomial distribution with parameters `n` and `p`: `Binom(n,p)`
    """
    M = n*p
    sd = math_sqrt(n*p*(1-p))
    (x_from, x_to) = max(0, np_floor(M - sds*sd) - 1), min(n, np_ceil(M + sds*sd) + 1)
    # (y_from, y_to) = binomial_distribution.pmf(x_from, n, p), binomial_distribution.pmf(x_to, n, p)
    return int(x_from), int(x_to)

def binomial_distribution_two_tailed_range_mass_coverage(n: int, p: float, sds: float) -> float:
    """
    Calculates the probability (mass) coverage by range of `sds` standard deviations from the mean
    of a particular binomial distribution defined by given `n` and `p`: `Binom(n,p)`
    """
    x_from, x_to = binomial_distribution_two_tailed_range(n, p, sds)
    return sum([binomial_distribution.pmf(x, n, p) for x in range(x_from, x_to+1)])


@lru_cache(500_000)
def binomial_distribution_pmf(x, n, p):
    return binomial_distribution.pmf(x, n, p)


@lru_cache(1000)
def get_binomial_z_precision(confidence: float) -> float:
    if not 0.01 < confidence < 1: raise ValueError(
        f"confidence level has to be a real value between 0 and 1. Got: confidence={confidence}")

    # This had been shown to be more optimal formula by the test at `/test_difference.py`
    z_precision = normal_z_score_two_tailed(confidence)*1.3 + 1.4
    return round(z_precision, 2)


if __name__ == '__main__':
    assert 2.4 < get_binomial_z_precision(0.60)# < 4.5
    assert 2.9 < get_binomial_z_precision(0.80)# < 4.7
    assert 3.4 < get_binomial_z_precision(0.90)# < 5
    assert 3.9 < get_binomial_z_precision(0.95)# < 5.5
    assert 4.4 < get_binomial_z_precision(0.99)# < 6
    assert 4.9 < get_binomial_z_precision(0.999)# < 7.5
    assert 5.3 < get_binomial_z_precision(0.9999)# < 8
    assert 5.7 < get_binomial_z_precision(0.99999)# < 9
    assert 6.1 < get_binomial_z_precision(0.999999)# < 10
    assert 6.4 < get_binomial_z_precision(0.9999999)# < 11
    assert 6.8 < get_binomial_z_precision(0.99999999)# < 11
    assert 7.2 < get_binomial_z_precision(0.999999999)# < 12
    assert 7.5 < get_binomial_z_precision(0.9999999999)# < 12

