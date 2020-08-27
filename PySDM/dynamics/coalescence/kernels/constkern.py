"""
Created at 24.08.2020 by edejong
"""

from PySDM.physics import constants as const

class ConstKern:
    def __init__(self, kernel_const):
        self.kernel_const = kernel_const

    def __call__(self, output, is_first_in_pair):
        output.product(is_first_in_pair, self.kernel_const)
        
    def register(self, builder):
        self.core = builder.core
        builder.request_attribute('volume')
