from PyQt5 import QtWidgets
from Crypto import Crypto

import sys


class TestWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.clickCount = 0
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Hello")
        self.label = QtWidgets.QLabel(self)
        self.label.move(50,50)
        self.label.setText("Hello. I'm a label")
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("I'm a button")
        self.button.move(50,100)
        self.button.clicked.connect(self.clickedButton)
        self.EPS = Crypto(tickerName = "ellipsis", database = "Coingecko", tickerBase = "usd")
        self.BTC = Crypto(tickerName = "bitcoin", database = "Coingecko", tickerBase = "usd")

    def clickedButton(self):
        """
        self.clickCount = self.clickCount + 1
        if self.clickCount > 1:
            self.label.setText("Clicked %d times" % self.clickCount)
        else:
            self.label.setText("Clicked %d time" % self.clickCount)
        """
        self.EPS.GetData()
        self.label.setText("%s : %s - Price = %.3f Volume = %d Market Cap = %d " % (self.EPS.tickerName,self.EPS.time,self.EPS.price,self.EPS.volume,self.EPS.marketCap))
        self.updateGui()

    def updateGui(self):
        self.label.adjustSize()

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()