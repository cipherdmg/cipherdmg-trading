#https://www.questrade.com/api/documentation/rest-operations/
#https://github.com/willmcgugan/rich

from rich import print
from rich.console import Console
from rich.table import Table

from datetime import datetime, timedelta
import os
import sys

from qtrade import Questrade

fridayDate = datetime(int(2022), int(1), 7)


#https://www.questrade.com/api/documentation/rest-operations

#https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=

def getStratNumber(candles,idx):

    if(isInsideCandle(candles,idx)):
        return "1"

    elif(isOutsideCandle(candles,idx)):
        return "3"

    elif(isTwoDownCandle(candles,idx)):
        return "2D"

    elif(isTwoUpCandle(candles,idx)):
        return "2U"

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


#qtrade = Questrade(access_code='')
qtrade = Questrade(token_yaml='C:\\gitbash\\home\\apps\\.ssh\\access_token.yml')
#qtrade.refresh_access_token(from_yaml=True,yaml_path='C:\\gitbash\\home\\apps\\.ssh\\access_token.yml')

tickers = ["AAPL", "AFRM", "AMD", "COIN", "IBM", "MSFT", "MA", "NFLX", "RBLX","NVDA", "TSLA", "XOP", "XLE", "V"]
#tickers = ["AAPL", "MSFT"]
# timeframes=["FifteenMinutes","HalfHour","OneHour","OneDay","OneWeek","OneMonth","OneYear"]
#timeframes=["FifteenMinutes","HalfHour","OneHour","OneDay","OneWeek"]
#timeframesShortForm=["15min","30min","1H","1D","1W"]

timeframes=["OneDay","OneWeek"]
timeframesShortForm=["1D","1W"]

# timeframes=["OneHour"]
# timeframesShortForm=["1H"]

today = datetime.today()
todaysDate = today.strftime('%Y-%m-%d')
#https://www.questrade.com/api/documentation/rest-operations/enumerations/enumerations#historical-data-granularity

