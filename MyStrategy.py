import pandas as pd
import backtrader as bt


cerebro = bt.Cerebro()
cerebro.broker.set_cash(100000)

data = bt.feeds.YahooFinanceCSVData(dataname='EURUSD.csv')
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.adddata(data)
cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
