class Factor:
    # I'm not totally sure how I should do this
    # it's pretty much just a dictionary of the feature characteristics
    # it should also contain a transformative function
    # Maybe it should be a tuple or named tuple
    #############################################
    # you could make each factor it's own child class
    # So there would be a class Country(Factor)
    # it would define how the factor is comstructed
    # maybe make the default categorical?
    def __init__(self, name, value, categorical=False, func=None):
        if categorical:
            # set the value as 1.0
            self.data = (value, 1.0)
        else:
            self.data = (name, value)
    