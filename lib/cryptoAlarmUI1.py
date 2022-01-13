# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cryptoAlarmUI1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Crypto import Crypto
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(471, 257)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushCrypto = QtWidgets.QPushButton(self.centralwidget)
        self.pushCrypto.setGeometry(QtCore.QRect(50, 90, 71, 61))
        self.pushCrypto.setObjectName("pushCrypto")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 90, 301, 61))
        self.label.setObjectName("label")
        self.textCrypto = QtWidgets.QTextEdit(self.centralwidget)
        self.textCrypto.setGeometry(QtCore.QRect(50, 40, 381, 41))
        self.textCrypto.setText("ellipsis")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textCrypto.setFont(font)
        self.textCrypto.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textCrypto.setObjectName("textCrypto")
        self.textCrypto.setAlignment(QtCore.Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 471, 21))
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
        self.cryptoObj = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushCrypto.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))

    def clickedPushCrypto(self):
        doCryptoInit = False
        # Get ticker name from the textbox
        tickerName = self.textCrypto.toPlainText().lower()

        if self.cryptoObj is not None:
            doCryptoInit = self.cryptoObj.tickerName != tickerName
        else:
            doCryptoInit = True

        if doCryptoInit:
            # Initialize crypto object if it wasn't
            self.cryptoObj = Crypto(tickerName=tickerName, database="Coingecko", tickerBase="usd")
            # Download thumbnail image to img folder
            self.cryptoObj.downloadThumbNail(fileName = "%s.png" % tickerName)


        self.cryptoObj.getData()
        self.label.setText("<b>%s :</b> %s <br><b>Price :</b> %.3f<br><b>Volume :</b> %d<br><b>Market Cap :</b> %d " % (self.cryptoObj.tickerName.upper(),self.cryptoObj.time,self.cryptoObj.price,self.cryptoObj.volume,self.cryptoObj.marketCap))
        self.pushCrypto.setStyleSheet("QPushButton{ image: url(../img/%s.png); }" % tickerName)
        self.pushCrypto.setText("")

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
