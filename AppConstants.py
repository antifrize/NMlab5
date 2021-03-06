__author__ = 'Antifrize'

from math import *


class AppConsts:
    class Scheme:
        IMPLICIT = 0
        EXPLICIT = 1
        MIXED = 2

    a = 1
    b = 0
    k = 0
    c = ""
    d = ""

    lN = 15
    tN = 40

    sigma = 0.5
    Q = 0.5

    x_0 = 0
    x_l = 1

    minT = 0
    maxT = 1.

    alpha = 1
    beta = -1
    gamma = 1
    delta = -1

    scheme = Scheme.EXPLICIT

    initCondition = "sin(2*pi*x)"
    initDerrivative = "1"
    phi_0 = "0"
    phi_l = "0"
    resF = "exp(-4*pi**2*AppConsts.a*t)*sin(2*pi*x)"

    h = (x_l-x_0)*1./lN
    print('h = ',h)
    tau = sigma * h**2/a
    print('tau = ',tau)
    maxT = tN/tau
    gradX = [x_0+i*h for i in range(lN+1)]
    print('gradX = ', gradX)
    gradT = [minT+i*tau for i in range(tN+1)]
    print('gradT = ', gradT)

    @staticmethod
    def getResF(x,t):
        return(eval(AppConsts.resF))

    @staticmethod
    def translate(string):
        for s in ['a','b']:
            string = string.replace(s,'AppConsts.'+s)
        return string

    @staticmethod
    def loadTask(task):
        AppConsts.a = eval(task['a'])
        AppConsts.b = eval(task['b'])
        AppConsts.k = eval(task['k'])
        AppConsts.c = task['c']
        AppConsts.d = task['d']
        AppConsts.x_l = eval(task['x_l'])
        AppConsts.initCondition = task['initCondition']
        AppConsts.initDerrivative = task['initDerrivative']
        AppConsts.phi_0 = task['phi_0']
        AppConsts.phi_l = task['phi_l']
        AppConsts.resF = task['resF']
        AppConsts.alpha = eval(task['alpha'])
        AppConsts.beta =  eval(task['beta'])
        AppConsts.gamma =  eval(task['gamma'])
        AppConsts.delta =  eval(task['delta'])
        AppConsts.refresh()

    @staticmethod
    def refresh():
        AppConsts.lN = int(AppConsts.lN)
        AppConsts.tN = int(AppConsts.tN)
        AppConsts.h = (AppConsts.x_l-AppConsts.x_0)*1./AppConsts.lN
        print('h = ',AppConsts.h)
        AppConsts.tau = (AppConsts.sigma-0.05) * AppConsts.h**2/AppConsts.a
        print('tau = ',AppConsts.tau)
        AppConsts.maxT = AppConsts.tN/AppConsts.tau
        AppConsts.gradX = [AppConsts.x_0+i*AppConsts.h for i in range(AppConsts.lN+1)]
        # print('gradX = ', AppConsts.gradX)
        AppConsts.gradT = [AppConsts.minT+i*AppConsts.tau for i in range(AppConsts.tN+1)]
        # print('gradT = ', AppConsts.gradT)

    @staticmethod
    def getInitCondition(x):
        a = AppConsts.a
        b = AppConsts.b
        c = AppConsts.getC(x,0)
        return eval(AppConsts.initCondition)

    @staticmethod
    def getInitDerrivative(x):
        a = AppConsts.a
        b = AppConsts.b
        c = AppConsts.getC(x,0)
        return eval(AppConsts.initDerrivative)

    @staticmethod
    def getPhi_0(t):
        a = AppConsts.a
        b = AppConsts.b
        c = AppConsts.getC(AppConsts.x_l,t)
        return eval(AppConsts.phi_0)

    @staticmethod
    def getPhi_l(t):
        a = AppConsts.a
        b = AppConsts.b
        c = AppConsts.getC(0,t)
        return eval(AppConsts.phi_l)

    @staticmethod
    def getC(x,t):
        a = AppConsts.a
        b = AppConsts.b
        return eval(AppConsts.c) if len(AppConsts.c)>0 else 0

    @staticmethod
    def getD(x,t):
        a = AppConsts.a
        b = AppConsts.b
        return eval(AppConsts.d) if len(AppConsts.d)>0 else 0

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

