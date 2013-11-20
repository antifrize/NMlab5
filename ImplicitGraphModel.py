__author__ = 'Antifrize'

from AppConstants import AppConsts
import GridGraphModel
from TMA import *

class ImplicitGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self):
        GridGraphModel.GridGraphModel.__init__(self)
        self.makeGrid()
        
    def makeSLAE(self,line,t):
        slae = []

        slae.append([0,AppConsts.beta-AppConsts.alpha/AppConsts.h,AppConsts.alpha/AppConsts.h,
                     AppConsts.getPhi_0(AppConsts.gradT[len(self.grid)+1])/(AppConsts.beta-AppConsts.alpha/AppConsts.h)])
        for (u,un) in zip(line[1:-1],range(1,len(line))):
            #print()
            slae.append([-AppConsts.a/AppConsts.h**2*AppConsts.tau+AppConsts.tau*AppConsts.b/(2*AppConsts.h),
                         1+2*AppConsts.a*AppConsts.tau/AppConsts.h**2-AppConsts.b*AppConsts.tau/(2*AppConsts.h)+AppConsts.tau*AppConsts.getC(AppConsts.gradX[un],AppConsts.gradT[t])
                            ,-AppConsts.a*AppConsts.tau/AppConsts.h**2,u])
        slae.append([-AppConsts.gamma/AppConsts.h, AppConsts.delta+AppConsts.gamma/AppConsts.h, 0
            ,AppConsts.getPhi_l(AppConsts.gradT[len(self.grid)+1])/(AppConsts.delta+AppConsts.gamma/AppConsts.h)])



        return slae

    def makeGrid(self):
        self.grid=[]
        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])
        for k in range(1,len(AppConsts.gradT)-1):
            slae = self.makeSLAE(self.grid[-1],k)
            self.grid.append(solveTMA(slae))
            if k==1:
            #    print('solutions = ')
                print(slae)
            #    print(list(solve1(slae)))