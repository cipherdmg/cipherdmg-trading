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

##https://github.com/pilwon/node-yahoo-finance/blob/HEAD/docs/quote.md
#
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=summaryDetail
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=recommendationTrend
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=calendarEvents
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=financialData
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=earnings
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=upgradeDowngradeHistory
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=price
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=defaultKeyStatistics
#   https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=summaryProfile
#
# Download History
# https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=915148800&period2=1641686400&interval=1d&events=history&includeAdjustedClose=true
# https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=915148800&period2=1641686400&interval=1wk&events=history&includeAdjustedClose=true
# https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=915148800&period2=1641686400&interval=1mo&events=history&includeAdjustedClose=true

#https://www.mssqltips.com/sqlservertip/6826/techniques-for-collecting-stock-data-with-python/

#
###############################################################################
#

from ast import For
from datetime import date
import sys
import random
import time
import logging

from rich import print
from rich.console import Console

logging.basicConfig(level=logging.DEBUG)


def getTickers():
    tickers_TEST = ["RBLX","SPY","QQQ"]

    tickers_ETFs= ["SPY","QQQ", "DIA", "IWM", "XBI", "XHB", "XLB", "XLC", "XLF", "XLI", "XLK", "XLRE", "XLU", "XLY", "XLV", "IYT", "OIH", "IBB"]

    tickers_Auto = ["AYRO", "CMI", "CHPT", "F", "GM", "HMC", "LCID", "LI", "LYFT", "MVIS", "NKLA", "NIO", "RIDE", "TM", "TSLA", "UBER", "VLTA", "WKHS", "WBX", "XPEV"]
    tickers_Airlines = [ "BA", "LUB", "UAL", "DAL", "AAL", "RCL", "CCL" ]
    tickers_Biotech = ["AMN", "BNTX", "JAZZ","HUM", "MRNA", "MRK", "NVAX","PFE", "TDOC" ]
    tickers_Cannabis=["SNDL", "TLRY", "CGC", "ACB", "OGI", "AMRS", "CPMD", "HEXO"]
    tickers_Consumer_Staples=["XLP","PG","COST","PEP","KO","PM","MDLZ","WMT","MO","EL","CL"]
    tickers_Energy = ["AMRC", "ARVL", "BEP", "BEPC", "BLNK", "DQ", "DUK", "ENPH", "EVGO", "FSLR", "FCEL", "HPK", "IVAN", "ISUN", "JKS", "MAXN", "NEE", "NEP", "PPSI", "QCLN", "QS", "RUN", "RIVN", "SEDG", "SO", "SOLO", "SPWR", "SU", "VST", "VLO"  ]
    tickers_Financial = ["JPM", "MS", "BAC", "WFC", "SQ", "C", "HIG", "AXP", "DFS", "COF", "MA", "V" ]
    tickers_XLE=["XLE","APA","BKR","BEP","CHPT","CVI", "CRL", "COP","COO","CVX","DVN","DUK","EOG","FAN","FTI","FCEL","FSLR","HAL","HES","HFC","HP","KMB","KMI","MCP","MAXN","NEE","NOV","OKE","OXY","PSX","PXD","PLUG","SLB","SPWR","SOLO","SU","VLCN","VLO","XOM","WMB","WM"]
    tickers_Oil=["XOP","AR","CPE","CLR","EQT","FTXN","LBRT","MGY","MUR","MRO","NRT","ROCC","SOI"]
    tickers_Gamming = ["CZR", "DKNG", "EA", "FUBO", "GENI", "GNOG", "SEAH", "LVS", "MGM", "PENN"]
    tickers_Insurance = ["AIG", "ALL"]
    tickers_Materials = ["AA", "SCCO", "TECK", "VALE"]
    tickers_Retail = ["AMZN", "BBBY", "CHWY", "DG", "DLTR", "EBAY", "ETSY", "EXPR", "GME", "GRPN", "GPS", "HD", "JD", "JACK",  "KR", "LOW", "M", "NEGG", "PVH", "PETS", "TGT", "URBN", "W", "WMT"]
    tickers_Tech = ["AAPL","ABNB","ADBE", "AFRM", "AMD","ADP","BABA","BIDU","CRM","CRWD", "CSCO", "CHKP", "COIN", "DISH", "DIS", "EXPE", "FB", "FVRR", "GOOG", "GOOGL", "IBM" , "INOD", "JNPR", "KLIC", "LSPD","MCHP", "META", "MU", "MSFT", "NFLX", "NVDA", "ORCL", "PLTR", "QCOM", "QRVO", "RBLX", "ROKU", "RNG", "SAVE", "SNPS", "SHOP", "SPOT","SMH", "SPLK", "TTD", "TWLO", "U", "Z", "ZG", "ZM", "WDAY"]

    tickers = tickers_ETFs + tickers_Auto + tickers_Airlines + tickers_Biotech + tickers_Cannabis + tickers_Consumer_Staples + tickers_Energy + tickers_Financial + tickers_XLE + tickers_Oil + tickers_Gamming + tickers_Insurance + tickers_Materials + tickers_Retail + tickers_Tech


    tickers = tickers_TEST
    # tickers=[random.choice (tickers)]
    # tickers=['WMG']
    # tickers = tickers_TEST
    #tickers=['ABNB']
    tickers.sort()
    return tickers


