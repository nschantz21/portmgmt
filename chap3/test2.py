import numpy as np


N = 100 # number of Securities
K = 5 # number of Factors
trading_days = 255*5

X = np.random.random(size=(N,K)) # Factor Exposures
b_returns = np.random.random((trading_days, K)) # Factor Returns
b = np.sum(np.log(1 + b_returns), axis=0)
u_returns = np.random.random((trading_days, N)) # Specific Returns
u = np.sum(np.log(1 + u_returns), axis=0)

from RiskModel import excess_returns_model
r = excess_returns_model(X, b, u) # excess returns

# Specific returns should uncorrelated with the Factor returns
np.cov(u_returns.T, b_returns.T) # should be zero

# Covariance of Specific Returns should also be zero
specific_covariance = np.cov(u_returns.T)

"""
Covariance of Stock Returns
"""
F = np.cov(b_returns.T) # covariance of Factor Returns
delta = np.diag(np.diag(specific_covariance)) # covariance of Specific Returns

from RiskModel import returns_covariance
V = returns_covariance(X, F, delta)

"""
Fama-MacBeth Procedure
"""
# first Regress stock Excess returns agains factor exposures, choosing Factor returns which minimize the (possibly weighted) sum of specific returns.  This is The Cross-Sectional regression
from statsmodels.regression.linear_model import GLS
model = GLS(r, X)
model.fit().summary()
fm_specific_returns = model.fit().resid

inverted_delta = np.linalg.inv(np.diag(fm_specific_returns))

# Next Estimate the Factor Returns
term1 = np.linalg.inv(np.dot(np.dot(X.T,inverted_delta), X))
est_factor_returns = np.dot(np.dot(term1, X.T), inverted_delta) *  r
F_cov = np.cov(est_factor_returns) # covariance of Factor Returns

"""
Matrix Expression for The Estimated Factor Returns
"""
from RiskModel import factor_return_matrix
b = factor_return_matrix(X, delta, r)



"""
Risk Analysis
"""
# test portfolio
hp = np.array([.1,.1,.1,.2,.3,.4,.5,.6,.7,.8,.9])
hp = hp / hp.sum()

# Factor exposures of portfolio
x_p = np.dot(X.T, hp) # Asset Factor Exposures * Holdings

# Total Variance (Risk) of Portfolio
factor_risk_p = np.dot(np.dot(x_p.T, F[:11]), x_p) # Factor Exposures * Factor Returns
specific_risk_p = np.dot(np.dot(hp.T, delta[:11,:11]), hp) # Holdings * Specific Variance
total_risk_p = factor_risk_p + specific_risk_p

# Active Risk or Tracking Error
hb = np.random.random(100)
hb = hb / hb.sum() # benchmark holdings
hpa = hp - hb # holdings of active portfolio. Will have negative weights
x_pa = np.dot(X.T, hpa) # Factor Exposures of Active portfolio
active_factor_risk_pa = np.dot(np.dot(x_pa.T, F), x_pa)
active_specific_risk_pa = np.dot(np.dot(hpa.T, delta), hpa)
active_risk_pa = active_factor_risk_pa + active_specific_risk_pa

# To separate Market Risk from Residual Risk
# first define Beta - should be the same as in the characteristic portfolio chapter - but  now broken down into factor and specific components
Beta_variance = (np.dot(np.dot(hb.T, V), hb))
Beta_factor = np.dot(F, xb) / Beta_variance
Beta_specific = np.dot(delta, hb) / Beta_variance
Beta = np.dot(X, Beta_factor) + Beta_specific

# Next we find the portfolio's exposure to Beta
# Each asset's beta contains a factor contribution and a specific contribution
# The specific contribution is zero for any asset not in the benchmark
Beta_factor_exposure_p = np.dot(xp.T, Beta_factor)
Beta_specific_exposure_p = np.dot(hp.T, Beta_specific)
Beta_p = Beta_factor_exposure_p + Beta_specific_exposure_p

# Now we can get the residual risk
residual_risk_p = total_risk_p - Beta_p * Beta_variance
# Make the Residual Covariance Matrix

