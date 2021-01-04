import pandas as pd
import backtrader as bt
import datetime
from TestStrategy import TestStrategy
from SMA_Strategy import SMA_Strategy
from RSI_Strategy import RSI_Strategy
from MACD_Strategy import MACD_Strategy
from SMA200_Strategy import SMA200_Strategy

cerebro = bt.Cerebro()
cerebro.broker.set_cash(100000)

data = bt.feeds.YahooFinanceCSVData(
    dataname='EURUSD.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2010, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2016, 1, 1),
    # Do not pass values after this date
    reverse=False)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.adddata(data)
cerebro.addstrategy(SMA200_Strategy)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
#set the comission - 0.1% ....divided by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
#edited Lib/site-packages/backtrader/plot/locator.py and removed warnings from the import funtion


