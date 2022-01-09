# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cryptoAlarmUI1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Crypto import Crypto

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(685, 358)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushCrypto = QtWidgets.QPushButton(self.centralwidget)
        self.pushCrypto.setGeometry(QtCore.QRect(70, 90, 71, 61))
        self.pushCrypto.setObjectName("pushCrypto")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 90, 301, 61))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")
        self.menuEdit.addAction(self.actionAdd)
        self.menuEdit.addAction(self.actionRemove)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushCrypto.clicked.connect(self.clickedPushCrypto)
        self.EPS = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushCrypto.setText(_translate("MainWindow", "Click"))
        self.label.setText(_translate("MainWindow", ""))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))

    def clickedPushCrypto(self):
        if self.EPS is None:
            self.EPS = Crypto(tickerName="ellipsis", database="Coingecko", tickerBase="usd")
        self.EPS.GetData()
        self.label.setText("%s : %s - Price = %.3f Volume = %d Market Cap = %d " % (self.EPS.tickerName,self.EPS.time,self.EPS.price,self.EPS.volume,self.EPS.marketCap))

        self.updateGui()

    def updateGui(self):
        self.label.adjustSize()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())