"""
The Characteristic Portfolio Module is used in conjunction with a covariance matrix of excess asset returns and factor values for each asset.
"""

import numpy as np

def characteristic_portfolio(xs_cov, f):
    """
    A unique portfolio that has minimum risk and unit exposure to the asset characteristic f.  Not necessarily fully invested. Can include long and short postisions and have significant leverage.
    
    cov : array
        covariance of asset excess returns
    f : array or scalar
        factor exposures. Use scalar when all of the exposures are equal, like 1.0 for a categorical exposure.
    
    Note : to build an investable portfolio, combine the benchmark with a small amount of the characteristic portfolio. This will effectively deleverage it.
    """
    inv_cov = np.linalg.inv(xs_cov)
    numerator = np.dot(inv_cov, f)
    denominator = np.dot(f.T, numerator)
    return numerator / denominator

def factor_exposure(holdings, f):
    """
    Exposure of portfolio to given asset characteristic (factor).
    
    holdings : array
        vector of portfolio weights
    factor : array
        asset exposure for each member of holdings
        
    returns : float
        cumulative sum of holding weights and asset factor exposures
    """
    return np.dot(holdings, f)


def portfolio_variance(xs_cov, f):
    """
    Variance of characteristic portfolio
    
    assets : array
        array of assets
    f : string
        asset characteristic (factor)
    """
    # inversion of the covariance matrix of excess returns
    inv_cov = np.linalg.inv(xs_cov)
    numerator = np.dot(inv_cov, f)
    denominator = np.dot(f.T, numerator)
    return 1.0 / denominator


def beta(xs_cov, f):
    """
    The beta of all assets with respect to the characteristic portfolio is equal to their characteristic value - the vector of factor exposures
    """
    return np.dot(xs_cov, characteristic_portfolio(xs_cov, f)) / port_variance(xs_cov, f)


def characteristic_covariance(xs_cov, f1, f2):
    """
    The exposure of one characteristic portfolio to another characteristic
    """
    return factor_exposure(characteristic_portfolio(xs_cov, f1), f2) * portfolio_variance(xs_cov, f2)


def combination_characteristic(xs_cov, f1, f2 , k1, k2):
    f = f1 * k1 + f2 * k2
    inv_variance = k1 * factor_exposure(characteristic_portfolio(xs_cov, f1), f) / portfolio_variance(xs_cov, f1) + k2 * factor_exposure(characteristic_portfolio(xs_cov, f2), f) / portfolio_variance(xs_cov, f2)
    return (((k1 * inv_variance**-1) / portfolio_variance(xs_cov, f1)) * characteristic_portfolio(xs_cov, f1) + ((k2 * inv_variance**-1) / portfolio_variance(xs_cov, f2)) * characteristic_portfolio(xs_cov, f2))