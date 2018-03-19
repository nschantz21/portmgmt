import numpy as np

def characteristic_portfolio(assets, c):
    """
    A unique portfolio that has minimum risk and unit exposure to the asset characteristic a.  Not necessarily fully invested. Can include long and short postisions and have significant leverage.
    assets : array
        array of assets
    c : string
        asset characteristic (factor)
    
    Note : to build an investable portfolio, combine the benchmark with a small amount of the characteristic portfolio. This will effectively deleverage it.
    """
    # excess returns of assets
    excess_returns = returns(assets) - returns(risk_free)
    # covariance of excess returns
    V = np.cov(excess_returns)
    # factor exposures
    a = np.array([i[c] for i in assets])
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

