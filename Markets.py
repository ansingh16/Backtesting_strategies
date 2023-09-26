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
    def __init__(self, symbol, timestamp, close=0,volume=0):
        self.stock_symbol = symbol
        self.timestamp = timestamp
        self.opening_price = 0
        self.closing_price = close
        self.trading_volume = volume


class StockHistory:
    # stores the recent data for each stock
    def __init__(self):
        self.stock_hist = {}
    
    def add_close_price(self, timestamp, symbol, price, volume):
        """
        Add a close price to the stock history.

        Parameters:
            timestamp (str): The timestamp of the close price.
            symbol (str): The symbol of the stock.
            price (float): The close price of the stock.

        Returns:
            None
        """
                
        sd =StockData(symbol,timestamp,price,volume)
        self.stock_hist[symbol] = sd 
    def add_open_price(self, timestamp, symbol, price):
        """
        Set the opening price for a given stock symbol and timestamp.

        Parameters:
            timestamp (int): The timestamp of the tick data.
            stock_symbol (str): The symbol of the stock.
            price (float): The opening price to be set.

        Returns:
            None
        """
        tick_data = self.get_current_data(symbol, timestamp)
        tick_data.opening_price = price

    def get_current_data(self,symbol,timestamp):
        """
        Retrieves the current data for a specific stock symbol at a given timestamp.
        
        Parameters:
            symbol (str): The symbol of the stock.
            timestamp (int): The timestamp for which to retrieve the data.
        
        Returns:
            StockData: The current data for the specified stock symbol at the given timestamp.
        """
        if not symbol in self.stock_hist:
            tick_data = StockData(symbol, timestamp)
            self.stock_hist[symbol] = tick_data
        
        return self.stock_hist[symbol]
    
    def get_close_price(self,symbol):
        """
        Get the closing price for a given symbol.
        
        Args:
            symbol (str): The symbol of the stock.
            
        Returns:
            float: The closing price of the stock.
        """

        return self.stock_hist[symbol].closing_price

    def get_open_price(self,symbol):
        """
        Get the opening price of a stock.

        Parameters:
            symbol (str): The symbol of the stock.

        Returns:
            float: The opening price of the stock.
        """
        return self.stock_hist[symbol].opening_price
    
    def get_timestamp(self,symbol):
        """
        Get the timestamp for a given symbol.

        Parameters:
            symbol (str): The symbol for which to retrieve the timestamp.

        Returns:
            int: The timestamp of the stock history for the given symbol.
        """
        return self.stock_hist[symbol].timestamp




class Data_Source:
    """
    Class for traversing the stock data
    """
    def __init__(self):

        # container for last stock Data
        self.prices = {}
        self.symbol = None
        # Dataframe for each stock
        self.start_date = None
        self.stop_date = None
        self.symbol_dat = StockHistory()
        self.event_tick = None
    def start_traverse(self):

        dat = pdr.get_data_yahoo(self.symbol,self.start_date,self.stop_date)
        
        
        
        for time, row in dat.iterrows():
                
                
                self.symbol_dat.add_close_price(time,self.symbol,row["Close"], row["Volume"])
                self.symbol_dat.add_open_price(time,self.symbol,row["Open"])

                # print(symbol)
                if self.event_tick is not None:
                    self.event_tick(self.symbol_dat)


