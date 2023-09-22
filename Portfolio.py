class Portfolio:
    def __init__(self):
        self.positions = dict()
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.buys = 0
        self.sells = 0
        self.executed=False
    
    def add_trade(self,symbol,kind,qty,price):
        if kind=='buy':
            self.buys += qty
        else:
            self.sells -= qty

        self.net_position = self.buys - self.sells
        sign = 1 if kind=='buy' else -1

        try:
            self.positions[symbol] += self.net_position*price*sign 
        except:
            self.positions[symbol] = self.net_position*price*sign 
        # if all the shares have been dealt with you get your realised PnL
        if self.net_position==0:
            self.realized_pnl = self.positions[symbol]

            self.unrealized_pnl = 0
    
    def update_ur_pnl(self,price,symbol):
        
        if self.net_position == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = price * self.net_position + \
            self.positions[symbol]



