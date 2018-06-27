"""
Portfolio Performance Analysis

Performance Analysis can, ex post, help the manager identify/avoid incidental risk and incremental decision making in an active strategy.  Risk Analysis can diagnose these problems ex ante.
The goal of performance analysis is to separate skill from luck, Cross-sectional comparisons are not up to this job.

Performance Analysis will involve comparing ex post returns to ex ante  risk in a statistically rigorous way.

Performance Analysis must account for both return and risk.

--Grinold & Kahn
"""
# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------
"""
Returns-based performance analysis is the simplest method for analyzing both return and risk, and distinguishing skill from luck.

Arithmetic Average Return >= Geometric Average Return >= Average Log Return.


"""
import numpy as np
from scipy import stats


def compound_returns(returns):
    """
    Compound Returns.
    Cumulative returns assuming reinvestment.
    Compound returns have the benefit of providing an accurate measure of the value of the ending portfolio. This assumes no cash inflows and outflows
    """
    return (np.cumprod(1.0 + returns) - 1.0)

def geometric_average_return(returns):
    """
    Geometric average return is compounded annually.
    """
    cmp_ret = compound_returns(returns)[-1]
    new_growth = np.log(cmp_ret) / len(returns)
    return np.exp(new_growth) - 1.0
    
def average_log_return(returns):
    """
    Average Log Return is compounded continuously.
    """
    return np.sum(np.log(returns + 1)) / len(returns)

def arithmetic_return(returns):
    """
    Arithmetic Average Return.
    """
    return sum(returns + 1) / len(returns) - 1.0

# Basic Returns-Based Performace

def jensen_analysis(prt, bmrk):
    """
    Jensen returns-based performance analysis involves regressing the time series of portfolio excess returns against benchmark excess returns.  
    
    The t-stat of the alpha is then tested for statistical significance.
    Rule of Thumb: a t-stat of 2 or more indicates that the performance of the portfolio is due to skill rather than luck.
    
    Parameters
    ----------
    prt: array-like
        Portfolio excess returns
    bmrk: array-like
        Benchmark excess returns
        
    Returns
    -------
    Probability of alpha being statistically different from zero.
    I think I should maybe do a one sided test, not a two sided test.
    """
    reg_result = stats.linregress(prt, bmrk) # this might include a pvalue as well
    alpha = reg_result[1]
    n = len(prt)
    t_stat = (alpha / np.std(prt)) * np.sqrt(n)
    pval = stats.t.sf(np.abs(t_stat), n-1)*2
    return t_stat, pval

def sharpe_analysis(prt, bmrk):
    """
    Sharpe Portfolio Performance Analysis
    Compares Sharpe ratios of portfolio and benchmark ofer period.
    Superior performance according to Sharpe Analysis implies positive Jensen alphas, however, positive Jensen alphas do not imply positive porformance according to Sharpe.
    
    Parameters
    ----------
    prt: array-like
        portfolio excess returns
    bmrk: array-like
        benchmark excess returns
    
    Returns
    -------
    boolean
    Statistically significant (95% confidence level) demonstration of skill has occured over period.
    """
    n = len(prt)
    term1 = (np.mean(prt) / np.std(prt)) - (np.mean(bmrk) / np.std(bmrk))
    # combined standard error of Sharpe Ratios
    term2 = 2.0 * np.sqrt(2.0 / n)
    return term1 > term2

# ------------------------------------------------------------------------------
# Advanced Returns-based Analysis
# ------------------------------------------------------------------------------
#
# Statistical Refinement
#
# Bayesian Correction

# Heteroskedasticity

# Autocorrelation

#
# Financial Refinement
#
# Benchmark Timing

# A Priori Beta Estimates

# Value added - probably will do this one

# Controlling for Public Information

# Style Analysis
# Only requires returns series of portfolio and style portfolios.
# Inaccurate, but improvement over basic returns-based performance analysis.
# Excellent tool for large studies of manager performance, when holdings info is unavailable.

# Controlling for Size and Value
# Fama-French - should probably do this one too.




"""
Portfolio-based performance analysis is the most sophisticated approach to distinguishing skill and luck along many different dimensions.
"""
