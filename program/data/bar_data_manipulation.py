import numpy as np
import pandas as pd

class BarDataManipulation():

    def __init__(self, dataframe):
        self.df = dataframe
        self._strip_cast_group_index_data()

        # computation
        self.df_computed = self.df.copy()
        self._compute_duration_in_seconds()
        self._compute_volume_per_second()
        self._compute_ticks_per_second()
        self._compute_bid_ask_ratio()
        self._compute_stacked_imbalance()
        self._compute_bar_profile()


    def get_dataframe(self):
        return self.df

    def get_computed_dataframe(self):
        return self.df_computed
    
    def _strip_cast_group_index_data(self):
        """
        The method strips the data of unneeded fields then it casts the values from string to numeric values
        Then it duplicates "Time" column as "time" and sets "time" as the index of the dataframe (I still need Time column to compute the duration between Time & LastTime)
        It also groups the data by TrendTicks if I will provide it with multiple tickframes
        """
        self.df = self.df[["TickValue", "TickSize", "TrendTicks", "ReversalTicks", "Time", "LastTime", "IsBomb", "IsPivot", "Open", "High", "Low", "Close", "Volume", "Delta", "MinDelta", "MaxDelta", "Ticks", "Bid", "Ask", "AllPriceLevels" ]]
        self.df = self.df.astype({"TickValue": "float", "TickSize": "float", "TrendTicks": "int", "ReversalTicks": "int", "Open": "float", "High": "float", "Low": "float", "Close": "float", "Volume" : "float", "Delta": "float", "MinDelta": "float", "MaxDelta": "float", "Ticks": "float", "Bid": "float", "Ask": "float" })
        self.df['time'] = self.df['Time'].copy()                
        self.df = self.df.groupby(['TrendTicks'])               
        self.df = self.df.apply(lambda x: x.set_index("time"))

    def _compute_duration_in_seconds(self):
        self.df_computed['duration_sec'] = (self.df_computed['LastTime'] - self.df_computed['Time']).dt.total_seconds()

    def _compute_volume_per_second(self):
        self.df_computed.loc[self.df_computed["duration_sec"] > 0, "vol_per_sec"] = (self.df_computed['Volume'] / self.df_computed['duration_sec'])
        self.df_computed.loc[self.df_computed["duration_sec"] == 0, "vol_per_sec"] = self.df_computed['Volume']

    def _compute_ticks_per_second(self):
        self.df_computed.loc[self.df_computed["duration_sec"] > 0, "ticks_per_sec"] = (self.df_computed['Ticks'] / self.df_computed['duration_sec'])
        self.df_computed.loc[self.df_computed["duration_sec"] == 0, "ticks_per_sec"] = self.df_computed['Ticks']

    def _compute_bid_ask_ratio(self):
        """
        1 = equilibrium
        <1 = sell pressure
        >1 = bull pressure
        inf = max bull pressure (Ask = 0)
        0 = max bear pressure (Bid = 0)
        """
        self.df_computed['bid_ask_ratio'] = (self.df_computed['Bid'] / self.df_computed['Ask']) 

    def _compute_delta_vol_ratio(self):
        """
        [-1; 1] result range
        closer to 0 = equilibrium
        closer to -1 = selling imbalance
        closer to 1 = buying imbalance
        """
        self.df_computed['delta_vol_ratio'] = abs(self.df_computed['Delta'] / self.df_computed['Volume'])

    def _compute_delta_variation(self):
        """
        Ex: if MinDelta is -500 but the bar closes towards the MaxDelta = +600
        There was a war in the bar and the bulls won.
        But how can I normalize the data?
        """
        self.df_computed['delta_variation'] = abs(self.df_computed['MaxDelta'] - self.df_computed['MinDelta'])

    def _compute_bar_spread_stats(self):
        """
        barspread_ticks = the number of ticks of each bar from H to L
           Trend bar max height = TrendTicks body + RevTicks-1 wick
           Reversal bar max height = TrendTicks-1 wick + RevTicks body
        barspread_surplus_ticks = the number of ticks in wick
            Trend bar = [0; RevTicks-1]
            Rev bar = [0; Trendticks-1]
        barspread_surplus_percent = percent for normalizing the surplus between trend and rev bars (because the absolute values differ)
        """
        self.df_computed['barspread_ticks'] = abs(self.df_computed['High'] - self.df_computed['Low']) / self.df_computed['TickSize']
        #IsPivot tells me it's a reversal bar
        self.df_computed.loc[self.df_computed["IsPivot"], "barspread_surplus_ticks"] = (self.df_computed['barspread_ticks'] - self.df_computed['ReversalTicks'])
        self.df_computed.loc[self.df_computed["IsPivot"] == False, "barspread_surplus_ticks"] = (self.df_computed['barspread_ticks'] - self.df_computed['TrendTicks'])
        self.df_computed.loc[self.df_computed["IsPivot"], "barspread_surplus_percent"] = ((self.df_computed['barspread_surplus_ticks'] * 100) / self.df_computed['TrendTicks'])
        self.df_computed.loc[self.df_computed["IsPivot"] == False, "barspread_surplus_percent"] = ((self.df_computed['barspread_surplus_ticks'] * 100) / self.df_computed['ReversalTicks'])

    def _compute_stacked_imbalance(self):
        """
        TODO: parse the data from all price levels
        add stacked imbalance column at the start
        add stacked imbalance column at the middle
        add stacked imbalance column at the end
        """
        print("TODO: Compute Stacked Imbalances")
        
    def _compute_bar_profile(self):
        """
        TODO: Compute Bar Profile
        Do I have trapped sellers/buyers in the wick in the wick
        Is the profile balanced
        ... 
        """
        print("TODO: Compute Bar Profile")
    

    def _perform_multirow_computations(self):
        print("TODO: Perform multirow computations")
        # trend rev perc avg over multilpe periods
        # height surplus absolute, percent
        # delta oi vol change

