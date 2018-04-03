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
    
    def pdreplace(series, replace, replacements=None, group=None):
    """
    series : Pandas Series
        series of weights with index of securities
    
    Note : if passing a value to the group argument, the value passed to the series argument must have a column named 'weights' in addition to the grouping column. In all cases the security identifiers should be the index of the series. I would suggest always passing a pandas series to this, although it will work with a DataFrame with a single weights column.
    """
    if group is not None:
        grpsum = series.groupby(group)['weights'].sum()
        new_grps = pdreplace(grpsum, replace, replacements)
        redxed = my_grp_frame.set_index(group, append = True).multiply(new_grps / grpsum, level=group, axis=0)
        return redxed.reset_index(level=group)
    if replacements is None:
        new_index = series.index ^ replace.index
        replacements = pd.Series((1.0 / len(new_index)), copy=True, index = new_index)
    nominal_percent = (series * replace).dropna()
    new_series = series.subtract(nominal_percent, fill_value = 0.0)
    new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
    return new_series
    
    def pdrestrict(series, limit, pos=None, rebal=True, repl=None, group=None):
        if group is not None:
            grpsum = series.groupby(group)['weights'].sum()
            new_grps = pdrestrict(grpsum, limit, pos=pos, rebal=rebal, repl=repl)
            redxed = my_grp_frame.set_index(group, append = True).multiply(new_grps / grpsum, level=group, axis=0)
            return redxed.reset_index(level=group)
        if pos is None:
            pos = series.index
            if limit < (1.0 / len(pos)):
                return "that's too small of a limit"
        over = series[pos].loc[series > limit]
        excess = (over - limit) / over
        restrict_series = pdreplace(series, excess, repl)
        if rebal:
            restrict_series = restrict_series / restrict_series.sum()
            while (restrict_series[pos] > limit).any():
                over = restrict_series[pos].loc[restrict_series > limit]
                excess = (over - limit) / over
                restrict_series = pdreplace(restrict_series, excess)
        return restrict_series
    
    
    
    
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
    
    