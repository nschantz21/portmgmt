import pandas as pd
from pandas import Series


# test data
test_port = pd.read_csv('test/test_portfolio.csv', index_col = ['name', 'country', 'industry'])['weight'].rename()

lvl = ['country', 'industry']
indx = pd.MultiIndex.from_tuples([('GB', 'O')], names=lvl)
rport = pd.Series(data=[.9], index=indx)
# replace works for MultiIndex, which I think isn't bad
rport = pd.Series({'O':1.0})
tp2 = replace(test_port, rport, lvl='industry')

############
# Restrict #
############
port = test_port
limit = .4
to_replace = None
rebal = True

#replacements = pd.Series(data=[1.0], index=pd.MultiIndex.from_tuples([('A', 'US', 'M')], names = ['name', 'country', 'industry']))
replacements=pd.Series({'M':1.0})
lvl = 'industry'

# to individually Restrict a position
restrict(port, limit, to_replace, rebal=False, replacements=replacements, lvl=lvl)