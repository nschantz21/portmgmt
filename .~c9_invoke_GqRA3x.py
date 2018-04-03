import pandas as pd

# rebalance the group
def pdreplace(series, replace, replacements=None, group=None):
    """
    series : Pandas Series
        series of weights with index of securities
    
    Note : if passing a value to the group argument, the value passed to the series argument must have a column named 'weights' in addition to the grouping column. In all cases the security identifiers should be the index of the series. I would suggest always passing a pandas series to this, although it will work with a DataFrame with a single weights column.
    """
    if group is not None:
        grpsum = series.groupby(group)['weights'].sum()
        new_grps = pdreplace(grpsum, replace, replacements)
        redxed = my_grp_frame.set_index(group, append = True).multiply(new_grps / grpsum, level=group, axis=0)
        return redxed.reset_index(level=group)
    if replacements is None:
        new_index = series.index ^ replace.index
        replacements = pd.Series((1.0 / len(new_index)), copy=True, index = new_index)
    nominal_percent = (series * replace).dropna()
    new_series = series.subtract(nominal_percent, fill_value = 0.0)
    new_series = new_series.add((replacements * nominal_percent.sum()), fill_value = 0.0)
    return new_series

##########
#Restrict#
##########
# function version


def pdrestrict(series, limit, pos=None, rebal=True, repl=None, group=None):
    if group is not None:
        grpsum = series.groupby(group)['weights'].sum()
        new_grps = pdrestrict(grpsum, limit, pos=pos, rebal=rebal, repl=repl)
        redxed = my_grp_frame.set_index(group, append = True).multiply(new_grps / grpsum, level=group, axis=0)
        return redxed.reset_index(level=group)
    if pos is None:
        pos = series.index
        if limit < (1.0 / len(pos)):
            return "that's too small of a limit"
    over = series[pos].loc[series > limit]
    excess = (over - limit) / over
    restrict_series = pdreplace(series, excess, repl)
    if rebal:
        restrict_series = restrict_series / restrict_series.sum()
        while (restrict_series[pos] > limit).any():
            over = restrict_series[pos].loc[restrict_series > limit]
            excess = (over - limit) / over
            restrict_series = pdreplace(restrict_series, excess)
    return restrict_series
    
if __name__ == '__main__':
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
    
    pdreplace(my_grp_frame, replace_grps, replacements = replacements_grps, group = grp)
    
    
    
    
    frame = pd.Series(index = ['A', 'B', 'C', 'D', 'H'], data = [.2,.2,.1,.1,.4])
    limit = .1
    pos = ['B', 'C']
    rebal = True
    repl = pd.Series(index = ['A'], data = [1.0])
    
    # regular series
    pdrestrict(frame,.08, pos=pos, repl = repl)
    
    # grouped data
    my_grp_frame = pd.DataFrame({'weights': [.2,.2,.1,.1,.4], 
                                 'country':['E','E','F','F','G']}, 
                                index = ['A','B','C','D','H'])
    grp_limit = .39
    my_group = ['country']
    grp_pos = ['E']
    replace_grps = pd.Series(index=['F', 'G'], data=[.7, .3])
    
    pdrestrict(my_grp_frame, limit=.35, group='country')
    pdrestrict(my_grp_frame, limit=.35, group='country', pos=grp_pos)
    pdrestrict(my_grp_frame, limit=.35, group='country', pos=grp_pos, repl=replace_grps)
    
    
    