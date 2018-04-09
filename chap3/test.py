import pandas as pd
import numpy as np
np.random.seed(42)

# these are percent changes
# I'm pretending I have 10 Years of prices for 100 stocks
returns = pd.DataFrame(np.random.normal(scale=.005, size=(255*10, 100)))
# now getting the log returns
log_returns = np.log(1 + returns)
annual_log_returns = log_returns.rolling(255).sum().shift(-255).dropna()

# estimating factor exposures
risk_free = .04
excess_returns = annual_log_returns - risk_free

# Simple Risk of Equally weighed portfolio with no correlations
excess_returns.std().mean() / np.sqrt(len(excess_returns.columns))
# Risk of Equally weighted Portfolio
excess_returns.std().mean() * (1 + excess_returns.corr() * (len(excess_returns.columns) - 1)) / 5


# active risk == standard deviation of active return, AKA tracking error
# benchmark returns
benchmark = pd.Series(np.random.normal(scale=.005, size=(255*10)))
benchmark_log_returns = np.log(1 + benchmark).rolling(255).sum().shift(-255).dropna()


# standard deviation of the difference between the portfolio and benchmark returns
portfolio_returns = annual_log_returns.sum(axis=1)
active_risk = (portfolio_returns - benchmark_log_returns).std()

# Portfolio exposure to the benchmark
beta = (np.cov(portfolio_returns, benchmark_log_returns) / benchmark_log_returns.var())[0,1]
# Residual Risk, the risk of the portfolio return orthogonal to the systematic return.
residual_risk = np.sqrt(portfolio_returns.var() - beta**2 * benchmark_log_returns.var())

# Variance is used to measure the cost of Risk. The cost of risk equates risk to an equivalent loss in expected return. We will generally associate this cost with either active or residual risk.



"""
Structural Risk Model

Multi-Factor risk model is based on the notion that the return of a stock can be explained by a collection of common factors plus an idiosyncratic element that pertains to that particular stock.
"""

#
# Return Structure
#
import characteristic as char
# Four Inputs 
# stock's Excess returns - not includeing the training set
train_returns = excess_returns[:255*3]
test_returns = excess_returns[255*3:]
# stock Exposure to factors

# pretending I have 3 factors - and standardizing them
factors = np.random.randint(low=1000, size=(3,100))
from scipy.stats import zscore
standard_factors = zscore(factors, axis=1, ddof=1)
train_cov = train_returns.cov()

# factor exposures at time t
a = standard_factors[0,]
b = standard_factors[1,]
c = standard_factors[2,]
# Factor portfolios
ha = char.characteristic_portfolio(train_cov, a)
hb = char.characteristic_portfolio(train_cov, b)
hc = char.characteristic_portfolio(train_cov, c)
# Factor returns over t, t+1
fra = test_returns[:255].multiply(ha) * a
frb = test_returns[:255].multiply(hb) * b
frc = test_returns[:255].multiply(hc) * c
# specific return
specific_return = excess_returns[:255] - (sra + srb + src)

#
# Risk Structure
#
test_cov = test_returns[:255].cov()
ab = char.characteristic_covariance(test_cov, a, b)
ac = char.characteristic_covariance(test_cov, a, c)
bc = char.characteristic_covariance(test_cov, b, c)
aa = 1.0; bb=1.0; cc = 1.0

factor_cov = np.asmatrix([[aa, ab, ac], [ab, bb, bc], [ac, bc, cc]])

# Covariance of Specific Returns
delta = np.diag(np.diag(specific_return.cov()))
# Covariance of Asset returns
asset_cov = pd.DataFrame(np.dot(np.dot(standard_factors.T, factor_cov), standard_factors) + delta)

