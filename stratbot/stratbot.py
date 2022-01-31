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


import logging
from ast import For
import datetime
import sys
import random
import pandas
import time
import stratbotapi

from rich import print
from rich.progress import track
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
console = Console(record=True)


from rich.table import Table
from rich.markdown import Markdown

VERBOSE_TABLE=True
THROTTLE_SLEEP=5
PROFIT_TARGET=5.00

logging.basicConfig(level=logging.INFO)


YEAR_BEGINNING=datetime.datetime(2021,1,1,23,59)
FIRST_MONDAY_OF_YEAR= YEAR_BEGINNING + datetime.timedelta( (0-YEAR_BEGINNING.weekday()) % 7 ) #Used for Weeklys

today=datetime.date.today()
#today=datetime.datetime(2022,1,26,23,00)
weekday=today.weekday()

monday = today + datetime.timedelta( (0-today.weekday()) % 7 )
tuesday = today + datetime.timedelta( (1-today.weekday()) % 7 )
wednesday = today + datetime.timedelta( (2-today.weekday()) % 7 )
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )

lastMonday = today - datetime.timedelta(days=(today.weekday()))
lastTuesday = today - datetime.timedelta(days=(today.weekday() - 1) % 7)
lastWednesday = today - datetime.timedelta(days=(today.weekday() - 2) % 7)
lastFriday = today - datetime.timedelta(days=(today.weekday() - 4) % 7)

yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)



def getYahooFinanceDailyCandles(symbol):

    #logging.debug("Getting Yahoo {} Symbol: {}".format('Daily', symbol))
    candles = []

    period1 = int(time.mktime(YEAR_BEGINNING.timetuple()))
    #period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    period2 = int(time.mktime(tomorrow.timetuple()))
    interval = '1d'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    logging.debug("Query String {}".format(query_string))

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

    #logging.debug("Getting Yahoo {} Symbol: {}".format('Weekly', symbol))

    #Yahoo Historical Data Should Start on a Monday for Weekly Candles.

    candles = []

    period1 = int(time.mktime(FIRST_MONDAY_OF_YEAR.timetuple()))
    #period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    period2 = int(time.mktime(tomorrow.timetuple()))
    interval = '1wk'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    logging.debug("Query String {}".format(query_string))

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

        #Daily candles don't close on yahoo until ???
        #Take the last candle which is actually a daily candle and remove it from this list and replace the new last candle close with the candle you removed candle's close
        candle = candles[len(candles)-1]
        candles.pop(len(candles)-1)
        candles[len(candles)-1].close=candle.close
    except:
        print("Unable to find symbol " + symbol)

    return candles


def getYahooFinanceMonthlyCandles(symbol):

    #logging.debug("Getting Yahoo {} Symbol: {}".format('Monthly', symbol))

    candles = []

    period1 = int(time.mktime(YEAR_BEGINNING.timetuple()))
    #period2 = int(time.mktime(datetime.datetime(2022,1,22,23,59).timetuple()))
    period2 = int(time.mktime(tomorrow.timetuple()))
    interval = '1mo'
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    logging.debug("Query String {}".format(query_string))

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

        #When doing monthly's the last candle is the daily candle and then the previous candle is the
        #monthly candle but assume the monthy has not incoporated the last daily
        #Take the last candle which is actually a daily candle and remove it from this list and replace the new last candle close with the candle you removed candle's close
        candle = candles[len(candles)-1]
        candles.pop(len(candles)-1)
        candles[len(candles)-1].close=candle.close
    except:
        print("Unable to find symbol " + symbol)

    return candles

