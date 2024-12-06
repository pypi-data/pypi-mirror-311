from typing import Generator, Union
from decimal import Decimal

from numpy import float64, longdouble


def float_to_str(inputValue: Union[float, Decimal, float64, longdouble], precision: int = 10):
    """
    Formats fractional float or Decimal to a string with a specific decimal precision.
    Has decimal format
    """
    return (f'%.{precision}f' % longdouble(inputValue)).rstrip('0').rstrip('.')

def float_to_str2(inputValue: Union[float, Decimal, float64, longdouble]):
    """
    Formats fractional float or Decimal to a string.
    May have scientific format. Doesn't round. Displays integer format if decimal part is 0
    """
    return str(longdouble(inputValue)).rstrip('0').rstrip('.')


# like python range, but for floats
def frange(x1: Union[float, Decimal], x2: Union[float, Decimal], step: Union[float, Decimal]) -> Generator[float64, None, None]:
    while x1 <= x2:
        yield float64(x1)
        x1 = Decimal(x1) + Decimal(step)


def precise_float_diff(flt1: Union[float, float64], flt2: Union[float, float64]):
    return float64(Decimal(str(flt1)) - Decimal(str(flt2)))
