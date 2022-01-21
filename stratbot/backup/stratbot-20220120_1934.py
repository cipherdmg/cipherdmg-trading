#https://www.questrade.com/api/documentation/rest-operations/
#https://github.com/willmcgugan/rich
#
# Ideas
#  - How far to take Day, Week and Month
# https://interactivebrokers.github.io/tws-api/md_request.html
#https://ib-insync.readthedocs.io/api.html
#

from ast import For
from datetime import date
import sys

from rich import print
from rich.console import Console
console = Console()

from rich.table import Table
from rich.markdown import Markdown


from ib_insync import *



ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1,readonly=True)


def getTickers():
    tickers_TEST = ["AAPL", "RBLX", "AAL", "MA", "U"]

    tickers_ETFs= ["SPY","QQQ", "DIA", "IWM", "XBI", "XHB", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLY", "XLV", "XOP", "IYT", "OIH", "IBB"]

    tickers_Auto = ["AYRO", "BLNK", "CMI", "CHPT", "F", "GM", "HMC", "LCID", "LI", "LYFT", "MVIS", "NKLA", "NIO", "RIDE", "TM", "TSLA", "UBER", "VLTA", "WKHS", "WBX", "XPEV"]
    tickers_Airlines = [ "BA", "LUB", "UAL", "DAL", "AAL", "RCL", "CCL" ]
    tickers_Biotech = ["AMN", "BNTX", "JAZZ","HUM", "MRNA", "MRK", "NVAX","PFE", "TDOC" ]
    tickers_Cannabis=["SNDL", "TLRY", "CGC", "MO", "ACB", "OGI", "AMRS", "CPMD", "HEXO"]
    tickers_Energy = ["AMRC", "ARVL", "BEP", "BEPC", "BLNK", "DQ", "DUK", "ENPH", "EVGO", "FSLR", "FCEL", "HPK", "IVAN", "ISUN", "JKS", "MAXN", "NEE", "NEP", "PPSI", "QCLN", "QS", "RUN", "RIVN", "SEDG", "SO", "SOLO", "SPWR", "SU", "VST", "VLO"  ]
    tickers_Financial = ["JPM", "MS", "BAC", "WFC", "SQ", "C", "HIG", "AXP", "DFS", "COF", "MA", "V" ]
    tickers_Gas = ["OXY", "APA", "CRL", "DVN", "EOG", "HES", "MRO", "MUR", "PXD", "WMB", "SLB","HAL", "HP", "KMI", "PSX", "CVI"]
    tickers_Gamming = ["CZR", "DKNG", "EA", "FUBO", "GENI", "GNOG", "SEAH", "LVS", "MGM", "PENN"]
    tickers_Insurance = ["AIG", "ALL"]
    tickers_Materials = ["AA", "SCCO", "TECK", "VALE"]
    tickers_Retail = ["AMZN", "BBBY", "CHWY", "COST", "DG", "DLTR", "EBAY", "ETSY", "EXPR", "GME", "GRPN", "GPS", "HD", "JD", "JACK",  "KR", "LOW", "M", "NEGG", "PVH", "PETS", "TGT", "URBN", "W", "WMT"]
    tickers_Tech = ["AAPL","ABNB","ADBE", "AFRM", "AMD","ADP","BABA","BIDU","CRM","CRWD", "CSCO", "CHKP", "COIN", "DISH", "DIS", "EXPE", "FB", "FVRR", "GOOG", "GOOGL", "IBM" , "INOD", "JNPR", "KLIC", "LSPD","MCHP", "META", "MU", "MSFT", "NFLX", "NVDA", "ORCL", "PLTR", "QCOM", "QRVO", "RBLX", "ROKU", "RNG", "SAVE", "SNPS", "SHOP", "SPOT","SMH", "SPLK", "TTD", "TWLO", "U", "Z", "ZG", "ZM", "WDAY"]

    if 'accessCode' in globals():
        tickers = tickers_TEST
    else:
        tickers = tickers_ETFs + tickers_Auto + tickers_Airlines + tickers_Biotech + tickers_Cannabis + tickers_Energy + tickers_Financial + tickers_Gas + tickers_Gamming + tickers_Insurance + tickers_Materials + tickers_Retail + tickers_Tech

    #tickers = tickers_TEST


def getHigh(candles,idx):
    return getHigh(candles[idx])

def getHigh(candle):
    return candle.high

def getLow(candles,idx):
    return getLow(candles[idx])

def getLow(candle):
    return candle.low

def getOpen(candles,idx):
    return getOpen(candles[idx])

def getOpen(candle):
    return candle.open
# end of getOpen()

def getClose(candles,idx):
    return getClose(candles[idx])
# end of getClose()

def getClose(candle):
    return candle.close
# end of getClose()

def getCandleColor(candles, idx):
    if(isGreenCandle(candles,idx)):
        return "green"
    else:
        return "red"
# end of getCandleColor()

def isGreenCandle(candles, idx):
    return getOpen(candles[idx]) < getClose(candles[idx])
# end of isGreenCandle()

def isRedCandle(candles, idx):
    return getOpen(candles[idx]) >= getClose(candles[idx])
# end of isRedCandle()

def getStockHistory(symbol , barSize="15 mins", duration="1 D", exchange="SMART", currency="USD" ):

    """
    Request historical bar data.

    This method is blocking.

    Args:
        symbol: Symbol name.
        exchange: Destination exchange.
        currency: Underlying currency.
        endDateTime: Can be set to '' to indicate the current time,
            or it can be given as a datetime.date or datetime.datetime,
            or it can be given as a string in 'yyyyMMdd HH:mm:ss' format.
            If no timezone is given then the TWS login timezone is used.
        duration: Time span of all the bars. Examples:
            '60 S', '30 D', '13 W', '6 M', '10 Y'.
        barSize: Time period of one bar. Must be one of:
            '1 secs', '5 secs', '10 secs' 15 secs', '30 secs',
            '1 min', '2 mins', '3 mins', '5 mins', '10 mins', '15 mins',
            '20 mins', '30 mins',
            '1 hour', '2 hours', '3 hours', '4 hours', '8 hours',
            '1 day', '1 week', '1 month'.
        whatToShow: Specifies the source for constructing bars.
            Must be one of:
            'TRADES', 'MIDPOINT', 'BID', 'ASK', 'BID_ASK',
            'ADJUSTED_LAST', 'HISTORICAL_VOLATILITY',
            'OPTION_IMPLIED_VOLATILITY', 'REBATE_RATE', 'FEE_RATE',
            'YIELD_BID', 'YIELD_ASK', 'YIELD_BID_ASK', 'YIELD_LAST'.
        useRTH: If True then only show data from within Regular
            Trading Hours, if False then show all data.
        formatDate: For an intraday request setting to 2 will cause
            the returned date fields to be timezone-aware
            datetime.datetime with UTC timezone, instead of local timezone
            as used by TWS.
        keepUpToDate: If True then a realtime subscription is started
            to keep the bars updated; ``endDateTime`` must be set
            empty ('') then.
        chartOptions: Unknown.
        timeout: Timeout in seconds after which to cancel the request
            and return an empty bar series. Set to ``0`` to wait
            indefinitely.
    """
    stock = Stock(symbol, exchange, currency)
    #ib.qualifyContracts(stock)

    #ib.sleep needs to be called to give time for any current IB operation to complete
    ib.sleep(1)

    Ticker data = ib.reqMktData(stock)

    ib.sleep(1)

    marketPrice = data.marketPrice()
    askPrice = data.ask
    bidPrice = data.bid
    openPrice = getOpen(data)
    closePrice = data.close
    highPrice = data.high
    lowPrice = data.low
    volume = data.volume

    console.print("[blue]symbol: %s [/blue] openPrice: %s closePrice: %s highPrice: %s lowPrice: %s volume: %s" % (symbol, openPrice,closePrice, highPrice, lowPrice, volume ))

    candles = ib.reqHistoricalData(stock, '', barSizeSetting=barSize, durationStr=duration, whatToShow='MIDPOINT', useRTH=True)

    #for candle in candles:
    for idx in range(len(candles)):
        candle = candles[idx]
        candleClose = candle.close
        candleOpen = candle.open
        candleHigh = candle.high
        candleLow = candle.low
        candleDate = candle.date
        candleVolume = candle.volume
        console.print("[blue]symbol: %s [/blue] openPrice: %s closePrice: %s highPrice: %s lowPrice: %s date: %s volume: %s" % (symbol, candleOpen,candleClose, candleHigh, candleLow, str(candleDate), candleVolume ))


    #print(util.df(candles))

# end of getStockHistory()


if __name__ == "__main__":

    print(sys.argv)

    # getStockHistory("AAPL","15 mins","1 D")

    # getStockHistory("AAPL","30 mins","1 D")

    # getStockHistory("AAPL","1 hour","1 D")

    # getStockHistory("AAPL","1 day","1 W")

    console.print("[red]AAPL Weekly 1 Month of Data [/red]")
    getStockHistory("AAPL","1 week","1 M")






#chains = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)

#print(util.df(chains))
