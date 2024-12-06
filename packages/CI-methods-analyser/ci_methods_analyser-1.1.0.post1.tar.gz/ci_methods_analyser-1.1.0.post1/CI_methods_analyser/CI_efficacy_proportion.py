from typing import Callable, List, Literal, Tuple, Union, TypedDict
from collections import defaultdict
from decimal import Decimal

from numpy import float64, longdouble, mean as np_mean, array as np_array, ndarray as np_adarray
from numpy.random import binomial as binomial_experiment
from matplotlib import pyplot as plt
from scipy.stats import binom as binomial_distribution
from tqdm.std import trange

from CI_methods_analyser.math_functions import binomial_distribution_two_tailed_range, get_binomial_z_precision, normal_z_score_two_tailed
from CI_methods_analyser.data_functions import float_to_str, frange, precise_float_diff
from CI_methods_analyser.CI_efficacy import CImethod_efficacyToolkit, NoCoverageException, plot_styles


CI_method_for_proportion = Callable[
    [int, int, float],
    Tuple[float, float]
]


proportion_type = Union[str, float, float64, Decimal]

# This is how dictionary type is defined
class proportions_type_range_named(TypedDict):
    start: proportion_type
    end: proportion_type
    step: proportion_type

proportions_type_range = Tuple[proportion_type, proportion_type, proportion_type]

proportions_type_list = Union[List[float], List[float64]]

proportions_type = Union[proportions_type_list, proportions_type_range, proportions_type_range_named]



class CImethodForProportion_efficacyToolkit_format():
    proportion_str_max_len: int
    coverage_str_max_len_total: int
    coverage_str_max_len_afterpoint: int

    confidence: str
    confidence_percent: str


    def __init__(self, efficacy_toolkit):
        self.efficacy_toolkit: CImethodForProportion_efficacyToolkit = efficacy_toolkit

    def calculation_inputs(self):
        printed_inputs = (
            f"CI_method = '{self.efficacy_toolkit.method_name}', confidence = {float_to_str(self.efficacy_toolkit.confidence*100)}%,\n"
            f"n = {self.efficacy_toolkit.sample_size}, ps[{len(self.efficacy_toolkit.proportions)}] = ({self.efficacy_toolkit.proportions[0]}...{self.efficacy_toolkit.proportions[-1]},d={precise_float_diff(self.efficacy_toolkit.proportions[1], self.efficacy_toolkit.proportions[0])})"
        )
        return printed_inputs

    """
    None of the following functions should be used before their dependent properties of this class
    were assigned.
    Checks/assertions are not made for performance reasons.
    These functions are meant to be executed millions+ of times within seconds.
    """

    def proportion(self, proportion_value):
        return f"{proportion_value:{self.proportion_str_max_len}}"

    def coverage(self, single_coverage_value):
        return f"{single_coverage_value:{self.coverage_str_max_len_total}.{self.coverage_str_max_len_afterpoint}f}"


