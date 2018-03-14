# Structural Risk Model
# The multiple-factor risk model is based on the notion that the return of  a stock can be explained by a collection of common factors plus an idiosyncratic element that pertains to that particular stock.
# Fama and MacBeth - Risk, Return,  and Equilibrium: Empirical Tests


def returns(X, b, u):
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
    return X * b + u


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
    return X * F * X.T + Delta



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
    return (X.T * Delta**-1 * X)**-1 * X.T * Delta**-1 * r


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

# French's website of factor returns
# http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

