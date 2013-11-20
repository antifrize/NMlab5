__author__ = 'Antifrize'

import GridGraphModel
from AppConstants import AppConsts
from math import exp,fabs

class ExplicitGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self):
        self.remakeGrid()

    def remakeGrid(self):
        self.grid = []

        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])

        for t in range(1,len(AppConsts.gradT)):
            newLine = [AppConsts.a*AppConsts.tau/AppConsts.h**2*(self.grid[-1][x-1]-2*self.grid[-1][x]+self.grid[-1][x+1])+
                                                                 AppConsts.b*AppConsts.tau/AppConsts.h*(self.grid[-1][x+1]-self.grid[-1][x])+
                                                                                                        self.grid[-1][x]+
                                                                AppConsts.getC(AppConsts.gradX[x],AppConsts.gradT[t])/AppConsts.tau for x in range(1,AppConsts.lN)]
          #  newLine = [(AppConsts.phi_0(AppConsts.gradT[t])-AppConsts.alpha*newLine[0]/AppConsts.h)/
           #            (-AppConsts.alpha/AppConsts.h * AppConsts.beta)] + newLine
            x = int(len(AppConsts.gradX)/2)
            #print("t = "+str(AppConsts.gradT[t])+", x = "+str(AppConsts.gradX[x])+"c="+AppConsts.c+", "+str(AppConsts.getC(AppConsts.gradX[x],AppConsts.gradT[t])))
            newLine = [-(AppConsts.alpha/AppConsts.h)/(AppConsts.beta - AppConsts.alpha/AppConsts.h)*newLine[0]+
                       AppConsts.getPhi_0(AppConsts.gradT[t])/(AppConsts.beta - AppConsts.alpha/AppConsts.h) ]+newLine
            newLine = newLine+ [(AppConsts.gamma/AppConsts.h)/(AppConsts.delta + AppConsts.gamma/AppConsts.h)*newLine[-1]+
                       AppConsts.getPhi_l(AppConsts.gradT[t])/(AppConsts.delta + AppConsts.gamma/AppConsts.h) ]
            #print((AppConsts.gamma/AppConsts.h)/(AppConsts.delta + AppConsts.gamma/AppConsts.h),AppConsts.phi_l(AppConsts.gradT[t]))

            self.grid.append(newLine)
        # print self.grid[1]