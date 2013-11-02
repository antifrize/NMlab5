__author__ = 'Antifrize'

import math
class AppConsts:
    class Scheme:
        IMPLICIT = 0
        EXPLICIT = 1
        MIXED = 2



    a = 1
    b = 0
    c = 0
    lN = 10
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
    h = (x_l-x_0)/lN
    print('h = ',h)
    tau = sigma * h**2/a
    print('tau = ',tau)
    tN = int((maxT-minT)/tau)
    gradX = [x_0+i*h for i in range(lN+1)]
    print('gradX = ', gradX)
    gradT = [minT+i*tau for i in range(tN+1)]
    print('gradT = ', gradT)

    def refresh(self):
        pass
    def initCondition(x):
        return math.cos(x)

    def phi_0(t):
        return -math.exp(-a*t)*(math.cos(b*t)+math.sin(b*t))

    def phi_l(t):
        return math.exp(-a*t)*(math.cos(b*t)+math.sin(b*t))

    def setApprox(n):
        pass

    def setScheme(schemeN):
        global scheme
        scheme = schemeN

