"""
Created at 22.02.2021 by edejong
"""
import numpy as np
from PySDM.physics import constants as const

class Polynomial():

    def __init__(self, params):
        self.params = params
        self.core = None

    def __call__(self, output, is_first_in_pair):
        self.tmp.sort_pair(self.core.particles['volume'], is_first_in_pair)
        self.core.backend.polynomial_kernel(
            self.params, output, self.tmp, is_first_in_pair)
        
    def register(self, builder):
        self.core = builder.core
        builder.request_attribute('volume')
        self.tmp = self.core.IndexedStorage.empty(self.core.n_sd, dtype=float)
