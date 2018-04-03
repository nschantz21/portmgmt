import numpy as np
a = np.array([-1.264911064, -0.632455532, 0.0, 0.632455532, 1.264911064])
#np.average(a, weights = ha)

returns = np.random.rand(5, 200)
risk_free = .04
excess_returns = returns - risk_free

excess_cov = np.cov(excess_returns)
inverted_cov = np.linalg.inv(excess_cov)

def port_exposure(h, char):
    return np.dot(h, char)

def char_portfolio(char):
    numerator = np.dot(inverted_cov, char)
    denominator = np.dot(char.T, numerator)
    return numerator / denominator

ha = char_portfolio(a)

d = np.array([0.296567751, 1.160700624, -0.595454937, -1.389784669, 0.527971232])
hd = char_portfolio(d)

def port_variance(char):
    numerator = np.dot(inverted_cov, char)
    denominator = np.dot(char.T, numerator)
    return 1.0 / denominator
    
# make beta function
def beta(char):
    return np.dot(excess_cov, char_portfolio(char)) / port_variance(char)


# make covariance of attributes
def char_port_covariance(char1, char2):
    return port_exposure(char_portfolio(char1), char2) * port_variance(char2)
    

def combination_characteristic(char1, char2 , weight1, weight2):
    ka = weight1
    kd = weight2
    f = char1 * ka + char2 * kd
    inv_variance = ka * port_exposure(char_portfolio(char1), f) / port_variance(char1) + kd * port_exposure(char_portfolio(char2), f) / port_variance(char2)
    return (((ka * inv_variance**-1) / port_variance(char1)) * char_portfolio(char1) + ((kd * inv_variance**-1) / port_variance(char2)) * char_portfolio(char2))
    
hf = combination_characteristic(a, d, .2, .8)


# Portfolio B
# the benchmark portfolio is the characteristic portfolio of beta
# b is the market cap percentages of each member of the benchmark
b = np.array([.1,.2,.3,.15,.25])
portb_beta = beta(b)
hb = char_portfolio(portb_beta)
b_variance = port_variance(b)
char_port_covariance(a, b)


# Portfolio C
c = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
hc = char_portfolio(c)
varianceC = port_variance(c)
betaC = beta(c)
char_port_covariance(a, c)

# Portfolio Q
# factor portfolio of expected excess returns
q = np.array([i.mean() for i in excess_returns]) # technically the expected excess returns
hq = char_portfolio(q)
sharpe_ratio_q = np.dot(np.dot(q.T, inverted_cov), q)**0.5 # 13.0 hahaha
varianceq = port_variance(q)
beta(q)

def SharpeRatio(portfolio):
    return np.corrcoef(np.dot(portfolio,excess_returns), np.dot(char_portfolio(q), excess_returns)) * sharpe_ratio_q
    
SharpeRatio(ha)
SharpeRatio(hc)
SharpeRatio(hb)
SharpeRatio(hf)

# fraction of q invested in risky assets
risky_assets = port_exposure(char_portfolio(c), q) * port_variance(q) / port_variance(c)


# Portfolio A
alpha = q - np.dot(b, port_exposure(hb, q))
char_port_covariance(alpha, b) # approx 0.0

# Portfolio Q - fully invested in some characteristic, net long. It is the characteristic portfolio of the Highest sharpe ratio portfolio for a categorical attribute
Q = port_exposure(hq, c) * q
hQ = hq / port_exposure(hq, c)
SharpeRatio(hq) == SharpeRatio(hQ)

# 2
(port_exposure(hc, q) / port_variance(c)) == (port_exposure(hQ, q) / port_variance(Q))

# below proves how Portfolio Q "explains" expected returns
# it says it isn't but it is. It's floating number bullshit
q == (port_exposure(hQ, q) * beta(Q))

# 3
# they're the same
port_exposure(hQ, b) == ((port_exposure(hb, q) * port_variance(Q)) / (port_exposure(hQ, q) * port_variance(b)))

# 4
# if the benchmark is fully invested i.e. port_exposure(b, c) == 1.0
# this will set the Beta portfolio's exposure to c to 1.0
# kinda cheating, but I'm tired
hb2 = hb / port_exposure(hb, c)
port_exposure(hb2, c) == 1.0
port_exposure(hQ, b) == (port_exposure(char_portfolio(c), b) * port_exposure(hb2)) / port_exposure(hc, q)

# to build portfolio based on our alphas, but with a beta of 1, full investment, and conforming to our preferences for risk and return, we will build a linear combination of portfolios A, B, and C
combined = ha * .3 + hb * .3 + hc * .4
# it's not necessarily fully invested
combined.sum()