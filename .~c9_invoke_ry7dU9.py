import numpy as np
import pandas as pd
from pandas import Series
from collections import defaultdict
from copy import deepcopy

class RebalanceTools:
    """
    Set of Portfolio Management tools. All functions take pandas series. Any attributes should be in the form of a Multi-index.
    """
    def normalize(port, total = 1.0):
        return port / port.sum() * total
    
    @staticmethod
    def clean(port, limit = 0.0, norm = True):
        tmp = port[port > limit]
        if norm:
            return normalize(tmp)
        return tmp
    
    @staticmethod
    def replace(port, replace, replacements=None):
        if replacements is None:
            new_index = port.index ^ replace.index
            replacements = Series((1.0 / len(new_index)), copy=True, index = new_index)
        nominal_percent = (port * replace).dropna()
        new_series = port.subtract(nominal_percent, fill_value = 0.0)
        new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
        return new_series
    
    @staticmethod
    def restrict(port, limit, pos=None, rebal=True, repl=None):
        if pos is None:
            pos = port.index
            if limit < (1.0 / len(pos)):
                return "that's too small of a limit"
        over = port[pos].loc[port > limit]
        excess = (over - limit) / over
        restrict_series = replace(port, excess, repl)
        if rebal:
            restrict_series = restrict_series / restrict_series.sum()
            while (restrict_series[pos] > limit).any():
                over = restrict_series[pos].loc[restrict_series > limit]
                excess = (over - limit) / over
                restrict_series = replace(port, restrict_series, excess)
        return restrict_series
        
        