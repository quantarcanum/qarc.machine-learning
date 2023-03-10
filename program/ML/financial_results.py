import numpy as np

class FinancialResults():

    def __init__(self):
        pass

    # def _compute_price_log_returns(self):
    #     """
    #     ML works best with price percent changes rather than price absolute values.
    #     To calculate the percent change from price1 to price2 you can take one of the following alternatives:
    #        - (price2 / price1) - 1
    #        - (price2 - price1) / price1
    #        - df["price"].pct_change()
    #     To calculate logarithmic returns (log rets is advised especially for lots of historical data that changed a lot from past to future)
    #        - np.log(price2 / price1)
    #     *Note that the first row return will be filled with NaN since there is no change (you need two rows to compute a change).    
    #     """
    #     self.df_engineered["returns"] = self.df_engineered["Close"].pct_change()
    #     self.df_engineered["log_returns"] = np.log(self.df_engineered["Close"] / self.df_engineered["Close"].shift(1))  # shift(1) takes the close from the row before "price1"

    # def _compute_price_log_returns_cumulative_sum(self):
    #     """
    #     cumulative sum of the log returns:
    #         log_returns_cumsum2 = log_returns2 + log_returns1
    #         log_returns_cumsum3 = log_returns3 + log_returns2
    #     """        
    #     self.df_engineered["log_returns_cumsum"] = self.df_engineered["log_returns"].cumsum()

    # def _compute_price_normal_returns_cumulative_sum(self):
    #     """
    #     This gives the equity curve
    #     It's the log returns cumulative sum normalized with the exponent
    #     """
    #     #self.df_engineered["normal_returns_cumsum"] = self.df_engineered["returns"].cumsum()        
    #     self.df_engineered["normal_returns_cumsum"] = np.exp(self.df_engineered["log_returns_cumsum"]) -1 

    def compute_sharpe_ratio(self, returns):
        """
        Sharpe ratio evaluates the return of an investment compared to its risk. (Risk adjusted returns)
        
        Sharpe Ratio = (Return of investment - Risk-free rate) / Standard deviation of investment's returns
           - ROI: return of the strategy
           - RFR: the rate of return on a risk-free investment, such as a government bond. approx 1-2%
              - ROI-RFR: excess return over risk free rate
           - Standard deviation of ROI: This measures the volatility of the investment. 
             It shows how much the returns of the investment vary from the average return. 
             A higher standard deviation indicates higher volatility.

        The higher the Sharpe ratio, the better the investment's returns relative to the risk taken
            to get a high quotient you need a small divisor => if stdev(ROI) is small => volatility is small => better risk adjusted return
        
        Example: Over the last year: 
           Investment A had a return of 12% with a returns standard deviation of 15%
           Investment B had a return of 10% with a returns standard deviation of 10%
           The risk-free rate is 2%.
            - Sharpe Ratio for Investment A = (12% - 2%) / 15% = 0.67
            - Sharpe Ratio for Investment B = (10% - 2%) / 10% = 0.80
           Result: Although A had better ROI than B, it has a lower sharpe ratio 
                   Investment B has a better risk-adjusted return than Investment A. 
                   In other words, Investment B is providing a higher return for the same level of risk compared to Investment A.  
        """
        N = 255
        SQRTN = np.sqrt(N)
        rfr = 0.02
        mean = returns.mean() * N
        sigma = returns.std() * SQRTN
        sharpe = round((mean-rfr) / sigma, 3)

        return sharpe