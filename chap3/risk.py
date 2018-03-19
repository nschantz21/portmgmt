import numpy as np


def cgr(beg, end, freq = 1, hold_period = 1):
    """
    Compound Growth Rate
    """
    return (end / beg) ** (freq / hold_period) - 1.0


def ror(prices):
    """
    Rate of Return
    pretty much a percent change
    """
    return np.diff(prices) / prices[:len(prices) - 1]


def compound_returns(returns):
    """
    Compound Returns
    Cumulative returns assuming reinvestment
    """
    return np.cumprod(1.0 + returns) - 1.0


def compounded_returns(prices):
    """
    Wrapper for ror and compound_returns functions
    """
    return compound_returns(ror(prices))


def annualized_return(R, t):
    """
    Converting a return R to an annual rate of return r, where the length of the period t is measured in years and the rate of return r is per year.
    
    R : array_like
        Total Return over period
    t : integer
        Number of period in a year 
    """
    return (1.0 + R) ** (1.0 / t) - 1.0
    

def period_risk(returns, freq = None):
    """
    returns : numpy array
        Total Returns for a period
    freq : integer
        number of instances that correspond to the return period - e.g. when calculation annual risk based on monthly total returns freq = 12
    """
    if(freq == None):
        freq = len(returns)
    return np.sqrt(freq) * np.std(returns)


def active_risk(portfolio_returns, benchmark_returns):
    """
    Difference between portfolio and benchmark returns.
    Tracking Error when investing to a benchmark - describes how well the portfolio tracks to the benchmark.
    """
    return np.std(portfolio_returns - benchmark_returns)


def beta(x, y):
    return np.cov(x, y) / np.var(y)


def residual_risk(portfolio_returns, benchmark_returns):
    """
    Residual Risk of a Portfolio is the risk of return orthogonal to the systematic risk (the Beta Portfolio)
    """
    return np.sqrt(np.std(portfolio_returns) -  beta(portfolio_returns, benchmark_returns)**2 * np.var(benchmark_returns))


def port_risk(positions):
    """
    Risk of Portfolio of equally weighted positions
    """
    returns = [compounded_returns(pos) for pos in positions]
    avg_risk = np.mean([period_risk(ret) for ret in returns])
    rho = np.corrcoef(returns)
    return avg_risk * np.sqrt((1 + rho * len(returns) - 1) / len(returns))


def total_risk(returns, weights):
    """
    """
    pass


def log_return(i, f, t = 1):
    """
    Continuously Compounded Return
    
    Supply t if you want the logarithmic rate of return
    
    f : numeric
        The final value
    i : numeric
        The initial value
    t : integer
        length of time period. i.e. compounding frequency over the holding period
        
    Note: This will work for annulization of returns as well. For annualized logarithmic rate of return based on daily price, supply t as the reciprocal of the compounding frequency.
    
    log_return(f = 150.0, i = 120.0, t = 250)  # 250 trading days in a year
    """
    return np.log(f / i) / t