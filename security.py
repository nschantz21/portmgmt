class Security:
    def __init__(self, name, factors = {}):
        self.name = name
        self.factors = factors
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def price(self):
        pass

class Equity(Security):
    pass
    
class Bond(Security):
    pass