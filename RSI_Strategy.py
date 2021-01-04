import backtrader as bt

class RSI_Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        #keep track of pending orders and buy price and comission
        self.order = None
        self.buyprice = None
        self.buycomm = None

       #todo RSI initialise 
        self.rsi = bt.indicators.RelativeStrengthIndex(period=14, upperband=70, lowerband=30)



    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f '
                  % (order.executed.price, order.executed.price, order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            elif order.issell():
                self.log('SELL EXECUTED,Price: %.2f, Cost: %.2f, Comm: %.2f '
                  % (order.executed.price, order.executed.price, order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None   

     #this method shows gross and net profit after a position has been closed
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # Check if we are in the market
        if not self.position:

            if self.rsi < 30:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # keep track of order
                self.order = self.buy()

        else:
            if self.rsi > 70:
                self.log('SELL CREATE, %.2f ' % self.dataclose[0])

                self.order = self.sell()