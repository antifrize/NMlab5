import math,sys

from PySide import QtGui, QtCore


from commonLib import floatRange
#from customComponents import *
import AppConstants as AppConsts
from GraphWidget import *


class Lab1MainWidget(QtGui.QWidget):


    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("LAB 1")
        self.resize(800,600)
        self.createForm()


    def onSliderMove(self,n):
        t = n/100
        self.analogGraphLt.setPointsArray([[x,self.U(x,t)] for x in self.X])

    def createForm(self):
        settingsLayout = QtGui.QHBoxLayout()
        settingsLayout.setSpacing(20)
        self.aLineEdit = QtGui.QLineEdit()
        self.aLineEdit.textChanged.connect(AppConsts.setA)
        self.aLineEdit.setText(str(AppConsts.a))
        self.bLineEdit = QtGui.QLineEdit()
        self.bLineEdit.textChanged.connect(AppConsts.setB)
        self.bLineEdit.setText(str(AppConsts.b))
        self.cLineEdit = QtGui.QLineEdit()
        self.cLineEdit.textChanged.connect(AppConsts.setC)
        self.cLineEdit.setText(str(AppConsts.c))
        self.sigmaLineEdit = QtGui.QLineEdit()
        self.sigmaLineEdit.textChanged.connect(AppConsts.setSigma)
        self.sigmaLineEdit.setText(str(AppConsts.sigma))
        self.hLineEdit = QtGui.QLineEdit()
        self.hLineEdit.textChanged.connect(AppConsts.setH)
        self.hLineEdit.setText(str(AppConsts.h))

        self.approxComboBox = QtGui.QComboBox()
        self.approxComboBox.currentIndexChanged.connect(AppConsts.setApprox)
        self.approxComboBox.addItem("Второго порядка")
        self.schemeComboBox = QtGui.QComboBox()
        self.schemeComboBox.currentIndexChanged.connect(AppConsts.setScheme)
        self.schemeComboBox.addItem("Явная")
        self.schemeComboBox.addItem("Неявная")
        self.schemeComboBox.addItem("Смешанная")

        self.qLineEdit = QtGui.QLineEdit()
        self.qLineEdit.textChanged.connect(AppConsts.setQ)
        self.qLineEdit.setText(str(AppConsts.q))

        equationLayout = QtGui.QHBoxLayout()
        equationLayout.addWidget(QtGui.QLabel("du/dt="))
        equationLayout.addWidget(self.aLineEdit)
        equationLayout.addWidget(QtGui.QLabel("d^2u/dx^2+"))
        equationLayout.addWidget(self.bLineEdit)
        equationLayout.addWidget(QtGui.QLabel("du/dx+"))
        equationLayout.addWidget(self.cLineEdit)



        constantsLayout = QtGui.QFormLayout()
        constantsLayout.addRow(QtGui.QLabel("a="),self.aLineEdit)
        constantsLayout.addRow(QtGui.QLabel("b="),self.bLineEdit)
        constantsLayout.addRow(QtGui.QLabel("h="),self.hLineEdit)
        constantsLayout.addRow(QtGui.QLabel("sigma="),self.sigmaLineEdit)

        constantsLayout2 = QtGui.QFormLayout()
        constantsLayout2.addRow(QtGui.QLabel("Аппроксимация"),self.approxComboBox)
        constantsLayout2.addRow(QtGui.QLabel("Схема"),self.schemeComboBox)
        constantsLayout2.addRow(QtGui.QLabel("Q = "),self.qLineEdit)

        constantsLayout.setSpacing(10)
        constantsLayout2.setSpacing(10)


        settingsLayout.addItem(constantsLayout)
        settingsLayout.addItem(constantsLayout2)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addItem(equationLayout)
        self.mainLayout.addItem(settingsLayout)
        self.mainLayout.addWidget(GraphWidget())
        self.setLayout(self.mainLayout)

    def onDataChanged(self):
        pass


    def paintEvent(self, event):
        QtGui.QWidget.paintEvent(self, event)
        # установим лейбл        # TODO добавить заголовки


    def readData(self):
        inputFile = open("data.in","r")

    def getExplicitResult(self):
        pass

    def getImplicitResult(self):
        pass

    def getCrankNickolsonResult(self):
        pass

    def plotResult(self):
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    window = Lab1MainWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()