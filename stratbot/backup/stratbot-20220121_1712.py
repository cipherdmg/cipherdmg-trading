# BEGIN COPYRIGHT
###############################################################################

###############################################################################
# END COPYRIGHT
#
###############################################################################
# @version 1.0.0
#
# @author Cipher DMG (cipherdmg@gmail.com)
#
# The stratbot.py script is a library to help with stratbot
#
#
#
# @references
#   * [Trader Workstation API](https://interactivebrokers.github.io/tws-api/index.html)
#   * [Requesting Watchlist Data](https://interactivebrokers.github.io/tws-api/md_request.html)
#   * [Historical Data Limitations](https://interactivebrokers.github.io/tws-api/historical_limitations.html)

#https://www.mssqltips.com/sqlservertip/6826/techniques-for-collecting-stock-data-with-python/

#
###############################################################################
#

from ast import For
from datetime import date
import sys
import random

from rich import print
from rich.console import Console
console = Console(record=True)


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

    tickers=[random.choice (tickers)]
    tickers=['WMG']
    #tickers = tickers_TEST
    return tickers


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

def getCandleColor(candle):
    if(isGreenCandle(candle)):
        return "green"
    else:
        return "red"
# end of getCandleColor()

def isGreenCandle(candle):
    return getOpen(candle) < getClose(candle)
# end of isGreenCandle()

def isRedCandle(candle):
    return getOpen(candle) >= getClose(candle)
# end of isRedCandle()

def isShootingStar(candle):
    openPrice=getOpen(candle)
    closePrice=getClose(candle)
    highPrice=getHigh(candle)
    lowPrice=getLow(candle)

    hc=highPrice-closePrice
    hl=highPrice-lowPrice

    if(isRedCandle(candle)):
        ratio = (highPrice - openPrice) / (openPrice-closePrice) #This will give you a ratio of the top wick compared to the body which should be
        ratioTail = (closePrice - lowPrice)/ (highPrice - openPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
        return ((ratio > 2) and (ratioTail < 0.30))
    else:
        ratio = (highPrice - closePrice) / (closePrice - openPrice) #This will give you a ratio of the top wick compared to the body which should be
        ratioTail = (openPrice - lowPrice)/ (highPrice - closePrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
        return ((ratio > 2) and (ratioTail < 0.30))

# end of isShootingStar()


#Hanging Man vs Hammer Candlestick Patterns The primary difference between the Hanging Man pattern and the Hammer Candlestick pattern is that the former is bullish and the latter is bearish. That’s because the Hanging Man appears at the top of uptrends while the Hammer appears at the bottom of downtrends.

# https://commodity.com/technical-analysis/hammer/
# The Hammer candlestick formation is viewed as a bullish reversal candlestick pattern that mainly occurs at the bottom of downtrends.
# The Hammer formation is created when the open, high, and close prices are roughly the same. Also, there is a long lower shadow that’s twice the length as the real body.
def isHammer(candle):
    openPrice=getOpen(candle)
    closePrice=getClose(candle)
    highPrice=getHigh(candle)
    lowPrice=getLow(candle)
    #return (highPrice - lowPrice > 3 * (openPrice - closePrice) and (closePrice - lowPrice) / (.001 +highPrice - lowPrice) > 0.6 and (openPrice - lowPrice) / (.001 + highPrice - lowPrice) > 0.6)
    if(isGreenCandle(candle)):
        ratio = (closePrice - lowPrice) / (closePrice-openPrice) #This will give you a ratio of the bottom wick compared to the body which should be
        ratioTip = (highPrice - closePrice)/ (openPrice - lowPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
        return ((ratio > 2) and (ratioTip < 0.30))
    else:
        ratio = (openPrice - lowPrice) / (openPrice - closePrice) #This will give you a ratio of the bottom wick compared to the body which should be
        ratioTip = (highPrice - openPrice)/ (closePrice - lowPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
        return ((ratio > 2) and (ratioTip < 0.30))

# end of isHammer()


def getTimeframe(barSize):

    if("1 secs" == barSize):
        return "1S"

    elif("5 secs" == barSize):
        return "5S"

    elif("10 secs" == barSize):
        return "10S"

    elif("15 mins" == barSize):
        return "15M"

    elif("30 mins" == barSize):
        return "30M"

    elif("60 mins" == barSize):
        return "60M"

    elif("1 hour" == barSize):
        return "60M"

    elif("4 hours" == barSize):
        return "4H"

    elif("1 day" == barSize):
        return "1D"

    elif("1 week" == barSize):
        return "1W"

    elif("1 month" == barSize):
        return "1M"

    elif("2 month" == barSize):
        return "2M"

    elif("3 month" == barSize):
        return "3M"

    elif("12 month" == barSize):
        return "12M"

    else:
        return "unknown"

# end of getTimeframe()




def getStockHistory(table,symbol ,duration="1 D", barSize="15 mins", exchange="SMART", currency="USD" ):

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

    timeframe = getTimeframe(barSize)
    stock = Stock(symbol, exchange, currency)
    #ib.qualifyContracts(stock)

    #ib.sleep needs to be called to give time for any current IB operation to complete
    ib.sleep(1)

    data = ib.reqMktData(stock)

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

        stratPattern="3,2,3"
        stratEnforced="true"
        profitTarget=2.33
        candlePattern="3,3,2,3"

        #Last Candle
        if((idx == (len(candles)-1)) and (isHammer(candle))):
            #console.print("[blue]symbol: %s [/blue] openPrice: %s closePrice: %s highPrice: %s lowPrice: %s date: %s volume: %s" % (symbol, candleOpen,candleClose, candleHigh, candleLow, str(candleDate), candleVolume ))
            table.add_row(str(symbol),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)),  candlePattern, "[bold]hammer[/bold]")

        elif((idx == (len(candles)-1)) and (isShootingStar(candle))):
            #console.print("[blue]symbol: %s [/blue] openPrice: %s closePrice: %s highPrice: %s lowPrice: %s date: %s volume: %s" % (symbol, candleOpen,candleClose, candleHigh, candleLow, str(candleDate), candleVolume ))
            table.add_row(str(symbol),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)),  candlePattern, "[bold]shooter[/bold]")
        else:
            #console.print("[blue]symbol: %s [/blue] openPrice: %s closePrice: %s highPrice: %s lowPrice: %s date: %s volume: %s" % (symbol, candleOpen,candleClose, candleHigh, candleLow, str(candleDate), candleVolume ))
            table.add_row(str(symbol),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)),  candlePattern, "[bold][/bold]")

    #print(util.df(candles))

