from Markets import *
from Strategy import *
from Portfolio import *

class BackTest:

    def __init__(self):

        self.unfilled_orders=[]
        self.portfio = Portfolio()
        self.positions = dict()
        self.realized_pnl, self.unrealized_pnl = pd.DataFrame(), pd.DataFrame()

        self.dats = Data_Source(['TSLA','AAPL','MSFT'],start_date='2019-01-01',stop_date='2020-01-01')
        
        self.startegy = MeanRevertingStrategy()

        self.dats.event_handler = self.startegy.send_signal

        self.startegy.send_market_order = self.order_book

        self.dats.execute_orders = self.execute_orders
        
        self.dats.print_position = self.print_position_status

        self.dats.start_traverse()

    def order_book(self, order):
        """
        handles the orders
        """
        self.unfilled_orders.append(order)
        print(order.timestamp, \
            "Received order:", \
            "BUY" if order.signal else "SELL", order.quant, \
            order.symbol)
    


    def execute_orders(self,prices):
        
        if len(self.unfilled_orders)>0:

            # get position of the portfolio
            
            self.unfilled_orders = [order for order in self.unfilled_orders if self.check_order_status(order,prices)]

                # self.portfio.add_trade(order.symbol,order.signal,order.quant,order.price)

                # self.portfio.update_ur_pnl(order.price,order.symbol)

    def check_order_status(self,order,prices):
        
        # get the time of the order and current time
        order_time = order.timestamp
        symbol = order.symbol
        timestamp = self.dats.get_last_timestamp(symbol)
        if order_time < timestamp:
            
            order.executed=True 
            open_price = prices[symbol].opening_price

            order.filled_timestamp = timestamp
            order.filled_price = open_price
            self.portfolio_update(symbol,order.quant,order.signal, open_price,timestamp)
            self.executed_order_list(order)
            return False
        
        return True

    def portfolio_update(self,symbol,quant,signal,price,timestamp):

        position = self.get_position(symbol)
        position.add_trade(symbol,signal,quant,price)

        self.realized_pnl.loc[timestamp, "rpnl"] = position.realized_pnl
        print(self.get_trade_date(timestamp), \
            "Filled:", "BUY" if signal else "SELL", \
            quant, symbol, "at", price)
        

    def get_position(self,symbol):
        
        if symbol not in self.positions:
            position = Portfolio()
            position.symbol = symbol
            self.positions[symbol] = position
        return self.positions[symbol]


    def executed_order_list(self,order):
        # fill the list of orders executed 
        self.portfio.event_fill(order)
        
    # def get_timestamp(self):
    #     """
    #     called by is ordered match to get timestamp
    #     """
    #     return self.dats.get_last_timestamp(self.symbol)

    def get_trade_date(self,timestamp):
        # called by update_filled_positon above to get date
        
        return timestamp.strftime("%Y-%m-%d")
    

    def print_position_status(self, symbol, prices):
        """
        called by evthandler_tick for printing positons
        printing the positions
        """
        if symbol in self.positions:
            position = self.positions[symbol]
            position.update_ur_pnl(prices,symbol)
            self.unrealized_pnl.loc[self.dats.get_last_timestamp(symbol), "upnl"] = \
                position.unrealized_pnl
            print(self.get_trade_date(self.dats.get_last_timestamp(symbol)), \
                "Net:", position.net_position, \
                "Value:", position.position, \
                "UPnL:", position.unrealized_pnl, \
                "RPnL:", position.realized_pnl)
    



back = BackTest()