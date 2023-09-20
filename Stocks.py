import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr

yf.pdr_override()


class MarketData:
    def __init__(self,symbol,start_date,stop_date):
        
        self.dat = pdr.get_data_yahoo(symbol,start_date,stop_date)
        
    def get_close_price(self,date):
        return self.dat[self.dat.index == date]['Close'].values[0]
    
    def get_open_price(self,date):
        return self.dat[self.dat.index == date]['Open'].values[0]
    

    def start_simulation(self):
        
        for date in self.dat.index:
            print(date,self.get_close_price(date),self.get_open_price(date))


class Portfolio:
    def __init__(self):
        self.positions = dict()
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.buys = 0
        self.sells = 0
    
    def event_add(self,symbol,order,qty,price):
        if order=='buy':
            self.buys += qty
        else:
            self.sells -= qty

        self.net_position = self.buys - self.sells
        sign = 1 if order=='buy' else -1
        self.positions[symbol] += self.net_position*price*sign 

        # if all the shares have been dealt with you get your realised PnL
        if self.net_position==0:
            self.realized_pnl = self.positions[symbol]

            self.unrealized_pnl = 0
    
    def update_ur_pnl(self,price):
        
        if self.net_position == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = price * self.net_position + \
            self.position_value





class strategy(MarketData):
    def __init__(self,symbol,start_date,stop_date):
        
        self.md = MarketData(symbol,start_date,stop_date)
        self.portfolio = Portfolio()

    def sign_changing(self):

        pass 