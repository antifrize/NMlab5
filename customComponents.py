__author__ = 'Antifrize'

from PySide import QtGui, QtCore
import AppConstants
import math
from graph import *

class GraphsSelection(QtGui.QHBoxLayout):
    def __init__(self, graphs):
        QtGui.QHBoxLayout.__init__(self)
        self.checkboxes = []
        for graph in graphs:
            self.checkboxes.append(QtGui.QCheckBox(graph.name))
            self.addWidget(self.checkboxes[-1])


class QGraphicsViewLt(QtGui.QVBoxLayout):

    graphs = []
    graphModels = []
    items = []

    selection = GraphsSelection

    def __init__(self):
        QtGui.QVBoxLayout.__init__(self)
        self.fillLayout()

    def resetObjects(self):
        self.label = ""
        # print(self.slider.value())
        for item in self.items:
            self.scene.removeItem(item)
        self.items = []
        for i in range(len(self.graphs)):
            if(self.selection.checkboxes[i].isChecked()):
                # print("adding "+str(i)+"st graph")
                self.graphs[i].resetObjects(AppConstants.tMin+self.slider.value()*AppConstants.tau)
                for item in self.graphs[i].items:
                    self.items.append(self.scene.addLine(item,self.graphs[i].pen))
            # print(self.graphs[i].pen)


        # print(len(self.items),len(self.graphs[i].items),len(self.scene.items()))
    def fillLayout(self):
        # добавим графики по именам и функциям построения

        self.slider = QtGui.QSlider()
        self.slider.setMaximum(AppConstants.numOfTSteps)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.resetObjects)
        self.graphs.clear()

        self.graphs.append(Graph("Original",OriginalGraphModel()))
        self.graphs.append(Graph("Explicit",ExplicitGraphModel()))
        self.graphs.append(Graph("Implicit",ImplicitGraphModel()))
        self.graphs.append(Graph("Crunk-Nikolson",None))

        self.selection = GraphsSelection(self.graphs)
        for checkbox in self.selection.checkboxes:
            checkbox.clicked.connect(self.resetObjects)



        self.scene = QtGui.QGraphicsScene()
        self.scene.addLine(AppConstants.leftBorder,0,AppConstants.rightBorder,0)
        self.scene.addLine(0,-2,0,2)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setTransform(QtGui.QTransform(1,0,0,0,-1,0,0,0,1))
        self.view.scale(100,100)
        self.view.show()
        self.label = QtGui.QLabel("Test Label")
        self.addWidget(self.label)
        self.addWidget(self.view)
        self.addItem(self.selection)
        self.addWidget(self.slider)

    def setLabel(self, string):
        self.label.setText(string)

    def setPointsArray(self,points):
        self.pointArray = points
        self.resetObjects(AppConstants.tMin+self.slider.value()*AppConstants.tau)
        self.scene.update()

