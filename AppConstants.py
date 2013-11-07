__author__ = 'Antifrize'

import math
class AppConsts:
    class Scheme:
        IMPLICIT = 0
        EXPLICIT = 1
        MIXED = 2

    a = 1
    b = 0
    c = ""

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

    initCondition = "math.sin(2*math.pi*x)"
    phi_0 = "0"
    phi_l = "0"
    resF = "math.exp(-4*math.pi**2*AppConsts.a*t)*math.sin(2*math.pi*x)"

    h = (x_l-x_0)/lN
    print('h = ',h)
    tau = sigma * h**2/a
    print('tau = ',tau)
    tN = int((maxT-minT)/tau)
    gradX = [x_0+i*h for i in range(lN+1)]
    print('gradX = ', gradX)
    gradT = [minT+i*tau for i in range(tN+1)]
    print('gradT = ', gradT)


    @staticmethod
    def refresh():
        pass

    @staticmethod
    def getInitCondition(x):
        return eval(AppConsts.initCondition)

    @staticmethod
    def getPhi_0(t):
        return eval(AppConsts.phi_0)

    @staticmethod
    def getPhi_l(t):
        return eval(AppConsts.phi_l)

    @staticmethod
    def getAnalog(x,t):
        return eval(AppConsts.resF)

    @staticmethod
    def setApprox(n):
        pass

    @staticmethod
    def setScheme(schemeN):
        global scheme
        scheme = schemeN

