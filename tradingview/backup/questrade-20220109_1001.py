#https://www.questrade.com/api/documentation/rest-operations/
#https://github.com/willmcgugan/rich
#
# Ideas
#  - How far to take Day, Week and Month
#

from rich import print
from rich.console import Console
from rich.table import Table

from datetime import datetime, timedelta
import os
import sys

from qtrade import Questrade

#accessCode = ""

fridayDate = datetime(int(2022), int(1), 7)


#https://www.questrade.com/api/documentation/rest-operations

#https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=


def getTickers():
    tickers_TEST = ["AAPL", "RBLX"]

    tickers_ETFs= ["SPY","QQQ", "DIA", "IWM", "XBI", "XHB", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLY", "XLV", "XOP"]

    tickersA_I = ["AAPL","ABNB","ADBE", "AFRM", "AMD","AMZN","ADP","BABA","BIDU","CRM","CRWD", "CSCO", "COIN", "DISH", "DIS", "EXPE", "FB", "FUBO", "FVRR", "GOOG", "GOOGL", "IBM" , "INOD"]
    tickersJ_R = ["JD", "JNPR", "KLIC", "LSPD","MCHP", "META", "MU", "MSFT", "MA", "NFLX", "NVDA", "ORCL", "PLTR", "RBLX", "ROKU", "RNG"]
    tickersS_Z = ["SAVE", "SHOP", "SPOT", "SPLK", "TDOC", "TWLO", "U", "UBER", "V", "Z", "ZG", "ZM", "WDAY"]


    tickers_Retail = ["AMZN", "BBBY", "CHWY", "COST", "DG", "DLTR", "EBAY", "ETSY", "EXPR", "GME", "GRPN", "GPS", "HD", "JD", "KR", "LOW", "M", "NEGG", "PETS", "TGT", "URBN", "W", "WMT"]
    tickers_Cannabis=["SNDL", "TLRY", "CGC", "MO", "ACB", "OGI", "AMRS", "CPMD", "HEXO"]
    tickers_Auto = ["AYRO", "BLNK", "CHPT", "F", "GM", "HMC", "LCID", "LI", "LYFT", "MVIS", "NKLA", "NIO", "RIDE", "TM", "TSLA", "UBER", "VLTA", "WKHS", "WBX", "XPEV"]
    tickers_Energy = [ "AMRC", "ARVL", "BEP", "BEPC", "BLNK", "CHPT", "DQ", "DUK", "ENPH", "EVGO", "FSLR", "FCEL", "HPK", "IVAN", "ISUN", "JKS", "MAXN", "NEE", "NEP", "PPSI", "QCLN", "QS", "RUN", "RIVN", "SEDG", "SO", "SOLO", "SPWR", "SU", "VST", "VLO"  ]


    if 'accessCode' in globals():
        tickers = tickers_TEST
    else:
        tickers = tickers_ETFs + tickersA_I + tickersJ_R + tickersS_Z + tickers_Retail + tickers_Cannabis + tickers_Auto + tickers_Energy

    tickers = tickers_TEST
    # tickers = tickers_ETFs + tickersA_I + tickersJ_R + tickersS_Z + tickers_Retail + tickers_Cannabis + tickers_Auto + tickers_Energy

    #tickers.sort()
    return tickers


def getPercentChange(ticker):
    openPrice=ticker['open']
    closePrice=ticker['close']

    percentChange = (closePrice - openPrice) / openPrice * 100.0
    return percentChange

# def isPriceMoveMatchThreshold(table,ticker,lastStartDateTimeString,timeframe,stratPattern, profitTarget, tickers):

def addTickerToTable(table,ticker,timeframe,stratPattern, candlePattern, profitTarget, tickers,takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage):
    if(profitTarget >= 2.00):

        if(timeframe == "1D"):
            table.add_row(str(ticker),str(timeframe), stratPattern , "$" + str(round(profitTarget, 2)),candlePattern, takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage)
        elif(timeframe == "1W"):
            table.add_row(str(ticker),str(timeframe), stratPattern , "$" + str(round(profitTarget, 2)),candlePattern,takeWeeklyPercentage,takeMonthlyPercentage)
        elif(timeframe == "1M"):
            table.add_row(str(ticker),str(timeframe), stratPattern , "$" + str(round(profitTarget, 2)),candlePattern,takeMonthlyPercentage)

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

    previousHigh=candles[idx-1]['high']
    high=candles[idx]['high']
    previousLow=candles[idx-1]['low']
    low=candles[idx]['low']
    return high <= previousHigh and low >= previousLow


def isOutsideCandle(candles,idx):
    previousHigh=candles[idx-1]['high']
    high=candles[idx]['high']
    previousLow=candles[idx-1]['low']
    low=candles[idx]['low']
    return high > previousHigh and low < previousLow


def isTwoDownCandle(candles,idx):
    previousHigh=candles[idx-1]['high']
    high=candles[idx]['high']
    previousLow=candles[idx-1]['low']
    low=candles[idx]['low']
    return low < previousLow and not (high > previousHigh)


def isTwoUpCandle(candles,idx):
    previousHigh=candles[idx-1]['high']
    high=candles[idx]['high']
    previousLow=candles[idx-1]['low']
    low=candles[idx]['low']
    return high > previousHigh and not (low < previousLow)

def getCandleColor(candles, idx):
    if(isGreenCandle(candles,idx)):
        return "green"
    else:
        return "red"

def isGreenCandle(candles, idx):
    return candles[idx]['open'] < candles[idx]['close']

def isRedCandle(candles, idx):
    return candles[idx]['open'] >= candles[idx]['close']

def stratBotTimeframe(table,timeframeShortForm, tickers, ticker,takeDailyPercentage,takeWeeklyPercentage,takeMonthlyPercentage):

    #ticker_candles = qtrade.get_historical_data(ticker, fourthLastSundayDate, todaysDate, timeframe)
    #ticker_candles = qtrade.get_historical_data(ticker, '2021-12-30', '2022-01-05', timeframes[index])
    lastClose = tickers[len(tickers)-1]['close']

    lastStartDateString = tickers[len(tickers)-1]['start']
    lastEndDateString = tickers[len(tickers)-1]['end']

    lastStartDate = datetime.fromisoformat(lastStartDateString)
    # testDate = datetime.strptime("2015-02-24T13:00:00-08:00", '%Y-%m-%dT%H:%M:%S%Z')
    #testDate = datetime.strptime("2015-02-24T13:00:00-08:00", "%Y-%B-%dT%H:%M:%S-%H:%M").date()
    lastStartDateTimeString=lastStartDate.strftime("%Y-%m-%d %H:%M:%S")

    thirdLastCandleLow = tickers[len(tickers)-3]['low']
    secondLastCandleLow = tickers[len(tickers)-2]['low']
    lastCandleLow = tickers[len(tickers)-1]['low']

    thirdLastCandleHigh = tickers[len(tickers)-3]['high']
    secondLastCandleHigh = tickers[len(tickers)-2]['high']
    lastCandleHigh = tickers[len(tickers)-1]['high']

    sixthLastCandle = getStratNumber(tickers,len(tickers)-6)
    fithLastCandle = getStratNumber(tickers,len(tickers)-5)
    fourthLastCandle = getStratNumber(tickers,len(tickers)-4)
    thirdLastCandle = getStratNumber(tickers,len(tickers)-3)
    secondLastCandle = getStratNumber(tickers,len(tickers)-2)
    lastCandle = getStratNumber(tickers,len(tickers)-1)

    #Last
    candlePattern = sixthLastCandle + "," + fithLastCandle + "," + fourthLastCandle + "," + thirdLastCandle + "," + secondLastCandle + "," + lastCandle

    #Determine if the next candle came out then would a reversal occur

    # 2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)
    if("2U" in secondLastCandle and "1" in lastCandle):
        #print("2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"

        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
    elif("2D" in secondLastCandle and "1" in lastCandle):
        #print("2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)
    elif("3" in secondLastCandle and "2U" in lastCandle):
        #print("3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern = secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)
    elif("3" in secondLastCandle and "2D" in lastCandle):
        #print("3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern = secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)
    elif("3" in secondLastCandle and "1" in lastCandle):
        #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2D/2U[/green]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 3-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be 2 Up)

    # 1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)
    elif("1" in secondLastCandle and "2U" in lastCandle):
        #print("1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  secondLastCandle + "," + lastCandle + ",[red]2D[/red]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)
    elif("1" in secondLastCandle and "2D" in lastCandle):
        #print("1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)")

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern =  secondLastCandle + "," + lastCandle + ",[green]2U[/green]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    #2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)
    #For quick reversal on the 2s make sure that its been running for a little bit
    #elif (lastCandle == "2U" and secondLastCandle != "2D" and thirdLastCandle != "2D"):
    elif ("2U" in lastCandle and "2D" not in secondLastCandle):
        #print("2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)")
        #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = lastCandleLow - secondLastCandleLow
        stratPattern =  lastCandle + ",[red]2D[/red]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    # 2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
    #elif (lastCandle == "2D" and secondLastCandle != "2U" and thirdLastCandle != "2U"):
    elif ("2D" in lastCandle and "2U" not in secondLastCandle):
        #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")
        #table.add_row(str(ticker), str(timeframeShortForm), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , str(lastClose), getCandleColor(tickers,len(tickers)-1))

        #Calculate what this reversal would be worth based on the first pivot/target
        profitTarget = secondLastCandleHigh - lastCandleHigh
        stratPattern =  lastCandle + ",[green]2U[/green]"
        addTickerToTable(table, ticker,timeframeShortForm,stratPattern, candlePattern, profitTarget, tickers, takeDailyPercentage, takeWeeklyPercentage, takeMonthlyPercentage)

    #table.add_row(str(ticker), str(timeframeShortForm), thirdLastCandle + "," + secondLastCandle + "," + lastCandle , str(lastClose), getCandleColor(tickers,len(ticker_candles)-1))


def stratBot():

    console = Console()

    dailyTable = Table(title="Daily")
    dailyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Aggregation", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Candle Pattern", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Day", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Week", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)

    weeklyTable = Table(title="Weekly")
    weeklyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Aggregation", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Candle Pattern", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Week", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)


    monthlyTable = Table(title="Monthly")
    monthlyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Aggregation", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Candle Pattern", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Month", justify="right", style="cyan", no_wrap=True)

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

        takeDailyPercentage = getPercentChange(daily_candles[len(daily_candles)-1])
        takeWeeklyPercentage = getPercentChange(weekly_candles[len(weekly_candles)-1])
        takeMonthlyPercentage = getPercentChange(monthly_candles[len(monthly_candles)-1])

        takeDailyPercentageStr= str(round(takeDailyPercentage, 2))
        takeWeeklyPercentageStr= str(round(takeWeeklyPercentage, 2))
        takeMonthlyPercentageStr= str(round(takeMonthlyPercentage, 2))

        if(takeDailyPercentageStr.startswith("-")):
            takeDailyPercentageStr="[red]" + takeDailyPercentageStr + "%[/red]"
        else:
            takeDailyPercentageStr="[green]" + takeDailyPercentageStr + "%[/green]"

        if(takeWeeklyPercentageStr.startswith("-")):
            takeWeeklyPercentageStr="[red]" + takeWeeklyPercentageStr + "%[/red]"
        else:
            takeWeeklyPercentageStr="[green]" + takeWeeklyPercentageStr + "%[/green]"

        if(takeMonthlyPercentageStr.startswith("-")):
            takeMonthlyPercentageStr="[red]" + takeMonthlyPercentageStr + "%[/red]"
        else:
            takeMonthlyPercentageStr="[green]" + takeMonthlyPercentageStr + "%[/green]"



        stratBotTimeframe(dailyTable,"1D",daily_candles, ticker, takeDailyPercentageStr, takeWeeklyPercentageStr, takeMonthlyPercentageStr)
        stratBotTimeframe(weeklyTable,"1W",weekly_candles, ticker, takeDailyPercentageStr, takeWeeklyPercentageStr, takeMonthlyPercentageStr)
        stratBotTimeframe(monthlyTable,"1M",monthly_candles, ticker, takeDailyPercentageStr, takeWeeklyPercentageStr, takeMonthlyPercentageStr)


    console.print(dailyTable)
    console.print(weeklyTable)
    console.print(monthlyTable)

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

