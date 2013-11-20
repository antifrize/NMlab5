__author__ = 'vmakarenko'

import GridGraphModel
from AppConstants import *

class MixedGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self,explicitGM,implicitGM,Q):
        GridGraphModel.GridGraphModel.__init__(self)

    def makeGrid(self,explicitGM,implicitGM,Q):
        self.grid = []
        for t in range(len(AppConsts.gradT)-1):
            self.grid.append([Q*explicitGM.getT(x,t)
                    +(1-Q)*implicitGM.getT(x,t) for x in range(len(AppConsts.gradX))])

