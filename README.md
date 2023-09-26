# Backtesting strategies

This repository contains the code developed for doing backtesting in quantitative finance.
The code will use object oriented programming in python to simulate scenario's that can be implemented
in real life trading situations.


It contains the following files:

- BackTest.py: Contains the main testing class where we define the portfolio and apply the simulation on historical data
- Strategy.py: Contains the Stratergy Class that decides given a historical data whether to buy of sell a stock depending upon the strategy used.
- Market.py: Contains the classes and functions related to stock data. It contains three classes:
    - Data_Source: Class for downloading and traversing stock market data.
    - StockHistory class acts like a container for storing the market data as an instance of StockData class and contains functions useful for finding latest data for a stock.
    - StockData class acts like a storage for stock data.
- Portfolio.py: Contains class for storing data and function related to portfolio management. It records the position for a stock.

The code is tested for implementing strategy of mean reverting applied for apple stock data in the period of 2019-20. This can be run using **python BackTest.py**

For any quesries feel free to open an issue of contact ankitsingh@kias.re.kr 


