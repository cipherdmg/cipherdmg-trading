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
import time
import stratbotapi

from rich import print
from rich.console import Console
console = Console(record=True)


from rich.table import Table
from rich.markdown import Markdown


from yahoo_fin.stock_info import get_data

#For instance tickers_dow() returns a list of all the tickers in the Dow Jones so we can do:
# import yahoo_fin.stock_info as si
import yfinance as yf

def getYahooFinanceDailyCandles(symbol):

    candles = []
    df = yf.download(tickers=symbol,interval="1d", periods="1y", start="2021-01-01", end="2022-01-23", group_by="ticker")


    for ind in df.index:
        high = df['High'][ind]
        low = df['Low'][ind]
        open = df['Open'][ind]
        close = df['Close'][ind]
        volume = df['Volume'][ind]

        #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

        candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
        candles.append(candle)
    #print(df)
    return candles

def getYahooFinanceWeeklyCandles(symbol):

    candles = []
    df = yf.download(tickers=symbol,interval="1mo", periods="1y", start="2021-01-01", end="2022-01-23", group_by="ticker")

    for ind in df.index:
        high = df['High'][ind]
        low = df['Low'][ind]
        open = df['Open'][ind]
        close = df['Close'][ind]
        volume = df['Volume'][ind]

        #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

        candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
        candles.append(candle)
    #print(df)

    return candles


def getYahooFinanceMonthlyCandles(symbol):

    candles = []
    df = yf.download(tickers=symbol,interval="1mo", periods="1y", start="2021-01-01", end="2022-01-23", group_by="ticker")

    for ind in df.index:
        high = df['High'][ind]
        low = df['Low'][ind]
        open = df['Open'][ind]
        close = df['Close'][ind]
        volume = df['Volume'][ind]

        #print(str(ind) + " open: " + str(open) + " close: " + str(close) + " low: " + str(low) + " high: " + str(high))

        candle = stratbotapi.Candle(symbol,open,close,high,low,ind,volume)
        candles.append(candle)

    #print(df)
    return candles

if __name__ == "__main__":

    dailyTable = Table(title="Daily")
    dailyTable.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Timeframe", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Setup", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Enforced", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Profit", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Last 5 Candles", justify="right", style="cyan", no_wrap=True)
    dailyTable.add_column("Candle Pattern", justify="center", style="cyan", no_wrap=True)


    #Get the tickers
    symbols=stratbotapi.getTickers()

    console.print("Starting Stratbot ...")

    for symbol in symbols:

        #time.sleep(15) #Sleep 15 seconds betwean each api call

        candles = getYahooFinanceDailyCandles(symbol)

        if(len(candles) > 0):
            stratbotapi.determineStratSetup(dailyTable,symbol,candles,"1D")
        else:
            console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))

    console.print(dailyTable)


    # for symbol in symbols:

    #     #time.sleep(15) #Sleep 15 seconds betwean each api call
    #     candles = getYahooFinanceWeeklyCandles(symbol)
    #     if(len(candles) > 0):
    #         stratbotapi.determineStratSetup(dailyTable,symbol,candles,"1D")
    #     else:
    #         console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))


    # for symbol in symbols:

    #     #time.sleep(15) #Sleep 15 seconds betwean each api call

    #     candles = getYahooFinanceWeeklyCandles(symbol)
    #     if(len(candles) > 0):
    #         stratbotapi.determineStratSetup(dailyTable,symbol,candles,"1D")
    #     else:
    #         console.print("[red]ERROR: Symbol: %s contains no candles.[/red]" % (symbol))