# end of getStockHistory()

#https://interactivebrokers.github.io/tws-api/historical_limitations.html

if __name__ == "__main__":

    console.print(sys.argv)


    dailyTable = Table(title="Daily")
    dailyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    # dailyTable.add_column("Price to Change \nDaily Continuity", justify="right", style="cyan", no_wrap=False)
    # dailyTable.add_column("Price to Change \nWeekly Continuity", justify="right", style="cyan", no_wrap=False)
    # dailyTable.add_column("Price to Change \nMonthly Continuity", justify="right", style="cyan", no_wrap=False)
    dailyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    weeklyTable = Table(title="Weekly")
    weeklyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Price to Change \nWeekly Continuity", justify="right", style="cyan", no_wrap=False)
    weeklyTable.add_column("Price to Change \nMonthly Continuity", justify="right", style="cyan", no_wrap=False)
    weeklyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    monthlyTable = Table(title="Monthly")
    monthlyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Price to Change \nMonthly Continuity", justify="right", style="cyan", no_wrap=False)
    monthlyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    #Get the tickers
    tickers=getTickers()

    for ticker in tickers:
        console.print("Searching Ticker %s ..." % (ticker))
        #getStockHistory("AAPL","1 D", "15 mins")
        #getStockHistory(dailyTable, ticker,"5400 S", "15 mins") #90 Mins all together [6 Candles of 15 mins]


        # getStockHistory("AAPL","1 D","30 mins")
        # getStockHistory("AAPL","10800 S","30 mins") #180 Mins all together [6 Candles of 30 mins]


        # getStockHistory("AAPL","1 D","1 hour")
        #getStockHistory("AAPL","21600 S","1 hour") #360 Mins all together [6 Candles of 60 mins]


        getStockHistory(dailyTable, ticker,"1 W","1 day")

        #console.print("[red]AAPL Weekly 1 Month of Data [/red]")
        # getStockHistory("AAPL","1 M","1 week")

        # getStockHistory("AAPL","1 Y","1 month")

    console.print(dailyTable)


#chains = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)

#print(util.df(chains))


