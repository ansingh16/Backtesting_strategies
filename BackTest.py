from Markets import *
from Strategy import *
from Portfolio import *

class BackTest:

    def __init__(self):

        self.unfilled_orders=[]
        self.portfio = Portfolio()
        self.dats = Data_Source(['TSLA','AAPL','MSFT'],start_date='2019-01-01',stop_date='2020-01-01')
        
        self.startegy = MeanRevertingStrategy()

        self.dats.event_handler = self.startegy.send_signal

        self.startegy.send_market_order = self.event_order

        self.dats.execute_orders = self.execute_orders
        
        self.dats.start_traverse()

    def event_order(self, order):
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
            
            self.orders_to_execute=[]
            for order in self.unfilled_orders:

                self.balance_position(order,prices)
            
                self.portfio.add_trade(order.symbol,order.signal,order.quant,order.price)

                self.portfio.update_ur_pnl(order.price,order.symbol)

    def balance_position(self,order,prices):

        order_time = order.timestamp
        symbol = order.symbol
        get_last_timestamp = self.dats.get_last_timestamp()
        if order_time < get_last_timestamp:
            
            order.executed=True 
            
    

back = BackTest()