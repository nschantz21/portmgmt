import numpy as np
import pandas as pd

df = pd.read_csv('../../data/spx2014to2017.csv', index_col = 'date', parse_dates = True)
df.drop(df.index[0], inplace = True)
# df.count()  # this could help
df.dropna(inplace=True, axis = 1)

# risk free rate
risk_free = df["USGG10YR Index"] / 100

# forward looking YoY returns
spx = df["SPX INDEX"]
yoy = spx.pct_change(250).shift(-250)
yoy.dropna(inplace = True)

# Forward looking annual returns for all index members
ann_returns = df.pct_change(250).shift(-250)
ann_returns.dropna(inplace = True, axis = 0, how = 'all')
ann_returns.drop("USGG10YR Index", inplace=True, axis = 1)


# subtract risk free returns as qutoed on the day from forward annual stock returns to get excess annual returns
excess_returns = ann_returns.subtract(risk_free, axis = 0)
excess_returns.drop('SPX INDEX', axis = 1, inplace=True)
excess_returns.dropna(inplace=True, how='all')


# Save that shit so I don't have to do it again
#excess_returns.to_csv('../data/excess_returns.csv')

# Get the Factor data and set categories as large and small market cap - I just took the most recent market cap, but I think historical market cap (based on the first day of forward looking returns) should be used.  I'm not sure if using an updating market cap would be beneficial since it's based on the price.
# using that sweet French sauce
factor_returns = pd.read_csv('../../data/factors.csv', parse_dates=True, index_col = 'date')


# this might be wrong because these are daily returns - not annual returns
# you want the annual geometric average of factor returns lagged by one year
new_data = excess_returns.merge(factor_returns, left_index=True, right_index=True)