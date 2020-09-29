"""
Created at 28.09.2020 by edejong
"""

from PySDM.product import MomentProduct
from PySDM.physics import formulae as phys
import numpy as np


class ParticlesNumberVolumeSpectrum(MomentProduct):

    def __init__(self):
        super().__init__(
            name='N(v)',
            unit='1',
            description='Particles volume distribution',
            scale='linear',
            range=[20, 50]
        )
        self.moment_0 = None
        self.moments = None

    def register(self, builder):
        super().register(builder)
        self.moment_0 = builder.core.backend.Storage.empty(1, dtype=int)
        self.moments = builder.core.backend.Storage.empty((1, 1), dtype=float)

    def get(self, volume_bins_edges):
        vals = np.empty(len(volume_bins_edges) - 1)
        for i in range(len(vals)):
            self.download_moment_to_buffer(attr='volume', rank=1,
                                           filter_range=(volume_bins_edges[i], volume_bins_edges[i + 1]))
            vals[i] = self.buffer[0]
        return vals