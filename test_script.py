from factor import Factor
af = Factor('country', 'Afghanistan', categorical=True)

from security import Security
abc = Security('abc', dict([af.data]))

from portfolio import Portfolio
my_port = Portfolio({abc:1.0})


