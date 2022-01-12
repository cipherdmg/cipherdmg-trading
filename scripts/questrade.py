#https://www.questrade.com/api/documentation/rest-operations/
#https://github.com/willmcgugan/rich
#
# Ideas
#  - How far to take Day, Week and Month
#

from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from datetime import datetime, timedelta
import os
import sys

from qtrade import Questrade

#accessCode = ""

fridayDate = datetime(int(2022), int(1), 7)


#https://www.questrade.com/api/documentation/rest-operations

#https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=


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

    tickers.sort()
    return tickers

def getHigh(candles,idx):
    return getHigh(candles[idx])

def getHigh(candle):
    return candle['high']

def getLow(candles,idx):
    return getLow(candles[idx])

def getLow(candle):
    return candle['low']

def getOpen(candles,idx):
    return getOpen(candles[idx])

def getOpen(candle):
    return candle['open']

def getClose(candles,idx):
    return getClose(candles[idx])

def getClose(candle):
    return candle['close']


def isShootingStar(ticker,nextTicker):
    openPrice=getOpen(ticker)
    closePrice=getClose(ticker)
    highPrice=getHigh(ticker)
    lowPrice=getLow(ticker)

    nextOpenPrice=getOpen(nextTicker)
    nextClosePrice=getClose(nextTicker)
    nextHighPrice=getHigh(nextTicker)
    nextLowPrice=getLow(nextTicker)

    return (nextOpenPrice < nextClosePrice and openPrice > nextClosePrice and highPrice - max(openPrice, closePrice) >= abs(openPrice - closePrice) * 3 and min(closePrice, openPrice) - lowPrice <= abs(openPrice - closePrice))

#Hanging Man vs Hammer Candlestick Patterns The primary difference between the Hanging Man pattern and the Hammer Candlestick pattern is that the former is bullish and the latter is bearish. That’s because the Hanging Man appears at the top of uptrends while the Hammer appears at the bottom of downtrends.

# https://commodity.com/technical-analysis/hammer/
# The Hammer candlestick formation is viewed as a bullish reversal candlestick pattern that mainly occurs at the bottom of downtrends.
# The Hammer formation is created when the open, high, and close prices are roughly the same. Also, there is a long lower shadow that’s twice the length as the real body.
def isHammer(ticker):
    openPrice=getOpen(ticker)
    closePrice=getClose(ticker)
    highPrice=getHigh(ticker)
    lowPrice=getLow(ticker)
    return (highPrice - lowPrice > 3 * (openPrice - closePrice) and (closePrice - lowPrice) / (.001 +highPrice - lowPrice) > 0.6 and (openPrice - lowPrice) / (.001 + highPrice - lowPrice) > 0.6)


def takeTimeFrameAmount(ticker):
    openPrice=getOpen(ticker)
    closePrice=getClose(ticker)

    # percentChange = (closePrice - openPrice) / openPrice * 100.0
    # return percentChange
    takeTimeframe = (closePrice - openPrice)

    takeTimeframeStr="[green]$" +  str(round(takeTimeframe, 2)) + "[/green]"

    if(str(takeTimeframe).startswith("-")):
        takeTimeframeStr="[red]$" +  str(round(takeTimeframe, 2)) + "[/red]"

    return takeTimeframeStr

# def isPriceMoveMatchThreshold(table,ticker,lastStartDateTimeString,timeframe,stratPattern, profitTarget, tickers):

def addTickerToTable(table,ticker,timeframe,stratPattern,enforced, candlePattern, profitTarget, tickers,takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage):
    if(profitTarget >= 2.00):

        lastHammer = isHammer(tickers[len(tickers)-1])
        lastShooter = isShootingStar(tickers[len(tickers)-2],tickers[len(tickers)-1])
        stratEnforced = ""
        if(enforced==True):
            stratEnforced = "[blue]Enforced[/blue]"

        if(timeframe == "1D"):

            if(lastHammer):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage,candlePattern, "[bold]hammer[/bold]")
            elif(lastShooter):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)),  takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage, candlePattern, "[bold]shooter[/bold]")
            else:
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)),  takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage, candlePattern, "")
        elif(timeframe == "1W"):
            if(lastHammer):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeWeeklyPercentage,takeMonthlyPercentage, candlePattern, "[bold]hammer[/bold]")
            elif(lastShooter):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeWeeklyPercentage,takeMonthlyPercentage, candlePattern, "[bold]shooter[/bold]")
            else:
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeWeeklyPercentage,takeMonthlyPercentage, candlePattern, "")
        elif(timeframe == "1M"):
            if(lastHammer):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeMonthlyPercentage, candlePattern, "[bold]hammer[/bold]")
            elif(lastShooter):
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeMonthlyPercentage, candlePattern, "[bold]shooter[/bold]")
            else:
                table.add_row(str(ticker),str(timeframe), stratPattern ,stratEnforced, "$" + str(round(profitTarget, 2)), takeMonthlyPercentage, candlePattern, "")

