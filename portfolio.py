import numpy as np
import pandas as pd
from collections import defaultdict
from copy import deepcopy

class Portfolio:
    def names(self): return self.port.keys()
    def weights(self): return self.port.values()
    
    def __init__(self, names = [], weights = [], factors = {}):
        self.port = defaultdict(float)
        for i in xrange(len(names)):
            self.port[names[i]] += weights[i]
    
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
    
    # these two suck - find a better way for repr and str
    def __str__(self):
        return str(self.port.items())
    def __repr__(self):
        return str(self.port.items())
    
    def to_pandas(self):
        return pd.DataFrame.from_dict(self.port, orient = 'index')
    
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
        
    def set_constraint(self, constraint_func, factor = None, factor_value = None):
        # group the port weights by the factor
        # call the replace function based on the factor and factor value
        # default to just the position weight
        # optionally pass postion characteristic for group level limit
        pass
        
    def factors(self):
        # get the factors of the securities being held
        # I'm not sure this should be implemented in the base object
        # I wish I could make it a pure virtual function
        # Factor exposure should be part of every object in the pipeline
        # Look at aggregated factor exposure formula
        return [key.factors for key in self.port.iterkeys()]
    
    
    # maybe try join multiplier like I did in R
    def limit(self, factor, group, limit, **kwargs):
        df = self.to_pandas()
        grp = df.groupby(factor)[group]
        if grp['weight'].sum() > limit:
            self.rebalance({name:weight / limit for (name, weight) in grp[['names', 'weights']]}, **kwargs)
            self.normalize()


class EquityPortfolio(Portfolio):
    def print_secnames(self):
        for n in self.names():
            print n.name

class CombinationPortfolio(Portfolio):
    # this class is for combining portfolios
    # would hold a dictionary of portfolio objects and their wieights
    # I don't know if this is all that necessary
    # the regular portfolio object can hold portfolios
    pass
