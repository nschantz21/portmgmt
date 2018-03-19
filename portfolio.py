import numpy as np
import pandas as pd
from collections import defaultdict
from copy import deepcopy

class Portfolio:
    def names(self): return self.port.keys()
    def weights(self): return self.port.values()
    
    def __init__(self, positions = [], weights = [], factors = {}):
        """
        Portfolio Object Constructor
        
        positions : list
            list of positions held. This could be Security objects or Portfolio objects
        weights : list
            list of weights corresponding to the positions
        
        Note : anything passed to positions argument needs a 'factors' dict object
        """
        self.port = defaultdict(float)
        for i in xrange(len(names)):
            self.port[names[i]] += weights[i]
        self.factors = factors
        self.df = pd.DataFrame(self.port)
        for f in factors:
            self.df[f] = [sec.factors[f] for sec in secs]
        
    
    def normalize(self, total = 1.0):
        weight_sum = sum(self.weights())
        for i in self.port:
            self.port[i] = (self.port[i] / weight_sum) * total
    
    def __add__(self, rhs):
        temp_port = deepcopy(self)
        for name in rhs.names():
            temp_port.port[name] += rhs.port[name]
        return temp_port
        
    def __mul__(self, rhs):
        temp_port = deepcopy(self)
        temp_port.normalize(total = rhs)
        return temp_port
    
    def remove(self, pos):
        del self.port[pos]
        self.normalize()
    
    def __str__(self):
        return str(self.port.items())
    def __repr__(self):
        return str(self.port.items())
    
    def sum_weights(self):
        return sum(self.weights())
    
    def replace(self, to_replace, replacements = None):
        """
        Replace Portfolio Positions
        
        to_replace : dict
            dictionary of postions to be replaced
        replacements : dict
            dictionary of replacement securities
        
        Note : This will work with many to one, one to many, and many to many replacements. It's annoying that there is no default value for replacement percentages.
        """
        if replacements == None:
            tempkeys = to_replace.viewkeys() ^ self.port.viewkeys()
            replacements = dict(zip(tempkeys, [1.0 / len(tempkeys) for x in range(len(tempkeys))]))
        for replaced in to_replace.iteritems():
            nominal_percent = self.port[replaced[0]] * replaced[1]
            for security in replacements.iteritems():
                self.port[security[0]] += security[1] * nominal_percent
            self.port[replaced[0]] -= nominal_percent
            if(self.port[replaced[0]] == 0.0):
                del self.port[replaced[0]]
    
    def get_drift(self, old_price, new_price):
        """
        Calculate the price drift (percent change) of each asset
        """
        return (new_price - old_price) / old_price
    
    def apply_drift(self, drift):
        """
        drift : dict
            dictionary of assets and the percent drift
        """
        for x in self.port.iterkeys():
            self.port[x] = self.port[x] * (1.0 + drift[x])
        self.normalize()
    
    def factors(self):
        """
        Recursively access the factors of the held assets.
        This should work for any asset (securities and other portfolios)
        
        Classifications need to use binarization - pandas.get_dummies()
        """
        for pos in self.names():
            for f in pos.factors.iteritems():
                self.factors[f[0]] += self.port[pos] * f[1]