def getStratNumber(candles,idx):

    candleColor = getCandleColor(candles,idx)

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


def isInsideCandle(candles,idx):

    previousHigh=getHigh(candles[idx-1])
    high=getHigh(candles[idx])
    previousLow=getLow(candles[idx-1])
    low=getLow(candles[idx])
    return high <= previousHigh and low >= previousLow


def isOutsideCandle(candles,idx):
    previousHigh=getHigh(candles[idx-1])
    high=getHigh(candles[idx])
    previousLow=getLow(candles[idx-1])
    low=getLow(candles[idx])
    return high > previousHigh and low < previousLow

def isTwoDownCandle(candles,idx):
    previousHigh=getHigh(candles[idx-1])
    high=getHigh(candles[idx])
    previousLow=getLow(candles[idx-1])
    low=getLow(candles[idx])
    return low < previousLow and not (high > previousHigh)


def isTwoUpCandle(candles,idx):
    previousHigh=getHigh(candles[idx-1])
    high=getHigh(candles[idx])
    previousLow=getLow(candles[idx-1])
    low=getLow(candles[idx])
    return high > previousHigh and not (low < previousLow)

def getCandleColor(candles, idx):
    if(isGreenCandle(candles,idx)):
        return "green"
    else:
        return "red"

def isGreenCandle(candles, idx):
    return getOpen(candles[idx]) < getClose(candles[idx])

def isRedCandle(candles, idx):
    return getOpen(candles[idx]) >= getClose(candles[idx])

