__author__ = 'vmakarenko'

from GraphModel import *
from math import *
from AppConstants import *



class AnalogGraphModel(GraphModel):
    def __init__(self,f):
        GraphModel.__init__(self)
        self.f = f

    def getT(self,x,t):
        c = AppConsts.getC(x,t)
        return eval(self.f)