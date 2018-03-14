import numpy as np
import pandas as pd
from sklearn import LinearRegression

# http://faculty.chicagobooth.edu/john.cochrane/teaching/35150_advanced_investments/week_5_notes.pdf

# https://nbviewer.jupyter.org/urls/www.kevinsheppard.com/images/f/f5/Example_Fama-MacBeth_regression.ipynb

# gather returns info for each factor

# gather returns info for each asset



# Step 1
# portfolio’s return is regressed against one or more factor time series to determine how exposed it is to each one

# Excess return is defined as the return above the risk-free return over the period t to t+1 - Treasuries I guess
# Excess return of asset n from tim t to t+1 = sum series from factor k to K of Asset n's exposure to factor k at time t times the returns of factor k over time t to t+1 plus asset n's specific returns over t to t+1.

# Step 2
#  the cross-section of portfolio returns is regressed against the factor exposures, at each time step, to give a time series of risk premia coefficients for each factor. Then average these coefficients, once for each factor, to give the premium expected for a unit exposure to each risk factor over time

# think of it as a Three dimensional matrix. x = N assets. y = T time steps. z = K Factors


def fm_regression():
    """
    testing how factors describe portfolio or asset returns.
    The goal is to find the premium from exposure to these factors.
    
    
    """
    pass


