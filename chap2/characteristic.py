import numpy as np
import Portfolio

def characteristic_portfolio(assets, f):
    """
    A unique portfolio that has minimum risk and unit exposure to the asset characteristic a.  Not necessarily fully invested. Can include long and short postisions and have significant leverage.
    
    assets : array
        array of assets
    f : string
        asset characteristic (factor)
    
    Note : to build an investable portfolio, combine the benchmark with a small amount of the characteristic portfolio. This will effectively deleverage it.
    """
    # excess returns of assets
    xs_rtrns = excess_returns(assets)
    # covariance of excess returns
    V = np.cov(excess_returns)
    # factor exposures
    a = np.array([i.factors[f] for i in assets])
    weights = (V**-1 * a) / a.T * V**-1 * a
    return Portfolio(dict(zip(assets, weights)))


# maybe this should be a single attribute
def factor_exposure(port, f):
    """
    Exposure of portfolio to given asset characteristic (factor).
    
    port : dict
        Portfolio of assets. Keys must have a dict-type attribute "factors"
    f : string
        Asset Characteristic
    """
    total = 0.0
    for (i, j) in port.iteritems():
        total += i.factors[f] * j
    return total


def variance(assets, f):
    """
    Variance of characteristic portfolio
    
    assets : array
        array of assets
    f : string
        asset characteristic (factor)
    """
    excess_returns = returns(assets) - returns(risk_free)
    # covariance of excess returns
    V = np.cov(excess_returns)
    # factor exposures
    a = np.array([i[f] for i in assets])
    return 1 / a.T * V**-1 * a


def Beta(assets, f):
    """
    The beta of all assets with respect to the characteristic portfolio is equal to their characteristic value - the vector of factor exposures
    """
    return np.array([a.factors[f] for a in assets])


def characteristic_covariance(assets, f1, f2):
    """
    The exposure of one characteristic portfolio to another characteristic
    
    assets : 
    f1 : 
    f2 : 
    
    """
    return factor_exposure(characteristic_portfolio(assets, f1), f2) * variance(assets, f2)


def char_mul_(char, k):
    """
    multitplication operation. If we multiply the attribute by k we will need to divide the characteristic portfolio by k to preserve unit exposure.
    
    char : characteristic portfolio
    k : numeric
        positive scalar
    """
    return char  * 1 / k

# unfinished
def char_add_(lhs, rhs, lw, rw):
    """
    lefthand side
    righthand side
    left weight
    right weight
    
    Creating characteristic portfolio from a combination of other factor portfolios.
    
    combo : dict
        factor and weight key-value pairs
    returns : array
        weights of characteristic portfolio
    
    Note : If characteristic a is a weighted combination of characteristics d and f, then the characteristic portfolio ofa is a weighted combination of the characteristic portfolios of d and f.
    """
    var_a = (weight_d * factor_exposure(a to d) / variance(d)) + (weight_f * factor_exposure(a to f) / variance(f))
    
    (weight_d * var_a**-1 / variance(d)) * characteristic_portfolio(d) + (weight_f * var_a**-1 / variance(f)) * characteristic_portfolio(f)