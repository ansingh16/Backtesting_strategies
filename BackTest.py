from Markets import *
from Strategy import *
from Portfolio import *

class BackTest:

    def __init__(self, symbol, start_date, end_date):

        self.symbol = symbol
        self.start_dt = start_date
        self.end_dt = end_date
        self.unfilled_orders = []
        self.positions = dict()
        self.realized_pnl, self.unrealized_pnl = pd.DataFrame(), pd.DataFrame()
        self.current_prices = None
        self.strategy=None
    
    def start_simulation(self):
        self.strategy = MeanRevertingStrategy(self.symbol)

        # this will be called by Startegy function send
        # send_market_order
        self.strategy.send_order = self.order_handler

        mds = Data_Source()
        mds.symbol = self.symbol
        mds.start_date = self.start_dt
        mds.stop_date = self.end_dt
        # event tick set for the Market Source
        # this will get the latest prices for stock
        mds.event_tick = self.tick_handler
        
        print("starting simulation")
        mds.start_traverse()
        print("simulation ended")

    def tick_handler(self, prices):
        # prices from Data_Source containing last
        # stock prices
        self.current_prices = prices

        # what to do with the tick depends on strategy
        # this will pass the latest market data
        # this will eventually call send_order function in
        # stategy class that is mapped to order_handler fn
        self.strategy.send_signal(prices)

        # As a result of above the unfilled orders list is 
        # appended and we execute the orders

        self.execute_orders(prices)

        # After all the orders are executed we print the positions
        # in our portfolio

        self.print_position_status(self.symbol, prices)



    def order_handler(self, order):
        # append the unfilled order
        self.unfilled_orders.append(order)
        print(order.timestamp, \
            "Received order:", \
            "BUY" if order.buy else "SELL", order.quant, \
            order.symbol)
    


    def execute_orders(self,prices):
        
        if len(self.unfilled_orders)>0:

            # check if the position of portfolio and 
            # execute orders 
            
            self.unfilled_orders = [order for order in self.unfilled_orders if self.check_order_status(order,prices)]

            

    def check_order_status(self,order,prices):
        
        # get the time of the order and current time
        order_time = order.timestamp
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)
        if order_time < timestamp:
            
            order.executed=True 
            open_price = prices.get_open_price(symbol)
            order.filled_timestamp = timestamp
            order.filled_price = open_price
            self.portfolio_update(symbol,order.quant,order.buy, open_price,timestamp)
            # self.executed_order_list(order)
            return False
        # order is not filled as time is not greater than order times
        return True

    def portfolio_update(self,symbol,quant,buy,price,timestamp):
        # get position for stock
        position = self.get_position(symbol)
        # add the trade depending on the position and buy signal
        # coming from strategy
        position.add_trade(buy,quant,price)

        self.realized_pnl.loc[timestamp, "rpnl"] = position.realized_pnl
        print(self.get_trade_date(), \
            "Filled:", "BUY" if buy else "SELL", \
            quant, symbol, "at", price)
        

    def get_position(self,symbol):
        
        if symbol not in self.positions:
            # the stock is here for first time
            # add the stock position
            position = Portfolio()
            position.symbol = symbol
            self.positions[symbol] = position
        return self.positions[symbol]


    def get_trade_date(self):
        # called by update_filled_positon above to get date
        timestamp = self.get_timestamp()
        return timestamp.strftime("%Y-%m-%d")
    
    def get_timestamp(self):
        """
        called by is ordered match to get timestamp
        """
        return self.current_prices.get_timestamp(self.symbol)
    
    def print_position_status(self, symbol, prices):
        """
        called by evthandler_tick for printing positons
        printing the positions
        """
        if symbol in self.positions:
            position = self.positions[symbol]
            close_price = prices.get_close_price(symbol)
            position.update_ur_pnl(close_price)
            self.unrealized_pnl.loc[self.get_timestamp(), "upnl"] = \
                position.unrealized_pnl
            print(self.get_trade_date(), \
                "Net:", position.net_position, \
                "Value:", position.position, \
                "UPnL:", position.unrealized_pnl, \
                "RPnL:", position.realized_pnl)
    



back = BackTest("AAPL", "2019-01-01", "2020-01-01")

back.start_simulation()