#Candle
class Candle:
    def __init__(self, symbol, open, close, high, low, date, volume):
        self.symbol = symbol
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.date = date
        self.volume = volume

    # end of __init__()

    def getCandleColor(self):
        if(self.isGreenCandle()):
            return "green"
        else:
            return "red"
    # end of getCandleColor()

    def isGreenCandle(self):
        return self.open < self.close
    # end of isGreenCandle()

    def isRedCandle(self):
        return self.open >= self.close
    # end of isRedCandle()


#     def __str__(self):
#         return "

#    # end of __str__()

#     def __repr__(self):
#         return

#     # end of __repr__()
# end of Candle

#Candle
class StratSetup:
    def __init__(self, symbol, timeframe, setup, inForce, profit, lastFiveCandles, candlePattern):
        self.symbol = symbol
        self.timeframe = timeframe
        self.setup = setup
        self.inForce = inForce
        self.profit = profit
        self.lastFiveCandles = lastFiveCandles
        self.candlePattern = candlePattern
    # end of __init__()

# end of StratSetup


def getStratNumber(candles,idx):

    candleColor = candles[idx].getCandleColor()

    if(isInsideCandle(candles,idx)):
        return "[" + candleColor + "]" + "1" + "[/" + candleColor + "]"

    elif(isOutsideCandle(candles,idx)):
        return "[" + candleColor + "]" + "3" + "[/" + candleColor + "]"

    elif(isTwoDownCandle(candles,idx)):
        return "[" + candleColor + "]" + "2D" + "[/" + candleColor + "]"

    elif(isTwoUpCandle(candles,idx)):
        return "[" + candleColor + "]" + "2U" + "[/" + candleColor + "]"

    else:
        return "Not Possible"
# end of getStratNumber()

def isInsideCandle(candles,idx):

    previousHigh=candles[idx-1].high
    high=candles[idx].high
    previousLow=candles[idx-1].low
    low=candles[idx].low
    return high <= previousHigh and low >= previousLow
# end of isInsideCandle()

def isOutsideCandle(candles,idx):
    previousHigh=candles[idx-1].high
    high=candles[idx].high
    previousLow=candles[idx-1].low
    low=candles[idx].low
    return high > previousHigh and low < previousLow
# end of isOutsideCandle()

def isTwoDownCandle(candles,idx):
    previousHigh=candles[idx-1].high
    high=candles[idx].high
    previousLow=candles[idx-1].low
    low=candles[idx].low
    return low < previousLow and not (high > previousHigh)
# end of isTwoDownCandle()

def isTwoUpCandle(candles,idx):
    previousHigh=candles[idx-1].high
    high=candles[idx].high
    previousLow=candles[idx-1].low
    low=candles[idx].low
    return high > previousHigh and not (low < previousLow)
# end of isTwoUpCandle()


