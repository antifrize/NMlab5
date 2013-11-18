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
                if i<(len(AppConsts.gradX)-1):
                    if math.fabs(AppConsts.gradX[i]-x_)<math.fabs(AppConsts.gradX[i+1]-x_):
                        xRes = i
                    else:
                        xRes = i+1
                else:
                    xRes = i
                    break

        for i in range(len(AppConsts.gradT)):
            if math.fabs(AppConsts.gradT[i]-t_)<AppConsts.tau:


                if i<(len(AppConsts.gradT)-1):
                    if math.fabs(AppConsts.gradT[i]-t_)<math.fabs(AppConsts.gradT[i+1]-t_):
                        tRes = i
                    else:
                        tRes = i+1
                else:
                    tRes = i
                    break
        return self.grid[tRes][xRes]


