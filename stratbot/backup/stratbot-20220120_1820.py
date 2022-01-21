#https://www.questrade.com/api/documentation/rest-operations/
#https://github.com/willmcgugan/rich
#
# Ideas
#  - How far to take Day, Week and Month
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

    data = ib.reqMktData(stock)

    ib.sleep(1)

    marketPrice = data.marketPrice()
    askPrice = data.ask
    bidPrice = data.bid
    openPrice = data.open
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
