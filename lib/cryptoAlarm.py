from PyQt5 import QtCore,QtWidgets,QtGui
from Crypto import Crypto
import sys

# CONSTANTS
TIMER_TIMEOUT = 1000 # in miliseconds
PRICE_UPDATE_TIMEOUT = 60 # in seconds

class cryptoAlarm(QtWidgets.QMainWindow):
    def __init__(self):
        super(cryptoAlarm, self).__init__()
        self.setupUi()
        self.connectUi()
        self.initializeUi()
        self.initializeDatabase()
        self.setupTimer()

    # UI related functions - Modified from QtDesigner ******************************************************************
    def setupUi(self):
        self.resize(471, 240)
        self.setUpCentralWidget()
        self.setUpPushCrypto() # Crypto button
        self.setUpLabelPrice() # Label display crypto price
        self.setUpTextCrypto() # Textbox key in crypto ticker
        self.setUpMenuBar()    # Set up menu bar
        self.setUpUiThreshold() # Set up UI threshold : label greater, label lesser, text greater, text lesser
        self.setUpLabelStatus() # Label status

    def setUpCentralWidget(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Crypto Alarm")

    def setUpPushCrypto(self):
        self.pushCrypto = QtWidgets.QPushButton(self.centralwidget)
        self.pushCrypto.setGeometry(50, 90, 71, 61)
        self.pushCrypto.setObjectName("pushCrypto")
        self.pushCrypto.setText("Alarm")

    def setUpLabelPrice(self):
        self.labelPrice = QtWidgets.QLabel(self.centralwidget)
        self.labelPrice.setGeometry(130, 90, 301, 61)

    def setUpTextCrypto(self):
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

    def setUpMenuBar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 471, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionAdd = QtWidgets.QAction(self)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(self)
        self.actionRemove.setObjectName("actionRemove")
        self.menuEdit.addAction(self.actionAdd)
        self.menuEdit.addAction(self.actionRemove)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuEdit.setTitle("Edit")
        self.actionAdd.setText("Add")
        self.actionRemove.setText("Remove")

    def setUpUiThreshold(self):
        # Set up textboxes
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textGreater = QtWidgets.QTextEdit(self.centralwidget)
        self.textGreater.setGeometry(QtCore.QRect(370, 90, 61, 31))
        self.textGreater.setFont(font)
        self.textGreater.setObjectName("textGreater")
        self.textGreater.setAlignment(QtCore.Qt.AlignCenter)
        self.textLesser = QtWidgets.QTextEdit(self.centralwidget)
        self.textLesser.setGeometry(QtCore.QRect(370, 120, 61, 31))
        self.textLesser.setAlignment(QtCore.Qt.AlignCenter)
        self.textLesser.setFont(font)
        self.textLesser.setObjectName("textLesser")
        # Set up labels
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelGreater = QtWidgets.QLabel(self.centralwidget)
        self.labelGreater.setGeometry(QtCore.QRect(340, 90, 21, 31))
        self.labelGreater.setFont(font)
        self.labelGreater.setObjectName("labelGreater")
        self.labelLesser = QtWidgets.QLabel(self.centralwidget)
        self.labelLesser.setGeometry(QtCore.QRect(340, 120, 21, 31))
        self.labelGreater.setText(">=")
        self.labelLesser.setFont(font)
        self.labelLesser.setObjectName("labelLesser")
        self.labelLesser.setText("<=")

    def setUpLabelStatus(self):
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setGeometry(QtCore.QRect(140, 160, 191, 31))
        self.labelStatus.setObjectName("labelStatus")

    # UI general functions ********************************************************************************************
    def connectUi(self):
        self.pushCrypto.clicked.connect(self.pushCryptoClickEvent)
        self.textCrypto.installEventFilter(self)  # Add listener for ticker texbox
        self.actionAdd.triggered.connect(self.updateDatabase)
        self.actionRemove.triggered.connect(self.removeDatabase)

    def initializeUi(self):
        self.cryptoObj = None

    def initializeDatabase(self):
        self.cryptoDatabase = {}
        self.cryptoDatabase['ticker'] = []
        self.cryptoDatabase['threshold'] = {}
        self.cryptoDatabase['price'] = {}
        self.cryptoDatabase['alarm'] = {}


    def updateGui(self):
        self.labelPrice.adjustSize()

    def writeStatus(self, message, messageType = "GENERAL"):
        # 3 types of messages. General -> Black color. Warning -> Yellow. Error -> Red
        self.labelStatus.setText(message)
        if messageType.upper() == "GENERAL":
            self.labelStatus.setStyleSheet("color : black")
        elif messageType.upper() == "WARNING":
            self.labelStatus.setStyleSheet("color : orange")
        elif messageType.upper() == "ERROR":
            self.labelStatus.setStyleSheet("color : red")

    # Timer and background task related functions **********************************************************************
    def setupTimer(self):
        # Set up clock label to display time every s
        self.labelTime = QtWidgets.QLabel(self.centralwidget)
        self.labelTime.setGeometry(QtCore.QRect(220, 20, 211, 21))
        self.labelTime.setObjectName("labelTime")
        self.labelTime.setAlignment(QtCore.Qt.AlignRight)
        # Set up timer, timeout = 1s, defined in TIMER_TIMEOUT
        self.timer = QtCore.QTimer()
        self.timer.start(TIMER_TIMEOUT)
        self.timer.timeout.connect(self.doBackgroundTasks)
        # Set up timer related variables
        self.timerCount = 0


    def doBackgroundTasks(self):
        # Update the clock
        self.updateClockLabel()
        self.timerCount = self.timerCount + 1
        # Update price every 1 min defined in PRICE_UPDATE_TIMEOUT
        if ( self.timerCount % PRICE_UPDATE_TIMEOUT == 0 ):
            self.updateCryptoDataBase()
            pass

    def updateClockLabel(self):
        time = QtCore.QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.labelTime.setText(timeDisplay)

    def updateCryptoDataBase(self):
        for tickerName in self.cryptoDatabase['ticker']:
            try:
                tempCrypto = Crypto(tickerName=tickerName, database="Coingecko", tickerBase="usd")
                tempCrypto.getData()
                self.cryptoDatabase['price'][tickerName] = tempCrypto.price
                self.cryptoDatabase['alarm'][tickerName] = [0, 0]
            except Exception as err:
                self.writeStatus("Error %s" % err, messageType = "ERROR")

        print("Price updated. %s" % self.cryptoDatabase)
        pass

    # UI Event related functions ***************************************************************************************
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.textCrypto:
            if event.key() in [QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter] and self.textCrypto.hasFocus():
                self.textCryptoEditEvent()
                return True
        return super(cryptoAlarm,self).eventFilter(source, event)

    def textCryptoEditEvent(self):
        self.updateCryptoPrice()    # Update crypto price after user finished editing crypto ticker

    def pushCryptoClickEvent(self):
        self.updateCryptoPrice()    # Update crypto price label and also related variables
        self.updateDatabase()       # UUpdate crypto database

    def menuAddClickEvent(self):
        self.updateCryptoPrice()    # Update crypto price label and also related variables
        self.updateDatabase()       # Update crypto database

    def menuRemoveClickEvent(self):
        self.removeDatabase()       # Remove ticker data in the database

    # Crypto data related functions ***********************************************************************************
    def updateCryptoPrice(self):
        doCryptoInit = False
        self.writeStatus("")
        try:
            # Get ticker name from the textbox
            tickerName = self.textCrypto.toPlainText().lower()

            if self.cryptoObj is not None:
                doCryptoInit = self.cryptoObj.tickerName != tickerName
            else:
                doCryptoInit = True

            if doCryptoInit:
                # Update crypto object
                self.cryptoObj = Crypto(tickerName=tickerName, database="Coingecko", tickerBase="usd")
                self.cryptoObj.validCrypto = True
                self.cryptoObj.upperThreshold = None
                self.cryptoObj.lowerThreshold = None
                # Download thumbnail image to img folder
                self.cryptoObj.downloadThumbNail(fileName = "%s.png" % tickerName)

            self.cryptoObj.getData()
            self.labelPrice.setText("<b>%s :</b> %s <br><b>Price :</b> %.3f<br><b>Volume :</b> %d<br><b>Market Cap :</b> %d " % (self.cryptoObj.tickerName.upper(),self.cryptoObj.time,self.cryptoObj.price,self.cryptoObj.volume,self.cryptoObj.marketCap))
            self.pushCrypto.setStyleSheet("QPushButton{ image: url(../img/%s.png); }" % tickerName)
            self.pushCrypto.setText("")

        except Exception as err:
            self.writeStatus("Error %s" % err, messageType = "ERROR")
            if self.cryptoObj is not None:
                self.cryptoObj.validCrypto = False
            pass

        self.updateGui()

    def isCryptoDataValid(self):
        isValid =   (   ( self.cryptoObj is not None )
                    and ( self.cryptoObj.validCrypto )
                    and ( self.upperThreshold is not None)
                    and ( self.lowerThreshold is not None) )
        return isValid

    def updateDatabase(self):
        self.upperThreshold, self.lowerThreshold = self.getCryptoThreshold() # Get upper and lower threshold
        # If data is valid, update database
        if self.isCryptoDataValid():
            self.cryptoDatabase['threshold'][self.cryptoObj.tickerName] = [self.upperThreshold, self.lowerThreshold]
            self.cryptoDatabase['price'][self.cryptoObj.tickerName] = self.cryptoObj.price
            self.cryptoDatabase['alarm'][self.cryptoObj.tickerName] = [0,0]

            if not self.cryptoObj.tickerName in self.cryptoDatabase['ticker']:
                self.cryptoDatabase['ticker'].append(self.cryptoObj.tickerName)

        print("Current crypto list: %s" % self.cryptoDatabase['ticker'])
        print("Current crypto dictionary: %s" % self.cryptoDatabase)

    def removeDatabase(self):
        tickerName = self.textCrypto.toPlainText().lower()
        if tickerName in self.cryptoDatabase['ticker']:
            self.cryptoDatabase['ticker'].remove(tickerName)
            del(self.cryptoDatabase['threshold'][tickerName])
            del (self.cryptoDatabase['price'][tickerName])
            del (self.cryptoDatabase['alarm'][tickerName])

        print("Current crypto list: %s" % self.cryptoDatabase['ticker'])
        print("Current crypto dictionary: %s" % self.cryptoDatabase)

    def getCryptoThreshold(self):
        upperThreshold = None
        lowerThreshold = None
        try:
            upperThreshold = float(self.textGreater.toPlainText())
            lowerThreshold = float(self.textLesser.toPlainText())
        except Exception as err:
            pass
        return (upperThreshold,lowerThreshold)

    def doCrytoPriceCheck(self):
        # This function will be run every 1min
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = cryptoAlarm()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()