import numpy as np
import pandas as pd

class FeatureEngineering():

    def __init__(self, dataframe_group):
        self.df = dataframe_group

        # feature engineering
        self.df_engineered = self.df.copy()
        self._compute_price_log_returns()
        self._compute_price_log_returns_cumulative_sum()
        self._compute_price_normal_returns_cumulative_sum()

        self._drop_NaNs()


    def get_engineered_dataframe(self):
        return self.df_engineered

    
    def _compute_price_log_returns(self):
        """
        ML works best with price percent changes rather than price absolute values.
        To calculate the percent change from price1 to price2 you can take one of the following alternatives:
           - (price2 / price1) - 1
           - (price2 - price1) / price1
           - df["price"].pct_change()
        To calculate logarithmic returns (log rets is advised especially for lots of historical data that changed a lot from past to future)
           - np.log(price2 / price1)
        *Note that the first row return will be filled with NaN since there is no change (you need two rows to compute a change).    
        """
        self.df_engineered["returns"] = self.df_engineered["Close"].pct_change()
        self.df_engineered["log_returns"] = np.log(self.df_engineered["Close"] / self.df_engineered["Close"].shift(1))  # shift(1) takes the close from the row before "price1"

    def _compute_price_log_returns_cumulative_sum(self):
        """
        cumulative sum of the log returns:
            log_returns_cumsum2 = log_returns2 + log_returns1
            log_returns_cumsum3 = log_returns3 + log_returns2
        """        
        self.df_engineered["log_returns_cumsum"] = self.df_engineered["log_returns"].cumsum()

    def _compute_price_normal_returns_cumulative_sum(self):
        """
        This gives the equity curve
        It's the log returns cumulative sum normalized with the exponent
        """
        #self.df_engineered["normal_returns_cumsum"] = self.df_engineered["returns"].cumsum()        
        self.df_engineered["normal_returns_cumsum"] = np.exp(self.df_engineered["log_returns_cumsum"]) -1 

    def _drop_NaNs(self):
        """
        When computing values on SEQUENTIAL data, e.g a 5 period SMA, the first four rows will have sma=NaN, you will get SMA values from row 5 on
        We cannot feed ML with NaN data so we need to either drop it or fill it with something (a mean value or 0)
        """
        self.df_engineered.dropna(inplace = True) # is equal to df = df.dropna()
        #self.df_engineered.fillna(0, inplace = True)