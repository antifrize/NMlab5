__author__ = 'Antifrize'

from AppConstants import AppConsts
import GridGraphModel
from TMA import *
from math import fabs


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
                            ,-AppConsts.a*AppConsts.tau/AppConsts.h**2,u+AppConsts.tau*AppConsts.getD(AppConsts.gradX[un],AppConsts.gradT[t])])
        slae.append([-AppConsts.gamma/AppConsts.h, AppConsts.delta+AppConsts.gamma/AppConsts.h, 0
            ,AppConsts.getPhi_l(AppConsts.gradT[len(self.grid)+1])/(AppConsts.delta+AppConsts.gamma/AppConsts.h)])


        return slae

    def isDiagMatrix(self,matrix):
        for line in matrix:
            if fabs(line[1])<(fabs(line[0])+fabs(line[2])):
                return False
        return True

    def makeGrid(self):
        self.grid=[]
        self.diag = True
        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])
        for k in range(1,len(AppConsts.gradT)-1):
            slae = self.makeSLAE(self.grid[-1],k)
            if not  self.isDiagMatrix(slae):
                self.diag = False
            self.grid.append(solve1(slae))
            if k==1:
            #    print('solutions = ')
                print(slae)
                print(solveTMA(slae))
                print(solve1(slae))
            #    print(list(solve1(slae)))


    def isDiag(self):
        return self.diag