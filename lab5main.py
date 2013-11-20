# -*- coding: utf-8 -*-
from numpy.lib.function_base import blackman

__author__ = 'Antifrize'

from AppConstants import AppConsts
import sys
import sip
from PyQt4 import QtGui,QtCore,Qt
import pyqtgraph as pg
from TaskLoader import TaskLoader
from math import *
from AnalogGraphModel import *
from ImplicitGraphModel import *
from ExplicitGraphModel import *
from MixedGraphModel import *

a = AppConsts.a

class MyLineEdit(QtGui.QLineEdit):
    def focusOutEvent(self, QFocusEvent):
        # var = self.accessibleName()[:-8]
        # setter = getattr(AppConsts,"set"+str(var).capitalize())
        # setter(str(self.text()))
        pass
class Lab5MainWidget(QtGui.QWidget):
    floatNames =("a","b","Q","alpha","beta","delta","gamma","lN","sigma")
    evalNames = ("c","phi_0","phi_l","initCondition","resF")

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.setWindowTitle(u"Решение параболических дифференциальных уравнений")
        self.resize(800,600)
        self.createControls()
        self.fillLayouts()
        self.explicitGraphModel = ExplicitGraphModel()
        self.implicitGraphModel = ImplicitGraphModel()
        self.mixedGraphModel = MixedGraphModel(self.explicitGraphModel,self.implicitGraphModel,0.5)
        self.activeGraphModel = self.implicitGraphModel
        self.taskChange(0)
        self.refreshView()
        sip.setdestroyonexit(False)

    def taskChange(self,n):
        AppConsts.loadTask(TaskLoader.getTask(n))
        self.analogGraphModel = AnalogGraphModel(AppConsts.translate(AppConsts.resF))
        self.recompute()
        self.refreshView()
        self.rescale()


    def createFieldAndSetters(self,module,name):
        def setter(x):
            var = setattr(module,name,x)

        if name in self.evalNames:
            def getter(t):
                return eval(getattr(module,name))
        else:
            def getter():
                var = getattr(module,name)
                return var
        setattr(module,"set"+name.capitalize(),staticmethod(setter))
        if name!='phi_0' and name!='phi_l' and name!='c':
            setattr(module,"get"+name.capitalize(),staticmethod(getter))

    def addLineEdit(self,var):
        lineEdit = MyLineEdit()
        outer = self

        lineEdit.setAccessibleName(var+'LineEdit')
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


    def rescale(self):
        self.graphWidget.getPlotItem().setXRange(AppConsts.gradX[0],AppConsts.gradX[-1])
        self.graphWidget.getPlotItem().setYRange(min([min(x) for x in self.activeGraphModel.grid]),
                                                 max([max(x) for x in self.activeGraphModel.grid]))


    def fillInitConditionLayout(self):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("u(x,0)="))
        layout.addWidget(self.initConditionLineEdit)
        return layout


    def fillSideConditionLayout(self):
        layout = QtGui.QVBoxLayout()
        layoutLeft = QtGui.QHBoxLayout()
        layoutRight = QtGui.QHBoxLayout()

        layoutLeft.addWidget(self.alphaLineEdit)
        layoutLeft.addWidget(QtGui.QLabel("du/dx(0,t)+"))
        layoutLeft.addWidget(self.betaLineEdit)
        layoutLeft.addWidget(QtGui.QLabel("u(0,t)="))
        layoutLeft.addWidget(self.phi_0LineEdit)
        layoutRight.addWidget(self.gammaLineEdit)
        layoutRight.addWidget(QtGui.QLabel("du/dx(l,t)+"))
        layoutRight.addWidget(self.deltaLineEdit)
        layoutRight.addWidget(QtGui.QLabel("u(l,t)="))
        layoutRight.addWidget(self.phi_lLineEdit)
        layout.addItem(layoutLeft)
        layout.addItem(layoutRight)
        layout.setSpacing(50)
        return layout

    def schemeChangeEvent(self,n ):
        if n==0:
            self.activeGraphModel = self.explicitGraphModel
        if n==1:
            self.activeGraphModel = self.implicitGraphModel
        if n==2:
            self.activeGraphModel = self.mixedGraphModel

        self.replot()


    def fillSettingsLayout(self):
        layout = QtGui.QVBoxLayout()
        upperLayout = QtGui.QHBoxLayout()
        leftUpperLayout = QtGui.QFormLayout()
        rightUpperLayout = QtGui.QFormLayout()
        self.schemeComboBox = QtGui.QComboBox()
        for scheme in [u'Явная',u'Неявная',u'Смешанная']:
            self.schemeComboBox.addItem(scheme,3)
        self.schemeComboBox.setCurrentIndex(0)
        self.schemeComboBox.currentIndexChanged.connect(self.schemeChangeEvent)
        self.approxComboBox = QtGui.QComboBox()
        self.taskNo = QtGui.QComboBox()
        for i in range(1,len(TaskLoader.tasks)):
            self.taskNo.addItem(str(i),100)
        self.taskNo.setCurrentIndex(0)
        self.taskNo.currentIndexChanged.connect(self.taskChange)
        self.t = QtGui.QComboBox()
        self.t.currentIndexChanged.connect(self.replot)
        leftUpperLayout.addRow(QtGui.QLabel(u"Схема"),self.schemeComboBox)
        leftUpperLayout.addRow(QtGui.QLabel(u"Вариант"),self.taskNo)
        leftUpperLayout.addRow(QtGui.QLabel(u"h = "),self.lNLineEdit)
        rightUpperLayout.addRow(QtGui.QLabel(u"Аппроксимация"),self.approxComboBox)
        rightUpperLayout.addRow(QtGui.QLabel(u"t = "),self.t)
        rightUpperLayout.addRow(QtGui.QLabel(u"Sigma = "),self.sigmaLineEdit)
        upperLayout.addItem(leftUpperLayout)
        upperLayout.addItem(rightUpperLayout)
        self.refreshButton = QtGui.QPushButton(u"Пересчитать")
        self.refreshButton.clicked.connect(self.refreshConsts)
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
        layout.setSpacing(10)
        return layout

    def fillAnalogLayout(self):
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel('u(x,t) = '),self.resFLineEdit)
        return layout

    def fillLayouts(self):
        equationLayout = self.fillEquationLayout()
        initConditionLayout = self.fillInitConditionLayout()
        sideConditionLayout = self.fillSideConditionLayout()
        analogLayout = self.fillAnalogLayout()
        settingsLayout = self.fillSettingsLayout()
        graphsLayout = self.fillGraphsLayout()
        mainLayout = QtGui.QVBoxLayout()

        mainLayout.addItem(equationLayout)
        mainLayout.addItem(initConditionLayout)
        mainLayout.addItem(sideConditionLayout)
        mainLayout.addItem(analogLayout)
        mainLayout.addItem(settingsLayout)
        mainLayout.addItem(graphsLayout)
        mainLayout.setSpacing(10)
        self.setLayout(mainLayout)

    def refreshView(self):
        for lineEdit in self.findChildren(QtGui.QLineEdit):
            getter = getattr(AppConsts,"get"+str(lineEdit.accessibleName()[:-8]).capitalize())
            # lineEdit.setText(Qt.QString(getter()))
            lineEdit.setText(str(getattr(AppConsts,str(lineEdit.accessibleName()[:-8]))))

        self.t.clear()
        for t in AppConsts.gradT:
            self.t.insertItem(100000000,str(t))

        self.approxComboBox.clear()
        if AppConsts.alpha == 0 and AppConsts.gamma ==0:
            self.approxComboBox.addItem(u'двухточечная с первым порядком',0)
        else:
            for approx in [u'двухточечная с первым порядком',u'двухточечная со вторым порядком',u'трехточечная']:
                self.approxComboBox.addItem(approx,3)
        self.approxComboBox.setCurrentIndex(0)
        self.replot()

    def refreshConsts(self):
        for lineEdit in self.findChildren(QtGui.QLineEdit):
            setattr(AppConsts,str(lineEdit.accessibleName()[:-8]),float(lineEdit.text()) if str(lineEdit.accessibleName()[:-8]) in self.floatNames else str(lineEdit.text()))
            # print(str(lineEdit.accessibleName())+" refreshed")
        AppConsts.refresh()
        self.recompute()

    def recompute(self):
        self.implicitGraphModel.makeGrid()
        self.explicitGraphModel.remakeGrid()
        self.analogGraphModel.f = AppConsts.translate(AppConsts.resF)
        self.replot()

    def replot(self,n):
        self.replot()

    def replot(self):
        t = self.t.currentIndex()
        analogT = AppConsts.gradT[self.t.currentIndex()]
        if len(self.graphWidget.getPlotItem().listDataItems())==0:
            blackPen = pg.mkPen(color = (0,0,0,255))
            redPen = pg.mkPen(color = (255,0,0,255))
            self.graphWidget.getPlotItem().plot(AppConsts.gradX,[self.analogGraphModel.getT(x,analogT) for x in AppConsts.gradX],pen = redPen)
            self.graphWidget.getPlotItem().plot(AppConsts.gradX,[self.activeGraphModel.getT(x,t) for x in range(len(AppConsts.gradX))],pen = blackPen)
        self.graphWidget.getPlotItem().listDataItems()[0].setData(AppConsts.gradX,[self.analogGraphModel.getT(x,analogT) for x in AppConsts.gradX])
        self.graphWidget.getPlotItem().listDataItems()[1].setData(AppConsts.gradX,[self.activeGraphModel.getT(x,t) for x in range(len(AppConsts.gradX))])

        if len(self.errorWidget.getPlotItem().listDataItems())==0:
            blackPen = pg.mkPen(color = (0,0,0,255))
            self.errorWidget.getPlotItem().plot(AppConsts.gradX,[fabs(self.analogGraphModel.getT(AppConsts.gradX[x],AppConsts.gradT[t])-self.activeGraphModel.getT(x,t)) for x in range(len(AppConsts.gradX))],pen = blackPen)
        self.errorWidget.getPlotItem().listDataItems()[0].setData(AppConsts.gradX,[fabs(self.analogGraphModel.getT(AppConsts.gradX[x],AppConsts.gradT[t])-self.activeGraphModel.getT(x,t)) for x in range(len(AppConsts.gradX))])

        self.graphWidget.getPlotItem().setXRange(AppConsts.gradX[0],AppConsts.gradX[-1])
        self.update()


def main():
    app = QtGui.QApplication(sys.argv)
    window = Lab5MainWidget()
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()