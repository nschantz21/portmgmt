import pandas as pd
from pandas import Series

# test data
test_port = pd.read_csv('test/test_portfolio.csv', index_col = ['name', 'country', 'industry'])['weight'].rename()

lvl = ['country', 'industry']
indx = pd.MultiIndex.from_tuples([('GB', 'O')], names=lvl)
rport1 = pd.Series(data=[.9], index=indx)
tp1 = replace(test_port, rport1, lvl=lvl)

# replace works for MultiIndex, which I think isn't bad
rport2 = pd.Series({'O':1.0})
tp2 = replace(test_port, rport2, lvl='industry')

rplcmnts = pd.Series({'N':.5})
tp3 = replace(test_port, rport2, replacements=rplcmnts, lvl='industry')

############
# Restrict #
############

#replacements = pd.Series(data=[1.0], index=pd.MultiIndex.from_tuples([('A', 'US', 'M')], names = ['name', 'country', 'industry']))
replacements=pd.Series({'M':1.0})
lvl = 'industry'

# to individually Restrict a position
restrict(port, limit, to_replace, rebal=False, replacements=replacements, lvl=lvl)

name_port = port.groupby('name').sum()
rn = restrict(name_port, .1)
rn2 = restrict(port, .1, lvl='name')

rc = restrict(port, limit=.3, lvl='country')
rc.groupby('country').sum()

ri = restrict(port, limit=.15, to_replace = ['O', 'M'], replacements = pd.Series({'N':1.0}), lvl='industry')
ri.groupby('industry').sum()

lvl = ['country', 'industry']
indx = pd.MultiIndex.from_tuples([('GB', 'O')], names=lvl)
rci = restrict(test_port, .1, to_replace = indx, lvl=lvl)

