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


from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1,readonly=True)

stock = Stock('AAPL', 'SMART', 'USD')
#ib.qualifyContracts(stock)

ib.sleep(1)

historical_data_nflx = ib.reqHistoricalData(stock, '', barSizeSetting='1 day', durationStr='2 D', whatToShow='MIDPOINT', useRTH=True)
print(util.df(historical_data_nflx))

#chains = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)

#print(util.df(chains))
