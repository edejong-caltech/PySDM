"""
Created at 03.06.2019
Modified by edejong 12.10.2020
"""

from scipy.stats import lognorm, expon, norm, gamma
import math
import numpy as np
from scipy.interpolate import interp1d


class Spectrum:

    def __init__(self, distribution, distribution_params, norm_factor):
        self.distribution_params = distribution_params  # (loc, scale)
        self.norm_factor = norm_factor
        self.distribution = distribution

    def size_distribution(self, x):
        result = self.norm_factor * self.distribution.pdf(x, *self.distribution_params)
        return result

    def stats(self, moments):
        result = self.distribution.stats(*self.distribution_params, moments)
        return result

    def cumulative(self, x):
        result = self.norm_factor * self.distribution.cdf(x, *self.distribution_params)
        return result

    def percentiles(self, cdf_values):
        result = self.distribution.ppf(cdf_values, *self.distribution_params)
        return result


class Exponential(Spectrum):

    def __init__(self, norm_factor, scale):
        super().__init__(expon, (
            0,     # loc
            scale  # scale = 1/lambda
        ), norm_factor)


class Lognormal(Spectrum):

    def __init__(self, norm_factor: float, m_mode: float, s_geom: float):
        super().__init__(lognorm, (
            math.log(s_geom),  # geometric std dev
            0,                 # loc
            m_mode             # scale
        ), norm_factor)

class Gaussian(Spectrum):
    
    def __init__(self, norm_factor, loc, scale):
        super().__init__(norm, (
            loc,     # mean
            scale    # std dev
        ), norm_factor)
        
        
class Gamma(Spectrum):
    
    def __init__(self, norm_factor, k, theta):
        super().__init__(gamma, (
            k,       # shape factor
            0,       # loc
            theta    # scale
        ), norm_factor)
                 
        
class Sum:

    def __init__(self, spectra: tuple, percentile=.001):
        self.spectra = spectra
        self.norm_factor = sum((s.norm_factor for s in self.spectra))
        num = 999
        p = [s.percentiles(np.linspace(percentile, 1-percentile, num)) for s in self.spectra]
        x = np.zeros(num * len(self.spectra) + 1)
        x[1:] = np.concatenate(p)
        y = self.cumulative(x) / self.norm_factor
        self.inverse_cdf = interp1d(y, x)

    def size_distribution(self, x):
        result = 0.
        for spectrum in self.spectra:
            result += spectrum.size_distribution(x)
        return result

    def cumulative(self, x):
        result = 0.
        for spectrum in self.spectra:
            result += spectrum.cumulative(x)
        return result

    def percentiles(self, cdf_values):
        return self.inverse_cdf(cdf_values)
