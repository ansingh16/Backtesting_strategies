class Portfolio:
    def __init__(self):
        self.position = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.net_position=0
        self.buys = 0
        self.sells = 0
        self.executed=False
        self.orders_executed=[]
    
    def add_trade(self,symbol,kind,qty,price):
        if kind=='buy':
            self.buys += qty
        else:
            self.sells -= qty

        self.net_position = self.buys - self.sells
        sign = 1 if kind=='buy' else -1

        try:
            self.position += self.net_position*price*sign 
        except:
            self.position = self.net_position*price*sign 
        # if all the shares have been dealt with you get your realised PnL
        if self.net_position==0:
            self.realized_pnl = self.position

            self.unrealized_pnl = 0
    
    def update_ur_pnl(self,prices,symbol):
        
        if self.net_position == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = prices[symbol].closing_price * self.net_position + \
            self.position

    def event_fill(self,order):
        
        self.orders_executed.append(order)

