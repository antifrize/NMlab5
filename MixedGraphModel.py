__author__ = 'vmakarenko'

import GridGraphModel
from AppConstants import *

class MixedGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self,explicitGM,implicitGM,Q):
        GridGraphModel.GridGraphModel.__init__()

        self.grid = []
        for t in range(len(AppConsts.gradT)):
            self.grid.append([Q*explicitGM.getT(AppConsts.gradX[x],AppConsts.gradT[t])
                    +(1-Q)*implicitGM.getT(AppConsts.gradX[x],AppConsts.gradT[t]) for x in range(len(AppConsts.gradX))])

