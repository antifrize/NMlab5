__author__ = 'vmakarenko'

import GridGraphModel
from AppConstants import *

class MixedGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self,explicitGM,implicitGM,Q):
        GridGraphModel.GridGraphModel.__init__(self)

    def makeGrid(self,explicitGM,implicitGM,Q):
        # print(explicitGM.[1])
        # print(implicitGM[1])
        self.grid = [[Q*xE+(1-Q)*xI for xE,xI in zip(lineExpl,lineImpl)] for lineExpl, lineImpl in zip(explicitGM.grid,implicitGM.grid)]

        print self.grid[1]

