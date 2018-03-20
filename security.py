from collections import defaultdict

class Security:
    def __init__(self, name, factors = None):
        """
        name : string
            Security Identifier
        factors : dict
            dictionary of Factors
            
        Note: factors can be Factor type objects or regular key-value pairs
        """
        self.factors = defaultdict(float)
        self.name = name
        for f in factors:
            self.factors[f] += factors[f]
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def price(self):
        # this will probably need to be implemented differently for each type of security
        pass
    def clean(self):
        for f in self.factors:
            if self.factors[f] == 0.0:
                del self.factors[f]


class Equity(Security):
    pass
    

class Bond(Security):
    pass