class CImethodForProportion_efficacyToolkit(CImethod_efficacyToolkit):
    """A toolkit for studying efficacy of a CI method for the proportion.

    Parameters
    ----------
    method : CI_method
        a studied method for calculating CI for the proportion

    method_name : str
        a human-readable name of the method.

    Attributes
    ----------
    method : CI_method
        a studied method for calculating CI for the proportion

    method_name : str
        a human-readable name of the method.

    confidence : float
        A number between 0 and 1.
        Confidence interval - coverage that you want to get
        (see frequentist definition of confidence interval).

    sample_size : int
        Total number of trials in the sample

    proportions : List[np.float64]
        A list of true proportions to try.

    coverage : np.ndarray
        1d array, np.longdouble, values between 0 and 100
        Coverage represents a proportion of cases that fall under the confidence interval produced
        by the given `method` for a particular proportion from the given list.
        User can assess the efficacy of a CI method by comparing these values to the `confidence`.
         - Values `< confidence` mean the `method` is more likely to cause a type I error.
         In simple words, this is bad because you would not be able say
         you are `confidence*100`% confident that the true difference between two true
         population proportions lies within the interval calculated by the `method`.
         - Values `> confidence` mean the `method` is even less likely to cause a type I error,
         but may be more likely to cause a type II error.
         In simple words, it doesn't necessarily mean the `method` is bad, but it's
         just "concervative". Whether it is way too concenrvative or not is up to you.
         If you pass `0.95` (95%) to the `method`, and it gives you 99.5% coverage, 
         it is hell of a concervative method.

    average_coverage : np.longdouble
        average of all values in `coverage`

    average_deviation : np.longdouble
        average deviation of all values in `coverage` from `confidence`

    f : CImethodForProportion_efficacyToolkit_format
        Formatting helper. See the class

    figure : matplotlib.figure.Figure
        a matplotlib figure that's being generated by plotting the `coverage`

    """


    def __init__(self, method: CI_method_for_proportion, method_name: str):
        self._method: CI_method_for_proportion = method
        self._method_name: str = method_name

        self._f = CImethodForProportion_efficacyToolkit_format(self)


    @property
    def confidence(self):
        return self._confidence

    @confidence.setter
    def confidence(self, value: float):
        if not 0.01 < value < 1: raise ValueError(
            f"confidence level has to be a real value between 0 and 1. Got: confidence={value}")
        self._confidence = value

        self.f.coverage_str_max_len_total = max(len(str(value))+2, 5)
        # 3 characters are reserved: 2 for tens and units, 1 for point
        self.f.coverage_str_max_len_afterpoint = max(self._f.coverage_str_max_len_total-3, 2)

        self.f.confidence = float_to_str(value)
        self.f.confidence_percent = f"{float_to_str(value*100)}%"


    @property
    def sample_size(self):
        return self._sample_size

    @sample_size.setter
    def sample_size(self, value: int):
        if not value > 0: raise ValueError(
            f"sample size has to be greater than 0. Got: sample_size={value}")
        self._sample_size = value


    @property
    def proportions(self) -> List[float64]:
        return self._proportions

    def form_proportions_list(self,
        proportions: proportions_type
    ):
        if type(proportions) is tuple:
            # proportions is proportions_type_range
            (start, end, step) = proportions
            return list(frange(
                Decimal(str(start)), Decimal(str(end)), Decimal(str(step))
            ))
        elif type(proportions) is proportions_type_range_named:
            (start, end, step) = (proportions["start"], proportions["end"], proportions["step"])
            return list(frange(
                Decimal(str(start)), Decimal(str(end)), Decimal(str(step))
            ))
        elif type(proportions) is list:
            # proportions is proportions_type_list
            return [float64(p) for p in proportions]
        else:
            raise ValueError(
                f"Somehow, the passed argument `proportions` is of wrong type")

    @proportions.setter
    def proportions(self, value: List[float64]):
        if not all([0 <= p <= 1 for p in value]): raise ValueError(
            f"a true population proportion can only be a real value between 0 and 1")
        if len(value) == 0: raise ValueError(
            f"list of proportions has to have at least 1 value")
        self._proportions = value

        self.f.proportion_str_max_len = max(len(str(self.proportions[0])),
                                            len(str(self.proportions[1])),
                                            len(str(self.proportions[-1])))


    @property
    def coverage(self):
        return self._coverage

    @coverage.setter
    def coverage(self, value: Union[List[longdouble], np_adarray]):
        self._coverage = value
        self._average_coverage: longdouble = np_mean(value, dtype=longdouble)
        self._average_deviation: longdouble = np_mean(
            abs(np_array(value) - (self.confidence*100)), dtype=longdouble)        

    @property
    def average_coverage(self) -> longdouble:
        return self._average_coverage

    @property
    def average_deviation(self) -> longdouble:
        return self._average_deviation


    @property
    def f(self) -> CImethodForProportion_efficacyToolkit_format:
        return self._f


    def calculate_coverage_randomly(self,
            sample_size: int,
            proportions: proportions_type,
            confidence: float,
            n_of_experiments: int = 20000
            ):
        """
        Calculates true coverage of confidence interval for proportion
        produced by the `method` for the given desired `confidence` using a simulation
        with a number of random experiments (`n_of_experiments`).

        Total number of trials in a sample is `sample_size`.

        Proportion for the sample is taken from the list `proportions`,
        producing a list of results, a value for each proportion.

        This list is `coverage`, and is saved to `self.coverage`.
        """
        self.confidence = confidence
        self.proportions = self.form_proportions_list(proportions)
        self.sample_size = sample_size

        if __debug__ is True:
            print(
                self.f.calculation_inputs() + ",\n"
                f"calculation_method = random simulation, " +
                f"n_of_experiments = {n_of_experiments}"
            )

        coverage = []

        # The return value of this function will be cached (this is not necessary)
        z = normal_z_score_two_tailed(p=confidence)

        progress_bar_str = "p={} => cov={}%"
        t = trange(len(self.proportions),
                   desc=progress_bar_str.format("***", "***"))
        for i in t:
            prob = self.proportions[i]
            x = binomial_experiment(sample_size, prob, n_of_experiments)

            CIs = [self.method(x[j], sample_size, confidence) for j in range(0, n_of_experiments)]
            covered = [int(CI[0] < prob < CI[1]) for CI in CIs]

            # multiplied by 100 in-place for better progress bar, and for a better figure later
            thiscoverage = (sum(covered)/n_of_experiments) * 100

            coverage.append(thiscoverage)

            t.set_description(progress_bar_str.format(
                self.f.proportion(prob),
                self.f.coverage(thiscoverage)))

        self.coverage = coverage
        t.set_description(progress_bar_str.format(
            "*", "*", self.f.coverage(self.average_coverage)))
        print(f"average confidence level {self.f.coverage(self.average_coverage)}")
        print(f"average deviation from {self.f.confidence_percent} = {self.f.coverage(self.average_deviation)} (coverage %)")
        print("")
        return self.coverage


    def calculate_coverage_analytically(self,
            sample_size: int,
            proportions: proportions_type,
            confidence: float,
            z_precision: Union[float, Literal['auto']] = 'auto'
            ):
        """
        Calculates true coverage of confidence interval for proportion
        produced by the `method` for the given desired `confidence` using
        an indistinguishably precise approximation for the analytical solution.

        Optimal approximation precision is auto-picked for the specific case,
        but can be set manually in `z_precision`. This is a z-value for precision instead of p.
        Meaning, `z_precision` of 1.96 is 95% precision (which is a terrible precision).
        See more comments below for the actual meaning of z_precision.

        Total number of trials in a sample is `sample_size`.

        Proportion for the sample is taken from the list `proportions`,
        producing a list of results, a value for each proportion.

        This list is `coverage`, and is saved to `self.coverage`.
        """
        self.confidence = confidence
        self.proportions = self.form_proportions_list(proportions)
        self.sample_size = sample_size

        if z_precision == 'auto':
            z_precision = get_binomial_z_precision(confidence)

        if __debug__ is True:
            print(
                self.f.calculation_inputs() + ",\n"
                f"calculation_method = analytical approximation, " +
                f"z_precision = {z_precision:5.2f}"
            )

        coverage = []

        # The return value of this function will be cached (this is not necessary)
        z = normal_z_score_two_tailed(p=confidence)

        progress_bar_str = "p={} => cov={}%"
        t = trange(len(self.proportions),
                   desc=progress_bar_str.format("***", "***"))
        for i in t:
            prob = self.proportions[i]

            """The entire range of the binomial distribution could be used"""
            #x_from, x_to = (0, sample_size)
            """
            But this is too computationally expensive to calculate CI for `y` value of each `x`
            of a binomial distribution.
            Since most `y` values of the binomial distribution are very close to zero,
            we can use only a small part of the binomial distribution around the peak.
            Such part of a binomial distribution can often be efficiently modeled
            with a normal distribution.

            Let's say we want to consider the span covering 99.999% of the mass
            of the binomial distribution. According to the normal distribution, this would be
            a range that spans 4.42 standard deviations from the mean on both sides.
            The span of 4.42 sigma would cover around 99.999% of a binomial distribution
            `Binom(n,p)` for most values of `n` and `p`. This would nail it for 95%CI, but
            what if a user wants to ask for 99.999%CI, and we are only considering 99.999%
            of the binomial distribution? We'd need to consider much more expansive range
            in our calculations.

            We would need something like this:
            for 95% confidence         => 99.995%         of the distribution (4.056 sigma)
            for 99% confidence         => 99.999%         of the distribution (4.417 sigma)
            for 99.9% confidence       => 99.9999%        of the distribution (4.892 sigma)
            for 99.99% confidence      => 99.999_99%      of the distribution (5.327 sigma)
            for significant range of 5 sigma:
            for 99.999_943% confidence => 99.999_999_943% of the distribution (6.199 sigma)
            etc.

            Thus, precision is to be determined given the `confidence`. A specific formula is used
            to figure out the optimal `z_precision`.
            """
            x_from, x_to = binomial_distribution_two_tailed_range(n=sample_size, p=prob, sds=z_precision)
            xs = range(x_from, x_to+1)

            CIs = [self.method(x, sample_size, confidence) for x in xs]

            # Array of `1`s and `0`s
            # int constructor could be used, but longdouble is used to provide better precision
            covered = [longdouble(CI[0] < prob < CI[1]) for CI in CIs]

            # multiplied by 100 in-place for better progress bar, and for a better figure later
            thiscoverage = sum(
                [covered[i]*binomial_distribution.pmf(xs[i], sample_size, prob) for i in range(len(xs))]
            ) * 100

            coverage.append(thiscoverage)

            t.set_description(progress_bar_str.format(
                self.f.proportion(prob),
                self.f.coverage(thiscoverage)))

        self.coverage = coverage
        t.set_description(progress_bar_str.format(
            "*", "*", self.f.coverage(self.average_coverage)))
        print(f"average confidence level {self.f.coverage(self.average_coverage)}")
        print(f"average deviation from {self.f.confidence_percent} = {self.f.coverage(self.average_deviation)} (coverage %)")
        print("")
        return self.coverage


    def plot_coverage(self,
            plt_figure_title: str,
            title: str = "Coverage of {method_name}\nsample size: n = {sample_size}",
            xlabel: str = "True Proportion (Population Proportion)",
            ylabel: str = "Coverage (%) for {confidence_percent}CI",
            theme: plot_styles = "default",
            plot_color: str = "blue",
            line_color: str = "red"
            ):
        """
        Plots the `matplotlib.pyplot` figure given the data from previous coverage calculation and
        some captions and formatting.
        """
        if not self.coverage: raise NoCoverageException(
            "you have to calculate coverage first before plotting it")

        # this unpacked defaultdict trouble allows for optional formatting placeholders
        title = title.format(**defaultdict(str, 
            method_name = self.method_name,
            sample_size = self.sample_size
        ))
        ylabel = ylabel.format(**defaultdict(str, 
            confidence_percent = self.f.confidence_percent,
            confidence = self.f.confidence
        ))


        plt.style.use(theme)

        fig = plt.figure(plt_figure_title)

        plt.plot(list(self.proportions), self.coverage,
                 color=plot_color, marker=',', linestyle='solid', zorder=5)
        plt.axhline(self.confidence*100,
                    color=line_color, linestyle=":", zorder=0)
        x1, x2, y1, y2 = plt.axis()
        # set vertical bondaries: from a point 10 times farther from 100 than `confidnece`, to 100
        y_min = 100 - ( (100-(self.confidence*100))*10 )
        plt.axis((x1, x2, y_min, 100))

        plt.title(title, fontsize="large", fontweight="bold")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        x1, x2, y1, y2 = plt.axis()
        # on the range (x1, x2) (left to right), the caption is centered in the middle
        # on the range (y1, y2) (bottom to top), the caption is on 1/10 of the way from y1 to y2
        plt.text(x = (x1+x2)/2,
                 y = y1 + (y2-y1)/10,
            s=f"average deviation from {self.f.confidence_percent} point = {self.f.coverage(self.average_deviation)} (coverage %)",
            ha="center", fontstyle="italic", fontsize=10, zorder=10)
        plt.xticks(fontsize=8)
        plt.ticklabel_format(scilimits=(-3,3), useMathText=True)

        self.figure = fig
        return fig


    def calculate_coverage_and_show_plot(self,
            sample_size: int,
            proportions: proportions_type,
            confidence: float,

            plt_figure_title: str = "",
            title: str = "Coverage of {method_name}\nsample size: n = {sample_size}",
            xlabel: str = "True Proportion (Population Proportion)",
            ylabel: str = "Coverage (%) for {confidence_percent}CI",
            theme: plot_styles = "default",
            plot_color: str = "blue",
            line_color: str = "red"
            ):
        self.calculate_coverage_analytically(sample_size, proportions, confidence)
        self.plot_coverage(plt_figure_title, title, xlabel, ylabel, theme, plot_color, line_color)
        self.show_plot()

