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
    Geometric average return is compounded annually
    """
    cmp_ret = compound_returns(returns)[-1]
    new_growth = np.log(cmp_ret) / len(returns)
    return np.exp(new_growth) - 1.0
    
    
def average_log_return(returns):
    """
    Average Log Return is compounded continuously
    """
    return np.sum(np.log(returns + 1)) / len(returns)


def arithmetic_return(returns):
    """
    Arithmetic Average Return
    """
    return sum(returns + 1) / len(returns) - 1.0


# Basic Returns-Based Performace

def jensen_analysis(prt, bmrk):
    """
    Jensen returns-based performance analysis involves regressing the time series of portfolio excess returns against benchmark excess returns.  
    The resulting alpha is a measure of the superior/inferior market timing/stock selection.
    The Jensen measure does not evaluate the ability to diversify because it calculates risk premiums in terms of systematic risk.
    
    The t-stat of the alpha is then tested for statistical significance.
    Rule of Thumb: a t-stat of 2 or more indicates that the performance of the portfolio is due to skill rather than luck.
    
    The R-squared is a measure of diversification.
    
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
    return alpha, reg_result[2]**2, reg_result[3], t_stat, pval


def treynor_measure(port, bmark, rf):
    """
    Treynor's Composite Performance Measure
    
    The Treynor Measure (T Value) indicates the portfolio's risk premium per unit of risk. Comparing a portfolio's T value to a similar measure for the market portfolio indicates whether the portfolio would plot above  the Security Market Line.
    Because negative Betas can yield T values that give confusing results, it is preferable either to plot the portfolio on an SML graph or to compute the expected return for this portfolio using the SML equation and then compare this expected return to the actual return. This comparison will reveal wheather the actual reutrn was above or below expectations.
    
    Parameters
    ----------
    port : array_like
        portfolio returns
    bmark : array_like
        benchmark returns
    rf : array_like
        risk-free rate
    
    Returns
    -------
    Treynor Measure
    """
    # I used a slightly different parameter name than the other functions because this one uses returns rather than excess returns
    slope = stats.linregress(port, bmark)[0]
    T = (np.mean(port) - np.mean(rf)) / slope
    return T


def diversification_measure(port, bmark, rf):
    """
    Measuring the diversification of a portfolio by the difference between the Sharpe Ratio and the Treynor measure.
    
    The Sharpe measure evaluates on the basis of both rate of return performance and (internal) diversification. 
    Any difference in rank between the Sharpe and Treynor measures would come directly from a difference in diversification.
    """
    return sharpe_ratio(port, rf) - treynor_measure(portm bmark, rf)


def sharpe_ratio(prt, rf):
    """
    Sharpe Portfolio Performance Measure
    Parameters
    ----------
    prt : array_like
        Portfolio Returns
    rf : array_like
        Risk-Free returns
    
    Returns
    -------
    Sharpe Ratio of portfolio over the period
    """
    return (np.mean(prt) - np.mean(rf)) / np.std(prt)


def sharpe_analysis(prt, bmrk):
    """
    Sharpe Portfolio Performance Analysis
    Compares Sharpe ratios of portfolio and benchmark ofer period.
    Superior performance according to Sharpe Analysis implies positive Jensen alphas, however, positive Jensen alphas do not imply positive porformance according to Sharpe.
    
    Parameters
    ----------
    prt: array-like
        Portfolio excess returns
    bmrk: array-like
        Benchmark excess returns
    
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

# Value added - probably will do this one - in technical appendix

# Controlling for Public Information

# Style Analysis
# Only requires returns series of portfolio and style portfolios.
# Inaccurate, but improvement over basic returns-based performance analysis.
# Excellent tool for large studies of manager performance, when holdings info is unavailable.

# Controlling for Size and Value
# Fama-French - should probably do this one too.




"""
Portfolio-based performance analysis is the most sophisticated approach to distinguishing skill and luck along many different dimensions.

We need portfolio holdings over time and the goals and strategy of the manager.

"""

# Performance Attribution
# Performance attribution looks at portfolio returns over a single period and attributes them to factors
# You need the portoflio's holdings at the beginning of the period, the portoflio's realized return, and the estimated factor returns over the period.
# you can use both ex ante and ex post factor. ex post factors are useful for determining forecasting ability.
# Controlling for returns attributed to factors will remain specific returns to the portfolio. You can group them together by analyst or industry or whatever. This will tell us if our strategy works better in some sectors than in others. Be aware that it only gives us insight to relative performance, not absolute.



# We can choose the factors for attribution; we can attribute or group specific returns; attribute part of returns to constraints in the portfolio construction process.
# you pretty much get the active attribution and attributed return to an arbitrary set of factors



# Performance Analysis
# Performance analysis begins with the attributed returns each period, and looks at the statistical significance and value added of the attributed return series. As before, this analysis will rely on t statistics and information ratios to determine statistical significance and value added

# Ex ante strategies that are inconsistent with best policy analysis can signal to the owner of the funds that the active manager has deviated in strategy and can signal to the manager that the strategy isn't doing what he or she expects it to do.


# ------------------
# Technical Appendix
# ------------------

def best_risk_estimate(prior, realized):
    """
    Bayesian best linear unbiased risk estimate for performance analysis given two estimated of risk.
    Assumes estimation errors uncorrelated.
    Assumes distribution of the underlying variable is normal.
    
    It's pretty much a time-weighted average of variances
    
    Parameters
    ----------
    prior : array-like
        Returns of prior period
    realize : array-like
        Realized returns over the evaluation period
    
    Results
    -------
    Estimated variance of returns
    """
    T_prior = float(len(prior))
    T_realized = float(len(realized))
    risk_prior = np.var(prior)
    risk_realized = np.var(realized)
    risk = risk_prior * (T_prior / (T_realized + T_prior)) + risk_realized * (T_realized / (T_realized + T_prior))
    return risk


# ------------------------
# Valuation-Based Approach
# ------------------------

def valuation_assertions(v, b, rf):
    """
    v : array-like
        valuations
    b : array-like
        benchmark returns
    rf : array-like
        riskfree returns
    """
    assertion1 = (np.sum(v * b / rf) == 1.0)
    assertion2 = (np.sum(v) == 1.0)
    return assertion1, assertion2


def valuation(b, rf):
    """
    Valuation from continuous time option theory.
    Valuation multiples are guaranteed to be positive with this method.
    We choose delta and sigma by the requirement that they fairly price the observed set of benchmark returns and risk-free returns.
    
    Parameters
    ----------
    
    
    
    Results
    -------
    
    
    
    """
    delta = None # proportionality constant
    sigma = None # 
    numerator = -(np.log(b / rf) + sigma**2 * delta_t / 2)**2
    denominator = 2 * sigma**2 * delta_t
    return delta * np.exp(numerator / denominator)



def value_added(valuations, ):
    """
    
    """
    # Equation 17A.22
    (valuations * portfolio_factor_return) / portfolio_return
    for j in factors:
        for t in time:
            pass
        
            
    