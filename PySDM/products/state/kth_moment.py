"""
Created at 10.7.2020 by edejong
"""

from PySDM.product import MomentProduct
import numpy as np


class KthMoment(MomentProduct):

    def __init__(self):
        super().__init__(
            name='Mk',
            unit='unit (mass or vol)**k',
            description='kth moment of distribution',
            scale='linear',
            range=[20, 50]
        )
        
    def register(self, builder):
        super().register(builder)
        self.moment_0 = builder.core.backend.Storage.empty(1, dtype=int)
        self.moments = builder.core.backend.Storage.empty((1, 1), dtype=float)

    def get(self, k):
        if (k == 0):
            self.download_moment_to_buffer(attr='volume', rank=0)
            return self.buffer[0]
            
        else:
            val = 0
            self.download_moment_to_buffer(attr='volume', rank=k)
            val = self.buffer[0]
            self.download_moment_to_buffer(attr='volume', rank=0)
            val *= self.buffer[0]
            return val