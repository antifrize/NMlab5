__author__ = 'Antifrize'


import GraphModel
import AppConstants as AppConsts
import math

class GridGraphModel(GraphModel.GraphModel):
    grid = []
    def getT(self,x_,t_):
        xRes = tRes = 0
        for i in range(len(AppConsts.gradX)):
            if math.fabs(AppConsts.gradX[i]-x_)<AppConsts.h:
                xRes = i

                break

        for i in range(len(AppConsts.gradT)):
            if math.fabs(AppConsts.gradT[i]-t_)<AppConsts.tau:
                tRes = i
                break
        return self.grid[tRes][xRes]


