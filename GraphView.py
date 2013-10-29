__author__ = 'Antifrize'
from PySide import QtGui,QtCore

class GraphView(QtGui.QWidget):
    boundingRect = QtCore.QRect()
    def __init__(self):
        QtGui.QWidget.__init__(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter
        painter.setPen(QtGui.QPen(QtCore))
        painter.drawRect(self.boundingRect)