#NOTE: If isRealtime is True then the last candle is still in play otherwise the last candle is closed and we should anticipate the next move
def stratBotTimeframe(table,timeframeShortForm, tickers, ticker,takeDailyAmount,takeWeeklyAmount,takeMonthlyAmount, isRealtime):

    tickers_length=len(tickers)
    #We have to take into considerations new IPO stocks so we have to have at least 6 candles
    if(tickers_length <= 5):
        return

    #ticker_candles = qtrade.get_historical_data(ticker, fourthLastSundayDate, todaysDate, timeframe)
    #ticker_candles = qtrade.get_historical_data(ticker, '2021-12-30', '2022-01-05', timeframes[index])
    lastClose = getClose(tickers[tickers_length-1])

    lastStartDateString = tickers[tickers_length-1]['start']
    lastEndDateString = tickers[tickers_length-1]['end']

    lastStartDate = datetime.fromisoformat(lastStartDateString)
    # testDate = datetime.strptime("2015-02-24T13:00:00-08:00", '%Y-%m-%dT%H:%M:%S%Z')
    #testDate = datetime.strptime("2015-02-24T13:00:00-08:00", "%Y-%B-%dT%H:%M:%S-%H:%M").date()
    lastStartDateTimeString=lastStartDate.strftime("%Y-%m-%d %H:%M:%S")

    thirdLastCandleLow = tickers[tickers_length-3]['low']
    secondLastCandleLow = tickers[tickers_length-2]['low']
    lastCandleLow = tickers[tickers_length-1]['low']

    thirdLastCandleHigh = tickers[tickers_length-3]['high']
    secondLastCandleHigh = tickers[tickers_length-2]['high']
    lastCandleHigh = tickers[tickers_length-1]['high']

    sixthLastCandle = getStratNumber(tickers,tickers_length-6)
    fithLastCandle = getStratNumber(tickers,tickers_length-5)
    fourthLastCandle = getStratNumber(tickers,tickers_length-4)
    thirdLastCandle = getStratNumber(tickers,tickers_length-3)
    secondLastCandle = getStratNumber(tickers,tickers_length-2)
    lastCandle = getStratNumber(tickers,tickers_length-1)

    #Last
    candlePattern = sixthLastCandle + "," + fithLastCandle + "," + fourthLastCandle + "," + thirdLastCandle + "," + secondLastCandle + "," + lastCandle

    #If the last candle is in realtime then don't anticipate the next move, use the existing candles to determine the next move
    if(isRealtime == True):
        #Determine if the next candle came out then would a reversal occur

        # 2-1-2 Bearish Reversal Enforced
        if("2U" in thirdLastCandle and "1" in secondLastCandle and "2D" in lastCandle):
            #print("2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle

            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-1-2 Bearish Reversal Not Enforced
        if("2U" in thirdLastCandle and "1" in secondLastCandle):
            #print("2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"

            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-1-2 Bullish Reversal Enforced
        elif("2D" in thirdLastCandle and "1" in secondLastCandle and "2U" in lastCandle):
            #print("2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-1-2 Bullish Reversal Not Enforced
        elif("2D" in thirdLastCandle and "1" in secondLastCandle):
            #print("2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bearish Reversal Enforced
        elif("3" in thirdLastCandle and "2U" in secondLastCandle and "2D" in lastCandle):
            #print("3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bearish Reversal Not Enforced
        elif("3" in thirdLastCandle and "2U" in secondLastCandle):
            #print("3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bullish Reversal Enforced
        elif("3" in thirdLastCandle and "2D" in secondLastCandle and "2U" in lastCandle):
            #print("3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bullish Reversal Not Enforced
        elif("3" in thirdLastCandle and "2D" in secondLastCandle):
            #print("3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-1-2 Bearish Reversal Enforced
        elif("3" in thirdLastCandle and "1" in secondLastCandle and "2D" in lastCandle):
            #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-1-2 Bullish Reversal Enforced
        elif("3" in thirdLastCandle and "1" in secondLastCandle and "2U" in lastCandle):
            #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-1-2 Bearish Reversal Not Enforced
        elif("3" in thirdLastCandle and "1" in secondLastCandle):
            #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[green]2D/2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 1-2-2 Bearish Rev Strat Enforced
        elif("1" in thirdLastCandle and "2U" in secondLastCandle and "2D" in lastCandle):
            #print("1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 1-2-2 Bearish Rev Strat Not Enforced
        elif("1" in thirdLastCandle and "2U" in secondLastCandle):
            #print("1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 1-2-2 Bullish Rev Strat Enforced
        elif("1" in thirdLastCandle and "2D" in secondLastCandle and "2U" in lastCandle):
            #print("1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = thirdLastCandle + "," + secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 1-2-2 Bullish Rev Strat Not Enforced
        elif("1" in thirdLastCandle and "2D" in secondLastCandle):
            #print("1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern =  thirdLastCandle + "," + secondLastCandle + ",[green]2D[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        #2-2 Bearish Reversal Enforced
        #For quick reversal on the 2s make sure that its been running for a little bit
        #elif (lastCandle == "2U" and secondLastCandle != "2D" and thirdLastCandle != "2D"):
        elif ("2D" in lastCandle and "2U" in secondLastCandle and "2D" not in thirdLastCandle):
            #print("2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern = secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        #2-2 Bearish Reversal Not Enforced
        #For quick reversal on the 2s make sure that its been running for a little bit
        #elif (lastCandle == "2U" and secondLastCandle != "2D" and thirdLastCandle != "2D"):
        elif ("2U" in secondLastCandle and "2D" not in thirdLastCandle):
            #print("2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleLow - thirdLastCandleLow
            stratPattern =  secondLastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-2 Bullish Reversal Enforced
        #elif (lastCandle == "2D" and secondLastCandle != "2U" and thirdLastCandle != "2U"):
        elif ("2U" in lastCandle and "2D" in secondLastCandle and "2U" not in thirdLastCandle):
            #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern = secondLastCandle + "," + lastCandle
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,True, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-2 Bullish Reversal Enforced
        #elif (lastCandle == "2D" and secondLastCandle != "2U" and thirdLastCandle != "2U"):
        elif ("2D" in secondLastCandle and "2U" not in thirdLastCandle):
            #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = thirdLastCandleHigh - secondLastCandleHigh
            stratPattern =  secondLastCandle + ",[green]2D[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        #table.add_row(str(ticker), str(timeframeShortForm), thirdLastCandle + "," + secondLastCandle + "," + lastCandle , str(lastClose), getCandleColor(tickers,len(ticker_candles)-1))


    else:
        #Determine if the next candle came out then would a reversal occur

        # 2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)
        if("2U" in secondLastCandle and "1" in lastCandle):
            #print("2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"

            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
        elif("2D" in secondLastCandle and "1" in lastCandle):
            #print("2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)
        elif("3" in secondLastCandle and "2U" in lastCandle):
            #print("3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)
        elif("3" in secondLastCandle and "2D" in lastCandle):
            #print("3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)
        elif("3" in secondLastCandle and "1" in lastCandle):
            #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2D/2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 3-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be 2 Up)

        # 1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)
        elif("1" in secondLastCandle and "2U" in lastCandle):
            #print("1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            stratPattern =  secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)
        elif("1" in secondLastCandle and "2D" in lastCandle):
            #print("1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        #2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)
        #For quick reversal on the 2s make sure that its been running for a little bit
        #elif (lastCandle == "2U" and secondLastCandle != "2D" and thirdLastCandle != "2D"):
        elif ("2U" in lastCandle and "2D" not in secondLastCandle):
            #print("2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            stratPattern =  lastCandle + ",[red]2D[/red]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        # 2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
        #elif (lastCandle == "2D" and secondLastCandle != "2U" and thirdLastCandle != "2U"):
        elif ("2D" in lastCandle and "2U" not in secondLastCandle):
            #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")
            #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            stratPattern =  lastCandle + ",[green]2U[/green]"
            addTickerToTable(table, ticker,timeframeShortForm,stratPattern,False, candlePattern, profitTarget, tickers, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount)

        #table.add_row(str(ticker), str(timeframeShortForm), thirdLastCandle + "," + secondLastCandle + "," + lastCandle , str(lastClose), getCandleColor(tickers,len(ticker_candles)-1))



