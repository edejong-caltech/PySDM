"""
Created at 19.02.2021 by edejong
"""
import numpy as np


class Product():

    def __init__(self, c):
        self.c = c
        self.core = None

    def __call__(self, output, is_first_in_pair):
        output.multiply_pair(self.core.particles['volume'], is_first_in_pair)
        output *= self.c
        
    def register(self, builder):
        self.core = builder.core
        builder.request_attribute('volume')