for ticker in tickers:

    tickerInfo=qtrade.ticker_information(ticker)
    prevDayClosePrice=int(tickerInfo['prevDayClosePrice'])

    symbolId=tickerInfo['symbolId']
    #chain = qtrade.get_option_chain(ticker)

    #nextFriday = (fridayDate + timedelta(days=7)).strftime('%Y-%m-%d')

    #Get Next Friday's Options
    friday = today + timedelta( (4-today.weekday()) % 7 )
    secondFriday = (friday + timedelta(days=7))
    thirdFriday = (secondFriday + timedelta(days=7))
    fourthFriday = (thirdFriday + timedelta(days=7))

    optionsExpiryDates = [friday,secondFriday,thirdFriday,fourthFriday]

    optionsTable = Table(show_lines=True,header_style="bold magenta",show_footer=False,border_style="bright_yellow")
    optionsTable.add_column("Symbol", justify="right", style="cyan", no_wrap=True)
    optionsTable.add_column("Spread", justify="right", style="cyan", no_wrap=True)
    optionsTable.add_column("Bid Price", justify="right", style="cyan", no_wrap=True)
    optionsTable.add_column("Ask Price", justify="right", style="cyan", no_wrap=True)
    optionsTable.add_column("Delta", justify="right", style="cyan", no_wrap=True)
    optionsTable.add_column("Open Interest", justify="right", style="cyan", no_wrap=True)

    for expiryDate in optionsExpiryDates:

        #optionIds=[39309304,39309305]
        optionIds=[]
        filters=[{"optionType": "Call", "underlyingId": symbolId, "minstrikePrice": prevDayClosePrice - 5, "maxstrikePrice": prevDayClosePrice + 5,"expiryDate": str(expiryDate.strftime('%Y-%m-%d')) + "T00:00:00.000000-05:00"}]
        #filters=[{"optionType": "Call", "underlyingId": symbolId, "minstrikePrice": prevDayClosePrice - 5, "maxstrikePrice": prevDayClosePrice + 5,"expiryDate": "2022-01-07T00:00:00.000000-05:00"}]
        callOptions = qtrade.get_option_quotes(filters,optionIds)


        for call in callOptions['optionQuotes']:
            bidPrice = call['bidPrice']
            askPrice = call['askPrice']
            spreadPrice = askPrice - bidPrice
            #print("symbol: %s bidPrice: %s askPrice: %s delta: %s dailyInterest: %s" %(call['symbol'], call['bidPrice'],call['askPrice'],call['delta'],call['openInterest']))
            optionsTable.add_row(str(call['symbol']),str(round(spreadPrice, 2)), str(call['bidPrice']), str(call['askPrice']), str(call['delta']), str(call['openInterest']))

        optionsTable.add_row('','', '', '', '', '')

    console = Console()
    #console.print(optionsTable)

    table = Table()
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Aggregation", justify="right", style="cyan", no_wrap=True)
    table.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    table.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    table.add_column("Candle Color", justify="right", style="cyan", no_wrap=True)

    for index in range(len(timeframes)):
        ticker_candles = qtrade.get_historical_data(ticker, '2021-12-30', todaysDate, timeframes[index])
        lastClose = ticker_candles[len(ticker_candles)-1]['close']

        thirdLastCandleLow = ticker_candles[len(ticker_candles)-3]['low']
        secondLastCandleLow = ticker_candles[len(ticker_candles)-2]['low']
        lastCandleLow = ticker_candles[len(ticker_candles)-1]['low']

        thirdLastCandleHigh = ticker_candles[len(ticker_candles)-3]['high']
        secondLastCandleHigh = ticker_candles[len(ticker_candles)-2]['high']
        lastCandleHigh = ticker_candles[len(ticker_candles)-1]['high']

        thirdLastCandle = getStratNumber(ticker_candles,len(ticker_candles)-3)
        secondLastCandle = getStratNumber(ticker_candles,len(ticker_candles)-2)
        lastCandle = getStratNumber(ticker_candles,len(ticker_candles)-1)

        #Determine if the next candle came out then would a reversal occur

        # 2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)
        if(secondLastCandle == "2U" and lastCandle == "1"):
            #print("2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
        elif(secondLastCandle == "2D" and lastCandle == "1"):
            #print("2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)
        elif(secondLastCandle == "3" and lastCandle == "2U"):
            #print("3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)
        elif(secondLastCandle == "3" and lastCandle == "2D"):
            #print("3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)
        elif(secondLastCandle == "3" and lastCandle == "1"):
            #print("3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[green]2D/2U[/green]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 3-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be 2 Up)

        # 1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)
        elif(secondLastCandle == "1" and lastCandle == "2U"):
            #print("1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)
        elif(secondLastCandle == "1" and lastCandle == "2D"):
            #print("1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)")

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        #2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)
        #For quick reversal on the 2s make sure that its been running for a little bit
        elif (lastCandle == "2U" and secondLastCandle != "2D" and thirdLastCandle != "2D"):
            #print("2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)")
            #table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[red]2D[/red]" , str(lastClose), getCandleColor(ticker_candles,len(ticker_candles)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = lastCandleLow - secondLastCandleLow
            table.add_row(str(ticker), str(timeframesShortForm[index]), lastCandle + ",[red]2D[/red]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        # 2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
        elif (lastCandle == "2D" and secondLastCandle != "2U" and thirdLastCandle != "2U"):
            #print("2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)")
            #table.add_row(str(ticker), str(timeframesShortForm[index]), secondLastCandle + "," + lastCandle + ",[green]2U[/green]" , str(lastClose), getCandleColor(ticker_candles,len(ticker_candles)-1))

            #Calculate what this reversal would be worth based on the first pivot/target
            profitTarget = secondLastCandleHigh - lastCandleHigh
            table.add_row(str(ticker), str(timeframesShortForm[index]), lastCandle + ",[green]2U[/green]" , "$" + str(round(profitTarget, 2)), getCandleColor(ticker_candles,len(ticker_candles)-1))

        #table.add_row(str(ticker), str(timeframesShortForm[index]), thirdLastCandle + "," + secondLastCandle + "," + lastCandle , str(lastClose), getCandleColor(ticker_candles,len(ticker_candles)-1))


console = Console()
console.print(table)


#Potential Reversals to Note:
#
# 2-2 Bearish Reversal has entry on low[1] and target low[2] (Next Candle Needs to be 2 Down)
#
# 2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
#
# 2-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle Needs to be 2 Down)
#
# 2-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle Needs to be 2 Up)
#
# 3-2-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be a 2 Down)
#
# 3-2-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be a 2 Up)
#
# 3-1-2 Bearish Reversal has entry low[1] and target low[2] (Next Candle needs to be 2 Down)
#
# 3-1-2 Bullish Reversal has entry high[1] and target high[2] (Next Candle needs to be 2 Up)
#
# 1-2-2 Bearish Rev Strat has entry low[1] and target low[3] (Next Candle needs to be 2 Down)
#
# 1-2-2 Bullish Rev Strat has entry high[1] and target high[3] (Next Candle needs to be 2 Up)

