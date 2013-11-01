# -*- coding: utf-8 -*-
import math,sys
from AnalogGraphModel import *
from PyQt4 import QtGui, QtCore,Qt

import pyqtgraph as pg
import AppConstants as AppConsts
import ExplicitGraphModel
import ImplicitGraphModel



class Lab1MainWidget(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("LAB 1")
        self.resize(800,600)
        self.createForm()
        self.loadData()
        self.redraw()

    def updateFields(self):

        self.aLineEdit.setText(str(AppConsts.a))
        self.bLineEdit.setText(str(AppConsts.b))
        self.sigmaLineEdit.setText(str(AppConsts.sigma))
        self.lNLineEdit.setText(str(AppConsts.lN))
        self.hLineEdit.setText(str(AppConsts.h))
        if AppConsts.scheme == AppConsts.Scheme.EXPLICIT:
            self.activeGraphModel = self.explicitGraphModel
        if AppConsts.scheme == AppConsts.Scheme.IMPLICIT:
            self.activeGraphModel = self.implicitGraphModel

        self.redraw()

    def loadData(self):
        self.analogGraphModel = AnalogGraphModel(lambda x,t: math.exp(-AppConsts.a*t)*math.cos(x+AppConsts.b*t))
        self.explicitGraphModel = ExplicitGraphModel.ExplicitGraphModel()
        self.implicitGraphModel = ImplicitGraphModel.ImplicitGraphModel()
        if self.schemeComboBox.currentIndex() == 0:
            self.activeGraphModel = self.implicitGraphModel
        else:
            self.activeGraphModel = self.explicitGraphModel



    def onSliderMove(self,n):
        self.redraw()

    def redraw(self):
        #print([self.activeGraphModel.getT(x,0) for x in AppConsts.gradX][0:3])
        #print([self.activeGraphModel.getT(x,AppConsts.tau) for x in AppConsts.gradX][0:3])
        t = self.slider.value()*1./100
        if len(self.graphWidget.getPlotItem().listDataItems())==0:
            self.graphWidget.getPlotItem().plot(AppConsts.gradX,[self.analogGraphModel.getT(x,t) for x in AppConsts.gradX])
            self.graphWidget.getPlotItem().plot(AppConsts.gradX,[self.activeGraphModel.getT(x,t) for x in AppConsts.gradX])
        self.graphWidget.getPlotItem().listDataItems()[0].setData(AppConsts.gradX,[self.analogGraphModel.getT(x,t) for x in AppConsts.gradX])
        self.graphWidget.getPlotItem().listDataItems()[1].setData(AppConsts.gradX,[self.activeGraphModel.getT(x,t) for x in AppConsts.gradX])

        if len(self.errorWidget.getPlotItem().listDataItems())==0:
          self.errorWidget.getPlotItem().plot(AppConsts.gradX,[math.fabs(self.analogGraphModel.getT(x,t)-self.activeGraphModel.getT(x,t)) for x in AppConsts.gradX])
        self.errorWidget.getPlotItem().listDataItems()[0].setData(AppConsts.gradX,[math.fabs(self.analogGraphModel.getT(x,t)-self.activeGraphModel.getT(x,t)) for x in AppConsts.gradX])


        self.update()

    def createForm(self):
        class RefreshListenerFactory:
            @staticmethod
            def getRefresherListener(setterF,outer,widget):
                def listener():
                    if isinstance(widget,QtGui.QLineEdit):
                        setterF(widget.text())
                    if isinstance(widget,QtGui.QComboBox):
                        setterF(widget.currentIndex())
                    AppConsts.refresh()
                    outer.updateFields()
                return listener

        class LabelFactory:
            @staticmethod
            def getLabel(string):
                label = QtGui.QLabel()
                label.setPixmap(QtGui.QPixmap(string))
                print QtGui.QPixmap(string).isNull()
                return label
        class LineEditFactory:
            @staticmethod
            def getLineEdit(outer,name):
                methodName = name.capitalize()
                le = QtGui.QLineEdit
                le.editingFinished.connect(RefreshListenerFactory.getRefresherListener(getattr(AppConsts,"set"+methodName), outer,le))
                le.setObjectName(QtCore.QString(name+"LineEdit"))
                return le
        settingsLayout = QtGui.QHBoxLayout()
        settingsLayout.setSpacing(20)

        self.aLineEdit = LineEditFactory.getLineEdit(self, "a")
        self.bLineEdit = LineEditFactory.getLineEdit(self, "b")
        self.cLineEdit = LineEditFactory.getLineEdit(self, "c")

        self.alphaLineEdit = LineEditFactory.getLineEdit(self, "alpha")
        self.betaLineEdit = LineEditFactory.getLineEdit(self, "beta")
        self.gammaLineEdit = LineEditFactory.getLineEdit(self, "gamma")
        self.deltaLineEdit = LineEditFactory.getLineEdit(self, "delta")

        self.sigmaLineEdit = LineEditFactory.getLineEdit(self, "sigma")
        self.lNLineEdit = LineEditFactory.getLineEdit(self, "lN")
        self.hLineEdit = LineEditFactory.getLineEdit(self, "h")


        self.refreshButton = QtGui.QPushButton(u"Пересчитать")
        self.refreshButton.pressed.connect(self.loadData)

        self.approxComboBox = QtGui.QComboBox()
        self.approxComboBox.currentIndexChanged.connect(RefreshListenerFactory.getRefresherListener(AppConsts.setApprox,self,self.approxComboBox))
        self.approxComboBox.addItem(u'Второго порядка')
        self.schemeComboBox = QtGui.QComboBox()
        self.schemeComboBox.currentIndexChanged.connect(RefreshListenerFactory.getRefresherListener(AppConsts.setScheme,self,self.schemeComboBox))
        self.schemeComboBox.addItem(u"Неявная")
        self.schemeComboBox.addItem(u"Явная")
        self.schemeComboBox.addItem(u"Смешанная")
        self.schemeComboBox.setCurrentIndex(0)

        self.slider = QtGui.QSlider()
        self.slider.setOrientation(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(AppConsts.maxT*100)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.onSliderMove)

        self.qLineEdit = QtGui.QLineEdit()
        self.qLineEdit.editingFinished.connect(AppConsts.setQ)
        self.qLineEdit.setText(str(AppConsts.q))

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.getPlotItem().setXRange(AppConsts.gradX[0],AppConsts.gradX[-1])
        self.graphWidget.getPlotItem().setYRange(-1,1)
        self.graphWidget.getPlotItem().enableAutoRange(pg.ViewBox.XYAxes,False)
        self.errorWidget = pg.PlotWidget()

        equationLayout = QtGui.QHBoxLayout()
        equationLayout.addWidget(QtGui.QLabel("du/dt="))
        equationLayout.addWidget(self.aLineEdit)
        equationLayout.addWidget(QtGui.QLabel("d^2u/dx^2+"))
        equationLayout.addWidget(self.bLineEdit)
        equationLayout.addWidget(QtGui.QLabel("du/dx+"))
        equationLayout.addWidget(self.cLineEdit)

        initCondLayout = QtGui.QHBoxLayout()
        initCondLayout.addWidget(self.alphaLineEdit)
        initCondLayout.addWidget(QtGui.QLabel("u(0,t)"))
        initCondLayout.addWidget(self.betaLineEdit)
        initCondLayout.addWidget(QtGui.QLabel("du/dx(0,t)"))
        initCondLayout.addWidget(self.gammaLineEdit)
        initCondLayout.addWidget(QtGui.QLabel("u(l,t)"))
        initCondLayout.addWidget(self.deltaLineEdit)
        initCondLayout.addWidget(QtGui.QLabel("du/dx(l,t)"))

        constantsLayout = QtGui.QFormLayout()
        constantsLayout.addRow(QtGui.QLabel("lN="),self.lNLineEdit)
        constantsLayout.addRow(QtGui.QLabel(u"h="),self.hLineEdit)
        constantsLayout.addRow(QtGui.QLabel(u"sigma="),self.sigmaLineEdit)

        constantsLayout2 = QtGui.QFormLayout()
        constantsLayout2.addRow(QtGui.QLabel(u"Аппроксимация"),self.approxComboBox)
        constantsLayout2.addRow(QtGui.QLabel(u"Схема"),self.schemeComboBox)
        constantsLayout2.addRow(QtGui.QLabel(u"Q = "),self.qLineEdit)
        #constantsLayout2.addRow(QtGui.QLabel(),self)
        constantsLayout2.addWidget(self.refreshButton)

        constantsLayout.setSpacing(10)
        constantsLayout2.setSpacing(10)


        settingsLayout.addItem(constantsLayout)
        settingsLayout.addItem(constantsLayout2)

        graphsLayout = QtGui.QHBoxLayout()
        graphsLayout.setSpacing(10)
        leftGraphLayout = QtGui.QVBoxLayout()
        leftGraphLayout.addWidget(QtGui.QLabel(u"Графики функций"))
        leftGraphLayout.addWidget(self.graphWidget)
        rightGraphLayout = QtGui.QVBoxLayout()
        rightGraphLayout.addWidget(QtGui.QLabel(u"Погрешность"))
        rightGraphLayout.addWidget(self.errorWidget)
        graphsLayout.addItem(leftGraphLayout)
        graphsLayout.addItem(rightGraphLayout)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addItem(equationLayout)
        self.mainLayout.addItem(initCondLayout)
        self.mainLayout.addItem(settingsLayout)
        self.mainLayout.addWidget(self.slider)
        self.mainLayout.addItem(graphsLayout)
        self.setLayout(self.mainLayout)
        pass



    def paintEvent(self, event):
        QtGui.QWidget.paintEvent(self, event)



    def readData(self):
        inputFile = open("data.in","r")

    def plotResult(self):
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    window = Lab1MainWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()