def fama_evaluation_model(r, mkt, rf):
    """
    Fama's Evaluation Model
    Assumes the returns on managed portfolios (and securities) can be judged relative to thoser of naively selected portfolioos with similar risk levels.
    The Technique uses the simple one-period version of the two-parameter model, all the perfect market assumptions, and derived the ex-ante market line.
    
    Parameters
    ----------
    
    
    Returns
    -------
    Expected Predicted Asset Return
    """
    
    # market price per unit of risk
    risk_premium = (np.mean(mkt) - rf) / np.std(mkt)
    
    risk_of_asset = np.cov(r, mkt) / np.std(mkt)
    return rf + risk_premium * risk_of_asset


def selectivity(r, risk_of_asset):
    """
    Measure of return due to selectivity
    
    Selectivity measures how well the chosen portfolio performed relative to a naively selected portfolio of equal risk. This measure indicates any difference from the ex post market line.
    Parameters
    ----------
    
    
    
    Returns
    -------
    
    
    
    """
    return excess_return - risk


def net_selectivity(selectivity, diversification):
    return selectivity - diversification


