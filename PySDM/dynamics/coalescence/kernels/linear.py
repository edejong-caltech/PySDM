"""
Created at 24.08.2020 by claresinger
"""

from PySDM.physics import constants as const

class Linear:
    def __init__(self, a):
        self.a = a
        
    def __call__(self, output, is_first_in_pair):
        # TODO: linear kernel
        output.sum_pair(self.core.state['volume'],is_first_in_pair)
        output *= 0
        
    def register(self, builder):
        self.core = builder.core
        builder.request_attribute('volume')
