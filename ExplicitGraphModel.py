__author__ = 'Antifrize'

import GridGraphModel
from AppConstants import AppConsts
from math import exp,fabs

class ExplicitGraphModel(GridGraphModel.GridGraphModel):
    def __init__(self):
        self.remakeGrid(0)

    def remakeGrid(self,l):
        self.grid = []
        self.grid.append([AppConsts.getInitCondition(x) for x in AppConsts.gradX])
        for t in range(1,len(AppConsts.gradT)):
            newLine = [AppConsts.a*AppConsts.tau/AppConsts.h**2*(self.grid[-1][x-1]-2*self.grid[-1][x]+self.grid[-1][x+1])+
                                                                 AppConsts.b*AppConsts.tau/(2*AppConsts.h)*(self.grid[-1][x+1]-self.grid[-1][x])+
                                                                                                        self.grid[-1][x]+
                                                                AppConsts.getC(AppConsts.gradX[x],AppConsts.gradT[t])*self.grid[-1][x]
                                                                 *AppConsts.tau
                       +AppConsts.getD(AppConsts.gradX[x],AppConsts.gradT[t])*AppConsts.tau# if (AppConsts.getD(AppConsts.gradX[x],AppConsts.gradT[t])-AppConsts.getD(AppConsts.gradX[x],AppConsts.gradT[t-1]))==0
                       # (AppConsts.getD(AppConsts.gradX[x],AppConsts.gradT[t])-AppConsts.getD(AppConsts.gradX[x],AppConsts.gradT[t-1]))

                       for x in range(1,AppConsts.lN)]

            x = int(len(AppConsts.gradX)/2)
            h = AppConsts.h
            alpha = AppConsts.alpha
            beta = AppConsts.beta
            gamma = AppConsts.gamma
            delta = AppConsts.delta
            phi_0 = AppConsts.getPhi_0
            phi_l = AppConsts.getPhi_l
            a = AppConsts.a
            b = AppConsts.b
            tau = AppConsts.tau
            # if t%2==0:
            #      print(str(
            #          -(AppConsts.alpha/AppConsts.h)/(AppConsts.beta - AppConsts.alpha/AppConsts.h)*
            #                newLine[0]
            #              +AppConsts.getPhi_0(AppConsts.gradT[t])/(AppConsts.beta - AppConsts.alpha/AppConsts.h)
            #             )+" "
            #            +str(
            #          -(AppConsts.gamma/AppConsts.h)/(AppConsts.delta + AppConsts.gamma/AppConsts.h)*
            #                 newLine[-1]
            #             +AppConsts.getPhi_l(AppConsts.gradT[t])/(AppConsts.delta + AppConsts.gamma/AppConsts.h)
            #            ))
            if l<=0:
                newLine = [-(AppConsts.alpha/AppConsts.h)/(AppConsts.beta - AppConsts.alpha/AppConsts.h)*newLine[0]+
                       AppConsts.getPhi_0(AppConsts.gradT[t])/(AppConsts.beta - AppConsts.alpha/AppConsts.h) ]+newLine
                newLine = newLine+ [(AppConsts.gamma/AppConsts.h)/(AppConsts.delta + AppConsts.gamma/AppConsts.h)*newLine[-1]+
                       AppConsts.getPhi_l(AppConsts.gradT[t])/(AppConsts.delta + AppConsts.gamma/AppConsts.h) ]
            if l==1:
                newLine = [(h/tau*self.grid[-1][0]-phi_0(AppConsts.gradT[len( self.grid)])*(2*a-b*h)/alpha+2*a/h*newLine[0])/((
                2*a/h + h/tau-AppConsts.getC(0,AppConsts.gradT[t])*h-beta/alpha*(2*a-b*h)))]+newLine
                newLine = newLine+[(h/tau*self.grid[-1][-1]+phi_l(AppConsts.gradT[len(self.grid)])*(2*a+b*h)/gamma +2*a/h*newLine[-1])
                                   /(2*a/h + h/tau-AppConsts.getC(0,AppConsts.gradT[t])*h+delta/gamma*(2*a+b*h))]
            if l==2:
                # print("left = "+str((phi_0(AppConsts.gradT[t])-2*alpha/h*newLine[0]+alpha/(2*h)*newLine[1])/(-3*alpha/(2*h)+beta)))
                # print("right = "+str((phi_l(AppConsts.gradT[t])+2*gamma/h*newLine[-2]-gamma/(2*h)*newLine[-1])/(3*gamma/(2*h)+delta)))
                newLine = [(phi_0(AppConsts.gradT[t])-2*alpha/h*newLine[0]+alpha/(2*h)*newLine[1])/(-3*alpha/(2*h)+beta)]+newLine
                newLine = newLine+ [(phi_l(AppConsts.gradT[t])+2*gamma/h*newLine[-1]-gamma/(2*h)*newLine[-2])/(3*gamma/(2*h)+delta) ]
            #print((AppConsts.gamma/AppConsts.h)/(AppConsts.delta + AppConsts.gamma/AppConsts.h),AppConsts.phi_l(AppConsts.gradT[t]))

            self.grid.append(newLine)
        # print self.grid[1]