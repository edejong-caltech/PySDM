"""
Created at 15.02.2021 by edejong
"""

import numpy as np

from PySDM.backends import CPU
from PySDM.builder import Builder
from PySDM.environments import Box
from PySDM.dynamics import Coalescence
from PySDM.dynamics.coalescence.kernels import SpecifiedEff
from PySDM.initialisation.spectral_sampling import ConstantMultiplicity

from PySDM.products.state import ParticlesVolumeSpectrum, KMoments


def run(settings, A=0, B=0, D1=0, D2=0, E1=0, E2=0, F1=0, F2=0, G1=0, G2=0, G3=0, Mf=0, Mg=0, backend=CPU):
    builder = Builder(n_sd=settings.n_sd, backend=backend)
    builder.set_environment(Box(dv=settings.dv, dt=settings.dt))
    attributes = {}
    attributes['volume'], attributes['n'] = ConstantMultiplicity(settings.spectrum).sample(settings.n_sd)
    kernel = SpecifiedEff(A=A, B=B, D1=D1, D2=D2, E1=E1, E2=E2, F1=F1, F2=F2, G1=G1, G2=G2, G3=G3, Mf=Mf, Mg=Mg)
    coalescence = Coalescence(kernel=kernel)
    coalescence.adaptive = settings.adaptive
    builder.add_dynamic(coalescence)
    products = [ParticlesVolumeSpectrum(), KMoments()]
    core = builder.build(attributes, products)
    if hasattr(settings, 'u_term') and 'terminal velocity' in core.particles.attributes:
        core.particles.attributes['terminal velocity'].approximation = settings.u_term(core)

    moments = {}
    for step in settings.steps:
        core.run(step - core.n_steps)
        moments[step] = core.products['M0-Mk'].get(3)

    return moments
