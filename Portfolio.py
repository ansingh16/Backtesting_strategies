class Portfolio:
    """
    Stores the information for a stack in your portfolio
    its position, realised and unrealized PNL and net quantity
    """
    def __init__(self):
        self.position = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.net_position=0
        self.buys = 0
        self.sells = 0
        self.symbol = None
        
    
    def add_trade(self,buy,qty,price):
        # This will wither buy or subtrac the quantity 
        # depending on position and buy singnal
        if buy==True:
            self.buys += qty
        else:
            self.sells += qty

        self.net_position = self.buys - self.sells

        diff = qty*price*(-1 if buy else 1)
        self.position += diff

        # if all the shares have been dealt with you get your realised PnL
        if self.net_position==0:
            self.realized_pnl = self.position

    
    def update_ur_pnl(self,price):
        
        if self.net_position == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = price*self.net_position + \
            self.position

    # def event_fill(self,order):
        
    #     self.orders_executed.append(order)

