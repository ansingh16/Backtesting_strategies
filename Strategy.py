from Markets import *


class OrderData:

    def __init__(self, symbol,timestamp,quant,buy,price):

        self.symbol = symbol
        self.timestamp = timestamp
        self.quant = quant
        self.buy = buy
        self.price = price



class MeanRevertingStrategy:
    def __init__(self,symbol,burnout=20,buy_threshold=-1.5,sell_threshold=1.5):
        # This will be set to a function in the backtesting
        # class

        self.symbol=symbol
        self.burnout=burnout
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        # A dataframe to store prices
        self.stock_df = pd.DataFrame()
        self.is_long, self.is_short = False, False
        self.send_order = None

    def current_position(self,positions):
        """
        Indicate a long or a short on every change in position
        """
        if self.symbol in positions:
            
            # get positions 
            position = positions[self.symbol]
            
            # if the net position is positive keep long else short
            if position.net_position > 0:
                self.is_long = True 
            else: 
                self.is_long = False            
            if position.net < 0:
                self.is_short = True  
            else:
                self.is_short = False   


    def send_signal(self,market_data):
        # event_tick
        self.store_prices(market_data)

        # check if the dataframe length is longer than the 
        # lookback interval
        if len(self.stock_df) < self.burnout:            
            return
        
        # calculate the Z score from the prices
        zscore = self.get_zscore()
        
        timestamp = market_data.get_timestamp(self.symbol)        
        
        # buy if signal is less than buy threshold
        # sell if the signal is greater than the sell threshold
        if zscore < self.buy_threshold:            
            self.on_buy_signal(timestamp)        
        elif zscore > self.sell_threshold:            
            self.on_sell_signal(timestamp)

    def store_prices(self, market_data):
        # store the open and close prices for the timestamp
        # in the prices dataframe
        timestamp = market_data.get_timestamp(self.symbol)
        self.stock_df.loc[timestamp,'close'] = market_data.get_close_price(self.symbol)
        self.stock_df.loc[timestamp,'open'] = market_data.get_open_price(self.symbol)


    def on_buy_signal(self, timestamp):
        if not self.is_long:            
            self.send_market_order(self.symbol,100,True, timestamp)    
    
    def on_sell_signal(self, timestamp):
        if not self.is_short:            
            self.send_market_order(self.symbol,100,False, timestamp)   

    def send_market_order(self, symbol, qty, buy, timestamp):
        """
        called by on_buy_signal and on_sell_signal
        called when the implementing strategy sends a market order
        Args:
            symbol (str): The symbol of the order.
            qty (int): The quantity of the order.
            is_buy (bool): True if it is a buy order, False if it is a sell order.
            timestamp (int): The timestamp of the order.

        Returns:
            None
        """
        if not self.send_order is None:
            order = OrderData(symbol, timestamp, qty, buy, True)
            self.send_order(order)

    
    def get_zscore(self):

        self.stock_df = self.stock_df[-self.burnout:]
        # calculate returns
        returns = self.stock_df["close"].pct_change().dropna()        
        # z score
        z_score = ((returns-returns.mean())/returns.std())[-1]        
        return z_score   
    
    # def send_market_order(self, order):
    #     pass 