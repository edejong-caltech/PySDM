"""
Created at 15.02.2021 by edejong
"""

import numpy as np
from PySDM.initialisation.spectra import Exponential
from PySDM.physics.constants import si


class Settings:

    n_sd = 2 ** 13                                        # number of superdroplets
    n_part = 239 / si.cm**3                            # particle density #/cm3
    X0 = 4 / 3 * np.pi * (30.531 * si.micrometres) ** 3   # scale factor of initial dist
    dv = 1e1 * si.m**3                                    # box volume
    x_min_r = 10 * si.um
    x_max_r = 5e3 * si.um
    
    norm_factor = n_part * dv
    dt = 1 * si.seconds
    adaptive = False
    seed = 44
    _steps = [0, 1200]

    @property
    def steps(self):
        return [int(step/self.dt) for step in self._steps]

    spectrum = Exponential(norm_factor=norm_factor, scale=X0)

    radius_bins_edges = np.logspace(np.log10(x_min_r), np.log10(x_max_r), num=128, endpoint=True)
