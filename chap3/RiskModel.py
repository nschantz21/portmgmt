# Structural Risk Model
# The multiple-factor risk model is based on the notion that the return of  a stock can be explained by a collection of common factors plus an idiosyncratic element that pertains to that particular stock.
# Fama and MacBeth - Risk, Return,  and Equilibrium: Empirical Tests
import numpy as np

def excess_returns_model(X, b, u):
    """
    Multiple-Factor Risk Model
    
    Parameters
    ----------
    X : N by K matrix
        Factor Exposures
    b : K length array
        Factor Returns
    u : N length array
        Specific Returns
    
    Returns
    -------
    r : N length array
        Excess Returns
    
    Note: asset returns, factor returns, and specific returns are all forward looking. Factor Exposures are those at the present time. See Active Portfolio Management, Chapter 2, Structural Risk Models
    """
    return np.dot(X, b) + u


def returns_covariance(X, F, Delta):
    """
    Risk Model of Factor-Based Portfolio
    
    Parameters
    ----------
    X : N by K matrix
        Factor Exposures
    F : K by K matrix
        Covariance matrix of factor returns
    Delta : N by N matrix
        Diagonal covariance matrix of specific returns
        
    Returns
    -------
    V : N by N matrix
        Covariance of stock returns.
    """
    return np.dot(np.dot(X, F), X.T) + Delta



def factor_return_matrix(X, Delta, r):
    """
    Matrix expression for the extimated Factor Returns
    
    Parameters
    ----------
    X : ndarray
        Exposure matrix
    Delta : ndarray
        Diagonal matrix of GLS Regression weights
    r : array_like
        Vector of excess returns
    
    Returns
    -------
    b : ndarray
        Estimated factor returns
    """
    return np.dot(np.dot(np.dot(np.linalg.inv(np.dot(np.dot(X.T, np.linalg.inv(Delta)), X)), X.T), np.linalg.inv(Delta)), r)


# This is just weighted returns of a portfolio
# There's probably a better way to do this with np.prod, but I couldn't figure it out right now
# Reread the Characteristic Portfolio Stuff
def factor_return(weights, returns):
    """
    Individual Factor return - returns to a factor portfolio
    
    Parameters
    ----------
    weights:
        exposure of asset to the factor
    returns:
        asset returns
    Returns
    -------
        Weighted Sum of excess returns for a factor 
    Notes
    -----
    Used for factor-mimicking portfolio.  Portfolio that capture the specific effect of the exposure.  Factor Portfolios are not investable since they hold all assets in some weight.
    """
    return np.sum([w * r for (w, r) in zip(weights, returns)], axis = 0)

def specific_risk(Sr):
    """
    Specific Risk of asset n
    
    Given the specific returns over a year for N assets, calculate the variance of each assets's specific return.
    Normalize these variances, to have a mean of 0 and a std of 1.
    
    The specific risk of asset n is then the average variance of all assets times (1 + the normalized variance of asset n)
    

    Parameters
    ----------
    Sr : t x N Matrix
        Matrix of specific returns over the time period for N assets
        
    Returns
    -------
    out : 
        vector of specific risk for each asset
    """
    from sklearn.preprocessing import scale
    Sv = np.var(Sr, axis = 1) # Variances
    St = np.mean(Sr) # Average Variance
    vt = scale(Sv.reshape(-1,1))
    return St * (1 + vt.reshape(1,-1))

   

"""
Risk Analysis Section
"""
def portfolio_factor_exposures(X, hp):
    """
    
    """