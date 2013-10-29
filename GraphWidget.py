__author__ = 'Antifrize'
from PySide import QtGui,QtCore

class GraphWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.graphs = []
        self.visibleRect = QtGui.QRect(0,0,0,0)

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor();
        color.setRgb(0,0,200);
        painter.setPen(color)
        painter.drawRect()
        print(self.size())
