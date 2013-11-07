# -*- coding: utf-8 -*-
__author__ = 'Antifrize'

from AppConstants import AppConsts
import sys
import sip
from PyQt4 import QtGui
import pyqtgraph as pg


class Lab5MainWidget(QtGui.QWidget):
    floatNames =("a","b","Q","alpha","beta","delta","gamma")
    evalNames = ("c","phi_0","phi_l","initCond")

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle(u"Решение параболических дифференциальных уравнений")
        self.resize(800,600)
        self.createControls()
        self.fillLayouts()
        self.refreshData()
        sip.setdestroyonexit(False)

    def createFieldAndSetters(self,module,name):
        def setter(x):
            var = setattr(module,name,x)

        def getter():
            var = getattr(module,name)
            return var
        setattr(module,"set"+name.capitalize(),staticmethod(setter))
        setattr(module,"get"+name.capitalize(),staticmethod(getter))

    def addLineEdit(self,var):
        lineEdit = QtGui.QLineEdit()
        outer = self
        def listener(self):
            if not self.focus():
                setter = getattr(AppConsts,"set"+var.capitalize())
                lineEdit = getattr(outer,var+"LineEdit")
                setter(lineEdit.value())


        lineEdit.textEdited.connect(listener)
        return lineEdit

    def createControls(self):
        # create getter and setter in AppConsts class
        for var in self.floatNames+self.evalNames:
            self.createFieldAndSetters(AppConsts,var)
            setattr(self, var+"LineEdit", self.addLineEdit(var))



    def fillEquationLayout(self):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("du/dt="))
        layout.addWidget(self.aLineEdit)
        layout.addWidget(QtGui.QLabel("d^2u/dx^2+"))
        layout.addWidget(self.bLineEdit)
        layout.addWidget(QtGui.QLabel("du/dx+"))
        layout.addWidget(self.cLineEdit)
        return layout


    def fillInitConditionLayout(self):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("u(x,0)="))
        layout.addWidget(self.initCondLineEdit)
        return layout


    def fillSideConditionLayout(self):
        layout = QtGui.QVBoxLayout()
        layoutLeft = QtGui.QHBoxLayout()
        layoutRight = QtGui.QHBoxLayout()

        layoutLeft.addWidget(self.alphaLineEdit)
        layoutLeft.addWidget(QtGui.QLabel("u(0,t)+"))
        layoutLeft.addWidget(self.betaLineEdit)
        layoutLeft.addWidget(QtGui.QLabel("du/dx(0,t)="))
        layoutLeft.addWidget(self.phi_0LineEdit)
        layoutRight.addWidget(self.gammaLineEdit)
        layoutRight.addWidget(QtGui.QLabel("u(l,t)+"))
        layoutRight.addWidget(self.deltaLineEdit)
        layoutRight.addWidget(QtGui.QLabel("du/dx(l,t)="))
        layoutRight.addWidget(self.phi_lLineEdit)
        layout.addItem(layoutLeft)
        layout.addItem(layoutRight)
        layout.setSpacing(50)
        return layout

    def fillSettingsLayout(self):
        layout = QtGui.QVBoxLayout()
        upperLayout = QtGui.QHBoxLayout()
        leftUpperLayout = QtGui.QFormLayout()
        rightUpperLayout = QtGui.QFormLayout()
        self.schemeComboBox = QtGui.QComboBox()
        self.approxComboBox = QtGui.QComboBox()
        self.taskNo = QtGui.QComboBox()
        self.t = QtGui.QComboBox()
        leftUpperLayout.addRow(QtGui.QLabel(u"Схема"),self.schemeComboBox)
        leftUpperLayout.addRow(QtGui.QLabel(u"Вариант"),self.taskNo)
        rightUpperLayout.addRow(QtGui.QLabel(u"Аппроксимация"),self.approxComboBox)
        rightUpperLayout.addRow(QtGui.QLabel(u"t = "),self.t)
        upperLayout.addItem(leftUpperLayout)
        upperLayout.addItem(rightUpperLayout)
        self.refreshButton = QtGui.QPushButton(u"Пересчитать")
        layout.addWidget(self.refreshButton)
        layout.addItem(upperLayout)
        upperLayout.setSpacing(50)



        return layout

    def fillGraphsLayout(self):
        layout = QtGui.QHBoxLayout()
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.getPlotItem().setXRange(AppConsts.gradX[0],AppConsts.gradX[-1])
        self.graphWidget.getPlotItem().setYRange(-1,1)
        self.graphWidget.getPlotItem().enableAutoRange(pg.ViewBox.XYAxes,False)
        self.errorWidget = pg.PlotWidget()
        leftGraphLayout = QtGui.QVBoxLayout()
        leftGraphLayout.addWidget(QtGui.QLabel(u"Графики функций"))
        leftGraphLayout.addWidget(self.graphWidget)
        rightGraphLayout = QtGui.QVBoxLayout()
        rightGraphLayout.addWidget(QtGui.QLabel(u"Погрешность"))
        rightGraphLayout.addWidget(self.errorWidget)

        layout.addItem(leftGraphLayout)
        layout.addItem(rightGraphLayout)
        return layout

    def fillLayouts(self):
        equationLayout = self.fillEquationLayout()
        initConditionLayout = self.fillInitConditionLayout()
        sideConditionLayout = self.fillSideConditionLayout()
        settingsLayout = self.fillSettingsLayout()
        graphsLayout = self.fillGraphsLayout()
        mainLayout = QtGui.QVBoxLayout()

        mainLayout.addItem(equationLayout)
        mainLayout.addItem(initConditionLayout)
        mainLayout.addItem(sideConditionLayout)
        mainLayout.addItem(settingsLayout)
        mainLayout.addItem(graphsLayout)
        mainLayout.setSpacing(10)
        self.setLayout(mainLayout)

    def refreshData(self):
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    window = Lab5MainWidget()
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()