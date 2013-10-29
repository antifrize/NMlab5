__author__ = 'Antifrize'

from PySide import QtGui,QtCore
import random,math,AppConstants
from commonLib import floatRange
from TMA import solveTMA

class Graph:
    points = []
    items = []
    color = QtGui.QColor()


    def __init__(self,name,model):
        self.name = name
        self.model = model
        while True:
            self.color = QtGui.QColor(random.choice(QtGui.QColor.colorNames()))
            if(self.color.greenF()*self.color.blueF()*self.color.redF()<0.15):
                break
        self.pen = QtGui.QPen()
        self.pen.setColor(self.color)


    def resetObjects(self,t):
        points = self.model.getPoints(t)
        self.items.clear()
        self.pointArray = self.model.getPoints(t)
        for i in range(0,len(self.pointArray)-1):
            self.items.append(QtCore.QLineF(self.pointArray[i][0],self.pointArray[i][1],self.pointArray[i+1][0],self.pointArray[i+1][1]))



class GraphModel():
    gradT=floatRange(AppConstants.tMin,AppConstants.tMax,AppConstants.numOfTSteps)
    gradX=floatRange(AppConstants.leftBorder,AppConstants.rightBorder,AppConstants.numOfXSteps)

    def f(self,x,t):
        pass

    def getPoints(self,t):
        return [[x, self.f(x,t)] for x in floatRange(AppConstants.leftBorder, AppConstants.rightBorder, AppConstants.numOfXSteps)]

class OriginalGraphModel(GraphModel):
    def f(self,x,t):
        return math.exp(-AppConstants.a*t)*math.cos(x+t*AppConstants.b)

class GridGraphModel(GraphModel):
    def f(self,x,t):
        xStr = self.findIndex(self.gradX,x)
        tStr = self.findIndex(self.gradT,t)
        # print(tStr,xStr,t,x)
        #TODO optimization
        return self.grid[tStr][xStr]

    def findIndex(self,list,x):
        temp=100000
        for i in range(len(list)):
            if temp<math.fabs(list[i]-x):
                xStr = i-1 if math.fabs(list[i-1]-x)<math.fabs(list[i]-x) else i
                return xStr
            else:
                temp = math.fabs(list[i]-x)
        return len(list)-1

    def initialCondition(self,x):
        return math.cos(x)

class ExplicitGraphModel(GridGraphModel):
    def __init__(self):
        GraphModel.__init__(self)
        self.makeGrid()

    def makeGrid(self):
        self.grid=[]
        self.grid.append([self.initialCondition(x) for x in floatRange(AppConstants.leftBorder,AppConstants.rightBorder,AppConstants.numOfXSteps)])
        AppConstants.printConstants()
        for k in range(AppConstants.numOfTSteps-1):
            newLine = []
            # print("newLine ",newLine)
            # print("grid ",self.grid)
            for j in range(1,len(self.gradX)-1):
                # print("j = {}, k={}, newLine={}".format(j,k,newLine))
                #newLine.append(self.grid[k][j]+ AppConstants.tau*(AppConstants.a*(self.grid[k][j+1]-2*self.grid[k][j]+\
                #self.grid[k][j-1])/(AppConstants.h**2)+AppConstants.b*(self.grid[k][j+1]-self.grid[k][j])/AppConstants.h))
                newLine.append(AppConstants.a*AppConstants.tau/AppConstants.h**2*(self.grid[k][j+1]-2*self.grid[k][j]+self.grid[k][j-1])+\
                AppConstants.b*AppConstants.tau/AppConstants.h*(self.grid[k][j+1]-self.grid[k][j])+self.grid[k][j])
                # print("j = {}, k={}, newLine={}".format(j,k,newLine))
            # newLine = [(AppConstants.phi_0(self.gradT[k])-AppConstants.alpha*newLine[0])/(-AppConstants.alpha/AppConstants.h+AppConstants.beta)] + newLine
            # newLine.append(-(AppConstants.phi_l(self.gradT[k])-AppConstants.gamma*newLine[-1])/(AppConstants.gamma/AppConstants.h+AppConstants.delta))
            newLine = [-(AppConstants.alpha/AppConstants.h)/(AppConstants.beta-AppConstants.alpha/AppConstants.h)*newLine[0]+AppConstants.phi_0(self.gradT[k+1])/(AppConstants.beta-AppConstants.alpha/AppConstants.h)] + newLine
            newLine.append((AppConstants.gamma/AppConstants.h)/(AppConstants.delta+AppConstants.gamma/AppConstants.h)*newLine[-1]+AppConstants.phi_l(self.gradT[k+1])/(AppConstants.delta+AppConstants.gamma/AppConstants.h))
            # print(newLine)
            self.grid.append(newLine)


class ImplicitGraphModel(GridGraphModel):
    def __init__(self):
        GraphModel.__init__(self)
        self.makeGrid()

    def makeSLAE(self,line):
        slae=[]
        slae.append([0,AppConstants.beta-AppConstants.alpha/AppConstants.h,AppConstants.alpha/AppConstants.h,AppConstants.phi_0(self.gradT[len(self.grid)+1])/(AppConstants.beta-AppConstants.alpha/AppConstants.h)])
        for u in line[1:-1]:
            slae.append([AppConstants.a/AppConstants.h**2,
                         -(1+2*AppConstants.a*AppConstants.tau/AppConstants.h**2+AppConstants.b*AppConstants.tau/AppConstants.h)
                            ,AppConstants.a/AppConstants.h**2,-u])
        slae.append([-AppConstants.gamma/AppConstants.h,AppConstants.delta+AppConstants.gamma/AppConstants.h,0,AppConstants.phi_l(self.gradT[len(self.grid)+1])/(AppConstants.delta+AppConstants.gamma/AppConstants.h)])
        return slae

    def makeGrid(self):
        self.grid=[]
        self.grid.append([self.initialCondition(x) for x in self.gradX])
        for k in range(AppConstants.numOfTSteps-1):
            slae = self.makeSLAE(self.grid[-1])
            self.grid.append(solveTMA(slae))
