import ipaddress
import random

class LCG:
    '''Linear Congruential Generator for deterministic random number generation'''

    def __init__(self, seed: int, m: int = 2**32):
        self.m       = m
        self.a       = 1664525
        self.c       = 1013904223
        self.current = seed

    def next(self) -> int:
        '''Generate next random number'''
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

# Rest of the code from pylcg.py goes here...
# (IPRange class and ip_stream function) 