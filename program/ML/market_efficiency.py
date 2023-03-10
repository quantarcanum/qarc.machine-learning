import numpy as np
import sklearn.mixture as mix
import matplotlib.pyplot as plt

# Efficiency Testing Libraries
from statsmodels.tsa.stattools import bds
from statsmodels.sandbox.stats.runs import runstest_1samp
from statsmodels.tsa.stattools import adfuller
import scipy.stats as sps

class MarketEfficiency():

    def __init__(self):
        """
        Resources and Useful References
        NEDL YouTube Channel - Hurst Exponent: https://www.youtube.com/watch?v=l08LICz8Ink
        NEDL YouTube Channel - Dynamic Hurst Exponent: https://www.youtube.com/watch?v=v0sivj2wGcA
        Hurst Exponent Coding: https://raposa.trade/blog/find-your-best-market-to-trade-with-the-hurst-exponent/
        More Hurst Exponent Coding: https://www.quantstart.com/articles/Basics-of-Statistical-Mean-Reversion-Testing/
        """
        pass


    def runs_test(self, returns):
        """Base standard test for randomness based on linearity"""
        # Convert Returns into binary outcomes
        returns_binary = [ 1 if x >= 0 else 0 for x in returns]
        (z_stat, p_value) = runstest_1samp(returns_binary[:10], correction=False)
        z_stat = round(z_stat, 3)
        p_value = round(p_value, 3)
        is_reject_runs = True if p_value < 0.05 else False
        print(f"Z-Statistic: {z_stat}")
        print(f"P-Value: {p_value}")
        print(f"Reject Null: {is_reject_runs}")
        print(f"Observable Runs Exceeds Excpected Runs by: {z_stat} Standard Deviations")
        print("Not Random") if is_reject_runs else print("Random")

    def bds_test(self, returns):
        """Testing for chaos and nonlinearity. Considered as your last line of defence as takes into account non-linear dependancies after running other efficiency tests."""
        bds_test = bds(returns[-500:], distance=2)
        bds_stat = float(bds_test[0])
        pvalue = float(bds_test[1])
        print("BDS Test Statistic: ", round(bds_stat, 3))
        print("BDS P-Value: ", round(pvalue, 3))
        print("Not Random") if pvalue < 0.05 else print("Random")

    def adfuller_test(self, returns):
        dftest = adfuller(returns)
        p_value = dftest[1]
        t_test = dftest[0] < dftest[4]["1%"]
        print(p_value, t_test)
        print("If < 0.05 and True then we can reject the null hypothesis and conclude that the index is stationary")
