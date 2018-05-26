import pandas as pd
import numpy as np
from portfolio_tools import normalize

def calc_drift(p1, p2, verbose=False):
    """
    p1 : array-like
        Old prices
    p2 : array-like
        New prices
    return : array
        Percent change of prices
    """
    d = (p2 - p1) / p1
    
    if verbose:
        # Quality check
        print 'positives ', (p2 > p1) & (d > 0.0)
        print 'negatives ', (p2 < p2) & (d < 0.0)
        print 'equals ', (p2 == p1) & (d == 0.0)
    return d

def apply_drift(weights, drift, normed=True):
    """
    weights : array-like
        position weights in protfolio
    drift: array-like
        percent change in prices
    returns : array
        normalized drifted weights
    """
    new_weight = weights * (1 + drift)
    if normed:
        return normalize(new_weight)
    return new_weight