def stratBot():

    console = Console(record=True)

    dailyTable = Table(title="Daily")
    dailyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Day", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Week", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    weeklyTable = Table(title="Weekly")
    weeklyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Week", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    monthlyTable = Table(title="Monthly")
    monthlyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Last 6 Candles", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    tickers=getTickers()
    for ticker in tickers:
        #print("Searching Ticker: %s" % (ticker))

        today = datetime.today()
        todaysDate = today.strftime('%Y-%m-%d')

        # sat_offset = (today.weekday() - 5) % 7
        # saturday = today - timedelta(days=sat_offset)
        # print("Last Saturday was on", saturday)

        sun_offset = (today.weekday() - 6) % 7
        lastSunday = today - timedelta(days=sun_offset)
        #print("Last Sunday was on", lastSunday)

        secondLastSunday = (lastSunday - timedelta(days=7))
        #print("Second Last Sunday was on", secondLastSunday)
        thirdLastSunday = (secondLastSunday - timedelta(days=7))
        #print("Third Last Sunday was on", thirdLastSunday)
        fourthLastSunday = (thirdLastSunday - timedelta(days=7))
        #print("Fourth Last Sunday was on", thirdLastSunday)
        fourthLastSundayDate = fourthLastSunday.strftime('%Y-%m-%d')

        #https://www.questrade.com/api/documentation/rest-operations/enumerations/enumerations#historical-data-granularity


        tickerInfo=qtrade.ticker_information(ticker)
        prevDayClosePrice=int(tickerInfo['prevDayClosePrice'])

        symbolId=tickerInfo['symbolId']
        #chain = qtrade.get_option_chain(ticker)

        #Get Next Friday's Options
        # friday = today + timedelta( (4-today.weekday()) % 7 )
        # secondFriday = (friday + timedelta(days=7))
        # thirdFriday = (secondFriday + timedelta(days=7))
        # fourthFriday = (thirdFriday + timedelta(days=7))

        # optionsExpiryDates = [friday,secondFriday,thirdFriday,fourthFriday]

        # optionsTable = Table(show_lines=True,header_style="bold magenta",show_footer=False,border_style="bright_yellow")
        # optionsTable.add_column("Symbol", justify="right", style="cyan", no_wrap=True)
        # optionsTable.add_column("Spread", justify="right", style="cyan", no_wrap=True)
        # optionsTable.add_column("Bid Price", justify="right", style="cyan", no_wrap=True)
        # optionsTable.add_column("Ask Price", justify="right", style="cyan", no_wrap=True)
        # optionsTable.add_column("Delta", justify="right", style="cyan", no_wrap=True)
        # optionsTable.add_column("Open Interest", justify="right", style="cyan", no_wrap=True)

        # for expiryDate in optionsExpiryDates:

        #     #optionIds=[39309304,39309305]
        #     optionIds=[]
        #     filters=[{"optionType": "Call", "underlyingId": symbolId, "minstrikePrice": prevDayClosePrice - 5, "maxstrikePrice": prevDayClosePrice + 5,"expiryDate": str(expiryDate.strftime('%Y-%m-%d')) + "T00:00:00.000000-05:00"}]
        #     #filters=[{"optionType": "Call", "underlyingId": symbolId, "minstrikePrice": prevDayClosePrice - 5, "maxstrikePrice": prevDayClosePrice + 5,"expiryDate": "2022-01-07T00:00:00.000000-05:00"}]
        #     callOptions = qtrade.get_option_quotes(filters,optionIds)


        #     for call in callOptions['optionQuotes']:
        #         bidPrice = call['bidPrice']
        #         askPrice = call['askPrice']
        #         spreadPrice = askPrice - bidPrice
        #         #print("symbol: %s bidPrice: %s askPrice: %s delta: %s dailyInterest: %s" %(call['symbol'], call['bidPrice'],call['askPrice'],call['delta'],call['openInterest']))
        #         optionsTable.add_row(str(call['symbol']),str(round(spreadPrice, 2)), str(call['bidPrice']), str(call['askPrice']), str(call['delta']), str(call['openInterest']))

        #     optionsTable.add_row('','', '', '', '', '')

        # console = Console()
        #console.print(optionsTable)

        daily_candles = qtrade.get_historical_data(ticker, '2021-01-01', todaysDate, "OneDay")

        weekly_candles = qtrade.get_historical_data(ticker, '2021-11-01', todaysDate, "OneWeek")

        monthly_candles = qtrade.get_historical_data(ticker, '2021-08-01', todaysDate, "OneMonth")

        takeDailyAmount = takeTimeFrameAmount(daily_candles[len(daily_candles)-1])
        takeWeeklyAmount = takeTimeFrameAmount(weekly_candles[len(weekly_candles)-1])
        takeMonthlyAmount = takeTimeFrameAmount(monthly_candles[len(monthly_candles)-1])

        stratBotTimeframe(dailyTable,"1D",daily_candles, ticker, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount,False)
        stratBotTimeframe(weeklyTable,"1W",weekly_candles, ticker, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount,True)
        stratBotTimeframe(monthlyTable,"1M",monthly_candles, ticker, takeDailyAmount, takeWeeklyAmount, takeMonthlyAmount,True)



    console.print(dailyTable)
    console.save_html("daily.html")
    console.print(weeklyTable)
    console.save_html("weekly.html")
    console.print(monthlyTable)
    console.save_html("monthly.html")

