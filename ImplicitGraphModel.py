__author__ = 'Antifrize'

from AppConstants import AppConsts
import GridGraphModel
from TMA import *
from math import fabs


class ImplicitGraphModel(GridGraphModel.GridGraphModel):

    def __init__(self):
        GridGraphModel.GridGraphModel.__init__(self)
        self.makeGrid(0)

        
    def makeSLAE(self,line,t,n):
        slae = []
        a = AppConsts.a
        b = AppConsts.b
        k = AppConsts.k
        alpha = AppConsts.alpha
        beta = AppConsts.beta
        gamma = AppConsts.gamma
        delta = AppConsts.delta
        phi_0 = AppConsts.getPhi_0
        phi_l = AppConsts.getPhi_l
        h = AppConsts.h
        tau = AppConsts.tau


        if n<=0:
            slae.append([0,AppConsts.beta-AppConsts.alpha/AppConsts.h,AppConsts.alpha/AppConsts.h,
                         AppConsts.getPhi_0(AppConsts.gradT[len(self.grid)])
            #              /(AppConsts.beta-AppConsts.alpha/AppConsts.h)
            ])
            for (u,un) in zip(line[1:-1],range(1,len(line)-1)):
                #print()
                slae.append([-a/h**2-b/h,
                                1/tau**2+k/tau +2*a/h**2+b/h-AppConsts.getC(AppConsts.gradX[un],AppConsts.gradT[t]),
                            -a/h**2,
                             AppConsts.getD(AppConsts.gradX[un],AppConsts.gradT[t])
                             -(-2*self.grid[-1][un]+self.grid[-2][un])/tau**2
                            +k*self.grid[-1][un]/tau
                ])
            slae.append([-gamma/h, delta+gamma/h, 0
                ,phi_l(AppConsts.gradT[len(self.grid)])
                 #/(AppConsts.delta+AppConsts.gamma/AppConsts.h)
             ])

        if n==2:
            slae.append([0,-3*alpha/(2*h)+beta,2*alpha/h,phi_0(AppConsts.gradT[len(self.grid)])])
            for (u,un) in zip(line[1:-1],range(1,len(line))):
                #print()
                slae.append([-a/h**2-b/h,
                                1/tau**2+k/tau +2*a/h**2+b/h-AppConsts.getC(AppConsts.gradX[un],AppConsts.gradT[t]),
                            -a/h**2,
                             AppConsts.getD(AppConsts.gradX[un],AppConsts.gradT[t])
                             -(-2*self.grid[-1][un]+self.grid[-2][un])/tau**2
                            +k*self.grid[-1][un]/tau])
            slae.append([delta - 2*gamma/(h),3.*gamma/(2*h), 0
                ,phi_l(AppConsts.gradT[len(self.grid)])])

            coeff =  (-1.*alpha/(2*h))/slae[1][2]
            slae[0][1] -= slae[1][0]*coeff
            slae[0][2] -= slae[1][1]*coeff
            slae[0][3] -= slae[1][3]*coeff

            coeff =  (1.*gamma/(2*h))/slae[-2][0]
            slae[-1][0] -= slae[-2][1]*coeff
            slae[-1][1] -= slae[-2][2]*coeff
            slae[-1][3] -= slae[-2][3]*coeff

        if n==1:
            slae.append([0,
            2*a/h + h/tau-AppConsts.getC(0,AppConsts.gradT[t])*h-beta/alpha*(2*a-b*h),
            -2*a/h,
            h/tau*self.grid[-1][0]-phi_0(AppConsts.gradT[len(self.grid)])*(2*a-b*h)/alpha])
            for (u,un) in zip(line[1:-1],range(1,len(line)-1)):
                #print()
                slae.append([-a/h**2-b/h,
                                1/tau**2+k/tau +2*a/h**2+b/h-AppConsts.getC(AppConsts.gradX[un],AppConsts.gradT[t]),
                            -a/h**2,
                             AppConsts.getD(AppConsts.gradX[un],AppConsts.gradT[t])
                             -(-2*self.grid[-1][un]+self.grid[-2][un])/tau**2
                            +k*self.grid[-1][un]/tau
                ])
            slae.append([-gamma/h, delta+gamma/h, 0
                ,phi_l(AppConsts.gradT[len(self.grid)])
                 #/(AppConsts.delta+AppConsts.gamma/AppConsts.h)
             ])
            slae.append([-2*a/h,
            2*a/h + h/tau-AppConsts.getC(0,AppConsts.gradT[t])*h+delta/gamma*(2*a+b*h),
            0,
            h/tau*self.grid[-1][-1]+phi_l(AppConsts.gradT[len(self.grid)])*(2*a+b*h)/gamma])
        return slae

    def isDiagMatrix(self,matrix):
        for line in matrix:
            if fabs(line[1])<(fabs(line[0])+fabs(line[2])):
                return False
        return True

    def makeGrid(self,n):
        self.grid=[]
        self.diag = True
        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])
        self.grid.append([AppConsts.getInitCondition(x)+AppConsts.getInitDerrivative(x)*AppConsts.tau for x in AppConsts.gradX])
        for k in range(2,len(AppConsts.gradT)):
            slae = self.makeSLAE(self.grid[-1],k,n)
            if not self.isDiagMatrix(slae):
                self.diag = False
                # print("f.ail slae: ",str(slae))

            self.grid.append(solve1(slae))
            # if k<10:
            #    print('solutions = ')
            #     print(slae)
                # print(solveTMA(slae))
                # print(solve1(slae))
            #    print(list(solve1(slae)))


    def isDiag(self):
        return self.diag