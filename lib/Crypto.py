import urllib.request
import json
import time
import os
import requests

# Constants
COINGECKO_URL_API = "https://api.coingecko.com/api/v3"
                    #"coins/markets?vs_currency=usd&ids=litecoin"

class Crypto():
    """
    @class crypto
    @brief This class hold all functions/attributes related to crypto
    """

    def __init__(self, tickerName = "bitcoin", database = "Coingecko", tickerBase = "usd"):
        """
        @fn __init__
        @brief This function to initialize attributes for class crypto
        @param database which database the instance use to retrieve crypto data from
                        either "Coingecko", "Binance", "Coinmarketcap"
        """
        self.database = database
        self.price = None
        self.time = None
        self.volume = None
        self.marketCap = None
        self.tickerName = tickerName #Default ticker is bitcoin
        self.tickerBase = tickerBase  # Default ticker base is USD

    def setData(self,varDict):
        """
        @fn GetData
        @brief This function to set the attribute of crypto object
        @param dataType which type of data need to set
                        either "database", "tickerName", "data"
        """
        for varName, varValue in varDict.items():
            setattr(self, varName, varValue)

    def getData(self):
        """
        @fn GetData
        @brief This function to retrieve crypto data from database
        @param dataType which type of data need to retrieved
                        either "Price"
        """
        status = False
        if self.database == "Coingecko":
            res = self.getCoinGeckoData(self.tickerName, self.tickerBase)
            if res is not None:
                self.price = res[0]["current_price"]
                self.time = res[0]["last_updated"]
                self.volume = res[0]["total_volume"]
                self.marketCap = res[0]["market_cap"]
                status = True
        return status

    def displayData(self, updateData = False):
        if updateData:
            self.getData()
        print("%s : %s - Price = %.3f Volume = %d Market Cap = %d " % (self.tickerName,self.time,self.price,self.volume,self.marketCap))

    def downloadThumbNail(self,fileName = "ellipsis.png"):
        urlImg = "https://assets.coingecko.com/coins/images/14498/large/ellipsis.png"
        imgFileDest = os.path.dirname(os.path.abspath(__file__)).replace("lib", "img")
        imgFileDest = imgFileDest + "\\" + fileName
        if not os.path.exists(imgFileDest):
            r = requests.get(urlImg)
            with open(imgFileDest, 'wb') as outfile:
                outfile.write(r.content)

    def getCoinGeckoData(self, tickerName = "bitcoin", tickerBase = "usd"):
        """
        @fn GetData
        @brief This function to retrieve crypto data from coingecko database
        @param dataType which type of data need to retrieved
                        either "Price"
        """
        res = None
        url     = "%s/coins/markets?vs_currency=%s&ids=%s" % (COINGECKO_URL_API,tickerBase,tickerName)
        data    = urllib.request.urlopen(url).read()
        try:
            res     = json.loads(data)
        except:
            pass
        #[{'id': 'ellipsis', 'symbol': 'eps', 'name': 'Ellipsis',
        # 'image': 'https://assets.coingecko.com/coins/images/14498/large/ellipsis.png?1616556354',
        # 'current_price': 0.282763, 'market_cap': 149839526, 'market_cap_rank': 392, 'fully_diluted_valuation': 282726909,
        # 'total_volume': 6991856, 'high_24h': 0.285344, 'low_24h': 0.268507, 'price_change_24h': 0.01391232,
        # 'price_change_percentage_24h': 5.17473, 'market_cap_change_24h': 7484448, 'market_cap_change_percentage_24h': 5.25759,
        # 'circulating_supply': 529979711.4424247, 'total_supply': 586685462.013201, 'max_supply': 1000000000.0, 'ath': 21.39,
        # 'ath_change_percentage': -98.67825, 'ath_date': '2021-03-24T06:47:04.289Z', 'atl': 0.242789, 'atl_change_percentage': 16.47114,
        # 'atl_date': '2021-12-20T14:39:18.549Z', 'roi': None, 'last_updated': '2021-12-27T15:32:02.554Z'}]

        return res