def addRowsToTable(symbol,candles,timeframe,isLastCandleActive=False):

    if(len(candles) > 5):
        stratSetup = stratbotapi.determineStratSetup(symbol,candles,timeframe,isLastCandleActive)
        if(stratSetup is not None):
            if(stratSetup.profit >= PROFIT_TARGET):
                lastCandle=candles[len(candles)-1]

                if(VERBOSE_TABLE):
                    dailyTable.add_row(str(stratSetup.symbol),str(stratSetup.timeframe), stratSetup.setup ,stratSetup.inForce, "$" + str(round(stratSetup.profit, 2)),  stratSetup.lastFiveCandles, stratSetup.candlePattern, str(lastCandle.open),str(lastCandle.high),str(lastCandle.low),str(lastCandle.close))
                else:
                    dailyTable.add_row(str(stratSetup.symbol),str(stratSetup.timeframe), stratSetup.setup ,stratSetup.inForce, "$" + str(round(stratSetup.profit, 2)),  stratSetup.lastFiveCandles, stratSetup.candlePattern)
                # else:
                #     console.print("[red]ERROR: Symbol: %s does not have a setup.[/red]" % (symbol))
            # elif(len(candles) > 0):
            #     console.print("[red]ERROR: Symbol: %s does not contain 5 candles.[/red]" % (symbol))
            # else:
            #     console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))


if __name__ == "__main__":

    dailyTable = Table(title="Daily")
    dailyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    if(VERBOSE_TABLE):
        dailyTable.add_column("Open", justify="right", style="cyan", no_wrap=True)
        dailyTable.add_column("High", justify="right", style="cyan", no_wrap=True)
        dailyTable.add_column("Low", justify="right", style="cyan", no_wrap=True)
        dailyTable.add_column("Close", justify="right", style="cyan", no_wrap=True)


    #Get the tickers
    symbols=stratbotapi.getTickers()

    console.print("Starting Stratbot ...")
    stratSetups = []

    with Progress() as progress:
        task = progress.add_task("Getting Daily Strat Setups", total=len(symbols))
        for symbol in symbols:
            progress.console.print(f"Checking symbol {symbol}")

            time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

            candles = getYahooFinanceDailyCandles(symbol)
            addRowsToTable(symbol,candles,"1D",False)
            progress.advance(task)


    weeklyTable = Table(title="Weekly")
    weeklyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    weeklyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    if(VERBOSE_TABLE):
        weeklyTable.add_column("Open", justify="right", style="cyan", no_wrap=True)
        weeklyTable.add_column("High", justify="right", style="cyan", no_wrap=True)
        weeklyTable.add_column("Low", justify="right", style="cyan", no_wrap=True)
        weeklyTable.add_column("Close", justify="right", style="cyan", no_wrap=True)


    stratSetups = []

    with Progress() as progress:
        task = progress.add_task("Getting Weekly Strat Setups", total=len(symbols))
        for symbol in symbols:
            progress.console.print(f"Checking symbol {symbol}")

            time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

            candles = getYahooFinanceWeeklyCandles(symbol)
            addRowsToTable(symbol,candles,"1W",True)
            progress.advance(task)


    monthlyTable = Table(title="Monthly")
    monthlyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("In forced", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    monthlyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)

    if(VERBOSE_TABLE):
        monthlyTable.add_column("Open", justify="right", style="cyan", no_wrap=True)
        monthlyTable.add_column("High", justify="right", style="cyan", no_wrap=True)
        monthlyTable.add_column("Low", justify="right", style="cyan", no_wrap=True)
        monthlyTable.add_column("Close", justify="right", style="cyan", no_wrap=True)


    stratSetups = []

    with Progress() as progress:
        task = progress.add_task("Getting Monthly Strat Setups", total=len(symbols))
        for symbol in symbols:
            progress.console.print(f"Checking symbol {symbol}")

            time.sleep(THROTTLE_SLEEP) #Sleep 15 seconds betwean each api call

            candles = getYahooFinanceMonthlyCandles(symbol)
            addRowsToTable(symbol,candles,"1M",True)
            progress.advance(task)

    console.print(dailyTable)
    console.print(weeklyTable)
    console.print(monthlyTable)
