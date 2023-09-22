from Markets import *

class MeanRevertingStrategy:
    def __init__(self):
        # This will be set to a function in the backtesting
        # class

        self.symbol_dat=0
        self.burnout=10
        self.timestamp=0
        self.buy_threshold = -1.5
        self.sell_threshold = 1.5
        self.send_market_order = None

    def send_signal(self,symbol,symbol_dat,sd):
        

        self.symbol_dat = symbol_dat
        timestamp = sd.timestamp

        if symbol_dat.shape[0]>self.burnout:
            
            if self.get_zscore() < self.buy_threshold:            
                self.on_buy_signal(symbol,timestamp,sd)        
            elif self.get_zscore() > self.sell_threshold:            
                self.on_sell_signal(symbol,timestamp,sd)

    
    def on_buy_signal(self, symbol, timestamp,sd):
        order = OrderData(symbol,timestamp,100,True,sd.closing_price)
        
        if not self.send_market_order is None:

            self.send_market_order(order)    
    
    def on_sell_signal(self, symbol, timestamp,sd):
        order = OrderData(symbol,timestamp,100,False,sd.closing_price)
        
        if not self.send_market_order is None:

            self.send_market_order(order)    
    

    
    
    def get_zscore(self):

        self.symbol_dat = self.symbol_dat[-self.burnout:]
        # calculate returns
        returns = self.symbol_dat["Close"].pct_change().dropna()        
        # z score
        z_score = ((returns-returns.mean())/returns.std())[-1]        
        return z_score   
    
    # def send_market_order(self, order):
    #     pass 