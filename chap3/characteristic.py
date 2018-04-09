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
    return np.dot(xs_cov, characteristic_portfolio(xs_cov, f)) / portfolio_variance(xs_cov, f)


def characteristic_covariance(xs_cov, f1, f2):
    """
    The exposure of one characteristic portfolio to another characteristic
    """
    return factor_exposure(characteristic_portfolio(xs_cov, f1), f2) * portfolio_variance(xs_cov, f2)


def combination_characteristic(xs_cov, f1, f2 , k1, k2):
    f = f1 * k1 + f2 * k2
    inv_variance = k1 * factor_exposure(characteristic_portfolio(xs_cov, f1), f) / portfolio_variance(xs_cov, f1) + k2 * factor_exposure(characteristic_portfolio(xs_cov, f2), f) / portfolio_variance(xs_cov, f2)
    return (((k1 * inv_variance**-1) / portfolio_variance(xs_cov, f1)) * characteristic_portfolio(xs_cov, f1) + ((k2 * inv_variance**-1) / portfolio_variance(xs_cov, f2)) * characteristic_portfolio(xs_cov, f2))
    
if __name__ == '__main__':
    import numpy as np
    np.random.seed(42)
    # Global variables
    returns = np.random.lognormal(sigma = .01, size=(5, 200))
    risk_free = .04
    excess_returns = returns - risk_free
    excess_cov = np.cov(excess_returns)
    inverted_cov = np.linalg.inv(excess_cov)
    
    # bunch of random distributions to stand it for asset factor values
    a = np.random.randn(5)
    b = np.random.random_sample(size = 5)
    b = b / b.sum() # I want it to sum to 1.0
    c = np.ones(5)
    d = np.random.binomial(5, .5, size=5)
    
    np.random.chisquare(2, 5)
    np.random.exponential(1.0, 5)
    np.random.logseries(0.65, size=5)
    np.random.poisson(size=5)
    np.random.pareto(1.0, size=5)
    np.random.standard_cauchy(5)
    
    ha = characteristic_portfolio(excess_cov, a)
    hd = characteristic_portfolio(excess_cov, d)
    characteristic_covariance(excess_cov, a, d)
    hf = combination_characteristic(excess_cov, a, d, .2, .8)
    
    # Portfolio B, The Benchmark Portfolio
    # this is the Beta Portfolio as well
    # b is the weight of the assets in the benchmark
    hb = characteristic_portfolio(excess_cov, b)
    
    # Portfolio C, the Characteristic Portfolio
    # Every asset has an exposure of 1.0
    # useful for categorical attributes (e.g. Asset Sector exposures are equal to 1.0 for it's respective sector and 0.0 for all others)
    hc = characteristic_portfolio(excess_cov, c)
    portfolio_variance(excess_cov, c)
    
    # Portfolio q: Portfolio with the Maximum Sharpe Ratio
    # simple definition of expected returns is the average value of each series of asset returns
    q = np.array([i.mean() for i in excess_returns])
    hq = characteristic_portfolio(excess_cov, q)
    sharpe_ratio_q = np.dot(np.dot(q.T, np.linalg.inv(excess_cov)), q)**0.5
    portfolio_variance(excess_cov, q)
    beta(excess_cov, q) # should be equal to q
    
    def SharpeRatio(portfolio):
        return (np.corrcoef(np.dot(portfolio, excess_returns), np.dot(characteristic_portfolio(excess_cov, q), excess_returns)) *  sharpe_ratio_q)[0,1]
    
    # these are super high Sharpe Ratios
    # function may be incorrect
    SharpeRatio(ha)
    SharpeRatio(hb)
    SharpeRatio(hc)
    SharpeRatio(hd)
    
    # fraction of q invested in risky assets, where Portfolio C is the fully invested portfolio of risk assets
    risky_assets = factor_exposure(characteristic_portfolio(excess_cov, c), q) * portfolio_variance(excess_cov, q) / portfolio_variance(excess_cov, c)
    
    # Portfolio A, the alpha Portfolio
    alpha = q - np.dot(b, factor_exposure(hb, q))
    halpha = characteristic_portfolio(excess_cov, alpha)
    characteristic_covariance(excess_cov, alpha, b) # approx 0.0
    factor_exposure(halpha, b) # approx 0.0
    
    # Portfolio Q - fully invested in some characteristic, net long. It is the characteristic portfolio of the Highest sharpe ratio portfolio for a categorical attribute
    Q = factor_exposure(hq, c) * q
    hQ = hq / factor_exposure(hq, c)
    SharpeRatio(hq) == SharpeRatio(hQ)
    # these are essentially the same - difference is approx 0.0
    (factor_exposure(hc, q) / portfolio_variance(excess_cov, c)) - (factor_exposure(hQ, q) / portfolio_variance(excess_cov, Q))
    
    # below proves how Portfolio Q "explains" expected returns
    # They should be equal, but they're not. It's very close to zero though
    (q - (factor_exposure(hQ, q) * beta(excess_cov, Q))).sum()
    # same shit, should be zero. still very close
    factor_exposure(hQ, b) - ((factor_exposure(hb, q) * portfolio_variance(excess_cov, Q)) / (factor_exposure(hQ, q) * portfolio_variance(excess_cov,b)))
    
    # 4
    # if the benchmark is fully invested i.e. port_exposure(b, c) == 1.0
    # this will set the Beta portfolio's exposure to c to 1.0
    factor_exposure(b, c) == 1.0
    factor_exposure(hQ, b) == (factor_exposure(characteristic_portfolio(excess_cov, c), b) * factor_exposure(b, q)) / factor_exposure(hc, q)
    
    # to build portfolio based on our alphas, but with a beta of 1, full investment, and conforming to our preferences for risk and return, we will build a linear combination of portfolios A, B, and C
    combined = ha * .3 + hb * .3 + hc * .4
    # it's not necessarily fully invested
    combined.sum()
    # Create an investable portfolio by adding characteristic portfolios to the benchmark (not the benchmark portfolio)
    deleveraged = b * .95 + ha * .05
    """
    The Efficient Frontier
    Every efficient portfolio is a combination of the characteristic portfolio and the expected excess returns portfolio
    
    You could use the below to make a continuous set of efficient-frontier portfolios
    """
    ap = .2 * c + .8 * Q
    hp = characteristic_portfolio(excess_cov, ap)
    # coefficient of variance... idk
    k = (portfolio_variance(excess_cov, Q) - portfolio_variance(excess_cov, c)) / (factor_exposure(characteristic_portfolio(excess_cov, Q), q) - factor_exposure(characteristic_portfolio(excess_cov, c), q))
    # variance of efficient frontier portfolios
    varp = portfolio_variance(excess_cov, c) + k * (factor_exposure(characteristic_portfolio(excess_cov, ap), q) - factor_exposure(characteristic_portfolio(excess_cov, c), q))
    
    """
    CAPM
    Portfolio Q, the portfolio with the highest ratio of expected excess return to risk (highest Sharpe Ratio) among all fully invested portfolios, is the Market Portfolio, Portfolio M.
    """
    
    