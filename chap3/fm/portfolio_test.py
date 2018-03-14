# Set up the package and test suite before you go any further!
# also look up automated documentation

import numpy as np
from collections import defaultdict, OrderedDict
from copy import deepcopy

class Portfolio:
    def names(self): return self.port.keys()
    def weights(self): return self.port.values()
    def __init__(self, names = [], weights = []):
        self.port = defaultdict(float)
        for i in xrange(len(names)):
            self.port[names[i]] += weights[i]
    
    def normalize(self, total = 1.0):
        weight_sum = sum(self.weights())
        for i in self.port:
            self.port[i] = (self.port[i] / weight_sum) * total
    
    def __add__(self, rhs):
        # maybe rename combine
        # see if you can make it only for Portfolio class family type objects
        temp_port = deepcopy(self)
        for name in rhs.names():
            temp_port.port[name] += rhs.port[name]
        return temp_port
        
    def __mul__(self, rhs):
        temp_port = deepcopy(self)
        temp_port.normalize(total = rhs)
        return temp_port
        
    def __str__(self):
        return self.port.viewitems()
        
    def sum_weights(self):
        return sum(self.weights())
        
    



class Equity:
    def __init__(self, name, factors = {}):
        self.name = name
        self.factors = factors
    def __repr__(self):
        return self.name


class EquityPortfolio(Portfolio):
    def print_secnames(self):
        for n in self.names():
            print n.name


if __name__ == '__main__':
    test_names = [i for i in "abcdefg"]
    test_weights = np.random.dirichlet(np.ones(len(test_names)), size = [1])[0]
    test_port = Portfolio(test_names, test_weights)
    five_port = test_port * 5
    sum(five_port.weights())
    
    test_secs = [Equity(i) for i in 'hijklmnop']
    test_weights = np.random.dirichlet(np.ones(len(test_secs)), size = [1])[0]
    test_secport = EquityPortfolio(test_secs, test_weights)
    test_secport.print_secnames()
    
    x = test_port + test_secport
    print x.names()
    print sum(x.weights())
    
    x.normalize(total = .5)
    print(x.weights())
    print sum(x.weights())
    
    
    super_port = test_port + test_secport * 0.5
    super_port.normalize()
    
    print sum(super_port.weights())
    print super_port