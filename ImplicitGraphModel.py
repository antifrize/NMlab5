__author__ = 'Antifrize'

from AppConstants import AppConsts
import GridGraphModel
from TMA import *

class ImplicitGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self):
        GridGraphModel.GridGraphModel.__init__(self)
        self.makeGrid()
        
    def makeSLAE(self,line):
        slae = []
        # for i in range(len(line)):
        #     slae.append([0 for j in range(len(line)+1)])
        #
        # slae[0][1] = AppConsts.beta-AppConsts.alpha/AppConsts.h
        # slae[0][2] = AppConsts.alpha/AppConsts.h
        # slae[0][3] = AppConsts.phi_0(AppConsts.gradT[len(self.grid)+1])/(AppConsts.beta-AppConsts.alpha/AppConsts.h)
        #
        # for i in range(1,len(line)-1):
        #     slae[i][i] = AppConsts.a/AppConsts.h**2
        #     slae[i][i+1] = -(1+2*AppConsts.a*AppConsts.tau/AppConsts.h**2+AppConsts.b*AppConsts.tau/AppConsts.h)
        #     slae[i][i+2] = AppConsts.a/AppConsts.h**2
        #     slae[i][-1] = -line[-i]
        #
        # slae[-1][-3] = -AppConsts.gamma/AppConsts.h
        # slae[-1][-2] = AppConsts.delta+AppConsts.gamma/AppConsts.h
        # slae[-1][-1] = AppConsts.phi_l(AppConsts.gradT[len(self.grid)+1])/(AppConsts.delta+AppConsts.gamma/AppConsts.h)

        slae.append([0,AppConsts.beta-AppConsts.alpha/AppConsts.h,AppConsts.alpha/AppConsts.h,
                     AppConsts.getPhi_0(AppConsts.gradT[len(self.grid)+1])/(AppConsts.beta-AppConsts.alpha/AppConsts.h)])
        for u in line[1:-1]:
            slae.append([AppConsts.a/AppConsts.h**2,
                         -(1+2*AppConsts.a*AppConsts.tau/AppConsts.h**2+AppConsts.b*AppConsts.tau/AppConsts.h)
                            ,AppConsts.a/AppConsts.h**2,u])
        slae.append([-AppConsts.gamma/AppConsts.h, AppConsts.delta+AppConsts.gamma/AppConsts.h, 0
            ,AppConsts.getPhi_l(AppConsts.gradT[len(self.grid)+1])/(AppConsts.delta+AppConsts.gamma/AppConsts.h)])

        return slae

    def makeGrid(self):
        self.grid=[]
        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])
        for k in range(1,len(AppConsts.gradT)-1):
            slae = self.makeSLAE(self.grid[-1])

            self.grid.append(solveTMA(slae))
            if k==100:
                 print(solveTMA(slae))
