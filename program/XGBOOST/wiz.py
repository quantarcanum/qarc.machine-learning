import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
import yfinance as yf

class WizXGBoost():

    def __init__(self, dataframe):
        """ 
        
        """
        self.full_data = dataframe

        self.df = self._data_extraction()
        print(self.df)
        #self._print_data()
        self.df_fe = self.df.copy()

    def _data_extraction(self):
        start_date = "2017-01-01"
        end_date = "2023-01-02"
        symbol = "SPY"
        data = yf.download(symbol, start_date, end_date)
        data = data[["Open", "High", "Low", "Close", "Volume"]]
        
        # Add Retruns and Range
        df = data.copy()
        df["Returns"] = (df["Close"] / df["Close"].shift(1)) - 1
        df["Range"] = (df["High"] / df["Low"]) - 1
        df.dropna(inplace = True)

        return df
    
    def _print_data(self):
        fig = plt.figure(figsize=(15, 3))
        plt.plot(self.df["Close"].values)
        plt.show()

        fig = plt.figure(figsize=(15, 3))
        plt.plot(self.df["Returns"].values)
        plt.show()

        fig = plt.figure(figsize=(15, 2))
        plt.plot(self.df["Range"].values)
        plt.show()