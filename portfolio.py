import numpy as np
import pandas as pd
from collections import defaultdict
from copy import deepcopy

class Portfolio:
    def names(self): return self.port.keys()
    def weights(self): return self.port.values()
    
    def __init__(self, port):
        """
        Portfolio Object Constructor
        
        port : dict
            names and weights of positions
        
        Note : anything passed to positions argument needs a 'factors' dict object
        """
        self.port = port
    
    def to_frame(self):
        df = pd.DataFrame.from_dict(self.port, orient='index')
        df.columns = ['weights']
        return df
    
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
        """
        removes a portfolio position, then normalizes portfolio weights
        """
        del self.port[pos]
        self.normalize()
    
    def __str__(self):
        return str(self.port.items())
    def __repr__(self):
        return str(self.port.items())
    
    def sum_weights(self):
        return sum(self.weights())
    
    def clean(self):
        for p in self.port:
            if self.port[p] == 0.0:
                del self.port[p]
    
    # The problem with these two functions is that they modify in-place. This makes operations less safe.  They also don't normalize on their own, so it's possible to under or overweight
    def replace(self, to_replace, replacements = None):
        """
        Replace Portfolio Positions
        
        to_replace : dict
            dictionary of postions to be replaced
        replacements : dict
            dictionary of replacement securities
        
        Note : This will work with many to one, one to many, and many to many replacements. When providing replacements 
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
    
    
    def restrict(self, limit, pos=None, rebal=True, repl = None):
        """
        Set an upper limit for position in Portfolio. Optionally specify target positions and replacements.
        
        limit : float
            upper limit of given positions
        pos : list
            list of positions names to limit. By default will be applied to all positions
        rebal : bool
            Normalize the portfolio weights
        repl : dict
            optional dict of replacement securities and weights for restricted positions. defaults to all other securities
        
        Note : To uniquely reallocate for each restriction based on the repl argument, I would suggest looping over this or the replace function with different replace values.  If you are restricting multiple securities, rebal should be True, otherwise it doesn't really matter
        """
        if pos == None:
            pos = self.names()
            # safety check
            if limit < (1.0 / len(pos)):
                return "That's too small of a limit"
        for p in pos:
            if self.port[p] > limit:
                excess = self.port[p] - limit
                self.replace({p: excess / self.port[p]}, repl)
        if rebal:
            self.normalize()
            while any([self.port[i] > limit for i in pos]):
                self.restrict(limit, pos, rebal)
    
    