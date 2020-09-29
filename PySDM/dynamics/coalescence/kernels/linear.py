"""
Created at 27.08.2020 by claresinger
"""

from PySDM.physics import constants as const

class Linear:
    def __init__(self, a):
        self.a = a
        
    def __call__(self, output, is_first_in_pair):
        #pair in order (R, r) to temporary memory self.tmp
        self.tmp.sort_pair(self.core.state['radius'], is_first_in_pair) #pair in order (R, r) to temporary memory self.tmp: see gravitational.py
        # f(R,r) = R+r, for R>=r
        output.polynomial_pair(self.tmp, is_first_in_pair, coef_0=(1,), coef_1=(1,), pow_0=(1), pow_1=(1))

    def register(self, builder):
        self.core = builder.core
        builder.request_attribute('volume')
