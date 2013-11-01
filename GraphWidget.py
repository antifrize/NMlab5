__author__ = 'Antifrize'
from PySide import QtGui,QtCore,QtDeclarative
import AppConstants as AppConsts
from AnalogGraphModel import *

class GraphWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.graphModels = []
        self.graphModels.append(AnalogGraphModel(lambda x: x**2))

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor()
        color.setRgb(0,0,200)
        painter.setPen(color)
        self.drawBackground(painter)
        for graphModel in self.graphModels:
            self.drawGraph([QtCore.QPointF(x,graphModel.getT(x)) for x in AppConsts.gradX],painter)

    def drawBackground(self,painter):
        painter.fillRect(self.rect(), QtCore.Qt.white)

    def drawGraph(self,points,painter):
        xCoeff = self.width()/(AppConsts.x_l-AppConsts.x_0)
        yCoeff = xCoeff*-1
        for i in range(len(points)-1):
            painter.drawLine(QtCore.QPoint(int(points[i].x()*xCoeff),int(points[i].y()*yCoeff))
                ,QtCore.QPoint(int(points[i+1].x()*xCoeff),int(points[i+1].y()*yCoeff)))
