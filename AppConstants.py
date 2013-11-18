__author__ = 'Antifrize'

import math

class Scheme:
    IMPLICIT = 0
    EXPLICIT = 1
    MIXED = 2



a = 1
b = 0
c = 0
lN = 15
tN = 40
sigma = 0.5
q = 0
x_0 = 0
x_l = math.pi
minT = 0
maxT = 5
alpha = 1
beta = -1
gamma = 1
delta = -1
scheme = Scheme.EXPLICIT
h = tau = tN = gradX = gradT = 0

def refresh():
    global h, tau, tN, gradX, gradT, lN, a, b
    h = (x_l-x_0)/lN
    print('h = ',h)
    tau = sigma * h**2/a
    print('tau = ',tau)
    tN = int((maxT-minT)/tau)
    gradX = [x_0+i*h for i in range(lN+1)]
    print('gradX = ', gradX)
    gradT = [minT+i*tau for i in range(tN+1)]
    print('gradT = ', gradT)


def initCondition(x):
    return math.cos(x)

def phi_0(t):
    return -math.exp(-a*t)*(math.cos(b*t)+math.sin(b*t))

def phi_l(t):
    return math.exp(-a*t)*(math.cos(b*t)+math.sin(b*t))


def setA(a_):
    global a
    a = int(a_)


def setB(b_):
    global b
    b = float(b_)

def setC(c_):
    global c
    c = c_

def setAlpha(alpha_):
    global alpha
    alpha = alpha_

def setBeta(beta_):
    global beta
    beta = beta_

def setGamma(gamma_):
    global gamma
    gamma = gamma_

def setDelta(delta_):
    global delta
    delta = delta_

def setLn(ln_):
    global lN
    lN = ln_



def setQ(q_):
    global q
    q = float(q_)

def setSigma(sigma_):
    global sigma
    sigma = float(sigma_)

def setH(h_):
    global h
    h = float(h_)

def setLN(lN_):
    global lN
    lN = int(lN_)

def setApprox(n):
    pass

def setScheme(schemeN):
    global scheme
    scheme = schemeN

refresh()
