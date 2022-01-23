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
#
#
#
#
# pip install yahoo_fin
# pip install requests_html
#
###############################################################################
#

from ast import For
import datetime
import sys
import random
import pandas
import time
import stratbotapi

from rich import print
from rich.console import Console
console = Console(record=True)


from rich.table import Table
from rich.markdown import Markdown

THROTTLE_SLEEP=10

def getYahooFinanceDailyCandles(symbol):

    candles = []

    period1 = int(time.mktime(datetime.datetime(2021,1,1,23,59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    interval = '1d'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    try:
        df = pandas.read_csv(query_string)
        for ind in df.index:
            high = df['High'][ind]
            low = df['Low'][ind]
            open = df['Open'][ind]
            close = df['Close'][ind]
            volume = df['Volume'][ind]

            #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

            candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
            candles.append(candle)
    except:
        print("Unable to find symbol " + symbol)

    #print(df)
    return candles

def getYahooFinanceWeeklyCandles(symbol):

    candles = []

    period1 = int(time.mktime(datetime.datetime(2021,1,1,23,59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    interval = '1wk'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    #print(df)

    try:
        df = pandas.read_csv(query_string)

        for ind in df.index:
            high = df['High'][ind]
            low = df['Low'][ind]
            open = df['Open'][ind]
            close = df['Close'][ind]
            volume = df['Volume'][ind]

            #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

            candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
            candles.append(candle)
    except:
        print("Unable to find symbol " + symbol)


    return candles


def getYahooFinanceMonthlyCandles(symbol):

    candles = []

    period1 = int(time.mktime(datetime.datetime(2021,1,1,23,59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    interval = '1mo'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    try:
        df = pandas.read_csv(query_string)

        for ind in df.index:
            high = df['High'][ind]
            low = df['Low'][ind]
            open = df['Open'][ind]
            close = df['Close'][ind]
            volume = df['Volume'][ind]

            #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

            candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
            candles.append(candle)
    except:
        print("Unable to find symbol " + symbol)

    #print(df)
    return candles


if __name__ == "__main__":

    table = Table(title="Daily")
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    table.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    table.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    table.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    table.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    table.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    #Get the tickers
    symbols=stratbotapi.getTickers()

    console.print("Starting Stratbot ...")
    stratSetups = []

    for symbol in symbols:

        time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

        candles = getYahooFinanceDailyCandles(symbol)

        if(len(candles) > 0):
            stratSetup = stratbotapi.determineStratSetup(symbol,candles,"1D",False)
            table.add_row(str(stratSetup.symbol),str(stratSetup.timeframe), stratSetup.setup ,stratSetup.inForce, "$" + str(round(stratSetup.profit, 2)),  stratSetup.lastFiveCandles, stratSetup.candlePattern)
        else:
            console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))

    console.print(table)


    table = Table(title="Daily")
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    table.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    table.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    table.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    table.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    table.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    stratSetups = []

    for symbol in symbols:

        time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

        candles = getYahooFinanceWeeklyCandles(symbol)

        if(len(candles) > 0):
            stratSetup = stratbotapi.determineStratSetup(symbol,candles,"1W",False)
            table.add_row(str(stratSetup.symbol),str(stratSetup.timeframe), stratSetup.setup ,stratSetup.inForce, "$" + str(round(stratSetup.profit, 2)),  stratSetup.lastFiveCandles, stratSetup.candlePattern)
        else:
            console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))

    console.print(table)



    table = Table(title="Daily")
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    table.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    table.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    table.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    table.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    table.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    stratSetups = []

    for symbol in symbols:

        time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

        candles = getYahooFinanceMonthlyCandles(symbol)

        if(len(candles) > 0):
            stratSetup = stratbotapi.determineStratSetup(symbol,candles,"1M",True)
            table.add_row(str(stratSetup.symbol),str(stratSetup.timeframe), stratSetup.setup ,stratSetup.inForce, "$" + str(round(stratSetup.profit, 2)),  stratSetup.lastFiveCandles, stratSetup.candlePattern)
        else:
            console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))

    console.print(table)



