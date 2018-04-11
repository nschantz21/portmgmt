import numpy as np
import pandas as pd
from pandas import Series
from collections import defaultdict
from copy import deepcopy

class RebalanceTools:
    """
    Set of Portfolio Management tools. All functions take pandas series. Any attributes should be in the form of a Multi-index.
    """
    @staticmethod
    def normalize(port, total = 1.0):
        return port / port.sum() * total
    
    @staticmethod
    def clean(port, limit = 0.0, norm = True):
        tmp = port[port > limit]
        if norm:
            return normalize(tmp)
        return tmp
    
    @staticmethod
    def replace(port, to_replace, replacements=None, lvl=None):
        if lvl is not None:
            gport = port.groupby(level=lvl).sum()
            rport = replace(gport, to_replace, replacements)
            rport.index.rename(lvl, inplace=True)
            mult = rport / gport.values
            # maybe use join instead
            merged = pd.merge(port.rename().reset_index(), mult.reset_index(), on=lvl, how='left')
            result = merged['0_x'] * merged['0_y']
            result.index = port.index
            return result
            #return port.multiply(mult, level=lvl)
        if replacements is None:
            new_index = port.index ^ to_replace.index
            replacements = Series((1.0 / len(new_index)), copy=True, index = new_index)
        nominal_percent = (port * to_replace).dropna()
        new_series = port.subtract(nominal_percent, fill_value = 0.0)
        new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
        return new_series
    
    
    @staticmethod
    def restrict(port, limit, to_replace=None, rebal=True, replacements=None, lvl=None):
        if lvl is not None:
            gport = port.groupby(level=lvl).sum()
            rport = restrict(gport, limit, to_replace, rebal, replacements)
            print rport
            mult = rport.divide(gport.values)
            print mult
            merged = pd.merge(port.rename().reset_index(), mult.reset_index(), on=lvl)
            result = merged['0_x'] * merged['0_y']
            result.index = port.index
            return result
        if to_replace is None:
            to_replace = port.index ^ replacements.index
            if limit < (1.0 / len(to_replace)):
                raise ValueError('{lim} is too small of an upper limit for {lng} positions. {u_lim} is the smallest upper limit you can have.'.format(lim=limit, lng = len(to_replace), u_lim = 1.0/len(to_replace)))
        over = port[to_replace].loc[port > limit]
        excess = (over - limit) / over
        restrict_series = replace(port, excess, replacements)
        if rebal:
            restrict_series = restrict_series / restrict_series.sum()
            while (restrict_series[to_replace] > limit).any():
                over = restrict_series[to_replace].loc[restrict_series > limit]
                xs = (over - limit) / over
                restrict_series = replace(restrict_series, to_replace = xs, replacements = replacements)
        return restrict_series
        
    