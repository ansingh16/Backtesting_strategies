import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr

yf.pdr_override()

class StockData:
    """
    Class for saving stock data, for each timestamp
    args: stock_symbol, timestamp, closing_price, trading_volume
    """
    def __init__(self, stock_symbol, timestamp, closing_price=0,opening_price=0, trading_volume=0):
        self.stock_symbol = stock_symbol
        self.timestamp = timestamp
        self.opening_price = opening_price
        self.closing_price = closing_price
        self.trading_volume = trading_volume


class OrderData:

    def __init__(self, symbol,timestamp,quant,signal,price):

        self.symbol = symbol
        self.timestamp = timestamp
        self.quant = quant
        self.signal = signal
        self.price = price


class Data_Source:
    def __init__(self,symbols,start_date,stop_date):

        # container for last stock Data
        self.prices = {}
        self.symbols = symbols
        # Dataframe for each stock
        self.start_date = start_date
        self.stop_date = stop_date
        self.symbol_dat = pd.DataFrame()
        self.event_handler=None
        self.execute_orders = None
        self.print_position = None
    def start_traverse(self):

        dat = pdr.get_data_yahoo(self.symbols,self.start_date,self.stop_date)
        
        
        
        for date in dat.index:
            for symbol in self.symbols:

                
                sd = StockData(symbol,date,dat.loc[date]['Close'][symbol],dat.loc[date]['Open'][symbol],dat.loc[date]['Volume'][symbol])
                
                self.symbol_dat.loc[date, "Close"] = dat.loc[date]['Close'][symbol]

                self.prices[symbol] = sd
                
                if self.event_handler is not None:
                    self.event_handler(symbol,self.symbol_dat,sd)

                if self.print_position is not None:
                    self.print_position(symbol, self.prices)
                
            # print(symbol)
            if self.execute_orders is not None:
                self.execute_orders(self.prices)

            
            
    
    def get_last_timestamp(self,symbol):

        return self.prices[symbol].timestamp

    def get_open_price(self,symbol):
        return self.prices[symbol].opening_price

    def get_close_price(self,symbol):
        return self.prices[symbol].closing_price