if __name__ == "__main__":


    if 'accessCode' in globals():
        qtrade = Questrade(access_code=accessCode)
    else:
        qtrade = Questrade(token_yaml='C:\\gitbash\\home\\apps\\.ssh\\access_token.yml')

    #qtrade.refresh_access_token(from_yaml=True,yaml_path='C:\\gitbash\\home\\apps\\.ssh\\access_token.yml')

    #qtrade.refresh_access_token(from_yaml=True,yaml_path='C:\\gitbash\\home\\apps\\.ssh\\access_token.yml')

    # timeframes=["FifteenMinutes","HalfHour","OneHour","OneDay","OneWeek","OneMonth","OneYear"]
    # timeframes=["FifteenMinutes","HalfHour","OneHour","OneDay","OneWeek"]
    # timeframesShortForm=["15min","30min","1H","1D","1W"]

    # timeframes=["OneHour"]
    # timeframesShortForm=["1H"]

    # today = datetime.today()
    # todaysDate = today.strftime('%Y-%m-%d')

    # timeframes=["OneDay","OneWeek","OneMonth"]
    # timeframesShortForm=["1D","1W","1M"]

    # daily_candles = qtrade.get_historical_data(ticker, '2021-01-01', todaysDate, "OneDay")

    # weekly_candles = qtrade.get_historical_data(ticker, '2021-11-01', todaysDate, "OneWeek")

    # monthly_candles = qtrade.get_historical_data(ticker, '2021-08-01', todaysDate, "OneMonth")

    # for index in range(len(timeframes)):
    #     stratBot(timeframes[index],timeframesShortForm[index])

    stratBot()

