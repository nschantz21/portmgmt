import portfolio
import numpy as np
# test script for portfolio package
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

print "original portfolio" + '\n'
print test_port

test_port.replace({'a':1.0, 'g':1.0}, {'c':0.1, 'q':0.9})
print "altered portfolio" + '\n'
print test_port


test_port.replace({'q': .85})
print "blanket rebal"
print test_port