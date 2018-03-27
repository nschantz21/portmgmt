from portfolio import Portfolio
import pandas as pd

# rebalance the group
def pdreplace(series, replace, replacements = None, group = None):
    """
    series : Pandas Series
        series of weights with index of securities
    
    Note : if passing a value to the group argument, the value passed to the series argument must have a column named 'weights' in addition to the grouping column. In all cases the security identifiers should be the index of the series. I would suggest always passing a pandas series to this, although it will work with a DataFrame with a single weights column.
    """
    if group is not None:
        grpsum = series.groupby(group)['weights'].sum()
        new_grps = pdreplace(grpsum, replace, replacements)
        redxed = my_grp_frame.set_index(grp, append = True).multiply(new_grps / grpsum, level=grp, axis=0)
        return redxed.reset_index(level=grp)
    if replacements is None:
        new_index = series.index ^ replace.index
        replacements = pd.Series((1.0 / len(new_index)), copy=True, index = new_index)
    nominal_percent = (series * replace).dropna()
    new_series = series.subtract(nominal_percent, fill_value = 0.0)
    new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
    return new_series


# works for dataframes
my_frame = Portfolio({'A' : .1, 'B':.4, 'C':.5}).to_frame()
another_frame = Portfolio({'A':.1, 'B':.5}).to_frame()
reps = Portfolio({'C':1.0}).to_frame()
pdreplace(my_frame, another_frame, replacements = reps)

# works with series
my_frame = pd.Series(index = ['A', 'B', 'C'], data = [.1, .4, .5])
another_frame = pd.Series(index = ['A', 'B'], data = [.1, .5])
reps = pd.Series(index = ['C'], data = [1.0])
pdreplace(my_frame, another_frame, replacements = reps)

# grouped data
my_grp_frame = pd.DataFrame({'weights': [.2,.2,.1,.1,.4], 'country':['E','E','F','F','G']}, index = ['A','B','C','D','H'])
replace_grps = pd.Series(index = ['E'], data=[.5])
replacements_grps = pd.Series(index = ['F','G'], data=[.1, .9])
grp = 'country'

grpsum = my_grp_frame.groupby(grp)['weights'].sum()
new_grps = pdreplace(grpsum, replace_grps, replacements_grps)
redxed = my_grp_frame.set_index(grp, append = True).multiply(new_grps / grpsum, level=grp, axis=0)
redxed.reset_index(level=grp, inplace=True)

pdreplace(my_grp_frame, replace_grps, replacements = replacements_grps, group = grp)