def isShootingStar(candle):
    openPrice=candle.open
    closePrice=candle.close
    highPrice=candle.high
    lowPrice=candle.low

    hc=highPrice-closePrice
    hl=highPrice-lowPrice

    if(candle.isRedCandle()):
        try:
            ratio = (highPrice - openPrice) / (openPrice-closePrice) #This will give you a ratio of the top wick compared to the body which should be
            ratioTail = (closePrice - lowPrice) / (highPrice - openPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
            return ((ratio > 2) and (ratioTail < 0.30))
        except:
            False

    else:
        try:
            ratio = (highPrice - closePrice) / (closePrice - openPrice) #This will give you a ratio of the top wick compared to the body which should be
            ratioTail = (openPrice - lowPrice)/ (highPrice - closePrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
            return ((ratio > 2) and (ratioTail < 0.30))
        except:
            False


# end of isShootingStar()


#Hanging Man vs Hammer Candlestick Patterns The primary difference between the Hanging Man pattern and the Hammer Candlestick pattern is that the former is bullish and the latter is bearish. That’s because the Hanging Man appears at the top of uptrends while the Hammer appears at the bottom of downtrends.

# https://commodity.com/technical-analysis/hammer/
# The Hammer candlestick formation is viewed as a bullish reversal candlestick pattern that mainly occurs at the bottom of downtrends.
# The Hammer formation is created when the open, high, and close prices are roughly the same. Also, there is a long lower shadow that’s twice the length as the real body.
def isHammer(candle):
    openPrice=candle.open
    closePrice=candle.close
    highPrice=candle.high
    lowPrice=candle.low
    #return (highPrice - lowPrice > 3 * (openPrice - closePrice) and (closePrice - lowPrice) / (.001 +highPrice - lowPrice) > 0.6 and (openPrice - lowPrice) / (.001 + highPrice - lowPrice) > 0.6)
    if(candle.isGreenCandle()):
        try:
            ratio = (closePrice - lowPrice) / (closePrice-openPrice) #This will give you a ratio of the bottom wick compared to the body which should be
            ratioTip = (highPrice - closePrice)/ (openPrice - lowPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
            return ((ratio > 2) and (ratioTip < 0.30))
        except ZeroDivisionError:
            False
    else:
        try:
            ratio = (openPrice - lowPrice) / (openPrice - closePrice) #This will give you a ratio of the bottom wick compared to the body which should be
            ratioTip = (highPrice - openPrice)/ (closePrice - lowPrice) #This will compare the upper wick to the lower wick and the comparison should be less then .25 or even .15
            return ((ratio > 2) and (ratioTip < 0.30))
        except ZeroDivisionError:
            False

# end of isHammer()


def determineStratSetup(symbol,candles,timeframe,isLastCandleActive) -> StratSetup:

    #We need to determine if we are doing realtime scans or anticipation scans

    #Determine if the next candle came out then would a reversal occur
    fithLastCandle = getStratNumber(candles,len(candles)-5)
    fourthLastCandle = getStratNumber(candles,len(candles)-4)
    thirdLastCandle = getStratNumber(candles,len(candles)-3)
    secondLastCandle = getStratNumber(candles,len(candles)-2)
    lastCandle = getStratNumber(candles,len(candles)-1)
    lastCandlePattern="[bold][/bold]"

    thirdLastCandleLow = candles[len(candles)-3].low
    secondLastCandleLow = candles[len(candles)-2].low
    lastCandleLow = candles[len(candles)-1].low

    thirdLastCandleHigh = candles[len(candles)-3].high
    secondLastCandleHigh = candles[len(candles)-2].high
    lastCandleHigh = candles[len(candles)-1].high

    if(isHammer(candles[len(candles)-1])):
        lastCandlePattern="[bold]hammer[/bold]"

    elif(isShootingStar(candles[len(candles)-1])):
        lastCandlePattern="[bold]shooter[/bold]"

    candlePattern = fithLastCandle + "," + fourthLastCandle + "," + thirdLastCandle + "," + secondLastCandle + "," + lastCandle

    # 2-1-2 Bearish Reversal Enforced
    if((isLastCandleActive) and "2U" in thirdLastCandle and "1" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"


    # 2-1-2 Bearish Reversal Not Enforced
    elif((isLastCandleActive) and "2U" in thirdLastCandle and "1" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"

        isInForce="false"

    # 2-1-2 Bearish Reversal Anticipate The Next Setup
    elif((not isLastCandleActive) and "2U" in secondLastCandle and "1" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"

        isInForce="false"





    # 2-1-2 Bullish Reversal Enforced
    elif((isLastCandleActive) and "2D" in thirdLastCandle and "1" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 2-1-2 Bullish Reversal Not Enforced
    elif((isLastCandleActive) and "2D" in thirdLastCandle and "1" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + ",[green]2U[/green]"
        isInForce="false"

    # 2-1-2 Bullish Reversal Anticipate The Next Setup
    elif((not isLastCandleActive) and "2D" in secondLastCandle and "1" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        isInForce="false"





    # 3-2-2 Bearish Reversal Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "2U" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 3-2-2 Bearish Reversal Not Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "2U" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"
        isInForce="false"

    # 3-2-2 Bearish Reversal Anticipate The Next Setup
    elif((not isLastCandleActive) and "3" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - lastCandleLow
        stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
        isInForce="false"




    # 3-2-2 Bullish Reversal Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "2D" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 3-2-2 Bullish Reversal Not Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "2D" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + ",[green]2U[/green]"
        isInForce="false"

    # 3-2-2 Bullish Reversal Anticipate The Next Setup
    elif((not isLastCandleActive) and "3" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        isInForce="false"







    # 3-1-2 Bearish Reversal Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "1" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 3-1-2 Bullish Reversal Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "1" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 3-1-2 Bearish Reversal Not Enforced
    elif((isLastCandleActive) and "3" in thirdLastCandle and "1" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[green]2D/2U[/green]"
        isInForce="false"

    # 3-1-2 Bearish Reversal Anticipate The Next Setup
    elif((not isLastCandleActive) and "3" in secondLastCandle and "1" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2D/2U[/green]"
        isInForce="false"








    # 1-2-2 Bearish Rev Strat Enforced
    elif((isLastCandleActive) and "1" in thirdLastCandle and "2U" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 1-2-2 Bearish Rev Strat Not Enforced
    elif((isLastCandleActive) and "1" in thirdLastCandle and "2U" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"
        isInForce="false"

    # 1-2-2 Bearish Rev Strat Anticipate The Next Setup
    elif((not isLastCandleActive) and "1" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
        isInForce="false"








    # 1-2-2 Bullish Rev Strat Enforced
    elif((isLastCandleActive) and "1" in thirdLastCandle and "2D" in secondLastCandle and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
        isInForce="true"

    # 1-2-2 Bullish Rev Strat Not Enforced
    elif((isLastCandleActive) and "1" in thirdLastCandle and "2D" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[green]2U[/green]"
        isInForce="false"

    # 1-2-2 Bullish Rev Strat Anticipate The Next Setup
    elif((not isLastCandleActive) and "1" in secondLastCandle and "2D" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        isInForce="false"



    #These are just 2-2 reversals left.
    #Just ignore 2U-2U continuations
    elif ((isLastCandleActive) and "2U" in lastCandle and "2U" in secondLastCandle):
        profitTarget = 0.00
        stratPattern =  None
        isInForce=None

    #2-2 Bearish Reversal Enforced
    #For quick reversal on the 2s make sure that its been running for a little bit
    #elif ("2D" in lastCandle and "2U" in secondLastCandle and "2D" not in thirdLastCandle):
    elif ((isLastCandleActive) and "2D" in lastCandle and "2U" in secondLastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern = secondLastCandle + "," + lastCandle
        isInForce="true"

    #2-2 Bearish Reversal Not Enforced
    #For quick reversal on the 2s make sure that its been running for a little bit
    #Also check that we don't already have a 2U on the last candle otherwise it would go 3
    #elif ("2U" in secondLastCandle and "2D" not in thirdLastCandle):
    elif ((isLastCandleActive) and "2U" in secondLastCandle and "2U" not in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleLow - thirdLastCandleLow
        stratPattern =  secondLastCandle + ",[red]2D[/red]"
        isInForce="false"

    #2-2 Bearish Reversal Anticipate The Next Setup
    #For quick reversal on the 2s make sure that its been running for a little bit
    #elif ("2U" in secondLastCandle and "2D" not in thirdLastCandle):
    elif ((not isLastCandleActive) and "2U" in lastCandle):

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  lastCandle + ",[red]2D[/red]"
        isInForce="false"




    # 2-2 Bullish Reversal Enforced
    #Just ignore 2D-2D continuations
    elif ((isLastCandleActive) and "2D" in lastCandle and "2D" in secondLastCandle):
        profitTarget = 0.00
        stratPattern =  None
        isInForce=None

    # 2-2 Bullish Reversal Enforced
    #elif ("2U" in lastCandle and "2D" in secondLastCandle and "2U" not in thirdLastCandle):
    elif ((isLastCandleActive) and "2U" in lastCandle and "2D" in secondLastCandle):
        #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern = secondLastCandle + "," + lastCandle
        isInForce="true"

    # 2-2 Bullish Reversal Not Enforced
    #elif ("2D" in secondLastCandle and "2U" not in thirdLastCandle):
    #Also check that we don't already have a 2D on the last candle otherwise it would go 3
    elif ((isLastCandleActive) and "2D" in secondLastCandle and lastCandle not in "2D"):
        #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = thirdLastCandleHigh - secondLastCandleHigh
        stratPattern =  secondLastCandle + ",[green]2U[/green]"
        isInForce="false"

    # 2-2 Bullish Reversal Anticipate The Next Setup
    #elif ("2D" in secondLastCandle and "2U" not in thirdLastCandle):
    elif ((not isLastCandleActive) and "2D" in lastCandle):
        #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern =  lastCandle + ",[green]2U[/green]"
        isInForce="false"



    else:
        profitTarget = 0.00
        stratPattern =  None
        isInForce=None

    if(isInForce is None):
        return None
    else:
        return StratSetup(str(symbol),str(timeframe), stratPattern ,isInForce, profitTarget,  candlePattern, lastCandlePattern)

# end of getStratSetup()
