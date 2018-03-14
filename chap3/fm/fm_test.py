import numpy as np
import pandas as pd
import risk
df = pd.read_csv('../data/spx2014to2017.csv', index_col = 'date', parse_dates = True)
df.drop(df.index[0], inplace = True)
df["USGG10YR Index"] = df["USGG10YR Index"] / 100
spx = df["SPX INDEX"]

# forward looking YoY returns
yoy = spx.pct_change(250).shift(-250)
yoy.dropna(inplace = True)

# Forward looking annual returns for all index members
ann_returns = df.pct_change(250).shift(-250)
ann_returns.dropna(inplace = True, axis = 0, how = 'all')
ann_returns.drop("USGG10YR Index", inplace=True, axis = 1)

# Risk free rate is 
risk_free = df["USGG10YR Index"]

# subtract risk free returns as qutoed on the day from forward annual stock returns to get excess annual returns
excess_returns = ann_returns.subtract(risk_free, axis = 0)
excess_returns.drop('SPX INDEX', axis = 1, inplace=True)
excess_returns.dropna(inplace=True, how='all')


# Save that shit so I don't have to do it again
#excess_returns.to_csv('../data/excess_returns.csv')

spx_excess = yoy - risk_free

# Get the Factor data and set categories as large and small market cap - I just took the most recent market cap, but I think historical market cap (based on the first day of forward looking returns) should be used.  I'm not sure if using an updating market cap would be beneficial since it's based on the price.

factors = pd.read_csv('../data/mrktcap.csv', index_col = 'figi')
factors['size'] = pd.qcut(factors['cap'], 2, labels = ["small", "large"])

# apply these labels to the excess returns
excess_returns = excess_returns.T
excess_returns['size'] = factors['size']
excess_returns.set_index(['size', excess_returns.index], inplace = True)
grouped = excess_returns.groupby(level = 0)
grouped = grouped.mean().T


# fama-macbeth regression
# for each asset, regress the asset returns to the factor returns
# we only have one factor
from sklearn import linear_model
from sklearn import model_selection
# hyper parameter alpha is used to control the magnitude of the penalty weight for outlying observations, which controls the degree of sparsity of the coefficients estimated.
excess_returns = excess_returns.T

data = excess_returns[('large','BBG0039320N9')].reset_index(level='size')
data.set_index('date', inplace = True)
data['y'] = grouped['large']
data.dropna(inplace = True)
y = data['y']
X = data['large'].values

reg = linear_model.LinearRegression()
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = .33, random_state = 42)

reg.fit(X_train, y_train)
reg_pred = reg.predict(X_test)
reg.score(X_test, y_test)

factor_expoosure = reg.coef_
specific_risk = reg.intercept_



# using that sweet French sauce
factor_returns = pd.read_csv('../data/factors.csv', parse_dates=True, index_col = 'date')

new_data = data.merge(factor_returns, left_index = True, right_index = True)
# target
y = new_data[('y', '')].values.reshape(-1, 1)
#['Mkt-RF','SMB', 'HML']
X = new_data['Mkt-RF'].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = .33, random_state = 42)
reg2 = linear_model.LinearRegression()

reg2.fit(X_train, y_train)
reg2_pred = reg2.predict(X_test)

reg2.score(X_test, y_test)

reg2.coef_
reg2.intercept_



# test portfolio data
test_portfolio = excess_returns[list(excess_returns)[0:5]]
test_portfolio = test_portfolio.T.reset_index(level = 0, drop = True).T

new_data = test_portfolio.merge(factor_returns, left_index = True, right_index = True)

y = new_data['BBG000C2V3D6'].values.reshape(-1,1)
X = new_data[['Mkt-RF', 'SMB', 'HML']].values

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = .33, random_state = 42)

reg = linear_model.LinearRegression()

reg.fit(X_train, y_train)
reg_pred = reg.predict(X_test)
reg.score(X_test, y_test)

reg.coef_
reg.intercept_



# bulk test
from sklearn.multioutput import MultiOutputRegressor
targets = new_data[['BBG000C2V3D6', 'BBG005P7Q881', 'BBG000F7RCJ1', 'BBG000B9XRY4', 'BBG0025Y4RY4']]
variables = new_data[['Mkt-RF', 'SMB', 'HML']].values

reg = linear_model.LinearRegression(n_jobs = -1)

for y in targets:
    reg.fit(X = variables, y = targets[y].values.reshape(-1,1))
    print reg.coef_, reg.intercept_

def fmb(series):
    reg = linear_model.LinearRegression(n_jobs = -1)
    reg.fit(X = variables, y = series.values.reshape(-1,1))
    return list(reg.coef_.flatten())

# returns a series - not ideal, but getting there
coefs = targets.apply(fmb)