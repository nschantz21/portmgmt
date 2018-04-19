import numpy as np
import pandas as pd
from pandas import Series

def normalize(port, total = 1.0):
    return port / port.sum() * total
    
def clean(port, limit = 0.0, norm = True):
    tmp = port[port > limit]
    if norm:
        return normalize(tmp)
    return tmp
 
def replace(port, to_replace, replacements=None, lvl=None):
    if lvl is not None:
        gport = port.groupby(level=lvl).sum()
        rport = replace(gport, to_replace, replacements)
        rport.index.rename(lvl, inplace=True)
        mult = rport.divide(gport, level=lvl, fill_value=1.0)
        merged = pd.merge(port.rename().reset_index(), mult.reset_index(), on=lvl, how='left')
        result = merged['0_x'] * merged['0_y']
        result.index = port.index
        return result
    if replacements is None:
        new_index = port.index ^ to_replace.index
        replacements = port.loc[new_index] / port.loc[new_index].sum()
    nominal_percent = (port * to_replace).dropna()
    new_series = port.subtract(nominal_percent, fill_value = 0.0)
    new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
    return new_series


def restrict(port, limit, to_replace=None, rebal=True, replacements=None, lvl=None, normed=True):
    if lvl is not None:
        gport = port.groupby(level=lvl).sum()
        rport = restrict(gport, limit, to_replace, rebal, replacements)
        rport.index.rename(lvl, inplace=True)
        mult = rport.divide(gport, level=lvl, fill_value=1.0)
        merged = pd.merge(port.rename().reset_index(), mult.reset_index(), on=lvl, how='left')
        result = merged['0_x'] * merged['0_y']
        result.index = port.index
        return result
    if to_replace is None:
        to_replace = port.index
        # maybe add default behavior for case when replacements is supplied and to_replace is not
        if replacments is not None:
            raise NotImplementedError('You cannot supply replacements without supplying to_replace argument')
        if limit < (1.0 / len(to_replace)):
            raise ValueError('{lim} is too small of an upper limit for {lng} positions. {u_lim} is the smallest upper limit you can have.'.format(lim=limit, lng = len(to_replace), u_lim = 1.0/len(to_replace)))
    over = port[to_replace].loc[port > limit]
    excess = (over - limit) / over
    restrict_series = replace(port, excess, replacements)
    if normed:
        restrict_series = restrict_series / restrict_series.sum()
    if rebal:
        while (restrict_series[to_replace] > limit).any():
            over = restrict_series[to_replace].loc[restrict_series > limit]
            xs = (over - limit) / over
            restrict_series = replace(restrict_series, to_replace = xs, replacements = replacements)
    return restrict_series


# maybe go recursively down through levels for MultiIndex series