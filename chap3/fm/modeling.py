# %run data_prep
import numpy as np
import pandas as pd
# http://home.uchicago.edu/~lhansen/HandBook-JSW-Oct-14-02.pdf


# Fama-Macbeth Two Step Regression
from sklearn import linear_model
from data_prep import new_data
# First step is regressing excess Asset returns for N assets to K factor returns
reg = linear_model.LinearRegression(n_jobs = -1, normalize=True)

# the model targets are all the asset excess returns
targets = list(new_data)[:-4]  # grab everything except the factor returns
variables = list(new_data)[::-1][1:4]  # the Fama-French Factors


factor_exposures = pd.DataFrame(columns = [variables], index = targets)
specific_returns = pd.Series(index = targets)

for asset in targets:
    reg.fit(X = new_data[variables], y = new_data[asset])
    factor_exposures.loc[asset] = reg.coef_
    specific_returns.loc[asset] = reg.score(X = new_data[variables], y = new_data[asset])
    

# second step you need a portfolio

# Compute the Portfolio Returns
# choosing first 10 stocks
portfolio = new_data[list(new_data)[:20]]

# exposures of portfolio
port_exposures = factor_exposures.loc[portfolio.columns]
port_exposures.index.names = ['sec']

stk = portfolio.stack()
stk.index.names = ['date', 'sec']
paneldata = port_exposures.mul(stk, axis = 0, level = 1)

pangroup = paneldata.groupby(level = [0], axis = 0).apply(np.mean)
port_returns = portfolio.mean(axis = 1)

# I don't think you normalize for this one
reg2 = linear_model.LinearRegression(n_jobs = -1)
reg2.fit(X = pangroup, y = port_returns)
reg2.coef_
reg2.intercept_
reg2.score(X = pangroup, y = port_returns)


# to find factor portfolios
# We minimize the factor exposures
from scipy.optimize import minimize, rosen

def mini_me(x, *args):
    return x == 1.0

res = minimize(rosen, factor_exposures, method='Nelder-Mead')