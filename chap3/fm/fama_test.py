#!/usr/bin/env python
from datetime import datetime
from pandas import Series, DataFrame
import pandas as pd
import numpy as np


def cumret(ret,beg,end):
  return pd.rolling_sum(np.log(1+ret),window=beg-end+1).shift(end)

if __name__ == '__main__':
  # custom date parser
  parse = lambda x: datetime(int(x[0:4]),int(x[4:6]),1)
  
  # import
  ind   = pd.read_csv('data/test.csv',index_col='caldt',
                      parse_dates=True,date_parser=parse)
  
  ind = ind.stack().reset_index()
  ind.columns = ['caldt','industry','ret']
  # turn return into percent
  ind['ret'] = ind['ret']/100
  # setting a multi index
  ind.set_index(['caldt','industry'],inplace=True)
  
  # Month over Month cumulative returns
  ind['rmom'] = ind['ret'].groupby(level='industry').apply(cumret,12,2);
  
  # removing null objects
  ind = ind[ind.rmom.notnull()]

  print ind.head(20)

  # target returns
  print pd.fama_macbeth(y=ind['ret'],x=ind.ix[:,['rmom']])
  
  