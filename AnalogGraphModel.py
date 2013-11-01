__author__ = 'vmakarenko'

from GraphModel import *


class AnalogGraphModel(GraphModel):
    def __init__(self,f):
        GraphModel.__init__(self)
        self.f = f

    def getT(self,x,t):
        return self.f(x,t)